# Python Cheat Sheet

A single-page reference for students in a statistics/probability lab who already finished an intro programming course and need quick refreshers on Python and its data libraries.

## People

**Student**:
The reader: someone who knows the basics, uses the sheet as a side-tab reference while working in Jupyter.
_Avoid_: User, learner

**Author**:
Whoever writes and maintains the content: the teacher, or an AI agent working on their behalf.
_Avoid_: Admin, editor, maintainer

## Content structure

**Area**:
A visual grouping of Topics on the Overview, usually one per library (e.g. _Python Basics_, _NumPy_, _Matplotlib_). Not a zoom level of its own.
_Avoid_: Section, category, chapter

**Topic**:
One tile on the Overview that zooms into its own page (e.g. _Lists_, _Functions_). Made up of Entries.
_Avoid_: Section, page, card

**Entry**:
One concept within a Topic (e.g. _list comprehension_): a title, a short explanation, a self-contained code example and its Output.
_Avoid_: Snippet, item, card, example

**Output**:
What an Entry's code example actually produces when run (text or a figure, and any widget controls it displays, drawn as a picture). Never written by hand.
_Avoid_: Result, expected output
_Polish_: Wynik

**Language**:
The language the cheat sheet's prose is shown in: English (the default) or Polish, chosen by each Student. Code and Outputs are the same in both.
_Avoid_: Locale, translation mode, version

**Pitfall**:
An optional callout on an Entry describing a common mistake Students make with that concept.
_Avoid_: Gotcha, warning, tip
_Polish_: Pułapka

**Figure description**:
A sentence or two in both Languages saying what the figures an example draws show; it is their accessible name for screen readers. Required exactly when the example draws a figure.
_Avoid_: Alt text, caption

## Navigation

**Overview**:
The zoomed-out view of the whole cheat sheet, where every part is visible at a glance and can be zoomed into.
_Avoid_: Home, map view, dashboard

**Map**:
The default arrangement of the Overview: one island per Area, with its Topics as bubbles on it.
_Avoid_: Archipelago, islands view
_Polish_: Mapa

**Trail**:
The alternative arrangement of the Overview: a path through the Topics in Topic order, one stretch per Area.
_Avoid_: Path, journey, roadmap
_Polish_: Szlak

**Topic order**:
The learning order of Topics within an Area: a Topic comes after the Topics its examples rely on (e.g. Loops after the collections they iterate over). Numbers the Trail and decides the "next stop" from a Topic.
_Avoid_: Sequence, curriculum

**Index**:
The always-reachable, clickable list of the cheat sheet's own parts, used to jump straight to one.
_Avoid_: TOC, glossary, menu, sidebar

**Term**:
A Python concept (e.g. _iterable_, _mutable_) with a short definition that links to where it is explained. A later addition, not part of the MVP.
_Avoid_: Glossary entry, keyword
