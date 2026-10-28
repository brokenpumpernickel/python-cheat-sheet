"""The Topic page: Entry cards and every kind of Output, copy, See also, the Entry flash and Previous /
Next stop, on the site built from tests/fixtures/site (Basics: Numbers, Strings, planned Sets; Plots: Charts)."""

import re

import pytest
from playwright.sync_api import BrowserContext, Page, expect

FLASHING = re.compile(r"\bflash\b")


def topic_page(page: Page, topic: str):
    return page.locator(f'[data-topic="{topic}"]')


def entry(page: Page, ref: str):
    return page.locator(f'[data-entry="{ref}"]')


def stop(page: Page, topic: str, which: str):
    return topic_page(page, topic).get_by_role("link", name=which)


def test_next_stop_follows_topic_order_skipping_planned_topics_and_crossing_areas(page: Page, site_url):
    page.goto(f"{site_url}#numbers")
    expect(stop(page, "numbers", "Previous stop")).to_have_count(0)

    stop(page, "numbers", "Next stop").click()
    expect(page).to_have_url(f"{site_url}#strings")

    stop(page, "strings", "Next stop").click()  # past the planned Sets, into the next Area
    expect(page).to_have_url(f"{site_url}#charts")
    expect(page.get_by_role("heading", name="Charts", level=1)).to_be_visible()
    expect(stop(page, "charts", "Next stop")).to_have_count(0)

    stop(page, "charts", "Previous stop").click()
    expect(page).to_have_url(f"{site_url}#strings")
    expect(stop(page, "strings", "Previous stop")).to_contain_text("Numbers")


def test_entry_chips_jump_to_entries_below_the_sticky_chips(page: Page, site_url):
    page.goto(f"{site_url}#numbers")
    chips = topic_page(page, "numbers").get_by_role("navigation", name="Entries")

    chips.get_by_role("link", name="Powers").click()

    expect(page).to_have_url(f"{site_url}#numbers/powers")
    powers = entry(page, "numbers/powers")
    expect(powers).to_be_in_viewport()
    assert powers.bounding_box()["y"] >= chips.bounding_box()["y"] + chips.bounding_box()["height"]


def test_see_also_navigates_to_the_linked_entry_in_another_topic(page: Page, site_url):
    page.goto(f"{site_url}#numbers")

    see_also = entry(page, "numbers/addition").get_by_role("navigation", name="See also")
    see_also.get_by_role("link", name="Joining").click()

    expect(page).to_have_url(f"{site_url}#strings/joining")
    expect(topic_page(page, "strings")).to_be_visible()
    expect(entry(page, "strings/joining")).to_have_class(FLASHING)


@pytest.mark.parametrize("motion", ["no-preference", "reduce"])
def test_deep_link_flashes_the_entry_briefly(page: Page, site_url, motion):
    page.emulate_media(reduced_motion=motion)
    page.goto(f"{site_url}#numbers/powers")

    powers = entry(page, "numbers/powers")
    expect(powers).to_be_in_viewport()
    expect(powers).to_have_class(FLASHING)
    expect(entry(page, "numbers/addition")).not_to_have_class(FLASHING)
    expect(powers).not_to_have_class(FLASHING, timeout=3000)


def test_copy_puts_the_exact_code_on_the_clipboard_and_confirms(page: Page, context: BrowserContext, site_url):
    context.grant_permissions(["clipboard-read", "clipboard-write"], origin=site_url.rstrip("/"))
    page.goto(f"{site_url}#strings/mixing-types")
    card = entry(page, "strings/mixing-types")

    card.hover()
    card.get_by_role("button", name="Copy").click()

    copied = page.evaluate("navigator.clipboard.readText()").replace("\r\n", "\n")  # Windows' clipboard uses CRLF
    assert copied == 'print("total: " + str(3))\nprint("total: " + 3)'
    expect(card.get_by_role("button")).to_have_text("Copied!")
    expect(card.get_by_role("button")).to_have_text("Copy", use_inner_text=True, timeout=3000)


