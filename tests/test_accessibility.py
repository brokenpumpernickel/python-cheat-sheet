"""Accessibility and devices (ticket 09): an axe audit of every view in both themes and both Languages,
colour contrast for every Area hue, a keyboard-only walkthrough, reduced motion and phone widths.
Most tests use the site built from tests/fixtures/site (Basics: Numbers, Strings, planned Sets; Plots: Charts)."""

import re
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from conftest import built_site

# axe-core, from the site's npm dev dependencies (installed by `npm ci` in site/).
AXE = Path(__file__).parent.parent / "site" / "node_modules" / "axe-core" / "axe.min.js"
# WCAG 2.2 A and AA, plus axe's best practices.
AXE_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]

THEMES = ["light", "dark"]
LANGUAGES = ["en", "pl"]
PHONES = [{"width": 320, "height": 640}, {"width": 375, "height": 700}]

# axe can't tell the contrast of text over a gradient, and reports it as needing review. This replaces each
# gradient background with one of its own colours ("first" or "last" stop), so that axe can judge the text
# against both ends. A small repeating pattern (the Overview's dotted sea) is texture, so it's left out, and
# so are decorative pictures drawn under text (the Trail's dotted path), which axe would otherwise give up
# on. RESTORE_GRADIENTS puts everything back.
FLATTEN_GRADIENTS = """(stop) => {
    window.flattened = [];
    for (const element of document.querySelectorAll('svg[aria-hidden="true"]')) {
        window.flattened.push([element, element.getAttribute("style")]);
        element.style.visibility = "hidden";
    }
    for (const element of document.querySelectorAll("*")) {
        const style = getComputedStyle(element);
        if (!style.backgroundImage.includes("gradient")) continue;
        const colours = style.backgroundImage.match(/(rgba?|color)\\([^)]*\\)/g) ?? [];
        const [width, height] = style.backgroundSize.split(" ").map(parseFloat);
        const texture = width < 40 && height < 40;
        window.flattened.push([element, element.getAttribute("style")]);
        element.style.backgroundImage = "none";
        if (!texture && colours.length) element.style.backgroundColor = stop === "first" ? colours[0] : colours.at(-1);
    }
}"""
RESTORE_GRADIENTS = """() => {
    for (const [element, style] of window.flattened) {
        if (style === null) element.removeAttribute("style");
        else element.setAttribute("style", style);
    }
}"""


def run_axe(page: Page, rules: list[str] | None = None) -> dict:
    if not page.evaluate("'axe' in window"):
        page.add_script_tag(path=str(AXE))
    options = {"runOnly": {"type": "rule", "values": rules}} if rules else {"runOnly": {"type": "tag", "values": AXE_TAGS}}
    return page.evaluate("(options) => axe.run(document, options)", options)


def describe(results: list[dict]) -> str:
    lines = []
    for result in results:
        lines.append(f"{result['id']}: {result['help']}")
        for node in result["nodes"]:
            lines.append(f"    {node['target']}: {node['failureSummary'] or node['any'][0]['message']}")
    return "\n".join(lines)


def audit(page: Page) -> str:
    """Every axe violation on the page as it stands, plus colour contrast that axe left for review, judged
    against both ends of every gradient. Empty when the page passes."""
    problems = run_axe(page)["violations"]
    for stop in ("first", "last"):
        page.evaluate(FLATTEN_GRADIENTS, stop)
        contrast = run_axe(page, ["color-contrast"])
        page.evaluate(RESTORE_GRADIENTS)
        problems += contrast["violations"] + undecided(contrast["incomplete"])
    return describe(problems)


def undecided(incomplete: list[dict]) -> list[dict]:
    """Contrast that axe left for review, except icons (only non-text characters), which aren't text."""
    results = []
    for result in incomplete:
        nodes = [n for n in result["nodes"] if not all(c.get("data", {}).get("messageKey") == "nonBmp" for c in n["any"])]
        if nodes:
            results.append({**result, "nodes": nodes})
    return results


