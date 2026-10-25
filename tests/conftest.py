"""Shared fixtures for the browser tests: sites built with the real Astro build and served locally."""

import threading
from contextlib import contextmanager
from pathlib import Path

import pytest

from cheatsheet.build import build_content, build_site, write_content_data
from cheatsheet.serve import make_server

FIXTURES = Path(__file__).parent / "fixtures"


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
def browser_context_args(browser_context_args):
    # Short enough that a later Entry starts below the fold.
    return {**browser_context_args, "viewport": {"width": 900, "height": 500}}
