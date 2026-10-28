# 28: pandas Plotting with pandas Topic

**What to build:** The last pandas Topic that ticket 24 left planned, **Plotting with pandas**. It covers `.plot()` on a Series or DataFrame: line plots of grouped counts, bar charts of counts, scatter plots of two columns and histograms, labelled with `plt` as in the lab notebook.

Decided with the Author (every recommendation accepted). The English titles are decided; the Polish titles are the agent's.

- **Plotting with pandas** (`pandas-plots`). The Entries:
  - **A line plot of a Series:**
    - `df.groupby("year").size().plot()`. The index becomes the x axis.
    - Then `plt.xlabel`, `plt.ylabel` and `plt.grid(ls="--")`, as in the notebook.
  - **Bar charts of counts:**
    - `df["shape"].value_counts().plot(kind="bar")`.
    - A sorted bar chart of a per-group mean: `groupby(...).mean().sort_values().plot(kind="bar")`.
  - **A scatter plot of two columns:** `df.plot(kind="scatter", x="height", y="weight")`.
  - **A histogram of a column:** `df["score"].plot(kind="hist", bins=20)`, and `df.hist()` for every numeric column. If `df.hist()` makes its own figure, find a way that keeps the one-figure, one-size rule (`figsize=(6, 3.5)`).
  - **Pandas plots are Matplotlib plots:**
    - `.plot()` draws on the current Matplotlib figure, so `plt.figure(figsize=(6, 3.5))` before it and `plt.title`, `plt.xlabel` and `plt.show()` after it work as usual.
    - Also mention `.plot(ax=ax)` for a plot from `plt.subplots`, with `figsize=(6, 3.5)`.
  - Where it fits, as a Pitfall:
    - `.plot()` without `plt.figure` reuses the open figure in a script.
    - Or `kind="bar"` on unsorted counts.
    - Choose one that shows a real, visible problem, or none.
- **Figures** follow the Matplotlib rules in the guide:
  - One figure per Entry, `figsize=(6, 3.5)`, `plt.show()` at the end.
  - Language-neutral text in figures. Pandas puts column names on the axes and in legends, so name the columns with symbols, letters or short neutral names, or set the labels yourself.
  - A figure description in both Languages.
  - Random data from seeded `np.random.*` functions in hidden lines.
- **Style:** as ticket 24 decided for the pandas Area.
- **Links:**
  - The Matplotlib Topics: *Plotting basics*, *Bar charts*, *Scatter plots*, *Histograms* and *Subplots*' *A grid of plots with plt.subplots*.
  - Ticket 24's *value_counts*, and ticket 27's *Group sizes* (parallel: list it under Links to add later).
  - Back from Matplotlib's *Bar charts* and *Histograms* where natural.
  - At most three per Entry.

Conventions from tickets 12–24 apply:
- Outputs show values, not English sentences.
- A blank line follows a compound block.
- "Polish term (English term)" at first mention.

**Running in parallel:** tickets 25–28 run at the same time, each in its own session and PR, all starting from `main` after ticket 24.
- **Edit only your own Topic files.** Make back-links (a See-also added to an Entry outside your Topics) only where the ticket asks for them, and keep them few. Two PRs editing the same Entry would conflict.
- **Link only to Entries that are on `main` or in your own Topics.** The other parallel tickets' Topics are still planned on `main`, and a link into a planned Topic fails the build.
- **List the links you'd add into the other parallel tickets' Topics** under a **Links to add later** heading in the Comments, as `your-topic/entry → other-topic/entry`. They're added in one pass after all four PRs are merged.
- **If `main` moves:** If another of these PRs is merged first and yours then conflicts, bring your branch up to date with `main` and resolve it. Don't push to a merged PR's branch.