def choose_trail(page: Page):
    page.locator('[data-arrangement-choice][value="trail"]').check()


def topic_page(page: Page, topic: str):
    return page.locator(f'[data-topic="{topic}"]')


def entry(page: Page, ref: str):
    return page.locator(f'[data-entry="{ref}"]')


def search(page: Page):
    return page.get_by_role("dialog")


# The automated audit


VIEWS = ["map", "trail", "topic in map", "topic in trail", "search"]


@pytest.mark.parametrize("view", VIEWS)
@pytest.mark.parametrize("language", LANGUAGES)
@pytest.mark.parametrize("theme", THEMES)
def test_axe_finds_nothing(page: Page, site_url, theme, language, view):
    page.emulate_media(color_scheme=theme, reduced_motion="reduce")
    page.goto(f"{site_url}?lang={language}")
    if "trail" in view:
        choose_trail(page)
    if view.startswith("topic"):
        page.goto(f"{site_url}?lang={language}#numbers")  # an Output, an error line, a Pitfall, See also
        expect(topic_page(page, "numbers")).to_be_visible()
    if view == "search":
        page.goto(f"{site_url}?lang={language}#charts")  # a figure behind the pop-up
        page.keyboard.press("Control+k")
        page.keyboard.type("string")  # results that fit without scrolling, so axe sees every one
        expect(search(page).get_by_role("option")).not_to_have_count(0)

    problems = audit(page)
    assert not problems, problems


def test_the_audit_catches_faint_text_on_the_sea(page: Page, site_url):
    """A control: text over the body's gradient is judged, not left for review."""
    page.goto(site_url)
    page.add_style_tag(content=".hint { color: var(--wave) !important }")

    assert "color-contrast" in audit(page)


@pytest.mark.parametrize("language", LANGUAGES)
@pytest.mark.parametrize("theme", THEMES)
def test_the_figure_topic_passes_too(page: Page, site_url, theme, language):
    """Figures, and the drawing of an example's widget controls with its screen-reader text."""
    page.emulate_media(color_scheme=theme)
    page.goto(f"{site_url}?lang={language}#charts")
    expect(topic_page(page, "charts")).to_be_visible()

    problems = audit(page)
    assert not problems, problems


# Contrast for any Area hue: the Author picks hues freely (0-360), so text in and on an Area's colour must
# meet AA whatever it is. Content data with an Area every 30 degrees, each with an Entry that has every kind
# of text, drawn widget controls included (no examples are run).

HUES = range(0, 360, 30)
HUE_WIDGETS = [
    {"kind": "slider", "description": "mu", "min": 0, "max": 10, "step": 1, "value": 3,
     "readout": "3", "minReadout": "0", "maxReadout": "10"},
    {"kind": "dropdown", "description": "kind", "options": ["a", "b"], "value": "a"},
    {"kind": "checkbox", "description": "show", "value": True},
    {"kind": "text", "description": "name", "value": "x"},
]


def hue_entry(topic_id: str, see: str) -> dict:
    return {
        "id": "values",
        "title": "Values",
        "explain": "Use <code>print</code> to show values.",
        "code": "# a comment\nx = [1, 'a', len('b')]\nprint(x)",
        "raises": None,
        "figure": None,
        "output": {"text": "[1, 'a', 1]\n", "error": None, "figures": [], "widgets": HUE_WIDGETS},
        "see": [see],
        "pitfall": {
            "text": "Indexes start at <code>0</code>.",
            "code": "x = []\nx[0]",
            "raises": "IndexError",
            "figure": None,
            "output": {"text": "", "error": "IndexError: list index out of range", "figures": [], "widgets": []},
        },
        "pl": {
            "title": "Wartości",
            "explain": "Użyj <code>print</code>.",
            "pitfall": "Indeksy od <code>0</code>.",
            "figure": None,
            "pitfallFigure": None,
        },
    }