def test_the_page_and_copy_give_the_shown_code_not_the_run_code(page: Page, context: BrowserContext, site_url):
    context.grant_permissions(["clipboard-read", "clipboard-write"], origin=site_url.rstrip("/"))
    page.goto(f"{site_url}#strings/repeating")
    card = entry(page, "strings/repeating")
    shown = "import random\n\nrng = random.Random()\nprint(\"ha\" * rng.randint(2, 4))"

    expect(card.locator("pre code")).to_have_text(shown)
    card.hover()
    card.get_by_role("button", name="Copy").click()
    assert page.evaluate("navigator.clipboard.readText()").replace("\r\n", "\n") == shown
    expect(card.locator("[data-output] pre")).not_to_be_empty()  # the seeded run code made the Output


def test_code_is_syntax_highlighted(page: Page, site_url):
    page.goto(f"{site_url}#strings")

    code = entry(page, "strings/joining").locator("pre code")
    expect(code).to_have_text('print("ab" + "cd")')
    colours = code.locator("span span").evaluate_all("(spans) => spans.map((s) => getComputedStyle(s).color)")
    assert len(set(colours)) >= 3  # the call, the strings and the operator differ


def test_text_output(page: Page, site_url):
    page.goto(f"{site_url}#numbers")

    output = entry(page, "numbers/addition").locator("[data-output]")
    expect(output).to_have_text("Output\n3\n7\n11\n15\n19\n23", use_inner_text=True, ignore_case=True)  # in capitals


def test_expected_error_output_shows_text_then_the_error_line(page: Page, site_url):
    page.goto(f"{site_url}#strings")

    output = entry(page, "strings/mixing-types").locator("[data-output]")
    expect(output.locator("pre")).to_have_text(["total: 3", 'TypeError: can only concatenate str (not "int") to str'])
    expect(output.locator("pre").last).to_have_css("color", "rgb(183, 28, 28)")  # --err


@pytest.mark.parametrize("scheme", ["light", "dark"])
def test_figure_output_sits_on_a_white_card(page: Page, site_url, scheme):
    page.emulate_media(color_scheme=scheme)
    page.goto(f"{site_url}#charts")

    figure = entry(page, "charts/line-chart").get_by_role("img", name="A line rising ever faster through three points.")
    expect(figure).to_be_visible()
    expect(figure.locator("svg")).to_have_count(1)
    expect(figure).to_have_css("background-color", "rgb(255, 255, 255)")
    assert figure.locator("svg").bounding_box()["width"] <= figure.bounding_box()["width"]


def widgets(page: Page, ref: str):
    return entry(page, ref).locator("[data-widgets]")


def test_widget_controls_are_drawn_above_the_figure_in_display_order(page: Page, site_url):
    page.goto(f"{site_url}#charts/interactive-chart")
    output = entry(page, "charts/interactive-chart").locator("[data-output]")
    drawing = widgets(page, "charts/interactive-chart").locator("[data-drawing]")

    expect(widgets(page, "charts/interactive-chart")).to_contain_text("Controls in Jupyter", use_inner_text=True)
    expect(drawing).to_have_attribute("aria-hidden", "true")
    expect(drawing.locator("[data-description]")).to_have_text(["mu", "n", "kind", "show", "grid", "name"])
    expect(drawing.locator("[data-value]")).to_have_text(["1.00", "10", "b", "x"])  # readouts, the choice, the text
    kinds = drawing.locator("[data-control]").evaluate_all("(rows) => rows.map((row) => row.dataset.control)")
    assert kinds == ["slider", "slider", "dropdown", "checkbox", "checkbox", "text"]
    checks = drawing.locator("[data-check]")
    assert checks.evaluate_all("(boxes) => boxes.map((box) => box.dataset.check)") == ["on", "off"]
    figure = output.locator('[role="img"]')  # not the svg inside it
    assert drawing.bounding_box()["y"] + drawing.bounding_box()["height"] <= figure.bounding_box()["y"]
    expect(entry(page, "charts/line-chart").locator("[data-widgets]")).to_have_count(0)  # only where there are any


