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

    figure = entry(page, "charts/line-chart").get_by_role("img", name="Figure drawn by the code above")
    expect(figure).to_be_visible()
    expect(figure.locator("svg")).to_have_count(1)
    expect(figure).to_have_css("background-color", "rgb(255, 255, 255)")
    assert figure.locator("svg").bounding_box()["width"] <= figure.bounding_box()["width"]


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


@pytest.mark.parametrize(("width", "columns"), [(1280, 2), (900, 1), (375, 1)])
def test_cards_take_two_columns_only_on_wide_screens_and_never_widen_the_page(page: Page, site_url, width, columns):
    page.set_viewport_size({"width": width, "height": 800})
    page.goto(f"{site_url}#numbers")

    lefts = {round(box["x"]) for box in (card.bounding_box() for card in page.locator(".entry:visible").all())}
    assert len(lefts) == columns
    assert page.evaluate("document.documentElement.scrollWidth") <= width