def hue_content() -> dict:
    areas = []
    names = [f"hue-{hue}" for hue in HUES]
    for k, hue in enumerate(HUES):
        name = names[k]
        see = f"{names[(k + 1) % len(names)]}-topic/values"
        topics = [
            {
                "id": f"{name}-topic",
                "title": f"Hue {hue}",
                "summary": f"Text on hue {hue}.",
                "glyph": "[ ]",
                "planned": False,
                "pl": {"title": f"Odcień {hue}", "summary": f"Tekst na odcieniu {hue}."},
                "entries": [hue_entry(f"{name}-topic", see)],
            },
            {
                "id": f"{name}-later",
                "title": "Later",
                "summary": None,
                "glyph": "…",
                "planned": True,
                "pl": {"title": "Później", "summary": None},
                "entries": [],
            },
        ]
        areas.append(
            {
                "id": name,
                "title": f"Hue {hue}",
                "blurb": f"The Area with hue {hue}.",
                "hue": hue,
                "planned": False,
                "pl": {"title": f"Odcień {hue}", "blurb": f"Obszar o odcieniu {hue}."},
                "topics": topics,
            }
        )
    areas.append(
        {
            "id": "planned",
            "title": "Planned",
            "blurb": "Coming later.",
            "hue": 200,
            "planned": True,
            "pl": {"title": "Planowany", "blurb": "Później."},
            "topics": [
                {
                    "id": "planned-topic",
                    "title": "Someday",
                    "summary": None,
                    "glyph": "?",
                    "planned": True,
                    "pl": {"title": "Kiedyś", "summary": None},
                    "entries": [],
                }
            ],
        }
    )
    return {"areas": areas, "meta": {"versions": [{"name": "Python", "version": "3.12.0"}]}}


@pytest.fixture(scope="module")
def hues_url(tmp_path_factory):
    with built_site(hue_content(), tmp_path_factory.mktemp("hues")) as url:
        yield url


@pytest.mark.parametrize("theme", THEMES)
def test_text_meets_aa_contrast_for_every_area_hue(page: Page, hues_url, theme):
    # Tall enough that the side rail shows every Area without scrolling: axe can't judge text scrolled away.
    page.set_viewport_size({"width": 1280, "height": 2000})
    page.emulate_media(color_scheme=theme, reduced_motion="reduce")
    failures = {}

    page.goto(hues_url)
    failures["map"] = audit(page)
    choose_trail(page)
    failures["trail"] = audit(page)
    for k, hue in enumerate(HUES):
        # The rail in both arrangements, alternately; each shows every Area.
        page.locator(f'[data-arrangement-choice][value="{"map" if k % 2 else "trail"}"]').check()
        page.goto(f"{hues_url}#hue-{hue}-topic")
        expect(topic_page(page, f"hue-{hue}-topic")).to_be_visible()
        failures[f"hue {hue}"] = audit(page)

    failing = "\n".join(f"{view}:\n{problems}" for view, problems in failures.items() if problems)
    assert not failing, failing


# Planned Topics are muted, but their names still read as text, and say they're planned.


@pytest.mark.parametrize("arrangement", ["map", "trail"])
@pytest.mark.parametrize("where", ["[data-overview]", "[data-rail]"])
def test_planned_topics_are_not_faded_and_say_they_are_planned(page: Page, site_url, arrangement, where):
    page.goto(site_url)
    page.locator(f'[data-arrangement-choice][value="{arrangement}"]').check()
    if where == "[data-rail]":
        page.goto(f"{site_url}#numbers")
    sets = page.locator(f"{where} .planned").filter(has_text="Sets").filter(visible=True)

    expect(sets).to_have_count(1)
    expect(sets).to_contain_text(re.compile(r"Sets\s*\(coming soon\)"), use_inner_text=True)
    assert sets.evaluate("(e) => getComputedStyle(e).opacity") == "1"


# The keyboard walkthrough