def test_a_slider_knob_sits_at_the_value_along_its_track(page: Page, site_url):
    page.goto(f"{site_url}#charts/interactive-chart")
    sliders = widgets(page, "charts/interactive-chart").locator('[data-control="slider"]')

    for index, proportion in [(0, 4 / 6), (1, 10 / 100)]:  # mu = 1.0 in -3..3, n = 10 in 0..100
        track = sliders.nth(index).locator("[data-track]").bounding_box()
        knob = sliders.nth(index).locator("[data-knob]").bounding_box()
        assert knob["width"] > 0
        assert abs(knob["x"] + knob["width"] / 2 - (track["x"] + proportion * track["width"])) < 1.5


def test_the_controls_are_a_picture_nothing_can_be_focused_or_used(page: Page, site_url):
    page.goto(f"{site_url}#charts/interactive-chart")
    controls = widgets(page, "charts/interactive-chart")

    expect(controls.locator("input, select, textarea, button, a, [tabindex], [contenteditable]")).to_have_count(0)
    expect(controls).to_have_css("pointer-events", "none")
    expect(controls.locator("[data-drawing]")).to_have_css("user-select", "none")


SPOKEN = {
    "en": [
        "mu: slider from -3.00 to 3.00, at 1.00",
        "n: slider from 0 to 100, at 10",
        "kind: dropdown with a, b; b selected",
        "show: checkbox, checked",
        "grid: checkbox, not checked",
        "name: text box, x",
    ],
    "pl": [
        "mu: suwak od -3.00 do 3.00, ustawiony na 1.00",
        "n: suwak od 0 do 100, ustawiony na 10",
        "kind: lista rozwijana z a, b; wybrane b",
        "show: pole wyboru, zaznaczone",
        "grid: pole wyboru, niezaznaczone",
        "name: pole tekstowe, x",
    ],
}


@pytest.mark.parametrize("language", ["en", "pl"])
def test_screen_readers_hear_each_control_in_the_page_language(page: Page, site_url, language):
    page.goto(f"{site_url}?lang={language}#charts/interactive-chart")
    controls = widgets(page, "charts/interactive-chart")

    expect(controls.get_by_role("listitem")).to_have_text(SPOKEN[language], use_inner_text=True)
    caption = {"en": "Controls in Jupyter", "pl": "Kontrolki w Jupyterze"}[language]
    expect(controls.get_by_role("list")).to_have_accessible_name(caption)


def test_pitfall_with_code_has_a_sticker_and_its_own_code_and_output(page: Page, site_url):
    page.goto(f"{site_url}#numbers")
    card = entry(page, "numbers/division")

    expect(card.get_by_text("Watch out!")).to_be_visible()
    pitfall = card.get_by_role("complementary", name="Pitfall")
    expect(pitfall).to_contain_text("Pitfall: Dividing by zero raises an error.", use_inner_text=True)
    expect(pitfall.locator("pre code")).to_have_text("print(1 / 0)")
    expect(pitfall.locator("[data-output] pre")).to_have_text("ZeroDivisionError: division by zero")


def test_pitfall_without_code_is_just_the_callout(page: Page, site_url):
    page.goto(f"{site_url}#strings")
    card = entry(page, "strings/joining")

    expect(card.get_by_text("Watch out!")).to_be_visible()
    pitfall = card.get_by_role("complementary", name="Pitfall")
    expect(pitfall).to_have_text("Pitfall: + adds no space between the strings.", use_inner_text=True)
    expect(pitfall.locator("pre")).to_have_count(0)
    expect(entry(page, "numbers/addition").get_by_text("Watch out!")).to_have_count(0)


