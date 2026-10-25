# 12: MVP content: Python Basics and the planned Areas

**What to build:** The real content for launch. The Python Basics Area has nine Topics in this Topic order: Variables, Strings, Conditionals, Lists, Tuples, Dictionaries, Sets, Loops, Functions. They contain exactly the Entries decided in ticket 11, with English and Polish text, Pitfalls where useful, and See-also links (including from loop-using Entries in earlier Topics to Loops). The NumPy, pandas, Matplotlib and SciPy stats Areas are added as planned Areas with their planned Topics. It's written by following the authoring guide; the prototype's sample text is the starting draft. The sample Topic from ticket 01 is replaced or brought in line.

**Blocked by:** 03 (Full content validation), 10 (Authoring guide), 11 (Review the Entry title lists).

**Status:** resolved

- [x] Every Entry in ticket 11's decision exists; no others.
- [x] The content build passes with no warnings; every Output comes from execution.
- [ ] Polish follows the terminology rule; spot-checked by the Author.
- [x] Each example pasted into a fresh Jupyter cell runs and prints the shown Output.
- [x] The deployed site shows the full Map and Trail, with the four planned Areas faded.

## Comments

**Resolved**, except the Author's Polish spot-check, which is left open for the Author. Python Basics has the nine Topics in the spec's Topic order with exactly the 29 Entries from ticket 11's decision, titles unchanged. The four library Areas are planned: NumPy 210, pandas 260, Matplotlib 25, SciPy stats 320, with the spec's Polish Topic titles. The Matplotlib figure Entries from the prototype stay out, as the spec says.

- **Checked:** `uv run cheatsheet build` is clean (29 Entries, 4 Pitfalls with code). Every example was also run on its own with `uv run python` in an empty folder: stdout matches the Output, and stderr is empty apart from the expected traceback, so there are no warnings. Each was also fed line by line to an interactive console, the way a paste into the `python` REPL runs. Map, Trail, Index rail and several Topics were looked at in both Languages in `uv run cheatsheet serve`. The deployed site will match once this is merged, since CI runs the same build.
- **Changes from the prototype text:**
  - Outputs show values, not English sentences. if / elif / else assigns significance stars (`**`, `*`, `ns`) instead of printing phrases. Looping over items prints `key value` instead of using `"->"`. Converting types uses `str(42) + "1"` instead of `" samples"`, and shows that `int(3.9)` drops the decimals.
  - Explanations lead with the syntax.
  - Inline code is the same in both Languages: `d[key]`, not `d[klucz]`.
  - The Loops summary no longer promises `while`.
  - The range Pitfall uses `range(1, 10)`.
- **REPL paste:** a compound block followed by an unindented line (`for …:` then `print(…)`) is a `SyntaxError` when pasted into the Python 3.12 REPL, though it works in Jupyter. Those examples have a blank line after the block. The guide doesn't mention this. It's worth a line under "Code example".
- **Pitfalls** are where the prototype had them (eight, four with code). No new ones were added.
- **See also:** Sorting → `functions/lambda` and List comprehensions → `loops/for-over-a-collection` are back. Loop-using Entries in earlier Topics link to Loops: Cleaning and splitting, zip, Looping over items, Counting occurrences.
- **For the Author to check:**
  - The Polish.
  - Library glyphs, picked as pieces of what Students type: `[[ ]]`, `a[i]`, `rng`, `.sum`; `df`, `df[ ]`, `group`; `plt`, `x, y`, `ax[ ]`; `pdf`, `ttest`, `corr`.
  - The Topic id `scatter-plots` (the prototype had `scatter`).
