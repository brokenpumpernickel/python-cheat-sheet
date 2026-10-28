# 24: pandas Area: setup, DataFrames, Reading and writing CSV, Exploring data

**What to build:** The pandas Area is still planned. Students meet pandas in the lab through a notebook that reads a CSV file, looks at it, selects, filters, sorts, adds columns, groups, merges and plots. This ticket opens the Area: it installs pandas, lays out all 11 Topics in their order (most as planned Topics), and writes the first three, **DataFrames**, **Reading and writing CSV** and **Exploring data**. Tickets 25–28 write the rest, one after another.

Decided with the Author (every recommendation accepted):

- **Setup:**
  - `uv add pandas` (pandas 3), add it to `EXAMPLE_LIBRARIES` in `cheatsheet/build.py` so the footer shows its version, commit `uv.lock`, and update the guide's *Libraries* line.
  - Do not add pyarrow, and don't use `dtype_backend="pyarrow"`.
  - Write for pandas 3: text columns have the `str` dtype, and copy-on-write applies.
- **The Area:**
  - Remove `planned: true` from `content/pandas/_area.md`.
  - Rewrite its blurb in both Languages to cover the 11 Topics.
  - Keep hue 260.
- **The Topic order** (11), with these ids and English titles; the Polish titles are the agent's. Choose distinct glyphs per the authoring guide; the suggested ones are in brackets.
  1. `dataframes`: **DataFrames** (`df`). Written here.
  2. `csv-files`: **Reading and writing CSV** (`read_csv`). Written here.
  3. `exploring`: **Exploring data** (`.info()`). Written here.
  4. `selecting`: **Selecting** (`df[ ]`). Ticket 25.
  5. `filtering`: **Filtering** (`mask`). Ticket 25.
  6. `sorting`: **Sorting** (`sort`). Ticket 25.
  7. `columns`: **Changing columns** (`df["new"]`). Ticket 26.
  8. `missing-values`: **Missing values** (`NaN`). Ticket 26.
  9. `grouping`: **Grouping** (`group`). Ticket 27.
  10. `merging`: **Joining tables** (`merge`). Ticket 27.
  11. `pandas-plots`: **Plotting with pandas** (`.plot()`). Ticket 28.

  Topics 4–11 are planned Topic files with a title, glyph and `pl.title`. `selecting` and `grouping` exist already; keep their ids and check their glyphs.
- **DataFrames** (`dataframes`). The Entries, with these English titles:
  - **A DataFrame from a dictionary:** `pd.DataFrame({"name": [...], "score": [...]})`, one key per column.
  - **A column is a Series:** `df["score"]` is a Series with the same index. `type(...)` or the printed column shows it.
  - **Shape, columns and index:** `df.shape`, `df.columns`, `df.index`, and `len(df)`.
  - **Column types:** `df.dtypes`, and `astype` to change one.
  - **Printing a DataFrame:**
    - `print(df)` and `print(df.head(3))`.
    - Say that in Jupyter a bare `df` or `df.head()` on the last line of a cell shows a formatted table instead. The cheat sheet prints, so its Outputs are text.
- **Reading and writing CSV** (`csv-files`). The Entries, with these English titles:
  - **Reading a CSV file:** `pd.read_csv("scores.csv")`. The file is written in a hidden line, and the explanation says what it contains.
  - **Semicolons and decimal commas:** `sep=";"` and `decimal=","`, as in a CSV saved by a Polish Excel.
    - **Pitfall:** without them, everything lands in one column, and you can see it in `df.shape` and `df.columns`.
  - **Reading from a URL:** `pd.read_csv("https://...")` shown with `#| show:`, while a local copy is read in the run code (ADR 0006). Use an example.org-style address, not a real dataset.
  - **Writing with to_csv:** `df.to_csv("out.csv", index=False)`, then read it back.
    - **Pitfall:** without `index=False`, reading it back gives an extra `Unnamed: 0` column.