@pytest.mark.parametrize(
    ("topic", "width", "columns"),
    [("numbers", 1280, 2), ("numbers", 900, 1), ("numbers", 375, 1), ("strings", 1280, 2)],  # Strings: three cards
)
def test_cards_take_two_columns_only_on_wide_screens_and_never_widen_the_page(
    page: Page, site_url, topic, width, columns
):
    page.set_viewport_size({"width": width, "height": 800})
    page.goto(f"{site_url}#{topic}")

    lefts = {round(box["x"]) for box in (card.bounding_box() for card in page.locator(".entry:visible").all())}
    assert len(lefts) == columns
    assert page.evaluate("document.documentElement.scrollWidth") <= width


STICKER_PIECES = """
() => [...document.querySelectorAll('.sticker')].filter((s) => s.offsetParent).map((s) => {
  const card = s.closest('[data-entry]').getBoundingClientRect();
  return {
    entry: s.closest('[data-entry]').dataset.entry,
    card: [card.left, card.right],
    pieces: [...s.getClientRects()].map((r) => [r.left, r.right]),
  };
})
"""


@pytest.mark.parametrize("topic", ["numbers", "strings"])
def test_a_pitfall_sticker_is_drawn_once_on_its_own_card_in_two_columns(page: Page, site_url, topic):
    # In CSS columns, anything sticking out above a card that starts a column used to be drawn a second
    # time at the bottom of the previous column.
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto(f"{site_url}#{topic}")
    expect(topic_page(page, topic)).to_be_visible()

    stickers = page.evaluate(STICKER_PIECES)
    assert stickers, "the Topic should have a Pitfall sticker"
    for sticker in stickers:
        assert len(sticker["pieces"]) == 1, sticker
        (left, right), (card_left, card_right) = sticker["pieces"][0], sticker["card"]
        assert card_left <= left and right <= card_right + 20, sticker  # it may overhang the corner a little


@pytest.mark.parametrize("lang", ["en", "pl"])
def test_a_long_summary_stays_beside_the_glyph_on_wide_screens(page: Page, long_text_url, lang):
    page.set_viewport_size({"width": 1280, "height": 800})
    page.goto(f"{long_text_url}?lang={lang}#numbers")
    hero = topic_page(page, "numbers").locator(".hero")
    expect(hero).to_be_visible()

    glyph = hero.locator(".hero-glyph").bounding_box()
    title = hero.get_by_role("heading", level=1).bounding_box()
    assert title["x"] > glyph["x"] + glyph["width"], "the title moved below the glyph"
    assert title["y"] < glyph["y"] + glyph["height"], "the title moved below the glyph"


def test_on_a_phone_the_header_text_may_go_below_the_glyph_without_widening_the_page(page: Page, long_text_url):
    page.set_viewport_size({"width": 375, "height": 800})
    page.goto(f"{long_text_url}?lang=pl#numbers")
    expect(topic_page(page, "numbers").locator(".hero")).to_be_visible()

    assert page.evaluate("document.documentElement.scrollWidth") <= 375


TEXT_UNDER_HOME = """(hero) => {
  const home = hero.querySelector('.home').getBoundingClientRect();
  const overlaps = (r) => r.left < home.right && home.left < r.right && r.top < home.bottom && home.top < r.bottom;
  return [...hero.querySelectorAll('.area-name, h1, .summary')]
    .filter((el) => {
      const range = document.createRange();
      range.selectNodeContents(el);
      return [...range.getClientRects()].some((r) => r.width > 0 && overlaps(r));
    })
    .map((el) => el.className.split(" ")[0] || el.tagName.toLowerCase());
}"""


@pytest.mark.parametrize("width", [1100, 900, 700, 375])
@pytest.mark.parametrize("lang", ["en", "pl"])
def test_a_long_title_never_runs_under_the_map_button(page: Page, long_text_url, lang, width):
    page.set_viewport_size({"width": width, "height": 800})
    page.goto(f"{long_text_url}?lang={lang}#numbers")
    hero = topic_page(page, "numbers").locator(".hero")
    expect(hero).to_be_visible()

    assert hero.evaluate(TEXT_UNDER_HOME) == []
