# 25: pandas Selecting, Filtering and Sorting Topics

**What to build:** Three pandas Topics that ticket 24 left planned: **Selecting** (columns and rows with `[]`, `loc` and `iloc`), **Filtering** (boolean masks) and **Sorting**. These are the parts of the lab notebook where Students most often mix things up: `df[...]` versus `loc` versus `iloc`, and `and` versus `&`.

Decided with the Author (every recommendation accepted). The English titles are decided; the Polish titles are the agent's.

- **Selecting** (`selecting`). The Entries:
  - **One column or several:** `df["score"]` gives a Series, and `df[["name", "score"]]` gives a DataFrame.
    - **Pitfall:** `df["name", "score"]` raises `KeyError` (`raises=KeyError`).
  - **Rows by position with iloc:** `df.iloc[0]`, `df.iloc[3:5]`, `df.iloc[3:5, :2]`.
  - **Rows and columns by label with loc:** `df.loc[3]`, `df.loc[3:5, "score"]`, `df.loc[3:5, "name":"score"]`.
    - **Pitfall:** a `loc` slice includes its end and an `iloc` slice doesn't. Show `df.loc[3:5]` and `df.iloc[3:5]` side by side: 3 rows against 2.
  - **A single value:** `df.loc[2, "score"]` and `df.iloc[2, 1]`. Print it on its own.
  - **Row slices with df[3:5]:** a slice in `[]` picks rows by position.
    - **Pitfall:** `df[3]` looks for a column named 3 and raises `KeyError`.
  - Use an index that isn't 0, 1, 2… in one Entry, e.g. names, or `set_index("name")`, so that labels and positions visibly differ.
- **Filtering** (`filtering`). The Entries:
  - **A boolean mask:** `df["score"] > 50` gives a Series of True/False, and `df[df["score"] > 50]` gives the matching rows.
  - **Combining conditions:** `&`, `|` and `~`, each condition in brackets.
    - **Pitfall:** `and` raises `ValueError` (the truth value of a Series is ambiguous), `raises=ValueError`.
  - **isin:** `df[df["group"].isin(["A", "C"])]`.
  - **Text that contains:** `df["comment"].str.contains("abduc", case=False)`, with `na=False` if the column has missing values.
  - **A column of the matching rows:** `df.loc[mask, "score"]`, and looping over it as in the notebook. A blank line follows the loop.
  - **Counting and proportions with a mask:** `mask.sum()` and `mask.mean()`. Link both ways with NumPy Aggregates' *Counting and proportions with a mask*, or one way if that Entry is full.
- **Sorting** (`sorting`). The Entries:
  - **sort_values:** by one column, and the result is a new DataFrame.
  - **Descending, and by several columns:** `ascending=False`, and `by=["group", "score"]` with a list for `ascending`.
  - **nlargest and nsmallest.**
  - **The row with the largest value:** `df.loc[df["score"].idxmax()]`, and a single column of it. This replaces the notebook's `iloc` with `columns.get_loc`.
  - **sort_index:** after sorting, or on a named index.
- **Style:** as ticket 24 decided for the pandas Area: printed small tables built inside each example, `import pandas as pd`, NumPy only where it's used.
- **Links:**
  - NumPy Indexing (*boolean masks*, slices) and Python Basics Lists (slices) where natural.
  - Between these three Topics and ticket 24's Topics.
  - At most three per Entry. No links into planned Topics.

Conventions from tickets 12–24 apply:
- Outputs show values, not English sentences.
- A blank line follows a compound block.
- "Polish term (English term)" at first mention, e.g. "maska logiczna (boolean mask)", "etykieta (label)", "pozycja (position)".

**Running in parallel:** tickets 25–28 run at the same time, each in its own session and PR, all starting from `main` after ticket 24.
- **Edit only your own Topic files.** Make back-links (a See-also added to an Entry outside your Topics) only where the ticket asks for them, and keep them few. Two PRs editing the same Entry would conflict.
- **Link only to Entries that are on `main` or in your own Topics.** The other parallel tickets' Topics are still planned on `main`, and a link into a planned Topic fails the build.
- **List the links you'd add into the other parallel tickets' Topics** under a **Links to add later** heading in the Comments, as `your-topic/entry → other-topic/entry`. They're added in one pass after all four PRs are merged.
- **If `main` moves:** If another of these PRs is merged first and yours then conflicts, bring your branch up to date with `main` and resolve it. Don't push to a merged PR's branch.

