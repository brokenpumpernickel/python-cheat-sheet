# 16: Matplotlib Area: line plots, histograms, bar charts, scatter plots, heatmaps and subplots

**What to build:** The Matplotlib Area stops being planned and gets real content: the plots a Student draws in a statistics lab, from a first line plot to a grid of plots. It is the first Area full of figures. Decided with the Author:

- **Plotting style:** examples use the `plt` style Students already know (`plt.plot`, `plt.xlabel`, `plt.title`, `plt.legend`, …). The Subplots Topic shows the pyplot `plt.subplot(121)` convention first ("For subplots, show them plt.subplot(121) convention first", the Author). Only after that does it introduce `fig, axes = plt.subplots(...)`, because grids need it, with a Pitfall that maps `plt.xlabel` to `ax.set_xlabel` and the like.
- **Topics,** in this Topic order. The Area keeps hue 25 and its planned Topics `plotting-basics`, `scatter-plots` and `subplots`, and gains `histograms` (*Histogramy*), `bar-charts` (*Wykresy słupkowe*) and `heatmaps` (*Mapy ciepła*), with glyphs chosen per the authoring guide:
  1. Plotting basics
  2. Histograms
  3. Bar charts
  4. Scatter plots
  5. Heatmaps
  6. Subplots
- **Entries** (about 24), with these English titles; the Polish titles are the agent's:
  - **Plotting basics:**
    - A line plot
    - Axis labels and a title
    - Several lines and a legend
    - Colours, markers and line styles
    - Axis limits and a grid
    - Horizontal and vertical lines: `plt.axhline` / `plt.axvline` spanning the whole plot, e.g. a threshold or the mean. The Author asked for this one specifically.
    - Saving a figure, with a Pitfall: in a script, call `savefig` before `show`, or the file comes out empty.
  - **Histograms:**
    - A histogram
    - Choosing bins
    - Density with a PDF on top, linking to *Horizontal and vertical lines* for marking the mean
    - Comparing two samples (transparency)
    - No box plots: the Author said they aren't needed yet.
  - **Bar charts:**
    - Bar chart of counts
    - A probability mass function (e.g. the sum of two dice)
    - Means with error bars
  - **Scatter plots:**
    - A scatter plot
    - Colour and size by value (with a colour bar)
    - Adding a fitted line (`np.polyfit`)
  - **Heatmaps** (the Author asked for heatmaps):
    - A matrix as a heatmap (`plt.imshow` and `plt.colorbar`)
    - Labelling rows and columns (ticks)
    - Colour maps and fixed limits (`cmap`, `vmin`/`vmax`, e.g. −1 to 1 for a correlation matrix from `np.corrcoef`)
    - Values in the cells
  - **Subplots** (in this order):
    - Side-by-side plots with `plt.subplot(121)`: the pyplot style `plt.subplot(121)` / `plt.subplot(122)` (the same as `plt.subplot(1, 2, 1)`), explaining the digits as rows, columns and index.
    - A grid of plots with `plt.subplots`: introduces `fig, axes = plt.subplots(...)`, with the Pitfall mapping `plt.xlabel` to `ax.set_xlabel`, `plt.title` to `ax.set_title` and so on.
    - Shared axes
    - Figure size and layout, with a Pitfall: labels overlap until `layout="constrained"`.
- **Randomness:** random data always comes from a seeded `np.random.default_rng`, as in the NumPy Area.
- **Text in figures** is language-neutral, because Outputs are shared by both Languages: symbols and maths (`x`, `f(x)`, `N(0, 1)`, `n = 30`), variable names and numbers. No English words or sentence-like titles in plots. The explanation says what the axes show, in both Languages. The authoring guide's "figures carry no translatable text" rule is made concrete with these examples.
- **Look:** one standard figure size (about 6 × 3.5 inches), Matplotlib's default style, and every example ends with `plt.show()`.
- **Figure descriptions** (ticket 15) are written for every figure, in both Languages.
- **Links:** two-way See-also links to related NumPy Entries (e.g. Random's *Normal samples*, Arrays' *Ranges* for `linspace`, Array maths' *Functions that work on whole arrays*) and to Python Basics where natural.

Conventions from tickets 12–14 apply: Outputs show values, not English sentences; inline code is the same in both Languages; a blank line follows a compound block so examples paste into the `python` REPL; "Polish term (English term)" at first mention.

**Blocked by:** 15 (Figure descriptions), and 14 (NumPy Area, merged in PR brokenpumpernickel/python-cheat-sheet#16), because the See-also links point at NumPy Entries.

**Status:** ready-for-agent

- [ ] The Matplotlib Area is no longer planned and has the six Topics in the decided Topic order, with hue 25, the Polish Topic titles above and a distinct glyph for each new Topic.
- [ ] The Entries exist with the decided English titles, each with Polish, including the three Pitfalls named above (savefig before show, `plt.xlabel` vs `ax.set_xlabel`, overlapping labels).
- [ ] Examples use the `plt` style. The Subplots Topic starts with `plt.subplot(121)` and only then introduces `fig, axes = plt.subplots(...)`.
- [ ] Every random example uses `np.random.default_rng` with a fixed seed.
- [ ] Text in every figure is language-neutral (symbols, maths, names, numbers), and the authoring guide's rule about text in figures gives these examples.
- [ ] Every figure uses the standard size and the default style, every example ends with `plt.show()`, and every figure has a description in both Languages.
- [ ] Two-way See-also links connect the Matplotlib Entries with related NumPy Entries, and with Python Basics where natural.
- [ ] Every example runs alone with `uv run python` in an empty folder with no warnings on stderr, and pastes into the REPL.
- [ ] `uv run cheatsheet build` and `uv run pytest` pass.
- [ ] The Matplotlib Topics were looked at on the Map, the Trail and the Topic pages in both Languages in `uv run cheatsheet serve`.
- [ ] The Comments list every Entry with its Polish title for the Author to skim.
- [ ] One session and one PR.

## Comments
