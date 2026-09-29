# Par Bahrae

Portfolio of Par Bahrae ([ParBproject](https://github.com/ParBproject)): forecasting, quantitative finance, machine learning, and data tools. GitHub Pages publishes this repository from the default branch.

**Live:** https://parbproject.github.io

## Rebuild

`index.html` is generated from `src/template.html` and the project data in `src/build.py`. Styles are compiled with the Tailwind CSS CLI (v3.4.17, the same theme as the original inline config) into `assets/site.css`. That file is committed, so GitHub Pages serves the site as static files and does not run a build.

```bash
npm install
python3 src/build.py
npx tailwindcss -i ./src/input.css -o ./assets/site.css --minify
```

`npm run build` runs both steps. Run `python3 src/build.py` after editing copy or project data. Run the Tailwind command after changing classes in `src/template.html`, `src/build.py`, `index.html`, or `404.html` — those files are the Tailwind content sources.

`render.py` is a dev-only Playwright script that screenshots `index.html`. GitHub Pages does not use it.
