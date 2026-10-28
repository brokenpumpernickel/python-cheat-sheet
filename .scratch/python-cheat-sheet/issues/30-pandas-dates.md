# 30: pandas Dates Topic (to_datetime and the .dt accessor)

**What to build:** Lab data often has dates, such as sighting dates or measurement days, and pandas reads them as text. A new Topic, **Dates**, covers turning text into dates, reading dates from a CSV file, the `.dt` accessor, time between dates, filtering by date, and grouping by month or year.

Decided with the Author (every recommendation accepted). The English titles are decided; the Polish titles are the agent's.

- **Where:**
  - `dates`, **Dates** (*Daty*, glyph `.dt`), after Text columns and before Missing values.
  - The stubs PR (#41) already adds it to the Area's Topic order as a planned Topic and updates the Area blurb. Remove `planned: true` and add both summaries.
- **Entries:**
  - **Text to dates:**
    - `pd.to_datetime(df["date"])` for ISO dates (`"2026-10-28"`), and the dtype it gives.
    - Polish dates `"28.10.2026"` with `format="%d.%m.%Y"` (or `dayfirst=True`).
    - `errors="coerce"` turns what it can't read into `NaT`.
  - **Dates from a CSV file:** `pd.read_csv(..., parse_dates=["date"])`, with the file written in a hidden line.
  - **Parts of a date:**
    - `.dt.year`, `.dt.month`, `.dt.day` and `.dt.dayofweek` (0 is Monday).
    - Mention that `.dt.day_name()` gives English names. Don't rely on system locales.
    - **Pitfall:** `.dt` on a column that is still text raises `AttributeError` (`raises=AttributeError`).
  - **Time between dates:** subtracting two dates gives a Timedelta; `.dt.days` gives whole days. Add a `pd.Timedelta(days=7)` to a date.
  - **Filtering by date:** `df[df["date"] >= "2024-03-01"]` compares with a date written as text, and `.between("2024-03-01", "2024-03-31")` covers a range.
  - **Grouping by month or year:**
    - `df.groupby(df["date"].dt.year).size()`.
    - `df.groupby(df["date"].dt.to_period("M"))["value"].mean()`.
    - Leave out `resample`, which needs a date index.
- **Style:** as ticket 24 decided for the pandas Area: printed small made-up tables built inside each example, `import pandas as pd`. Avoid the current date (`pd.Timestamp.now()`, `today`), since the Output must stay the same on every build.
- **Links:**
  - Reading and writing CSV's *Reading a CSV file*, Changing columns' *Text to numbers* (the same idea for numbers), and Missing values (`NaT`).
  - Grouping's *Group sizes* and *A column's mean per group*.
  - Plotting with pandas' *A line plot of a Series*, for a plot over time.
  - At most three per Entry.

**Running in parallel** with tickets 29 (Text columns) and 31 (NumPy arrays and plotting with plt). Each runs in its own session and PR.
- Your worktree starts from the stubs branch `content/pandas-text-and-dates-stubs` (PR #41), so the planned Topic is already there. Open your PR against `main`. Until #41 is merged, your PR also shows its commit.
- Edit only `dates.md`. Back-links into other Topics: at most two, and not in `columns.md`, `filtering.md`, `dataframes.md` or `pandas-plots.md`, which the other tickets edit.
- `text-columns` is still planned, so don't link to it. List any link you'd add under **Links to add later** in the Comments.
- If `main` moves and your PR conflicts, bring your branch up to date with `main` and resolve it. Check that the PR is still OPEN before every push.

Conventions from tickets 12–24 apply:
- Outputs show values, not English sentences.
- A blank line follows a compound block.
- "Polish term (English term)" at first mention, e.g. "data (date)", "akcesor .dt (.dt accessor)", "różnica czasu (Timedelta)".

**Blocked by:** none (it starts from #41's branch).

**Status:** resolved

- [x] Dates is written (no longer planned), with a summary in both Languages, and the six decided Entries with their English titles and Polish, including the `.dt`-on-text Pitfall.
- [x] Polish `dd.mm.yyyy` dates are covered, and no example depends on the current date.
- [x] Every example runs alone with `uv run python` in an empty folder, with no warnings, and pastes into the REPL.
- [x] `uv run cheatsheet build` and `uv run pytest` pass. The page was looked at in both Languages in `uv run cheatsheet serve`.
- [x] The Comments list every Entry with its Polish title, plus any decisions made on the way and any Links to add later.
- [x] One session and one PR.

## Comments

- **The Topic:** `planned: true` removed; glyph `.dt` kept. Summary: "Date columns: text to dates, dates from a CSV file, parts of a date with .dt, time between dates, filtering by date, and grouping by month or year." / "Kolumny z datami (dates): tekst na daty, daty z pliku CSV, części daty przez akcesor .dt (.dt accessor), czas między datami, filtrowanie po dacie oraz grupowanie po miesiącu lub roku."
- **Entries** (English / Polish):
  - *Text to dates* / *Tekst na daty*: one table with an ISO column (`pd.to_datetime`), a Polish `dd.mm.yyyy` column (`format="%d.%m.%Y"`, with `dayfirst=True` in the explanation) and a column with `"unknown"` (`errors="coerce"` → `NaT`), then `df.dtypes`.
  - *Dates from a CSV file* / *Daty z pliku CSV*: `sightings.csv` (`date,shape`, three rows) written in a hidden line; the dtypes without `parse_dates` (both `str`), then `pd.read_csv(..., parse_dates=["date"])` and its dtypes. `date_format="%d.%m.%Y"` for Polish dates is in the explanation.
  - *Parts of a date* / *Części daty*: `.dt.year`, `.dt.month`, `.dt.day` and `.dt.day_of_week` as new columns, then `.dt.day_name()`. Pitfall: `.dt.year` on a text column, `raises=AttributeError` (`Can only use .dt accessor with datetimelike values`).
  - *Time between dates* / *Czas między datami*: `df["end"] - df["start"]` (a `timedelta64` column) and `.dt.days` in the table, then `df["end"] + pd.Timedelta(days=7)` printed on its own, so the Output stays narrow enough for the card.
  - *Filtering by date* / *Filtrowanie po dacie*: `df[df["date"] >= "2024-03-01"]`, then `.between("2024-03-01", "2024-03-31")`, with a row on 31 March to show that both ends count.
  - *Grouping by month or year* / *Grupowanie po miesiącu lub roku*: `df.groupby(df["date"].dt.year).size()` and `df.groupby(df["date"].dt.to_period("M"))["minutes"].mean()`. No `resample`.
- **Links:** *Text to dates* → Changing columns' *Text to numbers* and Missing values' *Finding missing values* (for `NaT`). *Dates from a CSV file* → Reading and writing CSV's *Reading a CSV file* and *Semicolons and decimal commas*. *Parts of a date* → DataFrames' *Column types*. *Time between dates* → Changing columns' *A column from other columns*. *Filtering by date* → Filtering's *A boolean mask* and *Combining conditions*. *Grouping by month or year* → Grouping's *Group sizes* and *A column's mean per group*, and Plotting with pandas' *A line plot of a Series*. Back-links, both in `csv-files.md`: *Reading a CSV file* → *Dates from a CSV file* (now 3 links), and *Semicolons and decimal commas* → *Text to dates* (its first link: a Polish Excel CSV writes dates as `28.10.2026` too).
- Decisions:
  - **`.dt.day_of_week`, not `.dt.dayofweek`.** In pandas 3.1, `.dt.dayofweek` raises `Pandas4Warning: Series.dt.dayofweek is deprecated … Use Series.dt.day_of_week instead`, which breaks the no-warnings rule, so the Entry uses `day_of_week` (same values, 0 is Monday).
  - **Why `format=` matters.** Without it, pandas 3 guesses month first from the first value, so a lone `"04.03.2026"` silently becomes 3 April. The explanation says so in one clause instead of adding a second Pitfall the ticket didn't decide.
  - **`day_name()` and locales.** The explanation says it gives English names and that its `locale=` depends on what the computer has installed, so the Entry doesn't use it.
  - **No current date.** Every date is a fixed literal; there is no `now()`, `today` or `Timestamp.now()`. pandas 3 prints the dtype as `datetime64[us]` (not `[ns]`), and text columns as `str`; the explanations say `datetime64` and don't name the unit.
  - **Data.** Small tables built in each example; the sightings theme (`shape`, `minutes`) matches Grouping and Plotting with pandas. The only file is the hidden `sightings.csv` in *Dates from a CSV file*.
  - **Polish terms.** "daty (dates)" in the summary and at the first mention per Entry where dates are the concept, "akcesor .dt (.dt accessor)", "różnica czasu (Timedelta)", "brakująca data (missing value)" for `NaT`, "grupuje (grouping)".
- All 7 examples (6 Entries and 1 Pitfall) were run alone with `uv run python -W default` in their own empty folders: no warnings, and the Pitfall's only stderr is its expected `AttributeError`. Each shown code was also pasted into `code.InteractiveConsole` after its hidden lines: no `SyntaxError`.

### Links to add later

- `dates/text-to-dates → text-columns/cleaning-text`: dates often need `.str.strip()` before `pd.to_datetime`.
- `dates/parts-of-a-date → text-columns/the-str-accessor`: `.dt` is the date twin of `.str`, and both Pitfalls are the same `AttributeError` on the wrong kind of column. Back, where natural: `text-columns/the-str-accessor → dates/parts-of-a-date`.
- `dates/grouping-by-month-or-year → pandas-plots/plotting-columns-with-plt`, for `plt.plot(df["date"], ...)` over time, replacing `pandas-plots/a-line-plot-of-a-series` if the Author prefers it, to stay at three links.
- For the cross-link pass: Grouping's *A column's mean per group* has the id `grouping/a-column-s-mean-per-group` (the apostrophe becomes a `-`), not `a-columns-mean-per-group` as ticket 28's Links to add later writes it.
- The page was checked in both Languages (Playwright screenshots of `site/dist`, EN and `?lang=pl`). Two code cards were too wide at first, the `shape` list in *Filtering by date* and a fifth `next` column in *Time between dates*: the list now wraps, and the shifted dates print on their own. Every shown line is at most 44 characters, like the rest of the Area.
