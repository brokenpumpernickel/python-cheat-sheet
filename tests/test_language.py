"""The EN | PL Language switch (ADR 0005), on the site built from tests/fixtures/site (Basics: Numbers, Strings,
planned Sets; Plots: Charts). Every piece of prose is in the page in both Languages, and <html lang> shows one."""

import re

import pytest
from playwright.sync_api import BrowserContext, Page, expect

PHONES = [{"width": 320, "height": 640}, {"width": 375, "height": 700}]

# The text a Student sees or hears: the title, rendered text nodes (screen-reader-only ones too) outside
# code, printed Output, figures and key caps, which are the same in both Languages, and every aria-label
# and placeholder.
VISIBLE_TEXT = """() => {
    const texts = [document.title];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    for (let node; (node = walker.nextNode()); ) {
        const parent = node.parentElement;
        if (parent.closest("pre, code, kbd, svg, script, style") || !parent.checkVisibility()) continue;
        if (node.textContent.trim()) texts.push(node.textContent.trim());
    }
    for (const element of document.querySelectorAll("[aria-label], [placeholder]")) {
        texts.push(element.getAttribute("aria-label") ?? "", element.getAttribute("placeholder") ?? "");
    }
    return texts.filter(Boolean).join("\\n");
}"""

# Each piece of text the page holds in `language`, wherever it differs from its twin (components/Text.astro
# renders the English, then the Polish), and content prose in labelled attributes, such as a figure's
# description (labels.ts keeps its twins in data-<name>-<language>).
PROSE = """(language) => {
    const texts = [...document.querySelectorAll(`[data-lang="${language}"]`)]
        .filter((element) => {
            const twin = language === "en" ? element.nextElementSibling : element.previousElementSibling;
            return element.textContent !== twin.textContent;
        })
        .map((element) => element.textContent.trim());
    const other = language === "en" ? "pl" : "en";
    for (const element of document.querySelectorAll("[data-label-attributes]")) {
        for (const name of element.dataset.labelAttributes.split(" ").filter((pair) => !pair.includes("="))) {
            const text = element.getAttribute(`data-${name}-${language}`);
            if (text !== element.getAttribute(`data-${name}-${other}`)) texts.push(text);
        }
    }
    return texts;
}"""


def switch(page: Page):
    return page.get_by_role("radiogroup", name=re.compile("^(Language|Język)$"))


def choose(page: Page, language: str):
    switch(page).get_by_role("radio", name=language).check()


def choose_in_place(page: Page, language: str):
    """Chooses without scrolling the top bar into view first, as check() does, to see what the switch
    itself does to the scroll position."""
    switch(page).get_by_role("radio", name=language).evaluate("(radio) => radio.click()")


def choose_trail(page: Page, in_place: bool = False):
    radio = page.get_by_role("radiogroup", name=re.compile("^(Overview style|Widok przeglądu)$")).get_by_role(
        "radio", name=re.compile("^(Trail|Szlak)$")
    )
    if in_place:
        radio.evaluate("(radio) => radio.click()")
    else:
        radio.check()


def rail(page: Page):
    return page.get_by_role("navigation", name=re.compile("^(Index|Indeks)$"))


def entry(page: Page, ref: str):
    return page.locator(f'[data-entry="{ref}"]')


def top(locator) -> float:
    return locator.bounding_box()["y"]


def on_screen(page: Page, labels: dict, language: str) -> list[str]:
    """The labels and prose in `language` (where they differ from the other Language's) that are on screen
    or in an accessible name."""
    text = page.evaluate(VISIBLE_TEXT)
    twin = "pl" if language == "en" else "en"
    words = {value for key, value in labels[language].items() if value != labels[twin][key]}
    words |= set(page.evaluate(PROSE, language))
    return sorted(word for word in words if re.search(rf"(?<!\w){re.escape(word)}(?!\w)", text))


# The switch


