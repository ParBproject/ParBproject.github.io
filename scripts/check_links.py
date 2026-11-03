#!/usr/bin/env python3
"""Check links in the published HTML.

Internal links must point at a file in the repo (GitHub Pages serves the
repository root) and at an id that exists. External links must answer with
an HTTP status below 400. Transient statuses and connection errors are
retried. GitHub URLs are checked through the API, which is steadier than
scraping github.com from CI.
"""

from __future__ import annotations

import http.cookiejar
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES_GLOB = "*.html"
BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)
RETRY_STATUSES = {408, 429, 500, 502, 503, 504}
ATTEMPTS = 3
TIMEOUT = 12
WORKERS = 6
ID_RE = re.compile(r"""(?:^|\s)id\s*=\s*(?:"([^"]*)"|'([^']*)')""")
SKIP_RELS = {"preconnect", "dns-prefetch", "prefetch"}
META_URL_KEYS = {"og:url", "og:image", "twitter:url", "twitter:image"}


class FetchError(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)
        self.detail = detail


class Collector(HTMLParser):
    def __init__(self, page: Path):
        super().__init__(convert_charrefs=True)
        self.page = page
        self.refs: list[tuple[int, str]] = []

    def handle_starttag(self, tag, attrs):
        attr = {}
        for key, value in attrs:
            attr.setdefault(key, value if value is not None else "")
        line = self.getpos()[0]
        if tag == "a" and attr.get("href"):
            self._add(line, attr["href"])
        elif tag == "link" and attr.get("href"):
            rels = set(attr.get("rel", "").split())
            if not rels & SKIP_RELS:
                self._add(line, attr["href"])
        elif tag in {"img", "script", "source", "iframe"} and attr.get("src"):
            self._add(line, attr["src"])
        elif tag == "meta":
            key = (attr.get("property") or attr.get("name") or "").lower()
            content = attr.get("content", "")
            if key in META_URL_KEYS and content.startswith(("http://", "https://")):
                self._add(line, content)

    def _add(self, line: int, url: str):
        url = url.strip()
        if not url or url.startswith(("javascript:", "data:")):
            return
        self.refs.append((line, url))


def collect(pages: list[Path]) -> list[tuple[Path, int, str]]:
    found = []
    for page in pages:
        parser = Collector(page)
        parser.feed(page.read_text(encoding="utf-8"))
        found.extend((page, line, url) for line, url in parser.refs)
    return found