- **Exploring data** (`exploring`). The Entries, with these English titles:
  - **head and tail:** with and without `n`.
  - **info():** it prints the column types, the non-null counts and the memory use.
    - Check that the Output is stable between runs.
    - If the memory line differs between machines or pandas versions, say so, or use `memory_usage=False`.
  - **describe():** numeric columns, and `describe(include="all")` for text columns too.
  - **Column statistics:** `df["score"].mean()`, `median()`, `std()`, `quantile(0.9)`, `min()`/`max()`. Point out that pandas' `std()` uses `ddof=1`, unlike NumPy's default, and link to the NumPy Entry that covers `ddof` if there is one.
  - **value_counts:** counts per value, and `normalize=True` for proportions.
  - **unique and nunique.**
  - **Correlation with corr():** `df[["height", "weight"]].corr()`. Link to SciPy stats' Correlation if it's written by then; it's planned now, so no link yet.
- **Style for the whole pandas Area** (tickets 25–28 follow it too):
  - `import pandas as pd`, plus `import numpy as np` only where it's used.
  - **Tables are printed:** `print(df)`, `print(df.head())`, `print(df["col"].mean())`. Keep frames small, about 5 columns and 8 rows, so the text table doesn't wrap.
  - **Data:** small made-up tables built inside each example, with a statistics flavour, e.g. students with `name`, `group` (`"A"`/`"B"`), `height` and `score`, or measurements and dice rolls.
  - **Files:** examples that read a file write it first in a `#| hide` line. Writing examples write and read back in plain sight, as in ticket 23.
  - **Random data** (if any) uses the `np.random.*` functions, seeded by a hidden `np.random.seed(n)  #| hide`.
  - **Numbers:** print NumPy and pandas scalars on their own or in f-strings, rounded where needed. Check how pandas 3 prints a scalar inside a list, and avoid that.
  - **Figures** (mostly ticket 28) follow the Matplotlib figure rules.
- **Links:** See-also links to Python Basics' *Files* and NumPy's *Saving and loading* Entries (both ways where natural), and to NumPy Aggregates for column statistics. At most three per Entry. No links into planned Topics.
- **Out of scope for the Area:** dates (`to_datetime`, `.dt`), `read_excel`, `iterrows`, `sample` and maps (folium).

Conventions from tickets 12–23 apply:
- Outputs show values, not English sentences.
- A blank line follows a compound block, so examples paste into the `python` REPL.
- "Polish term (English term)" at first mention, e.g. "ramka danych (DataFrame)", "seria (Series)", "indeks (index)", "separator (delimiter)".

**Blocked by:** none.

**Status:** resolved

- [x] pandas is installed with uv, listed in `EXAMPLE_LIBRARIES`, in the guide's *Libraries* line, and `uv.lock` is committed.
- [x] The pandas Area is no longer planned, has a new blurb in both Languages, and lists the 11 Topics in the decided order. Topics 4–11 are planned files with distinct glyphs and Polish titles.
- [x] DataFrames, Reading and writing CSV, and Exploring data have the decided Entries with their English titles, each with Polish, including the two Pitfalls (one column without `sep=";"`, `Unnamed: 0` without `index=False`).
- [x] Files are written in hidden lines, and the URL Entry uses `#| show:`. Outputs are printed text tables that stay the same on every build.
- [x] Every example runs alone with `uv run python` in an empty folder (with its hidden lines), with no warnings, and pastes into the REPL.
- [x] `uv run cheatsheet build` and `uv run pytest` pass, and the footer shows pandas' version. The Area was looked at on the Map, and the three Topic pages in both Languages, in `uv run cheatsheet serve`.
- [x] The Comments list every Topic and Entry with its Polish title and glyph, plus any decisions made on the way.
- [x] One session and one PR.

## Comments

