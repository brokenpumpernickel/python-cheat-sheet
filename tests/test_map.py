"""The Map's layout and look, from content data with Areas of many sizes (no examples are run)."""

import math

import pytest
from playwright.sync_api import Page, expect

from conftest import built_site

SIZES = {"one": 1, "three": 3, "nine": 9, "fifteen": 15}
SWAY = 8  # px: islands tilt and bubbles bob a little, so positions are only roughly on the axes


def topic(topic_id: str, *, planned: bool = False) -> dict:
    title = topic_id.replace("-", " ").capitalize()
    return {
        "id": topic_id,
        "title": title,
        "summary": None if planned else f"About {title}.",
        "glyph": "#",
        "planned": planned,
        "pl": {"title": title, "summary": None if planned else f"O {title}."},
        "entries": [],
    }


def area(area_id: str, topics: list[dict], hue: int, *, planned: bool = False) -> dict:
    return {
        "id": area_id,
        "title": area_id.capitalize(),
        "blurb": f"The {area_id} Area.",
        "hue": hue,
        "planned": planned,
        "pl": {"title": area_id.capitalize(), "blurb": f"Obszar {area_id}."},
        "topics": topics,
    }


def map_content() -> dict:
    areas = [
        area(name, [topic(f"{name}-{k}") for k in range(1, size + 1)], hue=40 * i)
        for i, (name, size) in enumerate(SIZES.items())
    ]
    areas.append(area("later", [topic(f"later-{k}", planned=True) for k in range(1, 5)], hue=300, planned=True))
    return {"areas": areas, "meta": {"versions": [{"name": "Python", "version": "3.12.0"}]}}


@pytest.fixture(scope="module")
def map_url(tmp_path_factory):
    with built_site(map_content(), tmp_path_factory.mktemp("map")) as url:
        yield url


def circles(page: Page, area_id: str) -> tuple[dict, list[dict]]:
    """The island and its bubbles as circles: centre from the rendered box, radius from the layout size."""
    return page.evaluate(
        """(id) => {
            const circle = (el) => {
                const r = el.getBoundingClientRect();
                return { x: r.left + r.width / 2, y: r.top + r.height / 2, r: el.offsetWidth / 2 };
            };
            const island = document.querySelector(`[data-area="${id}"]`);
            return [circle(island), [...island.querySelectorAll(".bubble")].map(circle)];
        }""",
        area_id,
    )


def distance(a: dict, b: dict) -> float:
    return math.hypot(a["x"] - b["x"], a["y"] - b["y"])


@pytest.mark.parametrize("width", [1280, 375])
@pytest.mark.parametrize("area_id", [*SIZES, "later"])
def test_every_bubble_fits_inside_its_island_without_overlapping(page: Page, map_url, area_id, width):
    page.set_viewport_size({"width": width, "height": 800})
    page.goto(map_url)

    island, bubbles = circles(page, area_id)

    assert len(bubbles) == SIZES.get(area_id, 4)
    for bubble in bubbles:
        assert distance(bubble, island) + bubble["r"] <= island["r"]
    for i, a in enumerate(bubbles):
        for b in bubbles[i + 1 :]:
            assert distance(a, b) >= a["r"] + b["r"]


def test_topics_go_in_the_centre_then_clockwise_from_the_top(page: Page, map_url):
    page.goto(map_url)

    for area_id in ["nine", "fifteen"]:
        island, (first, second, third, *_) = circles(page, area_id)
        assert distance(first, island) < 2  # the centre, once there are five or more
        assert abs(second["x"] - island["x"]) < SWAY and second["y"] < island["y"]  # straight above
        assert third["x"] > second["x"]  # then clockwise

    island, (top, right, left) = circles(page, "three")
    assert abs(top["x"] - island["x"]) < SWAY and top["y"] < island["y"]
    assert right["x"] > island["x"] > left["x"]

    island, bubbles = circles(page, "fifteen")
    inner, outer = bubbles[1:7], bubbles[7:]
    assert min(distance(b, island) for b in outer) > max(distance(b, island) for b in inner)


@pytest.mark.parametrize("width", [1280, 900, 375])
def test_islands_wrap_to_fit_the_screen(page: Page, map_url, width):
    page.set_viewport_size({"width": width, "height": 800})
    page.goto(map_url)

    boxes = [page.locator(f'[data-area="{a}"]').bounding_box() for a in [*SIZES, "later"]]
    rows = {round(box["y"] + box["height"] / 2, -2) for box in boxes}

    assert len(rows) > 1
    assert page.evaluate("document.documentElement.scrollWidth") <= width


def test_planned_areas_and_topics_are_muted_and_not_links(page: Page, map_url):
    page.goto(map_url)
    later = page.locator('[data-area="later"]')

    expect(later.get_by_role("heading", name="Later")).to_contain_text("coming soon")
    expect(later.get_by_text("Later 1").filter(visible=True)).to_be_visible()
    expect(later.get_by_role("link")).to_have_count(0)
    # Muted by a dashed outline with no fill, not by fading, so the text keeps its contrast (ticket 09).
    bubble = later.locator(".bubble").first
    expect(bubble).to_have_css("border-top-style", "dashed")
    expect(bubble).to_have_css("background-color", "rgba(0, 0, 0, 0)")


def test_fonts_are_self_hosted(page: Page, map_url):
    requests = []
    page.on("request", lambda request: requests.append(request.url))
    page.goto(map_url)

    loaded = page.evaluate(
        "document.fonts.ready.then((fonts) => [...fonts].filter((f) => f.status === 'loaded').map((f) => f.family))"
    )

    assert {"Fredoka Variable", "Nunito Variable", "JetBrains Mono Variable"} <= {f.strip("\"'") for f in loaded}
    assert all(url.startswith(map_url) for url in requests)


@pytest.mark.parametrize(("scheme", "sea"), [("light", "#e9f2f7"), ("dark", "#121a2b")])
def test_theme_follows_the_system_setting(page: Page, map_url, scheme, sea):
    page.emulate_media(color_scheme=scheme)
    page.goto(map_url)

    assert page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--sea')").strip() == sea