def test_english_is_the_default_and_the_switch_is_a_radio_group(page: Page, site_url):
    page.goto(site_url)

    expect(page.locator("html")).to_have_attribute("lang", "en")
    expect(switch(page)).to_have_accessible_name("Language")
    expect(switch(page).get_by_role("radio")).to_have_count(2)
    expect(switch(page).get_by_role("radio", name="EN")).to_be_checked()
    expect(switch(page).get_by_role("radio", name="PL")).not_to_be_checked()

    # Arrow keys move between the radios and choose, as in any radio group.
    switch(page).get_by_role("radio", name="EN").focus()
    page.keyboard.press("ArrowRight")
    expect(switch(page).get_by_role("radio", name="PL")).to_be_checked()
    expect(page.locator("html")).to_have_attribute("lang", "pl")
    expect(switch(page)).to_have_accessible_name("Język")


def test_switching_on_the_map_changes_the_text_in_place(page: Page, site_url):
    page.goto(site_url)
    expect(page.get_by_role("link", name="Numbers")).to_be_visible()

    choose(page, "PL")

    expect(page).to_have_url(site_url)  # no parameter added, and still the Overview
    expect(page).to_have_title("Ściągawka z Pythona")
    expect(page.get_by_role("heading", name="Ściągawka z Pythona", level=1)).to_be_attached()
    expect(page.get_by_role("heading", name="Podstawy", level=2)).to_be_visible()
    expect(page.get_by_role("link", name="Liczby")).to_be_visible()
    expect(page.get_by_role("link", name="Numbers")).to_have_count(0)
    expect(page.get_by_role("radio", name="Mapa")).to_be_checked()
    expect(page.get_by_text("Kliknij bąbel, aby wejść")).to_be_visible()
    expect(page.get_by_role("contentinfo")).to_contain_text("Wersje użyte w przykładach:", use_inner_text=True)

    # The same links: the bubble still opens the Topic.
    page.get_by_role("link", name="Liczby").click()
    expect(page).to_have_url(f"{site_url}#numbers")
    expect(page.get_by_role("heading", name="Liczby", level=1)).to_be_visible()


def test_switching_on_the_trail_keeps_the_stretch_in_view(page: Page, site_url):
    page.goto(site_url)
    choose_trail(page)
    plots = page.locator('[data-land-section="plots"]')
    plots.scroll_into_view_if_needed()
    page.evaluate("window.scrollBy(0, 40)")
    before = top(plots)

    choose_in_place(page, "PL")

    expect(plots.get_by_role("heading", name="Wykresy", level=2)).to_be_in_viewport()
    expect(plots.get_by_role("link")).to_have_accessible_name("1 Diagramy Wykresy liniowe.")
    expect(page.get_by_role("radio", name="Szlak")).to_be_checked()
    assert abs(top(plots) - before) < 2

    choose_in_place(page, "EN")
    expect(plots.get_by_role("heading", name="Plots", level=2)).to_be_in_viewport()
    assert abs(top(plots) - before) < 2


@pytest.mark.parametrize("arrangement", ["map", "trail"])
def test_switching_inside_a_topic_keeps_the_topic_the_entry_and_the_scroll(page: Page, site_url, arrangement):
    page.goto(f"{site_url}#numbers/multiplication")
    if arrangement == "trail":
        choose_trail(page, in_place=True)
    card = entry(page, "numbers/multiplication")
    highlighted = rail(page).locator('[data-rail-entry][aria-current="true"]:visible')
    expect(card).to_be_in_viewport()
    expect(card).not_to_have_class(re.compile(r"\bflash\b"), timeout=3000)  # it scales the card while it plays
    expect(highlighted).to_have_accessible_name("Multiplication")
    page.evaluate("window.scrollBy(0, 30)")  # reading a little way into the Entry
    expect(highlighted).to_have_accessible_name("Multiplication")
    scroll, before = page.evaluate("window.scrollY"), top(card)

    choose_in_place(page, "PL")

    expect(page).to_have_url(f"{site_url}#numbers/multiplication")
    expect(page.get_by_role("heading", name="Liczby", level=1)).to_be_visible()
    expect(card.get_by_role("heading", name="Mnożenie")).to_be_in_viewport()
    expect(highlighted).to_have_accessible_name("Mnożenie")
    expect(rail(page).get_by_role("link", name="Liczby")).to_have_attribute("aria-current", "page")
    assert abs(top(card) - before) < 2
    assert abs(page.evaluate("window.scrollY") - scroll) < 100

    choose_in_place(page, "EN")
    expect(highlighted).to_have_accessible_name("Multiplication")
    assert abs(top(card) - before) < 2


