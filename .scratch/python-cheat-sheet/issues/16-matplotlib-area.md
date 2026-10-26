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
    - A 2D histogram of points (`plt.hist2d`): added after the PR opened, at the Author's request, with a picture of a point-density heatmap as the model.
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

**Status:** resolved

- [x] The Matplotlib Area is no longer planned and has the six Topics in the decided Topic order, with hue 25, the Polish Topic titles above and a distinct glyph for each new Topic.
- [x] The Entries exist with the decided English titles, each with Polish, including the three Pitfalls named above (savefig before show, `plt.xlabel` vs `ax.set_xlabel`, overlapping labels).
- [x] Examples use the `plt` style. The Subplots Topic starts with `plt.subplot(121)` and only then introduces `fig, axes = plt.subplots(...)`.
- [x] Every random example uses `np.random.default_rng` with a fixed seed.
- [x] Text in every figure is language-neutral (symbols, maths, names, numbers), and the authoring guide's rule about text in figures gives these examples.
- [x] Every figure uses the standard size and the default style, every example ends with `plt.show()`, and every figure has a description in both Languages.
- [x] Two-way See-also links connect the Matplotlib Entries with related NumPy Entries, and with Python Basics where natural.
- [x] Every example runs alone with `uv run python` in an empty folder with no warnings on stderr, and pastes into the REPL.
- [x] `uv run cheatsheet build` and `uv run pytest` pass.
- [x] The Matplotlib Topics were looked at on the Map, the Trail and the Topic pages in both Languages in `uv run cheatsheet serve`.
- [x] The Comments list every Entry with its Polish title for the Author to skim.
- [x] One session and one PR.

## Comments

**Resolved** in PR brokenpumpernickel/python-cheat-sheet#19 (https://github.com/brokenpumpernickel/python-cheat-sheet/pull/19). The Matplotlib Area is real: six Topics, 26 Entries, 28 figures (26 Entries and 2 Pitfalls), each with a figure description in English and Polish. The Area blurb now names the six kinds of plot.

Every Entry with its Polish title and English figure description, for the Author to skim (the Polish descriptions say the same):

- **Plotting basics** / *Podstawy wykresów* (glyph `plt`)
  - *A line plot* / *Wykres liniowy*: A sine wave from x = 0 to 10, swinging between −1 and 1 a little over one and a half times.
  - *Axis labels and a title* / *Opisy osi i tytuł*: A bell curve titled N(0, 1), peaking at about 0.4 at x = 0, with the x-axis labelled x and the y-axis f(x).
  - *Several lines and a legend* / *Kilka linii i legenda*: Three bell curves centred on 0, with a legend for σ = 0.5, σ = 1 and σ = 2; the smaller σ, the taller and narrower the curve.
  - *Colours, markers and line styles* / *Kolory, znaczniki i style linii*: Three lines over x = 1 to 10: red dots on a curve rising ever faster, a black dashed straight line, and green squares on a dotted, less steep straight line.
  - *Axis limits and a grid* / *Zakresy osi i siatka*: A jagged line over n = 1 to 500 on a grid, jumping around at first and then settling close to 0.5, on a y-axis from 0 to 1.
  - *Horizontal and vertical lines* / *Linie poziome i pionowe*: Thirty points joined by a zigzag line between about 55 and 85, a red horizontal line across the plot at their mean, and a grey dashed vertical line through the highest point.
  - *Saving a figure* / *Zapisywanie wykresu*: A curve rising steeply from 0 and then flattening, reaching about 3.2 at x = 10.
- **Histograms** / *Histogramy* (glyph `hist`)
  - *A histogram* / *Histogram*: Ten bars forming a bell shape that peaks around 170, with counts falling away on both sides, from about 140 to 195.
  - *Choosing bins* / *Wybór przedziałów*: Outlined bars, each 10 points wide, on an axis from 0 to 100: the bin from 60 to 70 is the tallest, the bins on either side of it are equal, and the bins below 30 are empty.
  - *Density with a PDF on top* / *Gęstość z krzywą PDF*: Thirty bars in a bell shape around 0, with the smooth normal curve drawn over them and following their tops closely, peaking near 0.4.
  - *Comparing two samples* / *Porównanie dwóch próbek*: Two see-through bell-shaped histograms with a legend, μ = 0 and μ = 1; the second is the same shape shifted one unit to the right, and they overlap in the middle.
- **Bar charts** / *Wykresy słupkowe* (glyph `bar`)
  - *Bar chart of counts* / *Wykres słupkowy liczebności*: Six bars for the faces 1 to 6 of uneven height, from 6 for face 5 to 17 for face 3.
  - *A probability mass function* / *Funkcja prawdopodobieństwa*: Eleven bars for the sums 2 to 12 forming a triangle: rising evenly to the tallest bar at 7, about 0.16, then falling evenly.
  - *Means with error bars* / *Średnie ze słupkami błędów*: Three bars, A, B and C, each with a short capped error bar on top; A and B are close, at about 5 and 5.5, and C is clearly lower, below 3.5.
