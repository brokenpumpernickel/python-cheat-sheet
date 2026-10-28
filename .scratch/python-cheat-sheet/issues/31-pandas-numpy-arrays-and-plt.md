# 31: pandas columns as NumPy arrays, and plotting columns with plt

**What to build:** Nothing in the cheat sheet shows that a pandas column can become a NumPy array (`.to_numpy()`, `.values`). Nor does it show that you can pass columns straight to `plt.plot`, `plt.scatter` and `plt.hist`. Students who know Matplotlib often find that simpler than pandas' `.plot()`. This ticket adds an Entry on arrays to DataFrames, and two Entries to Plotting with pandas.

Decided with the Author (every recommendation accepted). The English titles are decided; the Polish titles are the agent's.

- **DataFrames** (`dataframes`). A new Entry, **Columns as NumPy arrays**, placed after *A column is a Series*:
  - `df["score"].to_numpy()` gives a 1-D array, and `df[["height", "weight"]].to_numpy()` a 2-D array, one row per row of the table.
  - `.values` is the older way and still works, but `.to_numpy()` is the recommended one.
  - Use the array with a NumPy function, e.g. `np.percentile` or `np.std`. Note the ddof difference from pandas' `std()`, if *Column statistics* doesn't already cover it.
  - **Pitfall:** `.to_numpy()` on a table that includes a text column gives an `object` array, and maths on it fails or gives nonsense. Show the dtype and a failing or odd operation, and use `raises=` if it raises.
- **Plotting with pandas** (`pandas-plots`). Two new Entries, as the Topic's first Entries:
  - **Plotting columns with plt:**
    - `plt.plot(df["year"], df["n"])`, `plt.scatter(df["height"], df["weight"])`, `plt.hist(df["score"], bins=...)`.
    - Series work as they are, and `.to_numpy()` gives plain arrays.
    - Say that this is often simpler than `.plot()` when you already know Matplotlib. `.plot()`, as the next Entries show, is a shortcut that labels the axes from the column names.
    - One figure: choose one of the three, or `plt.subplot(121)`/`(122)` for two, per the figure rules.
  - **A column against a distribution:**
    - `plt.hist(df["score"], bins=..., density=True)` with a `stats.norm(m, s).pdf(x)` curve on top. `m` and `s` come from the column's `mean()` and `std()`, and `x = np.linspace(...)` covers the data's range, not the sample itself.
    - Link to Plotting distributions' *A histogram with the pdf*, which explains the `x` grid.
  - Update the Topic summary in both Languages to cover both ways: plain `plt` with columns, and `.plot()`.
- **Figures** follow the Matplotlib rules in the guide:
  - One figure per Entry, `figsize=(6, 3.5)`, `plt.show()` at the end.
  - Language-neutral text in figures, and a figure description in both Languages.
  - Random data from seeded `np.random.*` functions in hidden lines.
- **Style:** as ticket 24 decided for the pandas Area: printed small made-up tables, or seeded random ones for the plots.
- **Links:**
  - NumPy Arrays and Aggregates, Matplotlib *Plotting basics*, *Scatter plots* and *Histograms*, and SciPy stats Plotting distributions.
  - Between the new Entries and Plotting with pandas' existing ones.
  - At most three per Entry.