def test_switching_at_the_top_of_a_topic_stays_at_the_top(page: Page, site_url):
    page.goto(f"{site_url}#strings")

    choose(page, "PL")

    expect(page.get_by_role("heading", name="Napisy", level=1)).to_be_in_viewport()
    assert page.evaluate("window.scrollY") == 0


def test_the_copy_button_follows_the_switch(page: Page, context: BrowserContext, site_url):
    context.grant_permissions(["clipboard-read", "clipboard-write"], origin=site_url.rstrip("/"))
    page.goto(f"{site_url}#strings/joining")
    choose(page, "PL")
    card = entry(page, "strings/joining")

    card.hover()
    card.get_by_role("button", name="Kopiuj").click()
    expect(card.get_by_role("button")).to_have_text("Skopiowano!")
    expect(card.get_by_role("button")).to_have_text("Kopiuj", use_inner_text=True, timeout=3000)

    choose(page, "EN")
    expect(card.get_by_role("button")).to_have_text("Copy", use_inner_text=True)


def test_a_figure_is_named_by_its_description_in_the_active_language(page: Page, site_url):
    page.goto(f"{site_url}#charts")
    figure = entry(page, "charts/line-chart").locator('[role="img"]')  # not the svg inside it

    expect(figure).to_have_accessible_name("A line rising ever faster through three points.")
    choose(page, "PL")
    expect(figure).to_have_accessible_name("Linia rosnąca coraz szybciej przez trzy punkty.")
    choose(page, "EN")
    expect(figure).to_have_accessible_name("A line rising ever faster through three points.")


def test_a_figure_opened_in_polish_has_its_polish_name(page: Page, site_url):
    page.goto(f"{site_url}?lang=pl#charts")

    expect(entry(page, "charts/line-chart").locator('[role="img"]')).to_have_accessible_name(
        "Linia rosnąca coraz szybciej przez trzy punkty."
    )


# Remembering the choice, and ?lang=


def test_the_choice_is_remembered_across_reloads(page: Page, site_url):
    page.goto(f"{site_url}#numbers")
    choose(page, "PL")

    page.reload()
    expect(page.locator("html")).to_have_attribute("lang", "pl")
    expect(switch(page).get_by_role("radio", name="PL")).to_be_checked()
    expect(page.get_by_role("heading", name="Liczby", level=1)).to_be_visible()
    expect(page).to_have_title("Ściągawka z Pythona")

    choose(page, "EN")
    page.reload()
    expect(page.locator("html")).to_have_attribute("lang", "en")
    expect(page.get_by_role("heading", name="Numbers", level=1)).to_be_visible()


def test_the_remembered_choice_applies_before_the_page_script_runs(page: Page, site_url):
    page.goto(site_url)
    choose(page, "PL")
    page.route("**/*.js", lambda route: route.abort())  # the head's inline script alone

    page.reload()

    expect(page.locator("html")).to_have_attribute("lang", "pl")
    expect(page).to_have_title("Ściągawka z Pythona")
    expect(page.get_by_role("link", name="Liczby")).to_be_visible()


def test_lang_pl_opens_in_polish_on_a_first_visit_and_follows_the_switch(page: Page, site_url):
    page.goto(f"{site_url}?lang=pl#numbers")

    expect(page.locator("html")).to_have_attribute("lang", "pl")
    expect(switch(page).get_by_role("radio", name="PL")).to_be_checked()
    expect(page.get_by_role("heading", name="Liczby", level=1)).to_be_visible()

    choose(page, "EN")
    expect(page).to_have_url(f"{site_url}?lang=en#numbers")
    expect(page.get_by_role("heading", name="Numbers", level=1)).to_be_visible()

    # Links keep the parameter: the Topic's own links are only hashes.
    page.get_by_role("navigation", name="Entries").get_by_role("link", name="Division").click()
    expect(page).to_have_url(f"{site_url}?lang=en#numbers/division")
    page.keyboard.press("Escape")
    expect(page).to_have_url(f"{site_url}?lang=en")