**Blocked by:** 24 (resolved, PR #35).

**Status:** resolved

- [x] Selecting, Filtering and Sorting are written (no longer planned), each with a summary in both Languages, and the decided Entries with their English titles and Polish.
- [x] The Pitfalls are there: `df["a", "b"]` KeyError, `loc` versus `iloc` slice ends, `df[3]` KeyError, and `and` ValueError (expected errors marked with `raises=`).
- [x] Every example runs alone with `uv run python` in an empty folder, with no warnings, and pastes into the REPL.
- [x] `uv run cheatsheet build` and `uv run pytest` pass. The three pages were looked at in both Languages in `uv run cheatsheet serve`.
- [x] The Comments list every Entry with its Polish title, plus any decisions made on the way.
- [x] One session and one PR.

## Comments

- Resolved by PR #37: https://github.com/brokenpumpernickel/python-cheat-sheet/pull/37.
- **Topics** (English / Polish, glyph kept from ticket 24):
  - `selecting`: *Selecting* / *Wybieranie*, `df[ ]`. Summary: "Picking parts of a table: columns with [], rows by position with iloc, rows and columns by label with loc, single values and row slices." / "Wybieranie części ramki danych (DataFrame): kolumny przez [], wiersze według pozycji z iloc, wiersze i kolumny według etykiet z loc, pojedyncze wartości i wycinki wierszy."
  - `filtering`: *Filtering* / *Filtrowanie*, `mask`. Summary: "Keeping the rows that meet a condition: boolean masks, combining conditions, isin, text that contains a word, a column of the matching rows, and counting with a mask." / "Zostawianie wierszy, które spełniają warunek: maski logiczne (boolean masks), łączenie warunków, isin, tekst zawierający słowo, kolumna pasujących wierszy i zliczanie maską."
  - `sorting`: *Sorting* / *Sortowanie*, `sort`. Summary: "Putting rows in order: sort_values by one or several columns, descending order, nlargest and nsmallest, the row with the largest value, and sort_index." / "Ustawianie wierszy ramki danych (DataFrame) w kolejności: sort_values po jednej lub kilku kolumnach, kolejność malejąca, nlargest i nsmallest, wiersz z największą wartością i sort_index."
- **Entries** (English / Polish):
  - Selecting:
    - *One column or several* / *Jedna kolumna lub kilka*, with the `df["name", "score"]` Pitfall (`raises=KeyError`, Output `KeyError: ('name', 'score')`)
    - *Rows by position with iloc* / *Wiersze według pozycji z iloc*
    - *Rows and columns by label with loc* / *Wiersze i kolumny według etykiet z loc*, with the Pitfall printing `df.loc[3:5]` (3 rows) and `df.iloc[3:5]` (2 rows)
    - *A single value* / *Pojedyncza wartość*
    - *Row slices with df[3:5]* / *Wycinki wierszy przez df[3:5]* (id `row-slices-with-df-3-5`), with the `df[3]` Pitfall (`raises=KeyError`, Output `KeyError: 3`)
  - Filtering:
    - *A boolean mask* / *Maska logiczna*
    - *Combining conditions* / *Łączenie warunków*, with the `and` Pitfall (`raises=ValueError`)
    - *isin* / *isin*
    - *Text that contains* / *Tekst, który zawiera*
    - *A column of the matching rows* / *Kolumna pasujących wierszy*
    - *Counting and proportions with a mask* / *Zliczanie i proporcje z maską*
  - Sorting:
    - *sort_values* / *sort_values*
    - *Descending, and by several columns* / *Malejąco i po kilku kolumnach*
    - *nlargest and nsmallest* / *nlargest i nsmallest*
    - *The row with the largest value* / *Wiersz z największą wartością*
    - *sort_index* / *sort_index*
- **Links:** *One column or several* → DataFrames' *A column is a Series* and Exploring's *Correlation with corr()*, and back from *Correlation with corr()* (the double-bracket link ticket 24 left for Selecting). *Rows by position with iloc* → Lists' *Slicing* and NumPy Indexing's *Rows and columns*; *Row slices with df[3:5]* → *Slicing*; *A single value* → *Rows and columns* and Sorting's *sort_index*. *A boolean mask* → Indexing's *Boolean masks* and Array maths' *Comparisons*; *Combining conditions* → *Boolean masks* and Conditionals' *Combining conditions*; *isin* → Sets' *Set operations*; *Text that contains* → Strings' *Cleaning and splitting*; *A column of the matching rows* → Selecting's *Rows and columns by label with loc*, Loops' *for over a collection* and Exploring's *Column statistics*; *Counting and proportions with a mask* → Aggregates' *Counting and proportions with a mask*, Array maths' *True and False as numbers* and Exploring's *value_counts*. *sort_values* → Lists' *Sorting*; *nlargest and nsmallest* → Exploring's *head and tail*; *The row with the largest value* → Aggregates' *Where the minimum and maximum are* and Selecting's *A single value*; *sort_index* → *A single value*.
- Decisions:
  - **Aggregates is linked one way.** NumPy Aggregates' *Counting and proportions with a mask* already has four See-also links, so it is full and gets no back-link. The only Entry outside these Topics that changed is *Correlation with corr()* (one line added).
  - **The non-default index is in *A single value*.** It builds the table with `.set_index("name")`, so the Entry shows `df.loc["Ewa", "score"]` beside `df.iloc[2, 1]`, both giving 90, instead of the ticket's `df.loc[2, "score"]`, where label and position would look the same. The *loc* Entry keeps `df.loc[3]` and says that its labels are the default 0 to 5.
  - **The six-row tables have `name`, `score` and `age`.** Then `df.iloc[3:5, :2]` keeps `name` and `score`, and `df.loc[3:5, "name":"score"]` visibly stops at `score`, its end included. A six-letter `group` line would have been 44 characters, over the width.
  - **Line length:** the code box at 1280 px fits about 44 characters, so shown code keeps to 43, as in ticket 24. Five- and six-name lists are wrapped over two lines, and the long `sort_values` and `str.contains` calls are wrapped. At 390 px code boxes scroll sideways, as in the Topics already on `main`.
  - **`na=False` is in the code.** In pandas 3 a `str` column's missing value already gives `False` in `str.contains`, but an `object` column (and older pandas) gives `NaN`, and a mask with `NaN` can't select rows. The explanation says `na=False` makes it work in every pandas version, without the version history.
  - **The row with the largest value** says that `idxmax()` gives a label, so it goes with `loc`, not `iloc`: that is what replaces the notebook's `iloc` with `columns.get_loc`. No separate Pitfall.
  - **The loop** in *A column of the matching rows* prints the names, then a blank line, then `print(df.loc[mask, "score"].mean())`.
  - **No new Pitfalls** beyond the four the ticket decided.
- All 19 examples (16 Entries and 3 Pitfalls with code) were run alone with `uv run python -W default` in their own empty folders: no warnings, errors only where marked. Each was also pasted into `code.InteractiveConsole`: no `SyntaxError`, same Output. `uv run cheatsheet build` and `uv run pytest` (248 passed) pass, run one after the other. The three pages were checked with a Playwright script through `uv run python` at 1280 and 390 px in both Languages: no `#|` shown, no console errors, no code box scrolling at 1280 px.

### Links to add later

- `filtering/a-column-of-the-matching-rows → columns/dropping-columns` (its Pitfall assigns through `df.loc[mask, "score"]`)
- `filtering/text-that-contains → columns/text-methods`
- `filtering/text-that-contains → missing-values/finding-missing-values`
- `filtering/counting-and-proportions-with-a-mask → missing-values/finding-missing-values` (`isna().sum()` counts with a mask too)
- `sorting/descending-and-by-several-columns → grouping/the-latest-row-per-group`
- `sorting/sort-index → grouping/the-group-as-an-index-or-as-a-column`
- `filtering/isin → grouping/keeping-the-largest-groups`, if that Entry filters with `isin`
- The other way, where natural: `columns/dropping-columns → filtering/a-column-of-the-matching-rows`, `grouping/the-latest-row-per-group → sorting/descending-and-by-several-columns`, `missing-values/finding-missing-values → filtering/counting-and-proportions-with-a-mask`