# Where the focused element shows its focus: a radio on its segment, a Topic page on its header, the
# search input with its bottom border, everything else with its own outline. Empty when it's visible.
FOCUS_PROBLEM = """() => {
    const element = document.activeElement;
    if (!element || element === document.body) return "nothing has focus";
    if (!element.matches(":focus-visible")) return `${element.outerHTML.slice(0, 80)} is not :focus-visible`;
    if (element.matches("[data-search-input]")) {
        const probe = document.createElement("i");
        probe.style.color = "var(--focus)";
        element.after(probe);
        const focus = getComputedStyle(probe).color;
        probe.remove();
        return getComputedStyle(element).borderBottomColor === focus ? "" : "the search input shows no focus";
    }
    const shown = element.matches('input[type="radio"]') ? element.nextElementSibling
        : element.matches("[data-topic]") ? element.querySelector(".hero") : element;
    const style = getComputedStyle(shown);
    if (style.outlineStyle === "none" || parseFloat(style.outlineWidth) < 2) {
        return `${element.outerHTML.slice(0, 80)} has no focus ring`;
    }
    const box = shown.getBoundingClientRect();
    if (box.bottom < 0 || box.top > innerHeight || box.width === 0) return `${element.outerHTML.slice(0, 80)} is off screen`;
    return "";
}"""


def focus_shows(page: Page):
    assert page.evaluate(FOCUS_PROBLEM) == ""


def tab_to(page: Page, target, limit: int = 40):
    """Presses Tab until `target` has focus, checking at every stop that the focus can be seen."""
    for _ in range(limit):
        page.keyboard.press("Tab")
        focus_shows(page)
        if target.evaluate("(element) => element === document.activeElement"):
            return
    raise AssertionError(f"Tab never reached {target}")


def test_keyboard_walkthrough_with_visible_focus(page: Page, site_url):
    page.goto(site_url)

    # Overview → Topic
    numbers_tile = page.locator("[data-overview]").get_by_role("link", name="Numbers")
    tab_to(page, numbers_tile)
    page.keyboard.press("Enter")
    expect(topic_page(page, "numbers")).to_be_focused()
    focus_shows(page)

    # → an Entry chip
    chip = topic_page(page, "numbers").get_by_role("navigation", name="Entries").get_by_role("link", name="Addition")
    tab_to(page, chip)
    page.keyboard.press("Enter")
    expect(page).to_have_url(f"{site_url}#numbers/addition")
    expect(entry(page, "numbers/addition")).to_be_focused()
    focus_shows(page)

    # → See also, into another Topic
    see_also = entry(page, "numbers/addition").get_by_role("navigation", name="See also").get_by_role("link")
    tab_to(page, see_also)
    page.keyboard.press("Enter")
    expect(page).to_have_url(f"{site_url}#strings/joining")
    expect(entry(page, "strings/joining")).to_be_focused()
    focus_shows(page)

    # → Next stop
    next_stop = topic_page(page, "strings").get_by_role("link", name=re.compile("^Next stop"))
    tab_to(page, next_stop)
    page.keyboard.press("Enter")
    expect(page).to_have_url(f"{site_url}#charts")
    expect(topic_page(page, "charts")).to_be_focused()
    focus_shows(page)

    # → search, to an Entry
    page.keyboard.press("Control+k")
    expect(search(page).get_by_role("combobox")).to_be_focused()
    focus_shows(page)
    page.keyboard.type("powers")
    expect(search(page).get_by_role("option").first).to_have_attribute("aria-selected", "true")
    page.keyboard.press("Enter")
    expect(page).to_have_url(f"{site_url}#numbers/powers")
    expect(entry(page, "numbers/powers")).to_be_focused()
    focus_shows(page)

    # → Esc back out: closes search, then zooms out to the Topic's tile
    page.keyboard.press("/")
    expect(search(page)).to_be_visible()
    page.keyboard.press("Escape")
    expect(search(page)).to_be_hidden()
    expect(entry(page, "numbers/powers")).to_be_focused()
    page.keyboard.press("Escape")
    expect(numbers_tile).to_be_focused()
    focus_shows(page)


