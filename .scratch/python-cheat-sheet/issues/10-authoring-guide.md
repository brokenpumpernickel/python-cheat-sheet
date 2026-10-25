# 10: Authoring guide for agents

**What to build:** A written guide that lets an agent, or the Author, add or edit content correctly the first time, linked from the project's agent instructions. It covers:

- **Structure:** the Area and Topic file format; the Entry anatomy, with an explanation of 1–3 sentences, exactly one self-contained example that prints explicitly (ADR 0003), the Output never written by hand (ADR 0002), when to add a Pitfall, and when to mark an expected error.
- **Topic order:** a Topic comes after the Topics its examples rely on, and See-also links to a later Topic are preferred over reordering.
- **Polish:** Polish is required, with the Polish term plus the English one in parentheses at the first mention, and the agreed labels (ADR 0005).
- **Vocabulary:** use the glossary's terms.
- **Workflow:** how to build, read failures and preview locally.

**Blocked by:** 03 (Full content validation), since the guide documents the final rules.

**Status:** resolved

- [x] The guide includes one complete annotated example Topic covering every Entry feature.
- [x] Every validation rule from ticket 03 is listed with the error it produces and how to fix it.
- [x] The project's agent instructions point to the guide for any content task.
- [x] Verified by having a fresh agent add a small throwaway Topic using only the guide; it builds on the first or second try (then removed).

## Comments

**Resolved.** The guide is `docs/authoring-guide.md`. It grew out of `docs/content-format.md`, which is renamed, so the format reference and the writing rules are in one file. `CLAUDE.md` has a "Content" section pointing to it, and the README links it. The guide covers vocabulary, the file format, the Entry anatomy, Topic order, Polish, new Areas (hue and glyphs), the workflow, every `ContentError` message in `content.py` and `build.py` (grouped tables with cause and fix), and an annotated example Topic. The example is a Dictionaries Topic with a planned Loops Topic. It was extracted from the guide verbatim and built, content and site.

- **Verification:** a fresh agent given only the guide added a Tuples Topic (two Entries, one Pitfall with code). It built on the first try. Its questions led to these fixes:
  - Titles may be one word.
  - An explanation may state a side fact the example doesn't run.
  - "First mention" is defined per Entry.
  - A new Topic goes in its spec position among the Topics that exist.
  - The guide describes what a passing build looks like, and that `generated/` and `site/dist/` are not committed.
  - It has a one-line command that lists every Output from `generated/content.json`.
  - Where existing content disagrees with the guide, the guide wins.

  The throwaway Topic has been removed.
- **Decisions the Author may want to check:**
  - Polish uses lowercase "twój/twoja". The Lists sample's "Twoją" is changed in the guide's copy of it only.
  - Printed Output shows values, not English sentences, since Outputs are shared by both Languages.
  - Figures carry no translatable text.
  - Hues should be at least about 40° apart. Ticket 09 showed contrast holds at every hue, so this is for telling Areas apart.
- **For 12:**
  - Bring `lists.md` in line with the guide:
    - "Lista (list)" at first mention in Creating and indexing.
    - Lowercase "twoją" in the Sorting Pitfall.
    - Check the other Entries for the terminology rule.
  - Suggested hues for the planned Areas, spaced from Python Basics (160): NumPy 210, pandas 260, Matplotlib 25, SciPy stats 320.
  - Topic ids must be unique across Areas. "Indexing" (NumPy) and "Selecting" (pandas) don't clash with anything today.
  - The build ignores stderr, so check examples for warnings with `uv run python` on a copy.
- **Follow-up (code, not done here):** a code fence with no language (a bare ```` ``` ````) crashes `_example()` in `content.py` with `ValueError: not enough values to unpack`, instead of a `ContentError`. The guide documents the symptom. The fix is a one-line guard plus a fixture in `tests/fixtures/invalid/`. An example over 60 s also ends in a traceback (a `TimeoutError` from the kernel) rather than a `Content error:`.
- **Follow-up fixed** in PR_LINK: a bare fence and an example over the timeout now stop the build with a `ContentError` (`has no language; fence examples as ```python` and `the example timed out after 60 s`), and the guide's tables show both.
