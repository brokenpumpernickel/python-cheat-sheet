"""The Overview's two arrangements (Map and Trail), the Map | Trail toggle and the Index rail inside a Topic,
on the site built from tests/fixtures/site (Basics: Numbers, Strings, planned Sets; Plots: Charts)."""

import re

import pytest
from playwright.sync_api import Page, expect


PHONE = {"width": 375, "height": 700}
YOU_ARE_HERE = re.compile("you are here", re.IGNORECASE)  # shown in capitals


def toggle(page: Page):
    return page.get_by_role("radiogroup", name="Overview style")


def choose(page: Page, arrangement: str):
    toggle(page).get_by_role("radio", name=arrangement).check()


def island(page: Page, area: str):
    return page.locator(f'[data-area="{area}"]')


def land(page: Page, area: str):
    return page.locator(f'[data-land-section="{area}"]')


def rail(page: Page):
    return page.get_by_role("navigation", name="Index")


def topic_page(page: Page, topic: str):
    return page.locator(f'[data-topic="{topic}"]')


def entry(page: Page, ref: str):
    return page.locator(f'[data-entry="{ref}"]')


def box(locator) -> dict:
    return locator.bounding_box()


def centre_x(locator) -> float:
    b = box(locator)
    return b["x"] + b["width"] / 2


# The Overview


def test_the_map_is_the_default_and_the_toggle_is_a_radio_group(page: Page, site_url):
    page.goto(site_url)

    expect(toggle(page).get_by_role("radio")).to_have_count(2)
    expect(toggle(page).get_by_role("radio", name="Map")).to_be_checked()
    expect(toggle(page).get_by_role("radio", name="Trail")).not_to_be_checked()
    expect(island(page, "basics")).to_be_visible()
    expect(land(page, "basics")).to_be_hidden()


def test_choosing_the_trail_swaps_the_arrangement_and_is_remembered_across_reloads(page: Page, site_url):
    page.goto(site_url)

    choose(page, "Trail")
    expect(land(page, "basics")).to_be_visible()
    expect(island(page, "basics")).to_be_hidden()

    page.reload()
    expect(toggle(page).get_by_role("radio", name="Trail")).to_be_checked()
    expect(land(page, "basics")).to_be_visible()
    expect(island(page, "basics")).to_be_hidden()

    # Arrow keys move between the radios and choose, as in any radio group.
    toggle(page).get_by_role("radio", name="Trail").focus()
    page.keyboard.press("ArrowLeft")
    expect(toggle(page).get_by_role("radio", name="Map")).to_be_checked()
    expect(island(page, "basics")).to_be_visible()

    page.reload()
    expect(toggle(page).get_by_role("radio", name="Map")).to_be_checked()
    expect(island(page, "basics")).to_be_visible()
    expect(land(page, "basics")).to_be_hidden()


def test_the_trail_numbers_each_areas_stones_in_topic_order(page: Page, site_url):
    page.goto(site_url)
    choose(page, "Trail")

    basics = land(page, "basics")
    expect(basics.get_by_role("heading", name="Basics", level=2)).to_be_visible()
    expect(basics).to_contain_text("Core language.")
    stones = basics.get_by_role("link")
    expect(stones).to_have_count(2)  # the planned Sets is no link
    expect(stones.nth(0)).to_have_accessible_name("1 Numbers Arithmetic.")
    expect(stones.nth(1)).to_have_accessible_name("2 Strings Text.")
    expect(basics.get_by_role("listitem").nth(2)).to_contain_text("Sets")
    expect(land(page, "plots").get_by_role("link")).to_have_accessible_name("1 Charts Line charts.")


def test_area_dots_jump_to_each_area_and_mark_the_one_in_view(page: Page, site_url):
    page.goto(site_url)
    choose(page, "Trail")
    dots = page.get_by_role("navigation", name="Areas")

    expect(dots.get_by_role("button", name="Basics")).to_have_attribute("aria-current", "true")
    dots.get_by_role("button", name="Plots").click()

    expect(land(page, "plots").get_by_role("heading", name="Plots")).to_be_in_viewport()
    expect(dots.get_by_role("button", name="Plots")).to_have_attribute("aria-current", "true")
    expect(dots.get_by_role("button", name="Basics")).not_to_have_attribute("aria-current", "true")