def anchor_ids(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    return {a or b for a, b in ID_RE.findall(text)}


def outside_root(root: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return True
    return False


def local_target(root: Path, page: Path, url: str) -> Path | None:
    """Return the local file a URL points at, or None when it is not local."""
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme in {"http", "https"} or parsed.netloc:
        return None
    if parsed.scheme not in {"", "mailto"}:
        return None
    if parsed.scheme == "mailto":
        return None
    path = urllib.parse.unquote(parsed.path)
    if path == "":
        return page.resolve()
    if path.startswith("/"):
        relative = path.lstrip("/")
        target = (root / relative).resolve() if relative else root.resolve()
    else:
        target = (page.parent / path).resolve()
    if path.endswith("/") or target.is_dir():
        target = (target / "index.html").resolve()
    return target


def mailto_problem(url: str) -> str | None:
    address = url[len("mailto:") :].split("?", 1)[0]
    if "@" not in address or address.startswith("@") or address.endswith("@"):
        return "mailto address is not usable"
    return None


def local_problems(root: Path, refs: list[tuple[Path, int, str]]) -> list[str]:
    problems = []
    ids_cache: dict[Path, set[str]] = {}
    for page, line, url in refs:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme == "mailto":
            reason = mailto_problem(url)
            if reason:
                problems.append(f"{page.name}:{line}: {url} ({reason})")
            continue
        if parsed.scheme in {"http", "https"} or parsed.netloc:
            continue
        if parsed.scheme not in {"",}:
            problems.append(f"{page.name}:{line}: {url} (unsupported link)")
            continue
        target = local_target(root, page, url)
        if target is None:
            problems.append(f"{page.name}:{line}: {url} (unsupported link)")
            continue
        where = f"{page.name}:{line}"
        if outside_root(root, target):
            problems.append(f"{where}: {url} (leaves the site root)")
            continue
        if not target.is_file():
            problems.append(f"{where}: {url} (missing file)")
            continue
        fragment = urllib.parse.unquote(parsed.fragment)
        if not fragment:
            continue
        if target.suffix.lower() not in {".html", ".svg"}:
            problems.append(f"{where}: {url} (fragment on a non-HTML file)")
            continue
        if target not in ids_cache:
            ids_cache[target] = anchor_ids(target)
        if fragment not in ids_cache[target]:
            problems.append(f"{where}: {url} (missing id {fragment!r})")
    return problems


def github_api_url(url: str) -> str | None:
    parsed = urllib.parse.urlparse(url)
    if (parsed.hostname or "").lower() != "github.com":
        return None
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) == 1:
        user = urllib.parse.quote(parts[0])
        return f"https://api.github.com/users/{user}"
    if len(parts) == 2:
        owner, repo = (urllib.parse.quote(part) for part in parts)
        return f"https://api.github.com/repos/{owner}/{repo}"
    if len(parts) >= 4 and parts[2] in {"blob", "tree"}:
        owner, repo = (urllib.parse.quote(part) for part in parts[:2])
        path = urllib.parse.quote("/".join(parts[4:]), safe="/")
        base = f"https://api.github.com/repos/{owner}/{repo}/contents"
        if path:
            base += "/" + path
        return base + "?" + urllib.parse.urlencode({"ref": parts[3]})
    return None


def github_headers() -> dict[str, str]:
    headers = {
        "User-Agent": "parbproject-link-check",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def browser_headers() -> dict[str, str]:
    return {
        "User-Agent": BROWSER_UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en",
    }


def _sleep(attempt: int, headers) -> None:
    delay = 0.5 * (2**attempt)
    if headers is not None:
        retry_after = headers.get("Retry-After")
        if retry_after and retry_after.isdigit():
            delay = float(retry_after)
    time.sleep(min(delay, 2))


def once(url: str, headers: dict[str, str], read_body: bool) -> tuple[int, bytes, object]:
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    request = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with opener.open(request, timeout=TIMEOUT) as response:
            body = response.read(8192) if read_body else b""
            return response.status, body, response.headers
    except urllib.error.HTTPError as error:
        # A 3xx raised from here is a broken redirect, not a final document.
        if error.code < 400:
            raise FetchError(f"redirect failed ({error.code})") from None
        body = error.read(8192) if read_body else b""
        return error.code, body, error.headers


def call(url: str, headers: dict[str, str], read_body: bool = False) -> tuple[int, bytes]:
    last = "request failed"
    for attempt in range(ATTEMPTS):
        try:
            code, body, hdrs = once(url, headers, read_body)
        except FetchError:
            raise
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            reason = getattr(error, "reason", error)
            last = str(reason)
            if attempt + 1 < ATTEMPTS:
                _sleep(attempt, None)
                continue
            raise FetchError(last) from None
        if code in RETRY_STATUSES and attempt + 1 < ATTEMPTS:
            last = f"HTTP {code}"
            _sleep(attempt, hdrs)
            continue
        return code, body
    raise FetchError(last)


def rate_limited(code: int, body: bytes) -> bool:
    if code == 429:
        return True
    if code != 403:
        return False
    text = body.decode("utf-8", "replace").lower()
    return "rate limit" in text


def check_http(url: str) -> tuple[bool, str, bool]:
    """Return ok, detail, and whether a LinkedIn anti-bot status was accepted."""
    host = (urllib.parse.urlparse(url).hostname or "").lower()
    try:
        code, _body = call(url, browser_headers(), read_body=False)
    except FetchError as error:
        return False, error.detail, False
    if code == 999 and (host == "linkedin.com" or host.endswith(".linkedin.com")):
        return True, "HTTP 999", True
    if 200 <= code < 400:
        return True, f"HTTP {code}", False
    return False, f"HTTP {code}", False


def check_external(url: str) -> tuple[bool, str, bool]:
    api = github_api_url(url)
    if api is not None:
        try:
            code, body = call(api, github_headers(), read_body=True)
        except FetchError:
            code = 0
            body = b""
        else:
            if code == 404:
                return False, "HTTP 404", False
            if 200 <= code < 400:
                return True, f"HTTP {code}", False
            if not (code in RETRY_STATUSES or rate_limited(code, body) or code == 403):
                return False, f"HTTP {code}", False
        # Rate limits and API outages fall through to the public page.
    return check_http(url)


def strip_fragment(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    return urllib.parse.urlunparse(parsed._replace(fragment=""))


def external_problems(refs: list[tuple[Path, int, str]]) -> tuple[list[str], int, int]:
    grouped: dict[str, list[tuple[Path, int]]] = {}
    for page, line, url in refs:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme == "mailto":
            continue
        if parsed.scheme not in {"http", "https"} and not parsed.netloc:
            continue
        absolute = url
        if url.startswith("//"):
            absolute = "https:" + url
        key = strip_fragment(absolute)
        grouped.setdefault(key, []).append((page, line))

    problems = []
    soft = 0

    def check(item: tuple[str, list[tuple[Path, int]]]):
        url, locations = item
        ok, detail, linkedin_soft = check_external(url)
        return url, locations, ok, detail, linkedin_soft

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        results = list(pool.map(check, grouped.items()))

    for url, locations, ok, detail, linkedin_soft in results:
        if linkedin_soft:
            soft += 1
        if ok:
            continue
        where = ", ".join(f"{page.name}:{line}" for page, line in locations)
        problems.append(f"{where}: {url} ({detail})")
    return problems, len(grouped), soft


def internal_count(refs: list[tuple[Path, int, str]]) -> int:
    total = 0
    for _page, _line, url in refs:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme in {"http", "https", "mailto"} or parsed.netloc:
            continue
        total += 1
    return total


def run_self_test() -> None:
    def expect(condition: bool, message: str) -> None:
        if not condition:
            raise SystemExit(f"link checker self-test failed: {message}")

    expect(
        github_api_url("https://github.com/ParBproject/repo")
        == "https://api.github.com/repos/ParBproject/repo",
        "repo API URL",
    )
    expect(
        github_api_url("https://github.com/ParBproject?tab=repositories")
        == "https://api.github.com/users/ParBproject",
        "profile API URL",
    )
    contents = github_api_url(
        "https://github.com/ParBproject/energy-sector-deep-dive/blob/main/docs/findings.md"
    )
    expect(
        contents
        == "https://api.github.com/repos/ParBproject/energy-sector-deep-dive/contents/docs/findings.md?ref=main",
        f"contents API URL was {contents}",
    )
    expect(github_api_url("https://example.com/a") is None, "non-GitHub URL")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "assets").mkdir()
        (root / "assets" / "ok.css").write_text("x", encoding="utf-8")
        (root / "resume.pdf").write_bytes(b"%PDF")
        (root / "index.html").write_text(
            """<!doctype html><main id="top"></main>
            <div data-id="ghost"></div>
            <a href="#top">top</a>
            <a href="#ghost">ghost</a>
            <a href="assets/ok.css">css</a>
            <a href="/resume.pdf">pdf</a>
            <a href="missing.html">missing</a>
            <a href="mailto:a@b.co">mail</a>
            <a href="mailto:not-an-email">bad mail</a>
            <link rel="preconnect" href="https://fonts.googleapis.com" />
            <link rel="stylesheet" href="assets/ok.css" />
            """,
            encoding="utf-8",
        )
        (root / "404.html").write_text(
            '<a href="/#top">home</a><a href="/no-such.txt">nope</a>',
            encoding="utf-8",
        )
        pages = [root / "index.html", root / "404.html"]
        refs = collect(pages)
        urls = [url for _page, _line, url in refs]
        expect("https://fonts.googleapis.com" not in urls, "preconnect should be skipped")
        expect(urls.count("assets/ok.css") == 2, "stylesheet and anchor both count")
        problems = local_problems(root, refs)
        text = "\n".join(problems)
        expect(any("missing.html" in item for item in problems), text)
        expect(any("no-such.txt" in item for item in problems), text)
        expect(any("#ghost" in item for item in problems), text)
        expect(any("mailto:not-an-email" in item for item in problems), text)
        expect(not any("ok.css" in item for item in problems), text)
        expect(not any("resume.pdf" in item for item in problems), text)
        expect(not any("#top" in item for item in problems), text)
        expect(not any("mailto:a@b.co" in item for item in problems), text)
        expect(len(problems) == 4, text)


def main() -> int:
    run_self_test()
    pages = sorted(ROOT.glob(PAGES_GLOB))
    if not pages:
        print("no published HTML files found", file=sys.stderr)
        return 1
    refs = collect(pages)
    local = local_problems(ROOT, refs)
    remote, remote_count, soft = external_problems(refs)
    problems = local + remote
    for problem in problems:
        print(problem, flush=True)
    local_total = internal_count(refs)
    print(
        f"Checked {local_total} internal links and {remote_count} external URLs.",
        flush=True,
    )
    if soft:
        print(
            f"Accepted {soft} LinkedIn URL(s) that returned 999. "
            "LinkedIn blocks automated clients, so that status does not mean the profile is gone.",
            flush=True,
        )
    if problems:
        print(f"{len(problems)} dead link(s).", flush=True)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
