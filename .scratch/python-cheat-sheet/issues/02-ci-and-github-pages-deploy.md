# 02: CI and GitHub Pages deploy

**What to build:** Pushing to `main` on GitHub (brokenpumpernickel/python-cheat-sheet, public) runs a GitHub Actions workflow. It installs uv and Node, runs the full test suite, builds content and site, and publishes the result to GitHub Pages. Pull requests run the tests without deploying. A failing example, failing validation or failing test blocks the deploy. The Pages source is set to "GitHub Actions" (via `gh` or the repo settings; ask the Author if a settings change needs their approval). A short README explains how to build locally and where the site lives.

**Blocked by:** 01 (Tracer bullet).

**Status:** ready-for-agent

- [ ] Workflow runs on push to `main` and on pull requests; deploys only from `main`.
- [ ] Python version and libraries come from the pinned uv project; Node dependencies from a lockfile.
- [ ] Jupyter-kernel execution and Playwright browser tests both work in CI.
- [ ] The tracer-bullet page is live at the repository's GitHub Pages URL, and the URL is in the README and the repo description.
- [ ] A deliberately broken example on a branch makes the PR check fail (verified once, then reverted).