def test_the_selected_search_result_is_marked_in_the_focus_colour(page: Page, site_url):
    page.goto(site_url)
    page.keyboard.press("Control+k")
    page.keyboard.type("i")
    selected = search(page).locator('[aria-selected="true"]')
    expect(selected).to_have_count(1)

    focus = page.evaluate(
        "() => { const i = document.createElement('i'); i.style.color = 'var(--focus)'; document.body.append(i);"
        " const c = getComputedStyle(i).color; i.remove(); return c; }"
    )
    assert focus in selected.evaluate("(e) => getComputedStyle(e).boxShadow")


# Reduced motion: nothing animates, and every state change still completes.

NOTHING_MOVES = """() => {
    const moving = document.getAnimations().map((a) => a.animationName ?? a.transitionProperty ?? "script animation");
    for (const element of document.querySelectorAll("*")) {
        for (const pseudo of [null, "::before", "::after"]) {
            const style = getComputedStyle(element, pseudo);
            const timed = (value) => value.split(",").some((d) => parseFloat(d) > 0);
            if (timed(style.transitionDuration) || (style.animationName !== "none" && timed(style.animationDuration))) {
                moving.push(`${element.tagName.toLowerCase()}.${element.className}${pseudo ?? ""}`);
            }
        }
    }
    return moving;
}"""


def still(page: Page):
    assert page.evaluate(NOTHING_MOVES) == []


def test_reduced_motion_moves_nothing_and_every_change_completes(page: Page, site_url):
    page.emulate_media(reduced_motion="reduce")
    page.goto(site_url)
    still(page)

    page.locator("[data-overview]").get_by_role("link", name="Numbers").hover()
    still(page)
    page.locator("[data-overview]").get_by_role("link", name="Numbers").click()
    expect(topic_page(page, "numbers")).to_be_focused()
    still(page)

    page.locator(".code").first.hover()  # the copy button appears
    still(page)
    topic_page(page, "numbers").get_by_role("link", name="Powers").first.click()
    expect(entry(page, "numbers/powers")).to_be_focused()
    expect(entry(page, "numbers/powers")).to_have_class(re.compile(r"\bflash\b"))  # a still ring
    still(page)

    topic_page(page, "numbers").get_by_role("link", name=re.compile("^Next stop")).click()
    expect(topic_page(page, "strings")).to_be_focused()
    still(page)

    choose_trail(page)
    page.keyboard.press("Escape")
    stone = page.locator("[data-overview]").get_by_role("link", name=re.compile("Strings"))
    expect(stone).to_be_focused()
    still(page)

    page.get_by_role("button", name="Plots").click()  # an Area dot jumps at once
    expect(page.locator('[data-land="plots"]')).to_have_attribute("aria-current", "true")
    still(page)

    page.keyboard.press("Control+k")
    expect(search(page)).to_be_visible()
    still(page)


# Phones: no sideways page scroll, and nothing cut off at the edges outside the strips meant to scroll.

# Visible text that sticks out past the left or right edge of the screen, outside an element that scrolls
# sideways on its own (the rail strip, the chips, code and Output).
CUT_OFF = """() => {
    const cut = [];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    for (let node; (node = walker.nextNode()); ) {
        const parent = node.parentElement;
        if (!node.textContent.trim() || !parent.checkVisibility({ visibilityProperty: true })) continue;
        let clipped = false;
        for (let e = parent; e && e !== document.body && !clipped; e = e.parentElement) {
            const style = getComputedStyle(e);
            // Visually hidden text (the phone's icon-only pill), or inside a strip that scrolls sideways.
            clipped = style.clipPath !== "none" || ["auto", "scroll"].includes(style.overflowX);
        }
        if (clipped) continue;
        const range = document.createRange();
        range.selectNodeContents(node);
        for (const box of range.getClientRects()) {
            if (box.left < -1 || box.right > innerWidth + 1) cut.push(node.textContent.trim().slice(0, 40));
        }
    }
    return [...new Set(cut)];
}"""


