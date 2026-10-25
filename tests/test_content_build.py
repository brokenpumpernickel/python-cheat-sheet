"""Seam 1: a content folder goes in, the generated content data comes out."""

import platform
import re
import xml.etree.ElementTree as ElementTree
from importlib.metadata import version
from pathlib import Path

import pytest

from cheatsheet.build import build_content
from cheatsheet.content import ContentError

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="module")
def full_syntax():
    return build_content(FIXTURES / "full-syntax")


def test_valid_topic_produces_data_with_captured_output(full_syntax):
    basics, later = full_syntax["areas"]
    lists, sets = basics["topics"]

    assert {k: v for k, v in basics.items() if k != "topics"} == {
        "id": "basics",
        "title": "Basics",
        "blurb": "Core language: lists and sets.",
        "hue": 160,
        "planned": False,
        "pl": {"title": "Podstawy", "blurb": "Rdzeń języka: listy i zbiory."},
    }
    assert {k: v for k, v in lists.items() if k != "entries"} == {
        "id": "lists",
        "title": "Lists",
        "summary": "Ordered sequences.",
        "glyph": "[ ]",
        "planned": False,
        "pl": {"title": "Listy", "summary": "Uporządkowane sekwencje."},
    }
    assert [e["id"] for e in lists["entries"]] == ["slicing", "sorting", "missing-items"]
    assert lists["entries"][0] == {
        "id": "slicing",
        "title": "Slicing",
        "explain": "<code>data[start:stop]</code> takes a <em>part</em> of a list.",
        "code": "data = [10, 20, 30, 40]\nprint(data[1:3])\nprint(data[::2])",
        "raises": None,
        "figure": None,
        "see": [],
        "pitfall": None,
        "output": {"text": "[20, 30]\n[10, 30]", "error": None, "figures": []},
        "pl": {
            "title": "Wycinanie (slicing)",
            "explain": "<code>data[start:stop]</code> wybiera <em>fragment</em> listy.",
            "pitfall": None,
            "figure": None,
            "pitfallFigure": None,
        },
    }


def test_pitfall_and_see_also_are_parsed(full_syntax):
    sorting = full_syntax["areas"][0]["topics"][0]["entries"][1]

    assert sorting["pitfall"] == {
        "text": "<code>data = data.sort()</code> replaces your list with <code>None</code>.",
        "code": "data = [3, 1, 2]\ndata = data.sort()\nprint(data)",
        "raises": None,
        "figure": None,
        "output": {"text": "None", "error": None, "figures": []},
    }
    assert sorting["pl"]["pitfall"] == (
        "<code>data = data.sort()</code> zastępuje listę wartością <code>None</code>."
    )
    assert sorting["see"] == ["lists/slicing", "lists/missing-items"]


def test_expected_error_ends_output_with_its_final_line(full_syntax):
    missing = full_syntax["areas"][0]["topics"][0]["entries"][2]

    assert missing["raises"] == "IndexError"
    assert missing["output"] == {
        "text": "1",
        "error": "IndexError: list index out of range",
        "figures": [],
    }


def test_pitfall_code_runs_like_entry_code(full_syntax):
    missing = full_syntax["areas"][0]["topics"][0]["entries"][2]

    assert missing["pitfall"]["raises"] == "KeyError"
    assert missing["pitfall"]["output"] == {"text": "2.5", "error": "KeyError: 'sd'", "figures": []}


def test_planned_areas_and_topics_have_no_entries(full_syntax):
    basics, later = full_syntax["areas"]

    assert basics["topics"][1] == {
        "id": "sets",
        "title": "Sets",
        "summary": None,
        "glyph": "{ }",
        "planned": True,
        "pl": {"title": "Zbiory", "summary": None},
        "entries": [],
    }
    assert later["planned"] is True
    assert [t["id"] for t in later["topics"]] == ["arrays"]


def test_meta_lists_the_versions_examples_ran_with(full_syntax):
    assert full_syntax["meta"]["versions"] == [
        {"name": "Python", "version": platform.python_version()},
        {"name": "NumPy", "version": version("numpy")},
        {"name": "Matplotlib", "version": version("matplotlib")},
    ]


def test_entries_cannot_see_each_others_variables():
    names = build_content(FIXTURES / "isolation")["areas"][0]["topics"][0]

    defining, fresh = names["entries"]
    assert defining["output"]["text"] == "42"
    assert fresh["output"]["text"] == "False"


def test_matplotlib_figures_are_captured_as_svg():
    plots = build_content(FIXTURES / "figures")["areas"][0]["topics"][0]
    shown, closed = plots["entries"]

    assert shown["output"]["text"] == "two figures"
    assert len(shown["output"]["figures"]) == 2  # one at plt.show(), one still open at the end
    for svg in shown["output"]["figures"]:
        assert ElementTree.fromstring(svg).tag == "{http://www.w3.org/2000/svg}svg"
    assert closed["output"]["figures"] == []
    assert closed["pitfall"]["output"]["error"] == "ValueError: invalid literal for int() with base 10: 'two'"
    assert len(closed["pitfall"]["output"]["figures"]) == 1


