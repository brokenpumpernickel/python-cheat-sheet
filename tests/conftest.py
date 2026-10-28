"""Shared fixtures for the browser tests: sites built with the real Astro build and served locally."""

import json
import shutil
import subprocess
import threading
from contextlib import contextmanager
from pathlib import Path

import pytest

from cheatsheet.build import build_content, build_site, write_content_data
from cheatsheet.serve import make_server

FIXTURES = Path(__file__).parent / "fixtures"
LABELS = Path(__file__).parent.parent / "site" / "src" / "labels.ts"


@contextmanager
def built_site(data: dict, root: Path):
    """Build the site from content data, serve it, and yield its URL."""
    write_content_data(data, root / "content.json")
    build_site(root / "content.json", root / "dist")
    server = make_server(root / "dist")
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/"
    finally:
        server.shutdown()


@pytest.fixture(scope="session")
def site_url(tmp_path_factory):
    """The site built from the fixture content folder, whose examples really run."""
    with built_site(build_content(FIXTURES / "site"), tmp_path_factory.mktemp("site")) as url:
        yield url


@pytest.fixture(scope="session")
def long_text_url(tmp_path_factory):
    """The fixture site with Numbers given a title and a summary as long as the real ones'."""
    data = build_content(FIXTURES / "site")
    numbers = data["areas"][0]["topics"][0]
    numbers["title"] = "Continuous probability distributions"
    numbers["pl"]["title"] = "Ciągłe rozkłady prawdopodobieństwa"
    numbers["summary"] = "How a sample is spread: counting into bins, choosing bins, logarithmic bins, density with a PDF, comparing two samples."
    numbers["pl"]["summary"] = (
        "Histogramy (histograms), czyli rozkład próby: zliczanie w przedziałach, wybór przedziałów, "
        "przedziały logarytmiczne, gęstość z krzywą PDF, porównanie dwóch próbek."
    )
    with built_site(data, tmp_path_factory.mktemp("long-text")) as url:
        yield url


@pytest.fixture(scope="session")
def labels() -> dict:
    """The interface label table (site/src/labels.ts) by Language, read with Node as the site build reads it."""
    node = shutil.which("node")
    assert node, "node not found; install Node.js to build the site"
    script = f"const m = await import({json.dumps(LABELS.as_uri())}); console.log(JSON.stringify(m.labels));"
    run = subprocess.run(
        [node, "--input-type=module", "--no-warnings", "-e", script],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return json.loads(run.stdout)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    # Short enough that a later Entry starts below the fold.
    return {**browser_context_args, "viewport": {"width": 900, "height": 500}}
