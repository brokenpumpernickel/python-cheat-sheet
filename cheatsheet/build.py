"""The two build stages (ADR 0004): content build in Python, then the Astro site build."""

import json
import logging
import os
import platform
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from importlib.metadata import version
from pathlib import Path

from cheatsheet.content import ContentError, parse_content
from cheatsheet.execute import TIMEOUT_SECONDS, run_example

REPO = Path(__file__).resolve().parent.parent
CONTENT_DIR = REPO / "content"
CONTENT_DATA = REPO / "generated" / "content.json"
SITE_DIR = REPO / "site"
SITE_OUT_DIR = SITE_DIR / "dist"

# Libraries the examples use, shown in the footer: display name -> distribution name.
EXAMPLE_LIBRARIES = {
    "NumPy": "numpy",
    "Matplotlib": "matplotlib",
    "SciPy": "scipy",
    "pandas": "pandas",
    "SymPy": "sympy",
    "ipywidgets": "ipywidgets",
}

# Kernels running at once. Starting a kernel is mostly waiting, so a few per core is fine.
PARALLEL_KERNELS = min(8, 2 * (os.cpu_count() or 1))

# How the site build starts the message of a content problem it finds (site/src/maths.ts).
_CONTENT_ERROR = "Content error: "

log = logging.getLogger(__name__)


def build_content(content_dir: Path, timeout: float = TIMEOUT_SECONDS) -> dict:
    """Parse the content folder and run every example; return the generated content data.

    Examples run in parallel, each in its own fresh kernel. If any fail, one ContentError lists
    them all in content order, so every broken example can be fixed in one go. An example still
    running after `timeout` seconds is stopped and counts as failing.
    """
    areas = parse_content(content_dir)
    examples = []  # (the dict that gets the Output, run code, raises, where, where with the Entry's line)
    for area in areas:
        for topic in area["topics"]:
            for entry in topic["entries"]:
                where = f"{area['id']}/{topic['id']}.md ({topic['id']}/{entry['id']})"
                here = f"{area['id']}/{topic['id']}.md:{entry.pop('line')} ({topic['id']}/{entry['id']})"
                examples.append((entry, entry.pop("run"), entry["raises"], where, here))
                pitfall = entry["pitfall"]
                if pitfall:
                    pitfall["output"] = None
                    run = pitfall.pop("run")
                    if run:
                        examples.append((pitfall, run, pitfall["raises"], f"{where} Pitfall", f"{here} Pitfall"))

    failures = []
    with ThreadPoolExecutor(max_workers=PARALLEL_KERNELS) as pool:
        runs = [pool.submit(_output, code, raises, where, timeout) for _, code, raises, where, _ in examples]
        for (target, _, _, where, here), run in zip(examples, runs):
            try:
                target["output"] = run.result()
                log.info("ran %s", where)
                _check_figure_description(target, here)
            except ContentError as error:
                failures.append(str(error))
    if failures:
        raise ContentError("\n".join(failures))
    return {"areas": areas, "meta": {"versions": _versions()}}


def write_content_data(data: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def build_site(content_data: Path, out_dir: Path, base: str = "/") -> None:
    """Render the content data into a static site with Astro.

    Displayed maths that KaTeX can't typeset fails the site build (site/src/maths.ts); that raises a
    ContentError naming each Entry, like the content build's own checks.
    """
    npm = shutil.which("npm")
    if npm is None:
        raise RuntimeError("npm not found; install Node.js to build the site")
    # npm records what it installed in node_modules/.package-lock.json; an older record means the site's
    # packages changed since (a pull that added one), so they are installed again.
    installed = SITE_DIR / "node_modules" / ".package-lock.json"
    if not installed.is_file() or installed.stat().st_mtime < (SITE_DIR / "package-lock.json").stat().st_mtime:
        subprocess.run([npm, "ci"], cwd=SITE_DIR, check=True)
    # Astro moves built assets into its output folder by renaming them, which fails across drives
    # (EXDEV on Windows), so it builds inside the site folder and the result is copied to out_dir.
    staging = SITE_DIR / ".astro" / "out"
    env = {
        **os.environ,
        "CHEATSHEET_CONTENT_DATA": str(content_data.resolve()),
        "CHEATSHEET_OUT_DIR": str(staging),
        "SITE_BASE": base,
        "ASTRO_TELEMETRY_DISABLED": "1",
    }
    # Astro logs progress to stdout and problems to stderr, which is kept to find content errors in.
    astro = subprocess.run([npm, "run", "build"], cwd=SITE_DIR, env=env, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    content_errors = _content_errors(astro.stderr)
    if astro.returncode and content_errors:
        raise ContentError("\n".join(content_errors))
    sys.stderr.write(astro.stderr)
    astro.check_returncode()
    shutil.rmtree(out_dir, ignore_errors=True)
    shutil.copytree(staging, out_dir)


def _content_errors(log: str) -> list[str]:
    """The content errors the site build reported, once each, in order and without the prefix: Astro
    repeats an error's message, and its first line may follow "[ERROR] Error: "."""
    lines = (re.sub(r"\x1b\[[0-9;]*m", "", line) for line in log.splitlines())
    return list(dict.fromkeys(line.partition(_CONTENT_ERROR)[2] for line in lines if _CONTENT_ERROR in line))


def _output(code: str, raises: str | None, where: str, timeout: float) -> dict:
    run = run_example(code, timeout)
    if run.timed_out:
        raise ContentError(f"{where}: the example timed out after {timeout:g} s")
    if run.error and run.error_type != raises:
        expected = f" (marked raises={raises})" if raises else ""
        raise ContentError(f"{where}: the example failed with {run.error}{expected}")
    if raises and not run.error:
        raise ContentError(f"{where}: marked raises={raises}, but the example ran without an error")
    if run.unsupported_widget:
        raise ContentError(f"{where}: the example displays a {run.unsupported_widget} widget, which the site can't draw yet")
    return {"parts": list(run.parts), "error": run.error, "figures": list(run.figures), "widgets": list(run.widgets)}


def _check_figure_description(example: dict, here: str) -> None:
    """A figure's description is its accessible name, so an example needs one exactly when it draws figures."""
    count = len(example["output"]["figures"])
    if count and not example["figure"]:
        drawn = "a figure" if count == 1 else f"{count} figures"
        raise ContentError(f"{here}: the example draws {drawn} but has no description; add a '### Figure' section after its code")
    if not count and example["figure"]:
        raise ContentError(f"{here} Figure: the example draws no figure; remove the '### Figure' description")


def _versions() -> list[dict]:
    return [{"name": "Python", "version": platform.python_version()}] + [
        {"name": name, "version": version(dist)} for name, dist in EXAMPLE_LIBRARIES.items()
    ]