def test_zooming_in_and_out_from_the_trail_returns_to_the_stone(page: Page, site_url):
    page.goto(site_url)
    choose(page, "Trail")
    stone = land(page, "plots").get_by_role("link", name="Charts")

    stone.click()
    expect(page).to_have_url(f"{site_url}#charts")
    expect(topic_page(page, "charts")).to_be_focused()
    expect(land(page, "plots")).to_be_hidden()

    page.keyboard.press("Escape")
    expect(stone).to_be_focused()
    expect(stone).to_be_in_viewport()
    expect(island(page, "plots")).to_be_hidden()  # still the Trail


# The Index rail


def test_the_rail_is_the_index_only_inside_a_topic(page: Page, site_url):
    page.goto(site_url)
    expect(rail(page)).to_be_hidden()

    page.goto(f"{site_url}#numbers")
    expect(rail(page)).to_be_visible()
    # Map mode: one mini island per Area with its Topic pins, planned ones included but not links.
    expect(rail(page).get_by_role("list", name="Basics")).to_contain_text("Sets")
    expect(rail(page).get_by_role("list", name="Basics").get_by_role("link", name="Sets")).to_have_count(0)
    expect(rail(page).get_by_role("list", name="Plots").get_by_role("link")).to_have_accessible_name("Charts")


def test_the_toggle_inside_a_topic_swaps_only_the_rail(page: Page, site_url):
    page.goto(f"{site_url}#numbers")
    expect(rail(page).get_by_role("link", name="Charts")).to_have_accessible_name("Charts")

    choose(page, "Trail")

    expect(page).to_have_url(f"{site_url}#numbers")
    expect(topic_page(page, "numbers")).to_be_visible()
    expect(page.locator("[data-overview]")).to_be_hidden()
    # Trail mode: a numbered mini-trail, numbered as the Trail is.
    expect(rail(page).get_by_role("link", name="Numbers")).to_have_accessible_name("1 Numbers")
    expect(rail(page).get_by_role("link", name="Numbers")).to_have_attribute("aria-current", "page")
    expect(rail(page).get_by_role("link", name="Strings")).to_have_accessible_name("2 Strings")
    expect(rail(page).get_by_role("link", name="Charts")).to_have_accessible_name("1 Charts")
    expect(topic_page(page, "numbers").locator("[data-home]")).to_have_accessible_name("Trail")

    page.keyboard.press("Escape")  # the Overview now shows the Trail too
    expect(land(page, "basics")).to_be_visible()
    expect(land(page, "basics").get_by_role("link", name="Numbers")).to_be_focused()


@pytest.mark.parametrize("lang", ["en", "pl"])
@pytest.mark.parametrize("arrangement", ["Map", "Trail"])
def test_a_long_current_topic_wraps_in_the_rail_instead_of_widening_it(page: Page, long_text_url, arrangement, lang):
    page.goto(long_text_url)
    choose(page, arrangement)  # remembered, and the toggle's names are English here
    page.goto(f"{long_text_url}?lang={lang}#numbers")
    index = page.locator("[data-rail]")  # named in the page's Language
    expect(index.locator('[aria-current="page"][data-pin="numbers"]:visible')).to_contain_text(
        YOU_ARE_HERE if lang == "en" else re.compile("tu jesteś", re.IGNORECASE), use_inner_text=True
    )

    widths = index.evaluate("(r) => [r.scrollWidth, r.clientWidth]")
    assert widths[0] <= widths[1], f"the rail scrolls sideways: {widths}"


@pytest.mark.parametrize("arrangement", ["Map", "Trail"])
def test_the_rail_marks_you_are_here_and_expands_its_entries_and_pins_switch_topics(
    page: Page, site_url, arrangement
):
    page.goto(site_url)
    choose(page, arrangement)
    page.goto(f"{site_url}#numbers")
    numbers = rail(page).get_by_role("link", name="Numbers")
    strings = rail(page).get_by_role("link", name="Strings")

    expect(numbers).to_have_attribute("aria-current", "page")
    expect(numbers).to_contain_text(YOU_ARE_HERE, use_inner_text=True)
    expect(strings).not_to_have_attribute("aria-current", "page")
    expect(strings).not_to_contain_text(YOU_ARE_HERE, use_inner_text=True)
    for title in ["Addition", "Subtraction", "Multiplication", "Division", "Powers"]:
        expect(rail(page).get_by_role("link", name=title, exact=True)).to_be_visible()
    expect(rail(page).get_by_role("link", name="Joining")).to_be_hidden()

    strings.click()

    expect(page).to_have_url(f"{site_url}#strings")
    expect(topic_page(page, "strings")).to_be_focused()
    expect(topic_page(page, "numbers")).to_be_hidden()
    expect(strings).to_have_attribute("aria-current", "page")
    expect(numbers).not_to_have_attribute("aria-current", "page")
    expect(rail(page).get_by_role("link", name="Joining")).to_be_visible()
    expect(rail(page).get_by_role("link", name="Addition")).to_be_hidden()