**Blocked by:** 24 (resolved, PR #35).

**Status:** resolved

- [x] Plotting with pandas is written (no longer planned), with a summary in both Languages, and the decided Entries with their English titles and Polish.
- [x] Every figure follows the figure rules and has a figure description in both Languages, with no English words in the figures.
- [x] Every example runs alone with `MPLBACKEND=Agg uv run python` in an empty folder, with no warnings other than the expected non-interactive one, and pastes into the REPL.
- [x] `uv run cheatsheet build` and `uv run pytest` pass. The page was looked at in both Languages in `uv run cheatsheet serve`.
- [x] The Comments list every Entry with its Polish title, plus any decisions made on the way.
- [x] One session and one PR.

## Comments

- Resolved by PR #39: https://github.com/brokenpumpernickel/python-cheat-sheet/pull/39.
- **The Topic:** `planned: true` removed; glyph `.plot` kept. Summary: "Plots straight from a Series or DataFrame with .plot(): line plots, bar charts of counts, scatter plots, histograms, and how they fit with plt." / "Wykresy prosto z serii (Series) i ramki danych (DataFrame) przez .plot(): liniowe, słupkowe z liczebnościami, punktowe, histogramy i współpraca z plt."
- **Entries** (English / Polish):
  - *A line plot of a Series* / *Wykres liniowy serii*: `df.groupby("year").size().plot()`, then `plt.xlabel("t")`, `plt.ylabel("n")` and `plt.grid(ls="--")`.
  - *Bar charts of counts* / *Wykresy słupkowe liczebności*: `value_counts().plot(kind="bar")` on the left and `groupby("shape")["minutes"].mean().sort_values().plot(kind="bar")` on the right, in one figure with `plt.subplot(121)` and `plt.subplot(122)`.
  - *A scatter plot of two columns* / *Wykres punktowy dwóch kolumn*: `df.plot(kind="scatter", x="height", y="weight", figsize=(6, 3.5))`.
  - *A histogram of a column* / *Histogram kolumny*: `df["score"].plot(kind="hist", bins=20)`; `df.hist(bins=20, figsize=(6, 3.5))` is in the explanation. Pitfall: `plt.figure(figsize=(6, 3.5))` before `df.hist()`.
  - *Pandas plots are Matplotlib plots* / *Wykresy pandas to wykresy Matplotlib*: `df.plot(ax=ax)` on a plot from `plt.subplots(figsize=(6, 3.5))`, with `ax.axhline` and `ax.set_xlabel` added to it.
- **Links:** *A line plot of a Series* → Plotting basics' *A line plot* and *Axis limits and a grid*. *Bar charts of counts* → Exploring's *value_counts*, Bar charts' *Bar chart of counts* and Subplots' *Side-by-side plots with plt.subplot(121)*. *A scatter plot of two columns* → Scatter plots' *A scatter plot* and Exploring's *Correlation with corr()*. *A histogram of a column* → Histograms' *A histogram* and *Choosing bins*. *Pandas plots are Matplotlib plots* → Subplots' *A grid of plots with plt.subplots* and Plotting basics' *Axis labels and a title*. Back-links: Bar charts' *Bar chart of counts* → *Bar charts of counts*, and Histograms' *A histogram* → *A histogram of a column* (each now has 2 and 3 links).
- Decisions:
  - **Only a Series' `.plot()` draws on the current figure.** In pandas 3.1, `Series.plot()` reuses the open figure, but `DataFrame.plot()` and `df.hist()` always start a new one unless given `ax=`. So `plt.figure(figsize=(6, 3.5))` works before a Series' `.plot()` (Entries 1, 2 and 4), while the scatter plot passes `figsize=(6, 3.5)` to `df.plot` itself, and *Pandas plots are Matplotlib plots* says both halves and shows `df.plot(ax=ax)`. This is the "find a way" for `df.hist()` too: `df.hist(bins=20, figsize=(6, 3.5))`.
  - **The Pitfall** is neither suggested one: `.plot()` reusing the open figure in a script behaves exactly like `plt.plot` and doesn't happen in Jupyter, and `value_counts()` is already sorted, so neither shows a real problem. Instead, *A histogram of a column* has `plt.figure(figsize=(6, 3.5))` before `df.hist()`: the figure stays empty and the histograms come out at the default 6.4 × 4.8 inches. Like Jupyter's inline backend, the build shows no image for the empty figure (Jupyter prints `<Figure size 600x350 with 0 Axes>`, which the Pitfall text quotes), so the visible problem on the page is one figure taller than the rest. Its description says so.
  - **One figure for two bar charts.** *Bar charts of counts* has two decided charts, so they share one 6 × 3.5 figure through `plt.subplot(121)` / `plt.subplot(122)`; a Series' `.plot()` draws on the current subplot. The histogram Entry draws only the one-column histogram and names `df.hist()` in the explanation; `df.hist()` is drawn by the Pitfall.
  - **Language-neutral figures.** The code keeps real column names (`year`, `shape`, `minutes`, `height`, `weight`, `score`), and the labels pandas makes from them are replaced: `plt.xlabel("t")` / `plt.ylabel("n")` on the line plot, units (`cm`, `kg`) on the scatter plot, `plt.ylabel("n")` over pandas' `Frequency` on the histogram, and `plt.xlabel("")` under the bars, where pandas writes the index name `shape`. The shapes are the symbols ○ □ △ ◇, with `rot=0` so they stay upright (pandas turns bar labels 90° by default). `df.hist()` titles each plot with its column name, so the Pitfall and the last Entry build small tables with columns `A` and `B`.
  - **Data.** As in Exploring data, the Entries read a CSV written in hidden lines: `sightings.csv` (400 rows: `year` 2014–2024 with ever more sightings per year, `shape`, `minutes`) for Entries 1–2, and a 200-row `students.csv` (`height`, `weight`, `score`) for Entries 3–4. The hidden lines make the data with `np.random.*` after a hidden seed, so `import numpy as np` is hidden too where nothing shown uses it. The Pitfall and the last Entry build their random tables in the shown code.
  - **Title length.** *Pandas plots are Matplotlib plots* is five words, one over the guide's four; kept, since the English titles were decided.
- All 6 examples (5 Entries and 1 Pitfall) were run alone with `MPLBACKEND=Agg uv run python -W default` in their own empty folders: the only warning is the expected `FigureCanvasAgg is non-interactive`. Each figure is 6 × 3.5 inches except the Pitfall's default-size one. Each shown code was also pasted into `code.InteractiveConsole` after its hidden lines: no errors.

### Links to add later

- `pandas-plots/a-line-plot-of-a-series → grouping/group-sizes`
- `pandas-plots/bar-charts-of-counts → grouping/a-columns-mean-per-group`, replacing `subplots/side-by-side-plots-with-plt-subplot-121` to stay at three links
- `pandas-plots/bar-charts-of-counts → sorting/sort-values`, if the Author prefers it to `bar-charts/bar-chart-of-counts`
- Back, where natural: `grouping/group-sizes → pandas-plots/a-line-plot-of-a-series`
