"""Seam 1: a content folder goes in, the generated content data comes out."""

import platform
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
        "see": [],
        "pitfall": None,
        "output": {"text": "[20, 30]\n[10, 30]", "error": None, "figures": []},
        "pl": {
            "title": "Wycinanie (slicing)",
            "explain": "<code>data[start:stop]</code> wybiera <em>fragment</em> listy.",
            "pitfall": None,
        },
    }


def test_pitfall_and_see_also_are_parsed(full_syntax):
    sorting = full_syntax["areas"][0]["topics"][0]["entries"][1]

    assert sorting["pitfall"] == {
        "text": "<code>data = data.sort()</code> replaces your list with <code>None</code>.",
        "code": "data = [3, 1, 2]\ndata = data.sort()\nprint(data)",
        "raises": None,
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


def test_unmarked_error_fails_naming_the_entry():
    with pytest.raises(ContentError, match=r"names/dividing.*ZeroDivisionError: division by zero"):
        build_content(FIXTURES / "unmarked-error")