def test_switching_topics_from_the_rail_crossfades_and_the_rail_stays(page: Page, site_url):
    page.add_init_script("""
        window.animations = [];
        const animate = Element.prototype.animate;
        Element.prototype.animate = function (keyframes, options) {
          window.animations.push(this.matches("[data-rail]") ? "rail" : this.dataset.topic ?? this.tagName);
          return animate.call(this, keyframes, options);
        };
    """)
    page.goto(f"{site_url}#numbers")

    rail(page).get_by_role("link", name="Strings").click()

    expect(topic_page(page, "strings")).to_be_focused()
    assert page.evaluate("animations") == ["numbers", "strings"]


def test_rail_entry_links_jump_within_the_page_and_the_scroll_spy_follows(page: Page, site_url):
    page.goto(f"{site_url}#numbers")
    current = rail(page).locator('[data-rail-entry][aria-current="true"]:visible')
    expect(current).to_have_text("Addition", use_inner_text=True)

    rail(page).get_by_role("link", name="Division").click()
    expect(page).to_have_url(f"{site_url}#numbers/division")
    expect(entry(page, "numbers/division")).to_be_in_viewport()
    expect(current).to_have_text("Division", use_inner_text=True)

    # Scrolling by hand: the Entry that has reached the sticky chips is the one being read.
    page.evaluate("""() => {
        const card = document.querySelector('[data-entry="numbers/subtraction"]');
        window.scrollTo(0, card.getBoundingClientRect().top + window.scrollY - 80);
    }""")
    expect(current).to_have_text("Subtraction", use_inner_text=True)

    page.evaluate("window.scrollTo(0, 0)")
    expect(current).to_have_text("Addition", use_inner_text=True)


@pytest.mark.parametrize("ref", ["numbers/multiplication", "numbers/powers"])
def test_a_deep_link_highlights_its_entry_in_the_rail(page: Page, site_url, ref):
    page.goto(f"{site_url}#{ref}")

    expect(rail(page).locator('[data-rail-entry][aria-current="true"]:visible')).to_have_attribute("data-rail-entry", ref)


# Phone width


@pytest.mark.parametrize("arrangement", ["Map", "Trail"])
def test_on_a_phone_the_rail_is_a_strip_centred_on_the_current_topic_without_entries(
    page: Page, site_url, arrangement
):
    page.set_viewport_size(PHONE)
    page.goto(site_url)
    choose(page, arrangement)
    page.goto(f"{site_url}#strings")
    strip = rail(page)
    pins = strip.get_by_role("link")

    expect(pins).to_have_count(3)  # Numbers, Strings, Charts: no planned Topics, no Entries
    expect(strip.get_by_role("link", name="Joining")).to_be_hidden()
    expect(strip.get_by_text("Sets").filter(visible=True)).to_have_count(0)
    assert len({round(box(pin)["y"]) for pin in pins.all()}) == 1  # one row
    here = strip.get_by_role("link", name="Strings")
    expect(here).to_contain_text(YOU_ARE_HERE, use_inner_text=True)
    assert abs(centre_x(here) - centre_x(strip)) < 2
    assert page.evaluate("document.documentElement.scrollWidth") <= PHONE["width"]


def test_on_a_phone_the_strip_stays_above_the_sticky_chips(page: Page, site_url):
    page.set_viewport_size(PHONE)
    page.goto(f"{site_url}#numbers/subtraction")
    strip = rail(page)
    chips = topic_page(page, "numbers").get_by_role("navigation", name="Entries")
    subtraction = entry(page, "numbers/subtraction")

    expect(subtraction).to_be_in_viewport()
    assert box(strip)["y"] == 0
    assert box(chips)["y"] >= box(strip)["height"] - 1
    assert box(subtraction)["y"] >= box(chips)["y"] + box(chips)["height"]