def test_lang_overrides_the_remembered_choice(page: Page, site_url):
    page.goto(site_url)
    choose(page, "PL")

    page.goto(f"{site_url}?lang=en")
    expect(page.locator("html")).to_have_attribute("lang", "en")
    expect(switch(page).get_by_role("radio", name="EN")).to_be_checked()

    page.goto(f"{site_url}?lang=xx")  # not a Language: the remembered one
    expect(page.locator("html")).to_have_attribute("lang", "pl")


# Search


def test_search_results_show_in_the_active_language_and_match_both(page: Page, site_url):
    page.goto(site_url)
    choose(page, "PL")
    dialog = page.get_by_role("dialog", name="Szukaj")
    results = dialog.get_by_role("option")

    page.keyboard.press("Control+k")
    expect(dialog.get_by_role("combobox", name="Szukaj tematów, haseł i kodu")).to_have_attribute(
        "placeholder", "Szukaj tematów, haseł i kodu…"
    )
    page.keyboard.type("powers")
    expect(results).to_have_text([re.compile(r"^Potęgi\s*Podstawy › Liczby$")])
    page.keyboard.press("Control+a")
    page.keyboard.type("potęgi")
    expect(results).to_have_text([re.compile(r"^Potęgi\s*Podstawy › Liczby$")])
    page.keyboard.press("Control+a")
    page.keyboard.type("zzzz")
    expect(dialog.get_by_role("status")).to_have_text("Brak wyników dla “zzzz”")

    page.keyboard.press("Control+a")
    page.keyboard.type("potęgi")
    page.keyboard.press("Escape")
    choose(page, "EN")
    page.keyboard.press("Control+k")  # opens on the last query
    expect(page.get_by_role("dialog", name="Search").get_by_role("option")).to_have_text(
        [re.compile(r"^Powers\s*Basics › Numbers$")]
    )


# Nothing left in the other Language


VIEWS = {
    "map": lambda page, url: page.goto(url),
    "trail": lambda page, url: (page.goto(url), choose_trail(page)),
    "numbers": lambda page, url: page.goto(f"{url}#numbers/division"),
    "strings": lambda page, url: page.goto(f"{url}#strings"),
    "charts (trail rail)": lambda page, url: (page.goto(f"{url}#charts"), choose_trail(page)),
    "search": lambda page, url: (page.goto(url), page.keyboard.press("Control+k"), page.keyboard.type("a")),
}


@pytest.mark.parametrize("view", VIEWS)
@pytest.mark.parametrize(("language", "other"), [("PL", "en"), ("EN", "pl")])
def test_no_text_of_the_other_language_is_left_on_screen(page: Page, site_url, labels, view, language, other):
    VIEWS[view](page, f"{site_url}?lang={language.lower()}")
    if view == "search":
        expect(page.get_by_role("option").first).to_be_visible()

    assert on_screen(page, labels, other) == []
    assert on_screen(page, labels, language.lower())  # the check does see the Language shown


@pytest.mark.parametrize("view", ["map", "numbers", "charts (trail rail)"])
def test_no_english_is_left_after_switching_to_polish(page: Page, site_url, labels, view):
    VIEWS[view](page, site_url)
    choose(page, "PL")

    assert on_screen(page, labels, "en") == []
    assert on_screen(page, labels, "pl")


# Phones


@pytest.mark.parametrize("viewport", PHONES, ids=lambda v: f"{v['width']}px")
@pytest.mark.parametrize("language", ["EN", "PL"])
def test_the_top_bar_fits_a_phone_in_both_languages(page: Page, site_url, viewport, language):
    page.set_viewport_size(viewport)
    page.goto(f"{site_url}?lang={language.lower()}")

    assert page.evaluate("document.documentElement.scrollWidth") <= viewport["width"]
    for group in page.get_by_role("radiogroup").all():
        box = group.bounding_box()
        assert 0 <= box["x"] and box["x"] + box["width"] <= viewport["width"]
