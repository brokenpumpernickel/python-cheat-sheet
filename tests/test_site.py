"""Seam 2: the site built from a fixture content folder, driven in a real browser."""

import platform
import threading
from importlib.metadata import version
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from cheatsheet.build import build_content, build_site, write_content_data
from cheatsheet.serve import make_server

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def site_url(tmp_path_factory):
    root = tmp_path_factory.mktemp("site")
    write_content_data(build_content(FIXTURES / "site"), root / "content.json")
    build_site(root / "content.json", root / "dist")
    server = make_server(root / "dist")
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_port}/"
    server.shutdown()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    # Short enough that a later Entry starts below the fold.
    return {**browser_context_args, "viewport": {"width": 900, "height": 500}}


def overview(page: Page):
    return page.get_by_role("heading", name="Python Cheat Sheet", level=1)


def test_overview_lists_areas_and_topics(page: Page, site_url):
    page.goto(site_url)

    expect(page.get_by_role("heading", name="Basics", level=2)).to_be_visible()
    expect(page.get_by_role("link", name="Numbers")).to_be_visible()
    expect(page.get_by_role("link", name="Strings")).to_be_visible()
    expect(page.get_by_text("Sets")).to_be_visible()
    expect(page.get_by_role("link", name="Sets")).to_have_count(0)


def test_topic_link_opens_the_topic_and_back_returns_to_the_overview(page: Page, site_url):
    page.goto(site_url)
    page.get_by_role("link", name="Numbers").click()

    expect(page).to_have_url(f"{site_url}#numbers")
    expect(page.get_by_role("heading", name="Numbers", level=1)).to_be_visible()
    expect(page.get_by_role("heading", name="Addition")).to_be_visible()
    expect(page.get_by_text("3\n7\n11\n15\n19\n23")).to_be_visible()
    expect(overview(page)).to_be_hidden()

    page.go_back()

    expect(overview(page)).to_be_visible()
    expect(page.get_by_role("heading", name="Numbers", level=1)).to_be_hidden()


def test_entry_link_scrolls_to_the_entry_and_back_steps_out(page: Page, site_url):
    page.goto(site_url)
    page.get_by_role("link", name="Numbers").click()
    page.get_by_role("link", name="Division").click()

    expect(page).to_have_url(f"{site_url}#numbers/division")
    expect(page.get_by_role("heading", name="Division")).to_be_in_viewport()
    expect(page.get_by_role("heading", name="Addition")).not_to_be_in_viewport()

    page.go_back()
    expect(page).to_have_url(f"{site_url}#numbers")
    expect(page.get_by_role("heading", name="Numbers", level=1)).to_be_in_viewport()

    page.go_back()
    expect(overview(page)).to_be_visible()


def test_opening_a_deep_link_lands_on_the_entry(page: Page, site_url):
    page.goto(f"{site_url}#numbers/multiplication")

    expect(overview(page)).to_be_hidden()
    expect(page.get_by_role("heading", name="Multiplication")).to_be_in_viewport()
    expect(page.get_by_role("heading", name="Addition")).not_to_be_in_viewport()


@pytest.mark.parametrize("route", ["#sets", "#no-such-topic"])
def test_planned_or_unknown_topic_shows_the_overview(page: Page, site_url, route):
    page.goto(f"{site_url}{route}")

    expect(overview(page)).to_be_visible()


def test_footer_shows_the_versions_examples_ran_with(page: Page, site_url):
    page.goto(site_url)

    footer = page.get_by_role("contentinfo")
    expect(footer).to_contain_text(f"Python {platform.python_version()}")
    expect(footer).to_contain_text(f"NumPy {version('numpy')}")
    expect(footer).to_contain_text(f"Matplotlib {version('matplotlib')}")
