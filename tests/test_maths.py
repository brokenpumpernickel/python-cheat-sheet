"""Displayed maths in Outputs (ticket 32, ADR 0007): typeset at build time with KaTeX, in order with printed
text, on the site built from tests/fixtures/maths (SymPy: Algebra). How the build captures the maths is
tested with the other content-build tests, in test_content_build.py."""

import json
from urllib.request import urlopen

import pytest
from playwright.sync_api import Page, expect

from cheatsheet.build import build_content, build_site, write_content_data
from cheatsheet.content import ContentError
from conftest import FIXTURES, built_site
from test_accessibility import THEMES, audit, hue_content


@pytest.fixture(scope="module")
def maths_url(tmp_path_factory):
    with built_site(build_content(FIXTURES / "maths"), tmp_path_factory.mktemp("maths")) as url:
        yield url


def output(page: Page, ref: str):
    return page.locator(f'[data-entry="{ref}"] [data-output]').first


def test_maths_is_typeset_with_mathml_in_order_with_printed_text(page: Page, maths_url):
    page.goto(f"{maths_url}#algebra")
    shown = output(page, "algebra/printed-and-displayed")

    blocks = shown.locator(":scope > pre, :scope > .maths")
    expect(blocks).to_have_count(4)
    assert blocks.evaluate_all("(blocks) => blocks.map((block) => block.tagName)") == ["PRE", "DIV", "PRE", "DIV"]
    expect(shown.locator("pre")).to_have_text(["expand", "factor"])
    maths = shown.locator(".maths math")  # MathML, for screen readers
    expect(maths).to_have_count(2)
    expect(maths.first.locator("annotation")).to_have_text(r"\displaystyle x^{2} + 2 x + 1")
    expect(shown.locator(".maths .katex-html").first).to_have_attribute("aria-hidden", "true")  # drawn for the eye
    expect(output(page, "algebra/collections").locator(".maths math")).to_have_count(3)


def test_a_plain_display_shows_as_text(page: Page, maths_url):
    page.goto(f"{maths_url}#algebra")

    expect(output(page, "algebra/plain-display").locator("pre")).to_have_text("1\n3\n2")
    expect(output(page, "algebra/plain-display").locator(".maths")).to_have_count(0)


def test_the_error_line_comes_after_the_maths(page: Page, maths_url):
    page.goto(f"{maths_url}#algebra")
    pitfall = page.locator('[data-entry="algebra/wide-formula"] [data-output]').last

    classes = pitfall.locator(":scope > .maths, :scope > pre").evaluate_all("(blocks) => blocks.map((b) => b.className)")
    assert [name.split()[0] for name in classes] == ["maths", "error"]


@pytest.mark.parametrize("theme", THEMES)
def test_maths_is_left_aligned_in_the_text_colour(page: Page, maths_url, theme):
    page.emulate_media(color_scheme=theme)
    page.goto(f"{maths_url}#algebra")
    shown = output(page, "algebra/printed-and-displayed")
    text, maths = shown.locator("pre").first, shown.locator(".maths").first

    assert maths.locator(".katex").evaluate("(e) => getComputedStyle(e).color") == text.evaluate("(e) => getComputedStyle(e).color")
    assert abs(maths.locator(".katex-html").bounding_box()["x"] - text.bounding_box()["x"]) < 1


def test_a_wide_formula_scrolls_inside_its_output_not_the_page(page: Page, maths_url):
    page.goto(f"{maths_url}#algebra/wide-formula")
    shown = output(page, "algebra/wide-formula")
    maths = shown.locator(".maths")

    expect(maths.locator("math")).to_have_count(1)
    assert maths.evaluate("(e) => e.scrollWidth > e.clientWidth")  # it is wider than the card, and scrolls
    assert maths.evaluate("(e) => e.scrollHeight <= e.clientHeight")  # no vertical scroll as well
    assert maths.bounding_box()["width"] <= shown.bounding_box()["width"]
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
    expect(maths).to_have_attribute("tabindex", "0")  # so a keyboard can scroll it
    expect(output(page, "algebra/printed-and-displayed").locator("[tabindex]")).to_have_count(0)  # these fit


def test_katex_and_its_fonts_come_with_the_site(page: Page, maths_url):
    requests = []
    page.on("request", lambda request: requests.append(request.url))
    page.goto(f"{maths_url}#algebra")
    expect(output(page, "algebra/collections").locator(".maths math")).to_have_count(3)
    page.evaluate("document.fonts.ready")

    assert all(url.startswith(maths_url) for url in requests), [url for url in requests if not url.startswith(maths_url)]
    assert any("KaTeX_Main" in url for url in requests)
    assert page.evaluate("[...document.scripts].every((script) => !/katex/i.test(script.src))")  # no client-side maths


def test_search_indexes_no_latex_or_katex_markup(maths_url):
    with urlopen(f"{maths_url}search.json") as response:
        index = response.read().decode("utf-8")

    assert "displaystyle" not in index
    assert "katex" not in index.lower()
    assert any(doc["route"] == "algebra/printed-and-displayed" for doc in json.loads(index)["docs"])


@pytest.mark.parametrize("theme", THEMES)
def test_axe_finds_nothing_on_a_page_with_maths(page: Page, maths_url, theme):
    page.emulate_media(color_scheme=theme, reduced_motion="reduce")
    page.goto(f"{maths_url}#algebra")
    expect(output(page, "algebra/printed-and-displayed").locator(".maths")).to_have_count(2)
    expect(output(page, "algebra/wide-formula").locator(".maths")).to_have_attribute("tabindex", "0")

    problems = audit(page)
    assert not problems, problems


def test_maths_katex_cannot_typeset_fails_the_build_naming_the_entry(tmp_path):
    data = hue_content()
    values = data["areas"][0]["topics"][0]["entries"][0]
    values["output"]["parts"] = [{"text": "a"}, {"maths": r"\displaystyle \frac{1}{\notacommand{x}}"}]
    values["pitfall"]["output"]["parts"] = [{"maths": r"\left( x"}]
    write_content_data(data, tmp_path / "content.json")

    with pytest.raises(ContentError) as failure:
        build_site(tmp_path / "content.json", tmp_path / "dist")

    assert str(failure.value).splitlines() == [
        r"hue-0/hue-0-topic.md (hue-0-topic/values): KaTeX can't typeset the displayed maths "
        r"\displaystyle \frac{1}{\notacommand{x}} (Undefined control sequence: \notacommand)",
        r"hue-0/hue-0-topic.md (hue-0-topic/values) Pitfall: KaTeX can't typeset the displayed maths "
        r"\left( x (Expected '\right', got 'EOF')",
    ]