def fits(page: Page, viewport: dict):
    assert page.evaluate("document.documentElement.scrollWidth") <= viewport["width"]
    assert page.evaluate(CUT_OFF) == []


@pytest.mark.parametrize("viewport", PHONES, ids=lambda v: f"{v['width']}px")
@pytest.mark.parametrize("language", LANGUAGES)
def test_every_view_fits_a_phone(page: Page, site_url, viewport, language):
    page.set_viewport_size(viewport)
    page.goto(f"{site_url}?lang={language}")
    fits(page, viewport)

    page.goto(f"{site_url}?lang={language}#numbers/division")  # long code and Output, a Pitfall
    expect(entry(page, "numbers/division")).to_be_visible()
    fits(page, viewport)
    page.goto(f"{site_url}?lang={language}#charts")  # a figure
    fits(page, viewport)

    choose_trail(page)
    fits(page, viewport)
    page.keyboard.press("Escape")
    expect(page.locator("[data-overview]")).to_be_visible()
    fits(page, viewport)

    page.get_by_role("button", name=re.compile("^(Search|Szukaj)")).click()
    page.keyboard.type("a")
    expect(search(page).get_by_role("option")).not_to_have_count(0)
    fits(page, viewport)
    box = search(page).bounding_box()
    assert box["x"] >= 0 and box["x"] + box["width"] <= viewport["width"]


@pytest.mark.parametrize("viewport", PHONES, ids=lambda v: f"{v['width']}px")
def test_on_a_phone_the_strip_and_chips_scroll_to_every_link(page: Page, site_url, viewport):
    page.set_viewport_size(viewport)
    page.goto(f"{site_url}#numbers")

    chips = topic_page(page, "numbers").get_by_role("navigation", name="Entries")
    last_chip = chips.get_by_role("link").last
    last_chip.scroll_into_view_if_needed()
    expect(last_chip).to_be_in_viewport()
    last_chip.click()
    expect(page).to_have_url(f"{site_url}#numbers/powers")

    strip = page.get_by_role("navigation", name="Index")
    last_pin = strip.get_by_role("link").filter(visible=True).last
    last_pin.scroll_into_view_if_needed()
    expect(last_pin).to_be_in_viewport()
    last_pin.click()
    expect(topic_page(page, "charts")).to_be_visible()


def test_a_fifteen_topic_island_keeps_its_names_inside_their_bubbles_at_375_px(page: Page, tmp_path_factory):
    content = hue_content()
    topics = content["areas"][0]["topics"]
    topics += [
        {**topics[0], "id": f"extra-{k}", "title": f"Comprehensions {k}", "pl": {"title": f"Wyrażenia {k}", "summary": "x"}}
        for k in range(13)
    ]
    with built_site(content, tmp_path_factory.mktemp("fifteen")) as url:
        page.set_viewport_size({"width": 375, "height": 800})
        page.goto(url)
        spill = page.locator('[data-area="hue-0"] .bubble').evaluate_all(
            """(bubbles) => bubbles.filter((bubble) => {
                const outer = bubble.getBoundingClientRect();
                const name = bubble.querySelector(".name").getBoundingClientRect();
                return name.left < outer.left - 1 || name.right > outer.right + 1;
            }).length"""
        )
        assert spill == 0


# The Map | Trail and EN | PL segments show the remembered choice before the client modules run.


def test_the_switches_show_the_remembered_choices_before_the_page_script_runs(page: Page, site_url):
    page.goto(site_url)
    choose_trail(page)
    page.locator('[data-language-choice][value="pl"]').check()
    page.route("**/*.js", lambda route: route.abort())  # the inline scripts alone

    page.reload()

    expect(page.locator('[data-arrangement-choice][value="trail"]')).to_be_checked()
    expect(page.locator('[data-language-choice][value="pl"]')).to_be_checked()
