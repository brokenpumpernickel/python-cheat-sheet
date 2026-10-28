# 26: pandas Changing columns and Missing values Topics

**What to build:** Two pandas Topics that ticket 24 left planned. **Changing columns** covers computing, cleaning, converting, renaming and dropping columns. **Missing values** covers finding, counting, dropping and filling NaN. Together they are the data-cleaning part of the lab notebook, plus the missing-data basics a statistics lab needs.

Decided with the Author (every recommendation accepted). The English titles are decided; the Polish titles are the agent's.

- **Changing columns** (`columns`). The Entries:
  - **A column from other columns:** `df["hours"] = df["seconds"] / 3600`, vectorised, with no loop.
  - **Text methods:** `.str.len()`, `.str.lower()`, `.str.replace(...)`, `.str.strip()`.
  - **Text to numbers:**
    - `df["population"].str.replace(",", "").astype(int)`, as in the notebook.
    - `pd.to_numeric(..., errors="coerce")`, which turns what it can't read into NaN. Link to Missing values.
  - **A function on each value:** `df["state"].apply(convert)` with a small `def`, as in the notebook's `convert_state`. Use a self-made function, not the `us` package. A blank line follows the `def`.
  - **Mapping values with a dictionary:** `df["group"].map({"A": "control", "B": "treatment"})`, and what an unmapped value becomes (NaN).
  - **Renaming columns:**
    - `df.rename(columns={...})`.
    - Cleaning all names with `df.columns = df.columns.str.lower().str.replace(".", "_")`. Show the chained form in brackets over several lines, as in the notebook.
  - **Dropping columns:** `df.drop(columns=[...])`, and that it returns a new DataFrame.
    - **Pitfall:** changing a column of a filtered table doesn't change the original. Show `df[df["score"] < 50]["score"] = 50` leaving `df` unchanged, and `df.loc[df["score"] < 50, "score"] = 50` instead.
    - Check what pandas 3 prints (a ChainedAssignmentError warning or nothing): it goes to stderr, so the Output won't show it. Mention it in the text only if it's reliable.
- **Missing values** (`missing-values`). The Entries:
  - **Finding missing values:** `df.isna()` and `df.isna().sum()`, with a table where `np.nan` or `None` marks the gaps.
  - **Statistics skip NaN:** `mean()` ignores missing values, and `count()` counts the values that aren't missing, unlike `len(df)`.
  - **Dropping rows with missing values:** `dropna()`, and `dropna(subset=["score"])`.
  - **Filling missing values:** `fillna(0)`, and `fillna(df["score"].mean())`, with a word on when filling with the mean is a bad idea for statistics.
    - **Pitfall:** `df["score"] == np.nan` is all False, because NaN equals nothing, not even itself. Use `isna()`.
- **Style:** as ticket 24 decided for the pandas Area.
- **Links:**
  - Python Basics Strings for the `.str` methods, Functions for `apply`, and Dictionaries for `map`.
  - NumPy's *Missing values with genfromtxt* (Saving and loading), both ways.
  - Earlier pandas Topics where natural.
  - At most three per Entry. No links into planned Topics.

Conventions from tickets 12–24 apply:
- Outputs show values, not English sentences.
- A blank line follows a compound block.
- "Polish term (English term)" at first mention, e.g. "brakujące wartości (missing values)".

**Running in parallel:** tickets 25–28 run at the same time, each in its own session and PR, all starting from `main` after ticket 24.
- **Edit only your own Topic files.** Make back-links (a See-also added to an Entry outside your Topics) only where the ticket asks for them, and keep them few. Two PRs editing the same Entry would conflict.
- **Link only to Entries that are on `main` or in your own Topics.** The other parallel tickets' Topics are still planned on `main`, and a link into a planned Topic fails the build.
- **List the links you'd add into the other parallel tickets' Topics** under a **Links to add later** heading in the Comments, as `your-topic/entry → other-topic/entry`. They're added in one pass after all four PRs are merged.
- **If `main` moves:** If another of these PRs is merged first and yours then conflicts, bring your branch up to date with `main` and resolve it. Don't push to a merged PR's branch.