**Running in parallel** with tickets 29 (Text columns) and 30 (Dates). Each runs in its own session and PR.
- Your worktree starts from the stubs branch `content/pandas-text-and-dates-stubs` (PR #41). Open your PR against `main`. Until #41 is merged, your PR also shows its commit.
- Edit only `dataframes.md` and `pandas-plots.md`, plus at most two back-links elsewhere, not in `columns.md`, `filtering.md`, `text-columns.md` or `dates.md`.
- `text-columns` and `dates` are still planned, so don't link to them. List any link you'd add under **Links to add later** in the Comments.
- If `main` moves and your PR conflicts, bring your branch up to date with `main` and resolve it. Check that the PR is still OPEN before every push.

Conventions from tickets 12–24 apply:
- Outputs show values, not English sentences.
- A blank line follows a compound block.
- "Polish term (English term)" at first mention, e.g. "tablica NumPy (NumPy array)".

**Blocked by:** none (it starts from #41's branch).

**Status:** resolved

- [x] DataFrames has *Columns as NumPy arrays* with its Pitfall, and Plotting with pandas starts with *Plotting columns with plt* and *A column against a distribution*, all with Polish.
- [x] Plotting with pandas' summary covers both ways, in both Languages.
- [x] Every figure follows the figure rules and has a figure description in both Languages.
- [x] Every example runs alone with `MPLBACKEND=Agg uv run python` in an empty folder, with no warnings other than the expected non-interactive one, and pastes into the REPL.
- [x] `uv run cheatsheet build` and `uv run pytest` pass. Both pages were looked at in both Languages in `uv run cheatsheet serve`.
- [x] The Comments list every Entry with its Polish title, plus any decisions made on the way and any Links to add later.
- [x] One session and one PR.

## Comments

Resolved in PR brokenpumpernickel/python-cheat-sheet#43 (https://github.com/brokenpumpernickel/python-cheat-sheet/pull/43). Three Entries, with all their Polish:

- **DataFrames**: *Columns as NumPy arrays* (PL: *Kolumny jako tablice NumPy*), right after *A column is a Series*. It prints a 1-D array, a 2-D array, `np.percentile` and `np.std(..., ddof=1)` beside pandas' `.std()`, and has a Pitfall. Its Pitfall shows `df.to_numpy()` on a table with a name column: it prints the dtype `object`, then `a.sum(axis=0)` as `['AlaJanEwa' 247]`, then `a.mean(axis=0)` raises `TypeError` (`raises=TypeError`). See also: `arrays/two-dimensional-arrays`, `aggregates/median-and-percentiles`, `exploring/column-statistics`.
- **Plotting with pandas**: *Plotting columns with plt* (PL: *Wykresy kolumn przez plt*), the first Entry. One figure with `plt.subplot(121)`: `plt.scatter` of height against weight (axes `cm`, `kg`), and `(122)`: `plt.hist` of the scores. See also: `plotting-basics/a-line-plot`, `scatter-plots/a-scatter-plot`, `histograms/a-histogram`.
- **Plotting with pandas**: *A column against a distribution* (PL: *Kolumna na tle rozkładu*), the second Entry. `plt.hist(..., density=True)` of the heights, with `stats.norm(m, s).pdf(x)` over it, where `x = np.linspace(min, max, 200)`. See also: `plotting-distributions/a-histogram-with-the-pdf`, `histograms/density-with-a-pdf-on-top`, `exploring/column-statistics`.

Decisions made on the way:

- Both plotting Entries reuse the hidden `students.csv` lines (seed 7, 200 rows) of *A scatter plot of two columns* and *A histogram of a column*, so the page's data stays consistent.
- *A column against a distribution* fits the **height** column, not `score` as the ticket's sketch had it. The scores are whole numbers clipped at 100, so 20 bins over them come out jagged and a normal fit looks worse. Heights have one decimal and are close to normal.
- *Column statistics* already explains pandas' `ddof=1` against NumPy's `ddof=0`. So the new Entry states it in one clause, prints the two matching values and links there.
- The Pitfall shows both outcomes: a nonsense result without complaint (`sum`) and the `TypeError` (`mean`), with the raising line last.
- The DataFrames summary now says "columns as Series and NumPy arrays" in both Languages, to match the new Entry. The ticket only asked for the Plotting with pandas summary, but the old one would leave out the new Entry.
- Plotting with pandas' summary now reads: "Plots from a Series or DataFrame two ways, columns passed to plt or pandas' .plot(): …", in both Languages.
- Links between the new and existing Entries: *Pandas plots are Matplotlib plots* now links back to `pandas-plots/plotting-columns-with-plt` (its third link). The new Entries' explanations already point to "the next Entries".
- Two back-links elsewhere, as the ticket allows: `arrays/creating-arrays` → `dataframes/columns-as-numpy-arrays`, and `plotting-distributions/a-histogram-with-the-pdf` → `pandas-plots/a-column-against-a-distribution`.

**Links to add later**, once tickets 29 and 30 merge (the targets don't exist yet):

- `dataframes/columns-as-numpy-arrays` → the Text columns Entry on text to numbers (if it covers `pd.to_numeric`), as the fix for the Pitfall's `object` column. This would replace `arrays/two-dimensional-arrays` to keep three links.
- `pandas-plots/plotting-columns-with-plt` → the Dates Entry on plotting against dates, if ticket 30 writes one (`plt.plot(df["date"], df["n"])` works with a datetime column).

Checks:

- Every example ran alone with `MPLBACKEND=Agg` and `-W default` in an empty folder, with no warnings, and was pasted line by line into `code.InteractiveConsole`.
- `uv run cheatsheet build` passed, then `uv run pytest` (248 passed).
- Both pages and their three figures were looked at in both Languages in Playwright screenshots of the built site. No console errors, no markers or hidden lines shown, and the figure descriptions are read out in each Language.
