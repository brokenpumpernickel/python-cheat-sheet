# 15: Figure descriptions

**What to build:** Every figure gets a short description in English and Polish, used as its accessible name for screen readers, in place of the generic "Figure drawn by the code above" label. This is the follow-up in the Comments of ticket 09, and it comes before the Matplotlib Area (ticket 16), the first Area full of figures. Decided with the Author:

- **Content format:** an Entry or a Pitfall whose example draws one or more figures carries a figure description: an English text and its `PL:` twin, following the pair rule. The syntax fits the existing format in `docs/authoring-guide.md` (e.g. a `### Figure` block). One description per example is enough, even if it draws several figures.
- **Validation:** after the examples run, an example that produced figures but has no description fails the build with a `ContentError` naming the file, line and Entry, as a missing translation does (ADR 0005). A description on an example that draws no figure is an error too. A description without Polish fails as usual.
- **Rendering:** each figure's accessible name is the description in the active Language, and it follows the EN | PL switch (ticket 08's mechanism: both Languages are in the page and CSS shows one; `aria-label`s go through `labelAttributes` and `client/language.ts`). Any approach that gives a correct name in both Languages will do, proven with Playwright's accessible-name checks after switching.
- **Data shape:** the description is part of the generated content data and the Astro schema.
- **Tests:** content-build tests for a missing description, a description without a figure, a description without Polish, and a valid one reaching the data; browser tests for the figure's accessible name in EN and PL and the axe audit on the figure Topic. The fixtures that draw figures (`tests/fixtures/figures`, the site fixture's Plots › Charts) carry descriptions.
- **Guide:** the authoring guide documents the block, when it's required, how to write a good description (what the plot shows and its notable shape, 1–2 sentences, no "image of"), and the new error messages in the "When the build fails" tables.

**Blocked by:** None (can start immediately).

**Status:** resolved

- [x] The content format has a figure description for an Entry's example and for a Pitfall's, each with English and a `PL:` twin.
- [x] The build fails, naming the file, line and Entry, when an example draws a figure without a description, when a description sits on an example that draws no figure, and when a description has no Polish.
- [x] The description is in the generated content data and the Astro schema.
- [x] Each figure's accessible name is its description in the active Language, it changes with the EN | PL switch, and the generic figure label is gone.
- [x] Content-build tests cover the three failures and a valid description in the data; browser tests check the accessible name in EN and PL; the axe audit passes on the figure Topic.
- [x] The figure fixtures carry descriptions.
- [x] The authoring guide documents the block, when it's required, how to write a good description, and the new error messages.
- [x] `uv run cheatsheet build` and `uv run pytest` pass.

## Comments

**Resolved** in PR brokenpumpernickel/python-cheat-sheet#17 (https://github.com/brokenpumpernickel/python-cheat-sheet/pull/17).

- **Format:** a `### Figure` section right after the code it describes, holding one English paragraph and its `PL:` twin. Before `### Pitfall` it belongs to the Entry's example; after the Pitfall's code, to the Pitfall's. One description covers every figure an example draws. Descriptions are plain text, because they are read out, so Markdown in them fails the build.
- **Validation:** the parser checks the pair rule, plain text, a second `### Figure` for the same code, and a `### Figure` after a Pitfall that has no code. After the examples run, the build checks that an example has a description exactly when it drew figures. These two messages give the Entry's line (`basics/names.md:10 (names/binding): the example draws a figure but has no description; …`), and they are listed with the other failing examples. The other run failures still name the file and Entry without a line, as before.
- **Data:** `figure` on an Entry and on its Pitfall (`null` when there is none), with the Polish in `pl.figure` and `pl.pitfallFigure`, following how `pl.pitfall` holds the Pitfall's Polish. The Astro schema has all four. The parser also passes the Entry's heading line to the build for those messages, and the build drops it, so it's not in `generated/content.json`.
- **Rendering:** a figure stays a `role="img"` with an `aria-label`. `labelAttributes` now also takes content prose as twins (`{ en, pl }`): it renders the English, keeps both in `data-aria-label-en` / `data-aria-label-pl`, and `client/language.ts` copies the active one into `aria-label` on load and on every switch. An `aria-labelledby` pointing at the hidden `data-lang` spans wouldn't work: a hidden element that is referenced directly counts towards the name, so both Languages would be read. `OutputBlock` throws if it gets figures without a description, a second safety net after the build's check. The "Figure drawn by the code above" label is gone from `labels.ts`.
- **Tests:** seven invalid fixtures (no description, a description without a figure, no Polish, Markdown, two descriptions, a Pitfall figure without a description, a description after a Pitfall without code) and a test that the descriptions reach the data, including a two-figure example and a Pitfall's figure. In the browser: the Charts figure's accessible name in EN, after switching to PL and back, and when opened with `?lang=pl`. The axe audit of the figure Topic now runs in both Languages. The "nothing left in the other Language" checks now include content prose in labelled attributes, and the after-switching check also covers the Charts Topic.
- **Guide:** a "Figure description" section under Entry (when, a Pitfall's figure, one per example, what to write, plain text, Polish), the structure and pair-rule lines, a "Figure descriptions" table and two rows in "Running the examples", the Polish list, the checklist, and a description on the complete example's *Plotting counts* (its build was re-checked). `GLOSSARY.md` has the term *Figure description* (avoid: alt text, caption).
- **Content:** no Entry in `content/` draws a figure yet, so none needed a description. The Matplotlib Area (ticket 16) is the first that will.
