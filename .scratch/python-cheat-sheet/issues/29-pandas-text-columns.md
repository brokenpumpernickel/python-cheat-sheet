# 29: pandas Text columns Topic (the .str accessor)

**What to build:** Several pandas Entries use `.str`, but only Changing columns' *Text methods* explains it, in one sentence. Students then try `df["city"].lower()`, or wonder why `str.contains(".")` matches everything. A new Topic, **Text columns**, explains the `.str` accessor and the text operations Students need on a column.

Decided with the Author (every recommendation accepted). The English titles are decided; the Polish titles are the agent's.

- **Where:**
  - `text-columns`, **Text columns** (*Kolumny tekstowe*, glyph `.str`), right after Changing columns.
  - The stubs PR (#41) already adds it to the Area's Topic order as a planned Topic and updates the Area blurb. Remove `planned: true` and add both summaries.
- **It takes over Text methods.**
  - Move Changing columns' *Text methods* into this Topic, where it becomes, or merges into, *Cleaning text* below.
  - Its id changes, so update every See-also link to `columns/text-methods`. On `main`, `filtering/text-that-contains` links to it.
  - Changing columns keeps *Text to numbers* and *Renaming columns*, which use `.str`, and they gain a See-also link to *The .str accessor*.
  - Update Changing columns' summary in both Languages.
- **Entries:**
  - **The .str accessor:**
    - A column of text has no `.lower()` of its own; `.str` applies the string methods to every value.
    - The names match Python's string methods.
    - A missing value stays NaN; show one `None` in the column.
    - **Pitfall:** `df["city"].lower()` raises `AttributeError` (`raises=AttributeError`).
  - **Cleaning text:** `.str.strip()`, `.str.lower()`, `.str.title()` and `.str.replace(...)`, chained, on messy names or cities.
  - **Splitting text:** `.str.split(" ")` gives lists. `.str[0]` picks the first part, and `expand=True` gives new columns, e.g. "Kowalski Jan" into `surname` and `name`.
  - **Searching text:** `.str.contains(...)`, `.str.startswith(...)`, `.str.endswith(...)`, with `case=False` and `na=False`.
    - **Pitfall:** `contains` treats its pattern as a regular expression, so `"."` matches any character. Use `regex=False`.
    - Check pandas 3's defaults (`contains` versus `replace`) and say which one does what.
  - **Lengths, slices and counts:** `.str.len()`, `.str[:3]` and `.str.count("a")`.
- **Style:** as ticket 24 decided for the pandas Area: printed small made-up tables built inside each example, `import pandas as pd`. Polish names with Polish letters are welcome, and print fine.
- **Links:**
  - Python Basics Strings (*Cleaning and splitting*) and Changing columns.
  - Filtering's *Text that contains*, both ways. That Entry shows `contains` for filtering; this Topic explains it.
  - At most three per Entry.

**Running in parallel** with tickets 30 (Dates) and 31 (NumPy arrays and plotting with plt). Each runs in its own session and PR.
- Your worktree starts from the stubs branch `content/pandas-text-and-dates-stubs` (PR #41), so the planned Topic is already there. Open your PR against `main`. Until #41 is merged, your PR also shows its commit.
- Edit only `text-columns.md`, `columns.md`, and the links to `columns/text-methods` (in `filtering.md`). Don't touch `_area.md`, `dates.md`, `dataframes.md` or `pandas-plots.md`.
- `dates` is still planned, so don't link to it. List any link you'd add under **Links to add later** in the Comments.
- If `main` moves and your PR conflicts, bring your branch up to date with `main` and resolve it. Check that the PR is still OPEN before every push.

Conventions from tickets 12–24 apply:
- Outputs show values, not English sentences.
- A blank line follows a compound block.
- "Polish term (English term)" at first mention, e.g. "akcesor .str (.str accessor)", "wyrażenie regularne (regular expression)".

**Blocked by:** none (it starts from #41's branch).

**Status:** resolved

- [x] Text columns is written (no longer planned), with a summary in both Languages, and the five decided Entries with their English titles and Polish, including both Pitfalls.
- [x] *Text methods* is gone from Changing columns, every link to it is updated, and Changing columns links to Text columns, with its summary updated.
- [x] Every example runs alone with `uv run python` in an empty folder, with no warnings, and pastes into the REPL.
- [x] `uv run cheatsheet build` and `uv run pytest` pass. The page was looked at in both Languages in `uv run cheatsheet serve`.
- [x] The Comments list every Entry with its Polish title, plus any decisions made on the way and any Links to add later.
- [x] One session and one PR.

## Comments

Resolved in PR brokenpumpernickel/python-cheat-sheet#42 (https://github.com/brokenpumpernickel/python-cheat-sheet/pull/42), on branch `claude/ticket-29-pandas-text-columns-07f818`, started from the stubs branch `content/pandas-text-and-dates-stubs` (PR #41).

**Entries** in `content/pandas/text-columns.md` (glyph `.str`, *Kolumny tekstowe*):

- *The .str accessor* (*Akcesor .str*), with the Pitfall `df["city"].lower()` (`raises=AttributeError`).
- *Cleaning text* (*Czyszczenie tekstu*).
- *Splitting text* (*Dzielenie tekstu*).
- *Searching text* (*Wyszukiwanie tekstu*), with the Pitfall `.str.contains(".")` is `True` for every value.
- *Lengths, slices and counts* (*Długości, wycinki i zliczanie*).

**Changing columns:** *Text methods* is removed. *Text to numbers* and *Renaming columns* link to `text-columns/the-str-accessor`. The summary drops "text methods" / "metody tekstowe" in both Languages. Filtering's *Text that contains* now links to `text-columns/searching-text` instead of `columns/text-methods`, and *Searching text* links back to it. No other file linked to `columns/text-methods`.

**Decisions:**

- *Text methods* merged into *Cleaning text*: its `strip` / `replace` chain is there, its `.str.len()` moved to *Lengths, slices and counts*. Its See-also links went with it.
- *Cleaning text* chains `.str.strip()`, `.str.replace("_", " ")` and `.str.title()` on four spellings of two cities, printing `nunique()` before (4) and `value_counts()` after (2 each). `.str.lower()` is left out of the chain, since `.str.title()` after it would make it redundant; the explanation names it as the alternative, and *The .str accessor* runs it.
- *The .str accessor* shows the one `None` as `NaN` after `.str.lower()`, and prints `"GDAŃSK".lower()` beside it to show the names match Python's string methods.
- pandas 3.1 defaults, checked by running them: `.str.contains` (and `.str.count`) read the pattern as a regular expression (`regex=True`), `.str.replace` as plain text (`regex=False`). The Pitfall says both. `.str.split` with a single character treats it as plain text, so `split(" ")` needs no option.
- In pandas 3.1 a text column has dtype `str`, and `contains`/`startswith`/`endswith` already give `False` for a missing value; on an `object` column they give `NaN`, which breaks `df[mask]`. The Entry keeps `na=False`, as Filtering does, and says only what it does, not which versions need it.
- `startswith` and `endswith` have no `case=` option; the example shows `Exam_2025.CSV` giving `False` for both, and the explanation says they always match case.
- `.str.len()` on a column with a missing value gives `float64` (`3.0`), so *Lengths, slices and counts* uses a column without gaps.
- *Splitting text* has no Pitfall (the ticket decided none). A name with three parts would make `expand=True` give three columns and the two-name assignment fail; that could be a later Pitfall.
- Examples were checked alone in an empty folder with `-W always`; no warnings. None has a compound block, so they paste into the REPL as they are.

**Links to add later** (once `dates` has Entries; not added because it is planned):

- `dates` Entry on parsing dates from text (e.g. `pd.to_datetime`) → `text-columns/splitting-text` or `text-columns/cleaning-text`, for dates stored as text that need cleaning first.
- `text-columns/the-str-accessor` → the `dates` Entry on the `.dt` accessor, since `.dt` is the same idea for dates (Entry id to be read from ticket 30's Topic).
