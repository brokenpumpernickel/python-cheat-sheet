# 02: CI and GitHub Pages deploy

**What to build:** Pushing to `main` on GitHub (brokenpumpernickel/python-cheat-sheet, public) runs a GitHub Actions workflow. It installs uv and Node, runs the full test suite, builds content and site, and publishes the result to GitHub Pages. Pull requests run the tests without deploying. A failing example, failing validation or failing test blocks the deploy. The Pages source is set to "GitHub Actions" (via `gh` or the repo settings; ask the Author if a settings change needs their approval). A short README explains how to build locally and where the site lives.

**Blocked by:** 01 (Tracer bullet).

**Status:** resolved

- [x] Workflow runs on push to `main` and on pull requests; deploys only from `main`.
- [x] Python version and libraries come from the pinned uv project; Node dependencies from a lockfile.
- [x] Jupyter-kernel execution and Playwright browser tests both work in CI.
- [x] The tracer-bullet page is live at the repository's GitHub Pages URL, and the URL is in the README and the repo description. (Live since PR #2 merged; confirmed by the Author.)
- [x] A deliberately broken example on a branch makes the PR check fail (verified once, then reverted).

## Comments

**Resolved by PR #2.** Notes for later tickets:

- **Workflow:** `.github/workflows/site.yml`. One `build` job runs on every PR and push to `main`:
  - `uv sync` and `npm ci` from the lockfiles (`UV_LOCKED=1` makes a stale `uv.lock` fail the run)
  - `uv run playwright install --with-deps chromium`
  - `uv run pytest`
  - `uv run cheatsheet build --base /python-cheat-sheet/`

  Only on `main` does it upload `site/dist` and run the `deploy` job (GitHub Pages, `github-pages` environment). A failed step stops the run before the upload, so nothing deploys.
- **The real content build also runs on PRs.** The tests only use fixtures, so this step is what catches a broken example in `content/`. This was checked once on PR #2: a `NameError` added to `lists/creating-and-indexing` failed the check, naming the file and Entry, and was then reverted. Validation added in 03 fails CI the same way, as long as it raises `ContentError`.
- **Versions:** the workflow pins uv 0.12.10 and Node 24. Astro 7.4.2 needs Node 22.23 or newer. `astral-sh/setup-uv` publishes no major-version tags, so it is pinned to `v10.3.2`; the other actions use major tags.
- **Repo settings (via `gh`):**
  - Pages source is "GitHub Actions" (`build_type=workflow`).
  - The live URL is in the repo description and homepage.
- **Live page:** https://brokenpumpernickel.github.io/python-cheat-sheet/. The first deploy runs when PR #2 merges to `main`. To confirm it, check two things, then tick the "live" box above:
  - the Actions run on `main` shows a green `deploy` job
  - the URL serves the Lists Topic
- **Run time:** about 1.5 minutes. Each example takes about 0.5 s on the runner, so the MVP content (12) will add a minute or two unless examples run in parallel.