- **Scatter plots** / *Wykresy punktowe* (glyph `x, y`)
  - *A scatter plot* / *Wykres punktowy*: Fifty dots spread from lower left to upper right in a loose band, rising from about 0 to about 20 as x goes from 0 to 10.
  - *Colour and size by value* / *Kolor i rozmiar według wartości*: A round cloud of dots around (0, 0): small and dark purple in the middle, larger and yellow towards the edge, with a colour bar labelled r from 0 to about 2.5.
  - *Adding a fitted line* / *Dopasowana prosta*: Fifty dots in a loose band rising from lower left to upper right, with a red straight line running through the middle of the band.
- **Heatmaps** / *Mapy ciepła* (glyph `cmap`)
  - *A matrix as a heatmap* / *Macierz jako mapa ciepła*: A grid of 5 rows and 8 columns of coloured squares, from dark purple for about 40 to yellow for 100, with no clear pattern, and a colour bar beside it.
  - *Labelling rows and columns* / *Etykiety wierszy i kolumn*: A grid of 3 rows labelled A, B and C and 4 columns labelled 2 to 5, with a colour bar; the brightest cell is row C, column 4, and row C, column 2 is the darkest.
  - *Colour maps and fixed limits* / *Mapy kolorów i stałe zakresy*: A 3 by 3 grid for x, y and z with a colour bar from −1 in blue to 1 in red: the diagonal is dark red, x and y are light red, and z against x and y is blue.
  - *Values in the cells* / *Wartości w komórkach*: The grid of grades 2 to 5 by groups A, B and C in shades of blue, each cell showing its count in the middle; the darkest cell holds 12 and the lightest 1.
  - *A 2D histogram of points* / *Dwuwymiarowy histogram punktów*: A dark purple rectangle with a bright oval blob tilted from lower left to upper right, yellow at its centre near x = 10, y = 10 and fading to purple at its edges, with a colour bar of counts.
- **Subplots** / *Podwykresy* (glyph `ax[ ]`)
  - *Side-by-side plots with plt.subplot(121)* / *Wykresy obok siebie z plt.subplot(121)*: Two histograms side by side: on the left, U(0, 1), ten bars of similar height, between about 40 and 60; on the right, N(0, 1), a bell shape around 0.
  - *A grid of plots with plt.subplots* / *Siatka wykresów z plt.subplots*: Four histograms of normal samples in a 2 by 2 grid, titled n = 10, n = 100, n = 1000 and n = 10000; the larger n, the smoother the bell shape. Pitfall: Two plots side by side, a line rising on the left and a line falling on the right; only the right plot has a title, b, and the left one has none.
  - *Shared axes* / *Wspólne osie*: Two histograms stacked on one shared x-axis: the top one narrow and centred on 0, the bottom one about twice as wide and centred on 2.
  - *Figure size and layout* / *Rozmiar i układ rysunku*: A 2 by 2 grid of curves titled k = 0 to k = 3, each with its x-axis labelled x, all neatly spaced: a flat line, a straight line, and two curves rising ever faster. Pitfall: The same 2 by 2 grid squeezed together: the x labels and tick numbers of the top row overlap the titles k = 2 and k = 3 of the bottom row.

Pitfalls:

- **Decided with the Author:** `savefig` after `show` (*Saving a figure*, prose, since running it in the build would only capture an empty figure); `plt.title` on a grid (*A grid of plots with plt.subplots*, with code: both titles land on the right plot, and the text maps `plt.title`, `plt.xlabel` and the like to `ax.set_title`, `ax.set_xlabel`, `ax.set_ylabel`, `ax.set_xlim`, `ax.set_ylim`); overlapping labels (*Figure size and layout*, with code: the same grid without `layout="constrained"`, where the top row's `x` labels run into the bottom row's titles).
- **Added beyond the decision:** values outside the bin edges are silently left out (*Choosing bins*, prose).

Decisions made while writing:

