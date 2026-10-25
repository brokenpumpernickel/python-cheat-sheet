"""The semantic zoom between the Overview and a Topic page (ADR 0001), driven in a real browser."""

import pytest
from playwright.sync_api import Page, expect

# Records every animation the page starts, as "<what> shows" or "<what> hides".
RECORD_ANIMATIONS = """
window.animations = [];
const animate = Element.prototype.animate;
Element.prototype.animate = function (keyframes, options) {
  const what = this.matches("[data-overview]") ? "overview" : this.dataset.topic ?? this.tagName;
  const rect = this.getBoundingClientRect();
  const [x, y] = this.style.transformOrigin.split(" ").map(parseFloat);
  window.animations.push({
    step: `${what} ${keyframes[0].opacity === 0 ? "shows" : "hides"}`,
    origin: { x: rect.left + x, y: rect.top + y },
  });
  return animate.call(this, keyframes, options);
};
"""

# Pauses every animation, so its `finished` never resolves, as in a background tab that isn't painting.
NEVER_FINISH = """
const play = Element.prototype.animate;
Element.prototype.animate = function (...args) {
  const animation = play.apply(this, args);
  animation.pause();
  return animation;
};
"""

ZOOM_IN = ["overview hides", "numbers shows"]
ZOOM_OUT = ["numbers hides", "overview shows"]


@pytest.fixture
def page(page: Page):
    page.add_init_script(RECORD_ANIMATIONS)
    return page


def steps(page: Page) -> list[str]:
    return page.evaluate("animations.map((a) => a.step)")


def forget_animations(page: Page):
    page.evaluate("animations.length = 0")


def tile(page: Page, name: str):
    return page.get_by_role("link", name=name)


def topic_page(page: Page, topic: str):
    return page.locator(f'[data-topic="{topic}"]')


def overview(page: Page):
    return page.locator("[data-overview]")


def test_clicking_a_tile_zooms_in_toward_it_and_focuses_the_page(page: Page, site_url):
    page.goto(site_url)
    box = tile(page, "Numbers").bounding_box()

    tile(page, "Numbers").click()

    expect(page.get_by_role("heading", name="Numbers", level=1)).to_be_visible()
    expect(topic_page(page, "numbers")).to_be_focused()
    expect(overview(page)).to_be_hidden()
    assert steps(page) == ZOOM_IN
    origin = page.evaluate("animations[0].origin")
    assert box["x"] <= origin["x"] <= box["x"] + box["width"]
    assert box["y"] <= origin["y"] <= box["y"] + box["height"]


def test_back_zooms_out_to_the_tile_and_focuses_it(page: Page, site_url):
    page.goto(site_url)
    tile(page, "Numbers").click()
    expect(topic_page(page, "numbers")).to_be_focused()
    forget_animations(page)

    page.go_back()

    expect(overview(page)).to_be_visible()
    expect(tile(page, "Numbers")).to_be_focused()
    expect(topic_page(page, "numbers")).to_be_hidden()
    assert steps(page) == ZOOM_OUT


def test_keyboard_tabs_to_a_tile_enter_zooms_in_and_esc_zooms_out(page: Page, site_url):
    page.goto(site_url)

    page.keyboard.press("Tab")
    expect(tile(page, "Numbers")).to_be_focused()
    page.keyboard.press("Tab")
    expect(tile(page, "Strings")).to_be_focused()

    page.keyboard.press("Enter")
    expect(page).to_have_url(f"{site_url}#strings")
    expect(topic_page(page, "strings")).to_be_focused()

    page.keyboard.press("Escape")
    expect(page).to_have_url(site_url)
    expect(overview(page)).to_be_visible()
    expect(tile(page, "Strings")).to_be_focused()


def test_esc_while_typing_in_a_field_stays_on_the_topic(page: Page, site_url):
    page.goto(f"{site_url}#numbers")
    page.evaluate("""() => {
        const field = document.createElement("input");
        document.querySelector('[data-topic="numbers"]').append(field);
        field.focus();
    }""")

    page.keyboard.press("Escape")

    expect(page).to_have_url(f"{site_url}#numbers")
    expect(overview(page)).to_be_hidden()


def test_back_link_on_the_topic_page_zooms_out(page: Page, site_url):
    page.goto(f"{site_url}#numbers")

    topic_page(page, "numbers").get_by_role("link", name="Map").click()

    expect(page).to_have_url(site_url)
    expect(tile(page, "Numbers")).to_be_focused()


def test_deep_link_opens_without_animation_and_esc_zooms_out(page: Page, site_url):
    page.goto(f"{site_url}#numbers")

    expect(page.get_by_role("heading", name="Numbers", level=1)).to_be_visible()
    expect(topic_page(page, "numbers")).to_be_focused()
    assert steps(page) == []

    page.keyboard.press("Escape")

    expect(tile(page, "Numbers")).to_be_focused()
    assert steps(page) == ZOOM_OUT


def test_switching_topics_crossfades(page: Page, site_url):
    page.goto(f"{site_url}#numbers")

    page.evaluate("location.hash = '#strings'")

    expect(topic_page(page, "strings")).to_be_focused()
    expect(topic_page(page, "numbers")).to_be_hidden()
    assert steps(page) == ["numbers hides", "strings shows"]


def test_reduced_motion_navigates_without_any_animation(page: Page, site_url):
    page.emulate_media(reduced_motion="reduce")
    page.goto(site_url)

    tile(page, "Numbers").click()
    expect(topic_page(page, "numbers")).to_be_focused()
    page.keyboard.press("Escape")
    expect(tile(page, "Numbers")).to_be_focused()
    page.go_back()  # Esc added an Overview entry; Back returns to the Topic
    expect(topic_page(page, "numbers")).to_be_focused()

    assert steps(page) == []


def test_navigation_completes_when_animations_never_finish(page: Page, site_url):
    page.add_init_script(NEVER_FINISH)
    page.goto(site_url)

    tile(page, "Numbers").click()
    expect(topic_page(page, "numbers")).to_be_focused()
    page.go_back()
    expect(tile(page, "Numbers")).to_be_focused()

    assert steps(page) == ZOOM_IN + ZOOM_OUT
