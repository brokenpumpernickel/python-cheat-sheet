# Python Cheat Sheet

A zoomable, bilingual (English/Polish) Python reference for students in a statistics & probability lab.

**Live site:** https://brokenpumpernickel.github.io/python-cheat-sheet/ (in Polish: https://brokenpumpernickel.github.io/python-cheat-sheet/?lang=pl)

Content lives in `content/` as Markdown (see `docs/content-format.md`). A Python content build runs every example in a fresh Jupyter kernel and writes `generated/content.json`; Astro (`site/`) renders it into one static page.

## Building locally

You need [uv](https://docs.astral.sh/uv/) and Node.js 22.23 or newer. uv installs the pinned Python (3.12) and libraries.

```bash
uv run cheatsheet build
```

Runs every example and builds the site into `site/dist/` (runs `npm ci` first if `site/node_modules` is missing). Add `--base /python-cheat-sheet/` to build for GitHub Pages.

```bash
uv run cheatsheet serve
```

Serves `site/dist/` at http://127.0.0.1:4321/.

## Tests

Install Chromium for the browser tests once:

```bash
uv run playwright install chromium
```

Then run the content-build and browser tests:

```bash
uv run pytest
```

## Deployment

`.github/workflows/site.yml` runs the tests and the full build on every pull request and push to `main`. A failing example or test fails the check. Pushes to `main` that pass are deployed to GitHub Pages.