- **Figure size:** every example sets it in the code, `plt.figure(figsize=(6, 3.5))` or `figsize=(6, 3.5)` in `plt.subplots`, rather than through the kernel's settings, so a Student pasting into Jupyter gets the same figure (ADR 0003). *A line plot* explains it first. Every example ends with `plt.show()`, and none changes the style.
- **Text in figures:** only maths and names: `x`, `f(x)`, `N(0, 1)`, `U(0, 1)`, `σ = 0.5`, `μ = 0`, `n = 100`, `k = 2`, `r`, the groups `A`, `B`, `C`, the grades 2 to 5, `a` and `b`. Where the axes need explaining, the explanation does it in both Languages (*A histogram*, *Bar chart of counts*, *A matrix as a heatmap*, *Labelling rows and columns*). Matplotlib writes text as paths, so no figure text reaches the page's text or search.
- **Subplots:** *A grid of plots with plt.subplots* already uses `layout="constrained"`, with a short clause, because its titles would overlap otherwise; *Figure size and layout* explains it and its Pitfall shows the overlap.
- **Heatmaps:** *Values in the cells* uses `cmap="Blues"` with `vmax=20`, which keeps the darkest cell mid-blue so the black numbers stay readable. It reuses the grade counts and tick labels of *Labelling rows and columns*, and relies on `vmax` from *Colour maps and fixed limits*. *A 2D histogram of points* uses 20 000 points so the blob is smooth rather than grainy, and `rasterized=True`: without it the build's SVG showed thin light seams between the 1600 squares and weighed about 300 KB instead of about 22 KB. It keeps the default linear colour scale; a power or log scale (`norm=`) would bring out faint regions but is left out for now.
- **Randomness:** every random example uses `np.random.default_rng` with its own fixed seed.

Other changes:

- **See also, two-way with NumPy:** *A line plot* ↔ Arrays' *Ranges* and Array maths' *Maths functions*; *Horizontal and vertical lines* ↔ Aggregates' *Where the minimum and maximum are* and *Sum, mean, min and max*; *A histogram* ↔ Random's *Normal samples*; *Density with a PDF on top* ↔ *Functions that work on whole arrays*; *A probability mass function* ↔ *Simulating an experiment*; *Means with error bars* ↔ *Standard deviation and variance*; *A scatter plot* ↔ *Uniform numbers and integers*; *A matrix as a heatmap* ↔ *Two-dimensional arrays*; *Values in the cells* ↔ Indexing's *Rows and columns*. **Within the Area:** *A 2D histogram of points* ↔ *A scatter plot* and *A histogram*. **With Python Basics and the Standard library:** *Bar chart of counts* ↔ collections' *Counting with Counter*. One-way links: *Several lines and a legend* → *for over a collection* and *f-strings*; *Axis limits and a grid* → *Uniform numbers and integers*; *Choosing bins* → *Ranges*; *Density with a PDF on top* → *Horizontal and vertical lines*; *Means with error bars* → *Along an axis*; *Adding a fitted line* → Tuples' *Unpacking*; *Values in the cells* → Loops' *range*; *A grid of plots with plt.subplots* → *Looping with zip*; *Figure size and layout* → *enumerate*. The NumPy and collections edits touch only See-also lists, and no Entry has more than three links.
- **Authoring guide:** the "Figures" section is now a list: one figure and one size (`figsize=(6, 3.5)`), the default style, `plt.show()` at the end, the `plt` style; language-neutral text with the examples above and what not to write (`plt.xlabel("height")`); a seeded `default_rng`; and how to check warnings with `MPLBACKEND=Agg`. The guide's own figure examples (*Plotting counts*) now use `{"A": 7, "B": 3}` instead of heads and tails, and start with `plt.figure(figsize=(6, 3.5))`.
- **PR brokenpumpernickel/python-cheat-sheet#18** had merged before this work started, so the branch began from it and there were no conflicts.
- **Checked:** all 28 examples ran alone with `uv run python` in an empty folder with `MPLBACKEND=Agg`, each figure also rendered to SVG so warnings raised while drawing would show (a planted missing-glyph warning was caught). Stderr was empty apart from Agg's expected "FigureCanvasAgg is non-interactive" notice at `plt.show()`. Each was also fed line by line to `code.InteractiveConsole` like a REPL paste: no traceback, and the same printed lines. Code lines are at most 43 characters (39 in a Pitfall). `uv run cheatsheet build` and `uv run pytest` pass. Every figure was looked at at card width against its description, and six descriptions were corrected to match the plot. The Map, the Trail and the Topic pages were looked at in `uv run cheatsheet serve` in both Languages and both themes, and on Histograms the figures' accessible names were the Polish descriptions with `?lang=pl` and the English ones after switching to EN.

For the Author to check:

- The Polish, especially *Funkcja prawdopodobieństwa* for "A probability mass function", *Gęstość z krzywą PDF*, "rysunek (figure)" and "mapa kolorów (colormap)".
- The glyphs `hist`, `bar` and `cmap`.
- The extra Pitfall in *Choosing bins*.
- **Figures are small in the two-column layout.** At 1280 px a figure is about 350 px wide, so Matplotlib's 10 pt tick labels show at about 8 px, and the 2 by 2 grids in Subplots are hard to read. At 1920 px they are 10 to 12.5 px. Fixing it is a site layout change (for example letting a figure span the card's full width, or both columns), not a content one, so it isn't done here.
- *Side-by-side plots with plt.subplot(121)* and *A grid of plots with plt.subplots* are longer than the guide's four words and contain code; they were kept as decided, like NumPy's *Choosing between two arrays with np.where*.
