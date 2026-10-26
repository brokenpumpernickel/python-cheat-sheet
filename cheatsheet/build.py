"""The two build stages (ADR 0004): content build in Python, then the Astro site build."""

import json
import logging
import os
import platform
import shutil
import subprocess
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
EXAMPLE_LIBRARIES = {"NumPy": "numpy", "Matplotlib": "matplotlib", "SciPy": "scipy"}

# Kernels running at once. Starting a kernel is mostly waiting, so a few per core is fine.
PARALLEL_KERNELS = min(8, 2 * (os.cpu_count() or 1))

log = logging.getLogger(__name__)


def build_content(content_dir: Path, timeout: float = TIMEOUT_SECONDS) -> dict:
    """Parse the content folder and run every example; return the generated content data.

    Examples run in parallel, each in its own fresh kernel. If any fail, one ContentError lists
    them all in content order, so every broken example can be fixed in one go. An example still
    running after `timeout` seconds is stopped and counts as failing.
    """
    areas = parse_content(content_dir)
    examples = []  # (the dict that gets the Output, code, raises, where, where with the Entry's line)
    for area in areas:
        for topic in area["topics"]:
            for entry in topic["entries"]:
                where = f"{area['id']}/{topic['id']}.md ({topic['id']}/{entry['id']})"
                here = f"{area['id']}/{topic['id']}.md:{entry.pop('line')} ({topic['id']}/{entry['id']})"
                examples.append((entry, entry["code"], entry["raises"], where, here))
                pitfall = entry["pitfall"]
                if pitfall:
                    pitfall["output"] = None
                    if pitfall["code"]:
                        examples.append((pitfall, pitfall["code"], pitfall["raises"], f"{where} Pitfall", f"{here} Pitfall"))

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
    """Render the content data into a static site with Astro."""
    npm = shutil.which("npm")
    if npm is None:
        raise RuntimeError("npm not found; install Node.js to build the site")
    if not (SITE_DIR / "node_modules").is_dir():
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
    subprocess.run([npm, "run", "build"], cwd=SITE_DIR, env=env, check=True)
    shutil.rmtree(out_dir, ignore_errors=True)
    shutil.copytree(staging, out_dir)


def _output(code: str, raises: str | None, where: str, timeout: float) -> dict:
    run = run_example(code, timeout)
    if run.timed_out:
        raise ContentError(f"{where}: the example timed out after {timeout:g} s")
    if run.error and run.error_type != raises:
        expected = f" (marked raises={raises})" if raises else ""
        raise ContentError(f"{where}: the example failed with {run.error}{expected}")
    if raises and not run.error:
        raise ContentError(f"{where}: marked raises={raises}, but the example ran without an error")
    return {"text": run.stdout, "error": run.error, "figures": list(run.figures)}


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