- **Setup:** `uv add pandas` installed pandas 3.1.0 (no pyarrow). It is in `EXAMPLE_LIBRARIES` after SciPy, so the footer lists it; `tests/test_content_build.py`'s versions test lists it too. The guide's *Libraries* line now names pandas, and its "To add one" hint says `uv add <library>` instead of `uv add pandas`.
- **The Area:** `planned: true` removed, hue 260 kept. Blurb: "Tables of data: DataFrames, CSV files, exploring, selecting, filtering, sorting, changing columns, missing values, grouping, joining and plotting." / "Dane w tabelach: ramki danych (DataFrames), pliki CSV, przeglądanie, wybieranie, filtrowanie, sortowanie, zmiana kolumn, brakujące wartości, grupowanie, łączenie i wykresy."
- **Topics** (English / Polish, glyph), in the Topic order:
  1. `dataframes`: *DataFrames* / *Ramki danych*, `df`. Summary: "Tables with named columns: building one from a dictionary, columns as Series, shape, column types and printing." / "Ramki danych (DataFrames), czyli tabele z nazwanymi kolumnami: tworzenie ze słownika, kolumny jako serie, kształt, typy kolumn i wypisywanie."
  2. `csv-files`: *Reading and writing CSV* / *Odczyt i zapis CSV*, `.csv`. Summary: "CSV files as DataFrames: reading, semicolons and decimal commas, reading from a URL, and writing with to_csv." / "Pliki CSV jako ramki danych (DataFrames): odczyt, średniki i przecinki dziesiętne, odczyt z adresu URL oraz zapis przez to_csv."
  3. `exploring`: *Exploring data* / *Przeglądanie danych*, `.info`. Summary: "A first look at a table: head and tail, info, describe, column statistics, counts, distinct values and correlation." / "Pierwsze spojrzenie na ramkę danych (DataFrame): head i tail, info, describe, statystyki kolumn, zliczenia, różne wartości i korelacja."
  4. `selecting`: *Selecting* / *Wybieranie*, `df[ ]` (planned, existing file kept)
  5. `filtering`: *Filtering* / *Filtrowanie*, `mask` (planned)
  6. `sorting`: *Sorting* / *Sortowanie*, `sort` (planned)
  7. `columns`: *Changing columns* / *Zmiana kolumn*, `df[]=` (planned)
  8. `missing-values`: *Missing values* / *Brakujące wartości*, `NaN` (planned)
  9. `grouping`: *Grouping* / *Grupowanie*, `group` (planned, existing file kept)
  10. `merging`: *Joining tables* / *Łączenie tabel*, `merge` (planned)
  11. `pandas-plots`: *Plotting with pandas* / *Wykresy z pandas*, `.plot` (planned)
- **Entries** (English / Polish):
  - DataFrames:
    - *A DataFrame from a dictionary* / *Ramka danych ze słownika*
    - *A column is a Series* / *Kolumna to seria*
    - *Shape, columns and index* / *Kształt, kolumny i indeks*
    - *Column types* / *Typy kolumn*, with a Pitfall: `df["score"].astype("float64")` on its own line leaves `df` unchanged (added by me, not in the ticket; it is the copy-on-write habit the later Topics rely on)
    - *Printing a DataFrame* / *Wypisywanie ramki danych*
  - Reading and writing CSV:
    - *Reading a CSV file* / *Odczyt pliku CSV*
    - *Semicolons and decimal commas* / *Średniki i przecinki dziesiętne*, with the one-column Pitfall (`(3, 1)` and `Index(['name;height;score'], dtype='str')`)
    - *Reading from a URL* / *Odczyt z adresu URL*
    - *Writing with to_csv* / *Zapis przez to_csv*, with the `Unnamed: 0` Pitfall
  - Exploring data:
    - *head and tail* / *head i tail*
    - *info()* / *info()*
    - *describe()* / *describe()*
    - *Column statistics* / *Statystyki kolumn*
    - *value_counts* / *value_counts*
    - *unique and nunique* / *unique i nunique*
    - *Correlation with corr()* / *Korelacja z corr()*