def test_figure_descriptions_reach_the_data():
    plots = build_content(FIXTURES / "figures")["areas"][0]["topics"][0]
    shown, closed = plots["entries"]

    # One description for the example, however many figures it draws; the Pitfall's is its own.
    assert shown["figure"] == "A line rising ever faster through three points, then two bars, the second taller."
    assert shown["pl"]["figure"] == "Linia rosnąca coraz szybciej przez trzy punkty, potem dwa słupki, drugi wyższy."
    assert shown["pl"]["pitfallFigure"] is None
    assert closed["figure"] is None
    assert closed["pl"]["figure"] is None
    assert closed["pitfall"]["figure"] == "A straight line rising between two points."
    assert closed["pl"]["pitfallFigure"] == "Prosta linia rosnąca między dwoma punktami."
    assert "line" not in shown  # the Entry's line is for messages only


# One small content folder per rule in tests/fixtures/invalid/, and the exact message it must give.
INVALID = {
    # Required fields
    "missing-field": "basics/names.md: 'glyph' is required and must be text",
    "empty-field": "basics/names.md: 'summary' is required and must be text",
    "empty-code": "basics/names.md:10 (names/binding): the code block at line 18 is empty",
    "two-code-blocks": "basics/names.md:10 (names/binding): an Entry needs exactly one ```python code block, found 2",
    "bare-code-fence": "basics/names.md:10 (names/binding): the code block at line 18 has no language; fence examples as ```python",
    "duplicate-entry-ids": "basics/names.md:23: two Entries have the id 'binding'",
    # Polish counterparts (ADR 0005)
    "missing-polish-title": "basics/names.md:10 (names/binding): the heading must be followed by a 'PL: <Polish title>' paragraph",
    "missing-polish-explanation": "basics/names.md:10 (names/binding): expected one 'PL:' paragraph with the Polish text, found 0",
    "missing-polish-pitfall": "basics/names.md:10 (names/binding) Pitfall: expected one 'PL:' paragraph with the Polish text, found 0",
    "missing-polish-summary": "basics/names.md pl: 'summary' is required and must be text",
    "missing-polish-blurb": "basics/_area.md pl: 'blurb' is required and must be text",
    # References
    "see-also-unknown-entry": "basics/names.md:23 (names/rebinding) See also: 'names/unbinding' names no Entry of Topic 'names'",
    "see-also-unknown-topic": "basics/names.md:10 (names/binding) See also: 'loops/for-over-a-list' names Topic 'loops', which does not exist",
    "see-also-planned-topic": "basics/names.md:10 (names/binding) See also: 'sets/union' points into planned Topic 'sets'",
    "topic-order-unknown": "basics/_area.md: Topic order names 'loops', but there is no basics/loops.md",
    "topic-not-in-order": "basics/extra.md: Topic is not listed in the Topic order of basics/_area.md",
    "area-not-in-order": "numpy/: Area folder is not listed in areas.yaml",
    "planned-area-with-entries": "basics/names.md: a planned Area lists only planned Topics",
    # Running the examples
    "unmarked-error": "basics/names.md (names/dividing): the example failed with ZeroDivisionError: division by zero",
    "wrong-error-type": "basics/names.md (names/binding): the example failed with IndexError: list index out of range (marked raises=KeyError)",
    "marked-without-error": "basics/names.md (names/binding): marked raises=KeyError, but the example ran without an error",
    "pitfall-unmarked-error": "basics/names.md (names/binding) Pitfall: the example failed with NameError: name 'y' is not defined",
    # Figure descriptions, the figures' accessible names
    "figure-without-description": "basics/names.md:10 (names/binding): the example draws a figure but has no description; add a '### Figure' section after its code",
    "figure-description-without-figure": "basics/names.md:10 (names/binding) Figure: the example draws no figure; remove the '### Figure' description",
    "figure-description-without-polish": "basics/names.md:10 (names/binding) Figure: expected one 'PL:' paragraph with the Polish text, found 0",
    "figure-description-with-markdown": "basics/names.md:10 (names/binding) Figure: a figure description is plain text",
    "figure-description-twice": "basics/names.md:31: '### Figure' appears twice",
    "pitfall-figure-without-description": "basics/names.md:10 (names/binding) Pitfall: the example draws a figure but has no description",
    "pitfall-figure-description-without-code": "basics/names.md:10 (names/binding) Pitfall Figure: the Pitfall has no code, so it draws no figure",
}


@pytest.mark.parametrize("fixture", INVALID)
def test_invalid_content_fails_naming_the_place(fixture):
    with pytest.raises(ContentError, match=re.escape(INVALID[fixture])):
        build_content(FIXTURES / "invalid" / fixture)


def test_every_failing_example_is_reported_at_once():
    with pytest.raises(ContentError) as failure:
        build_content(FIXTURES / "invalid" / "two-failing-examples")

    assert str(failure.value).splitlines() == [
        "basics/names.md (names/binding): the example failed with ZeroDivisionError: division by zero",
        "basics/names.md (names/rebinding): the example failed with NameError: name 'z' is not defined",
    ]


def test_an_example_over_the_timeout_is_reported_with_the_other_failures():
    with pytest.raises(ContentError) as failure:
        build_content(FIXTURES / "invalid" / "slow-example", timeout=1)

    assert str(failure.value).splitlines() == [
        "basics/names.md (names/waiting): the example timed out after 1 s",
        "basics/names.md (names/dividing): the example failed with ZeroDivisionError: division by zero",
    ]
