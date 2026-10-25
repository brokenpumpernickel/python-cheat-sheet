"""Search: the matching and ranking (site/src/search, run with Node as the site runs it), and the pop-up in a
real browser on the site built from tests/fixtures/site (Basics: Numbers, Strings, planned Sets; Plots: Charts)."""

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

SEARCH = Path(__file__).parent.parent / "site" / "src" / "search"
FLASHING = re.compile(r"\bflash\b")


def node(script: str):
    """Run an ES module script with Node and return the JSON it prints."""
    executable = shutil.which("node")
    assert executable, "node not found; install Node.js to build the site"
    run = subprocess.run(
        [executable, "--input-type=module", "--no-warnings", "-e", script],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return json.loads(run.stdout)


def doc(route: str, title: str, *, topic: str = "Topic", body: str = "", pl: str = "Tytuł") -> dict:
    return {
        "route": route,
        "title": {"en": title, "pl": pl},
        "area": {"en": "Area", "pl": "Obszar"},
        "topic": {"en": topic, "pl": "Temat"},
        "body": body,
    }


def search(docs: list[dict], query: str) -> list[str]:
    """The routes of the results for `query` over `docs`, best first."""
    module = json.dumps((SEARCH / "match.ts").as_uri())
    script = (
        f"const {{ searcher }} = await import({module});"
        f"console.log(JSON.stringify(searcher({{ docs: {json.dumps(docs)} }})({json.dumps(query)}).map((d) => d.route)));"
    )
    return node(script)


# --- matching and ranking ---


def test_ranks_title_prefix_then_title_contains_then_topic_name_then_body():
    docs = [
        doc("t/body", "Keys", body="d = dict(a=1)"),
        doc("dictionaries/keys", "Keys", topic="Dictionaries"),
        doc("t/contains", "Ordered dicts"),
        doc("t/prefix", "Dict basics"),
        doc("t/none", "Lists"),
    ]
    assert search(docs, "dict") == ["t/prefix", "t/contains", "dictionaries/keys", "t/body"]


def test_every_query_word_must_match_in_some_field():
    docs = [
        doc("lists/sorting", "Sorting", topic="Lists"),
        doc("lists/slicing", "Slicing", topic="Lists"),
        doc("tuples/sorting", "Sorting", topic="Tuples"),
    ]
    assert search(docs, "list sort") == ["lists/sorting"]
    assert search(docs, "list sort zzz") == []


def test_matches_polish_with_or_without_diacritics_and_ignores_case():
    docs = [doc("dicts/basics", "Basics", pl="Słownik od podstaw"), doc("other/x", "Other")]
    assert search(docs, "słownik") == ["dicts/basics"]
    assert search(docs, "SLOWNIK") == ["dicts/basics"]


def test_matches_code_fragments_and_keeps_index_order_for_ties():
    docs = [doc("a/first", "First", body="d.get(key)"), doc("b/second", "Second", body="x = d.get(k, 0)")]
    assert search(docs, ".get(") == ["a/first", "b/second"]


def test_blank_query_has_no_results():
    assert search([doc("a/b", "Anything")], "   ") == []


def test_index_text_is_html_without_tags_or_entities():
    module = json.dumps((SEARCH / "build.ts").as_uri())
    html = "Use <code>d.get(k)</code> &amp; <em>not</em> <code>a &lt; b</code> &quot;x&quot;&#39;"
    text = node(f"const m = await import({module}); console.log(JSON.stringify(m.plainText({json.dumps(html)})));")
    assert text == "Use d.get(k) & not a < b \"x\"'"


# --- the pop-up ---


def dialog(page: Page):
    return page.get_by_role("dialog", name="Search")


def query(page: Page):
    return dialog(page).get_by_role("combobox")


def results(page: Page):
    return dialog(page).get_by_role("option")


def search_for(page: Page, text: str):
    """Open search with Ctrl+K and type `text`."""
    page.keyboard.press("Control+k")
    expect(dialog(page)).to_be_visible()
    query(page).fill(text)


def entry(page: Page, ref: str):
    return page.locator(f'[data-entry="{ref}"]')


def test_finds_an_entry_by_an_english_word_and_opens_it_with_enter(page: Page, site_url):
    page.goto(site_url)
    search_for(page, "powers")

    expect(results(page).first).to_contain_text("Powers")
    expect(results(page).first).to_contain_text("Basics › Numbers")
    page.keyboard.press("Enter")

    expect(dialog(page)).to_be_hidden()
    expect(page).to_have_url(f"{site_url}#numbers/powers")
    powers = entry(page, "numbers/powers")
    expect(powers).to_be_in_viewport()
    expect(powers).to_have_class(FLASHING)
    expect(powers).to_be_focused()


@pytest.mark.parametrize("word", ["Potęgi", "potegi"])
def test_finds_an_entry_by_a_polish_word_and_shows_it_in_english(page: Page, site_url, word):
    page.goto(site_url)
    search_for(page, word)

    expect(results(page)).to_have_count(1)
    expect(results(page)).to_have_text(re.compile(r"^Powers\s*Basics › Numbers$"))


def test_finds_an_entry_by_a_code_fragment_and_opens_it_with_a_click(page: Page, site_url):
    page.goto(site_url)
    search_for(page, 'print("ab"')

    expect(results(page)).to_have_count(1)
    results(page).first.click()

    expect(page).to_have_url(f"{site_url}#strings/joining")
    expect(entry(page, "strings/joining")).to_have_class(FLASHING)


def test_a_topic_result_opens_the_topic(page: Page, site_url):
    page.goto(site_url)
    search_for(page, "napisy")

    expect(results(page).first).to_have_text(re.compile(r"^Strings\s*Basics$"))
    page.keyboard.press("Enter")
    expect(page).to_have_url(f"{site_url}#strings")
    expect(page.locator('[data-topic="strings"]')).to_be_focused()


def test_arrow_keys_move_the_selection_and_enter_opens_it(page: Page, site_url):
    page.goto(site_url)
    search_for(page, "numbers")  # the Topic, then its Entries by Topic name
    selected = dialog(page).locator('[aria-selected="true"]')

    expect(selected).to_contain_text("Numbers")
    page.keyboard.press("ArrowUp")  # already at the top
    expect(selected).to_contain_text("Numbers")
    page.keyboard.press("ArrowDown")
    page.keyboard.press("ArrowDown")
    expect(selected).to_contain_text("Subtraction")
    expect(query(page)).to_have_attribute("aria-activedescendant", selected.get_attribute("id"))
    page.keyboard.press("ArrowUp")
    expect(selected).to_contain_text("Addition")
    page.keyboard.press("Enter")

    expect(page).to_have_url(f"{site_url}#numbers/addition")
    expect(entry(page, "numbers/addition")).to_have_class(FLASHING)


def test_opening_the_entry_already_shown_scrolls_back_and_flashes_it_again(page: Page, site_url):
    page.goto(f"{site_url}#numbers/powers")
    powers = entry(page, "numbers/powers")
    expect(powers).not_to_have_class(FLASHING, timeout=3000)
    page.evaluate("window.scrollTo(0, 0)")
    expect(powers).not_to_be_in_viewport()

    search_for(page, "powers")
    page.keyboard.press("Enter")

    expect(powers).to_be_in_viewport()
    expect(powers).to_have_class(FLASHING)


def test_shows_no_matches(page: Page, site_url):
    page.goto(site_url)
    search_for(page, "zzzz")

    expect(results(page)).to_have_count(0)
    expect(dialog(page).get_by_role("status")).to_have_text("No matches for “zzzz”")
    page.keyboard.press("Enter")  # nothing to open
    expect(dialog(page)).to_be_visible()


@pytest.mark.parametrize("word", ["sets", "zbiory"])
def test_planned_topics_never_appear(page: Page, site_url, word):
    page.goto(site_url)
    search_for(page, word)

    expect(dialog(page).get_by_role("status")).to_contain_text("No matches")


def test_slash_and_the_pill_open_search_and_slash_types_inside_it(page: Page, site_url):
    page.goto(site_url)
    page.keyboard.press("/")
    expect(query(page)).to_be_focused()
    page.keyboard.type("a/b")
    expect(query(page)).to_have_value("a/b")
    page.keyboard.press("Escape")

    pill = page.get_by_role("button", name="Search Topics, Entries and code")
    pill.click()
    expect(query(page)).to_be_focused()
    expect(query(page)).to_have_value("a/b")  # kept, and selected so typing replaces it
    page.keyboard.type("x")
    expect(query(page)).to_have_value("x")


def test_esc_closes_only_the_pop_up_and_focus_returns(page: Page, site_url):
    page.goto(f"{site_url}#numbers")
    pill = page.get_by_role("button", name="Search Topics, Entries and code")
    pill.click()
    query(page).fill("pow")

    page.keyboard.press("Escape")
    expect(dialog(page)).to_be_hidden()
    expect(page).to_have_url(f"{site_url}#numbers")  # still on the Topic
    expect(pill).to_be_focused()

    page.keyboard.press("Escape")  # with the pop-up closed, Esc zooms out as usual
    expect(page).to_have_url(site_url)


def test_a_click_outside_the_box_closes_it(page: Page, site_url):
    page.goto(site_url)
    search_for(page, "pow")
    page.mouse.click(5, 495)
    expect(dialog(page)).to_be_hidden()
    expect(page).to_have_url(site_url)


def test_the_index_loads_only_when_search_is_used(page: Page, site_url):
    requested = []
    page.on("request", lambda request: requested.append(request.url))
    page.goto(site_url)
    page.wait_for_load_state("networkidle")
    assert not any(url.endswith("/search.json") for url in requested)

    search_for(page, "powers")
    expect(results(page).first).to_contain_text("Powers")
    assert any(url.endswith("/search.json") for url in requested)


def test_enter_before_the_index_arrives_opens_the_top_result_once_it_does(page: Page, site_url):
    held = []
    page.route("**/search.json", lambda route: held.append(route))
    page.goto(site_url)
    search_for(page, "powers")
    expect(dialog(page).get_by_role("status")).to_have_text("Loading…")
    page.keyboard.press("Enter")

    held[0].continue_()
    expect(page).to_have_url(f"{site_url}#numbers/powers")
    expect(entry(page, "numbers/powers")).to_have_class(FLASHING)


def test_an_index_that_fails_to_load_says_so_and_is_retried(page: Page, site_url):
    page.route("**/search.json", lambda route: route.abort())
    page.goto(site_url)
    search_for(page, "powers")
    expect(dialog(page).get_by_role("status")).to_have_text("Search didn't load. Close it and try again.")
    page.keyboard.press("Escape")

    page.unroute("**/search.json")
    page.keyboard.press("Control+k")
    expect(results(page).first).to_contain_text("Powers")


def test_the_first_result_is_selected_when_the_index_arrives_after_typing(page: Page, site_url):
    held = []
    page.route("**/search.json", lambda route: held.append(route))
    page.goto(site_url)
    search_for(page, "numbers")
    expect(results(page)).to_have_count(0)

    held[0].continue_()
    selected = dialog(page).locator('[aria-selected="true"]')
    expect(selected).to_contain_text("Numbers")
    page.keyboard.press("ArrowDown")
    expect(selected).to_contain_text("Addition")
