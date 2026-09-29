import asyncio, pathlib
from playwright.async_api import async_playwright
D = pathlib.Path(__file__).resolve().parent
URL = (D/'index.html').as_uri()
OUT = D / 'screenshots'
async def shot(b, w, h, out, full):
    p = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
    await p.goto(URL, wait_until='networkidle')
    await p.evaluate("document.fonts.ready")
    await p.wait_for_timeout(800)
    broken = await p.evaluate("[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src)")
    ovf = await p.evaluate("document.documentElement.scrollWidth > window.innerWidth")
    OUT.mkdir(exist_ok=True)
    await p.screenshot(path=str(OUT/out), full_page=full)
    print(out, 'broken:', broken, 'h-overflow:', ovf, 'height:', await p.evaluate("document.body.scrollHeight"))
    await p.close()
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path='/usr/bin/google-chrome')
        await shot(b, 1440, 900, 'desktop.png', True)
        await shot(b, 1440, 900, 'desktop-hero.png', False)
        await shot(b, 390, 844, 'mobile.png', True)
        await b.close()
asyncio.run(main())