**Blocked by:** 24 (resolved, PR #35).

**Status:** resolved

- [x] Changing columns and Missing values are written (no longer planned), each with a summary in both Languages, and the decided Entries with their English titles and Polish.
- [x] The Pitfalls are there: changing a filtered copy, and `== np.nan`.
- [x] Every example runs alone with `uv run python` in an empty folder, with no warnings, and pastes into the REPL.
- [x] `uv run cheatsheet build` and `uv run pytest` pass. Both pages were looked at in both Languages in `uv run cheatsheet serve`.
- [x] The Comments list every Entry with its Polish title, plus any decisions made on the way.
- [x] One session and one PR.

## Comments

- **Topics** (English / Polish, glyph unchanged):
  - `columns`: *Changing columns* / *Zmiana kolumn*, `df[]=`. Summary: "Adding and cleaning columns: computing from other columns, text methods, text to numbers, apply, map, renaming and dropping." / "Dodawanie i czyszczenie kolumn ramki danych (DataFrame): obliczanie z innych kolumn, metody tekstowe, tekst na liczby, apply, map, zmiana nazw i usuwanie."
  - `missing-values`: *Missing values* / *Brakujące wartości*, `NaN`. Summary: "Gaps in a table: finding and counting NaN, statistics that skip it, dropping rows and filling gaps." / "Brakujące wartości (missing values) w ramce danych: znajdowanie i zliczanie NaN, statystyki, które je pomijają, usuwanie wierszy i uzupełnianie braków."
- **Entries** (English / Polish):
  - Changing columns:
    - *A column from other columns* / *Kolumna z innych kolumn*
    - *Text methods* / *Metody tekstowe*
    - *Text to numbers* / *Tekst na liczby*
    - *A function on each value* / *Funkcja na każdej wartości*
    - *Mapping values with a dictionary* / *Zamiana wartości słownikiem*
    - *Renaming columns* / *Zmiana nazw kolumn*
    - *Dropping columns* / *Usuwanie kolumn*, with the Pitfall on changing a column of a filtered table
  - Missing values:
    - *Finding missing values* / *Znajdowanie brakujących wartości*
    - *Statistics skip NaN* / *Statystyki pomijają NaN*
    - *Dropping rows with missing values* / *Usuwanie wierszy z brakami*
    - *Filling missing values* / *Uzupełnianie brakujących wartości*, with the `== np.nan` Pitfall
- **Links:**
  - *A column from other columns* → *A column is a Series*, Array maths' *Element-wise arithmetic*.
  - *Text methods* → Strings' *Cleaning and splitting*.
  - *Text to numbers* → *Column types*, *Finding missing values*.
  - *A function on each value* → Functions' *Defining and calling*, Conditionals' *if / elif / else*.
  - *Mapping values with a dictionary* → Dictionaries' *Creating and accessing*, *Finding missing values*.
  - *Renaming columns* → *Shape, columns and index*.
  - *Dropping columns* → *Column types* (the same "returns a new column / table" habit).
  - *Finding missing values* → *info()*, *Missing values with genfromtxt*, *True and False as numbers* (why `isna().sum()` counts).
  - *Statistics skip NaN* → *Column statistics*, *Missing values with genfromtxt*.
  - *Filling missing values* → *Column statistics*, Aggregates' *Standard deviation and variance*.
  - Back-link (the one edit outside my Topics): *Missing values with genfromtxt* → *Statistics skip NaN*, which is the pandas side of its `np.nanmean` point.
- **Decisions:**
  - **The ChainedAssignmentError is mentioned.** In pandas 3.1.0, `df[df["score"] < 50]["score"] = 50` warns with `ChainedAssignmentError` (on stderr, so not in the Output) both as a script and in a Jupyter kernel, every time it runs, not only the first. pandas sets its reference-count threshold per Python version (`REF_COUNT = 2 if PY314 else 3`), so it holds on 3.14 too. The Pitfall says pandas 3 "only warns", so Students know the warning they see in the lab means "nothing changed". This is the one example with stderr output, and it is the point of the Pitfall.
  - **The filtered-copy Pitfall shows the fix too.** The guide says a Pitfall's code shows the mistake and the Entry's example is the fix, but Dropping columns' example is about `drop`, not `.loc`. As the ticket asked, the Pitfall code runs the chained assignment, prints `df` unchanged, then runs `df.loc[df["score"] < 50, "score"] = 50` and prints the changed `df`.
  - **Pitfall placement as in the ticket:** the filtered copy under *Dropping columns*, `== np.nan` under *Filling missing values* (a fill such as `df.loc[df["score"] == np.nan, "score"] = 0` is where Students meet it). The text says a filter or a fill built on the comparison changes nothing and names `isna()`.
  - **A function on each value** uses a `grade(score)` function with two `if`s (90+ → 5, 50+ → 3, else 2) rather than a state converter. A self-made state-name converter needs a dictionary, which would repeat the next Entry; grades are numbers, so the Output is the same in both Languages. The `def` is followed by a blank line.
  - **Text to numbers** uses a two-row table: `population` with thousands commas (`str.replace` then `astype(int)`, in two lines to keep to 43 characters) and `area` with an `"unknown"` that `pd.to_numeric(..., errors="coerce")` turns into `NaN`. It prints the table and `df.dtypes` (`int64`, `float64`).
  - **Text methods** uses `[" Kraków", "NOWY_SĄCZ "]`, so `strip`, `lower` and `replace("_", " ")` each have something to do, in two rows to keep the line within 43 characters.
  - **Renaming columns** prints `list(df.columns)` after `rename` (35 characters; `print(df.columns)` would be 50+ and scroll), then the chained form in brackets, one method per line, and the cleaned table. In pandas 3 `.str.replace(".", "_")` is literal (`regex=False` is the default).
  - **Mapping values** prints `control` / `treatment` as values in the table, as the ticket decided; they are data, not sentences.
  - **Filling missing values** prints both filled columns, then the standard deviation before (12.49, over 3 known scores) and after filling with the mean (10.20), so the "too small" warning in the text is visible in the Output.
  - **NumPy is imported** in every Missing values example, since each writes `np.nan`. *Finding missing values* also uses `None` in the text column, so both spellings appear.
  - *Dropping rows with missing values* and *Mapping values with a dictionary* are five words, one over the guide's four, but those titles were decided.
- **Checks:** all 13 examples (11 Entries and 2 Pitfalls) were run alone with `uv run python -W default` in empty folders and pasted into `code.InteractiveConsole`: same output, no `SyntaxError`, and no stderr except the Pitfall's intended `ChainedAssignmentError`. The build's Outputs match those runs. Shown code keeps to 43 characters (38 in the Pitfall). `uv run cheatsheet build` and then `uv run pytest` pass. Both pages were checked with a Playwright script through `uv run python` in English and Polish at 1280 px: no `#|` shown, no console errors, See-also chips resolve, and Changing columns' Previous stop is Exploring data while Missing values' Next stop is Matplotlib's Plotting basics (the later pandas Topics are still planned on `main`).

### Links to add later

Entry ids in tickets 25 and 27 are guessed from their titles; check them once those Topics are merged.

- `columns/dropping-columns` → `selecting/rows-and-columns-by-label-with-loc` (the `.loc[rows, "score"] = 50` fix)
- `columns/dropping-columns` → `filtering/a-boolean-mask` (the filtered table in the Pitfall)
- `columns/text-methods` → `filtering/text-that-contains`
- `missing-values/finding-missing-values` → `filtering/a-boolean-mask` (`df[df["score"].isna()]` gives the rows with gaps)
- `missing-values/statistics-skip-nan` → a grouping Entry on group means, if one says `NaN` is skipped per group
- Reverse: `filtering/text-that-contains` (`na=False`) → `missing-values/finding-missing-values`