- **Links:** *Reading a CSV file* ↔ Files' *CSV files with the csv module* and NumPy Saving and loading's *CSV files* (both ways). *Writing with to_csv* → Files' *Writing a text file* and *Text files with savetxt and loadtxt*. *Column statistics* → NumPy Aggregates' *Sum, mean, min and max*, *Standard deviation and variance* (the `ddof` Entry) and *Median and percentiles*; *describe()* → *Median and percentiles*. Also: *A DataFrame from a dictionary* → Dictionaries' *Creating and accessing*; *Shape, columns and index* and *Column types* → Arrays' *Shape and dtype*; *Printing a DataFrame* → *head and tail*; *head and tail* → *Printing a DataFrame* and *Reading a CSV file*; *info()* → *Column types*; *value_counts* → collections' *Counting with Counter* and Aggregates' *Counting and proportions with a mask*; *unique and nunique* → Sets' *Unique values*; *Correlation with corr()* → Heatmaps' *Colour maps and fixed limits* (the correlation-matrix heatmap). No links into planned Topics: SciPy stats' Correlation and pandas' Selecting (for `df[["height", "weight"]]`) and Missing values get theirs when written.
- Decisions:
  - **Glyphs at most five characters.** The guide allows one to five characters and every existing glyph keeps to that, so four suggested glyphs were shortened: `read_csv` → `.csv` (like NumPy's `.npy`), `.info()` → `.info`, `df["new"]` → `df[]=` (assigning a column), `.plot()` → `.plot`.
  - **Exploring data reads one file.** Its eight-row table would take 10+ lines to build inline, so every Exploring Entry writes the same `students.csv` (name, group, height, weight, score; 8 rows, groups A×5 and B×3, one repeated score) in a hidden line and reads it with `pd.read_csv`, as in the lab. *head and tail* says what the file holds. The DataFrames and CSV-writing Entries build their small tables inline.
  - **`info()` keeps the memory line.** On this machine it is `memory usage: 452.0 bytes`, the same on every build; the explanation says it can differ between computers and pandas versions, rather than hiding it with `memory_usage=False`, since Students see it in the lab. `df.info()` prints by itself, and the explanation says so.
  - **`unique()` on a numeric column.** In pandas 3 `df["group"].unique()` prints a `<StringArray>` with a `Length: 2, dtype: str` footer, so the Entry prints the unique scores (a plain NumPy array) and counts groups with `nunique()`.
  - **Scalars** are printed on their own, side by side in one `print`, or in f-strings (`.std()` to 3 places, `.quantile(0.9)` to 1). In pandas 3, `[df["score"].mean()]` prints `[np.float64(79.0)]`, so no scalar is printed inside a list.
  - **Reading from a URL** shows `url = "https://example.org/scores.csv"` and `df = pd.read_csv(url)`; the run code reads a local `scores.csv` written in a hidden line. The `url` line runs too (unused), which keeps the shown `read_csv` line short.
  - **Line length:** shown code keeps to 43 characters; the `pd.read_csv(..., sep=";", decimal=",")` call is wrapped. Hidden lines are longer.
  - **`describe()` is rounded.** Unrounded, `describe(include="all")` on five columns is 56 characters wide and scrolls sideways in the Output box at 1280 px, so both calls end in `.round(2)` (40 characters), and the explanation says why.
- All 19 examples (16 Entries and 3 Pitfalls) were run alone with `uv run python -W default` in their own empty folders, with their hidden lines: no warnings, and the build's Outputs match those runs. Each was also pasted into `code.InteractiveConsole` after its hidden lines: no `SyntaxError`. (Pasted into the REPL, the *Column types* Pitfall's bare `df["score"].astype("float64")` echoes the float column; in Jupyter it shows nothing, since it isn't the last line.)
- `uv run cheatsheet build` and `uv run pytest` (248 tests) pass, run one after the other. The site was checked with a Playwright script through `uv run python`: the pandas island shows the three written Topics and eight dashed planned ones; the three pages read well in English and Polish with no hidden line or `#|` shown, no console errors, and the footer shows pandas 3.1.0. On the Trail, DataFrames follows NumPy's Saving and loading, and Exploring data's Next stop skips the planned Topics to Matplotlib's Plotting basics.
