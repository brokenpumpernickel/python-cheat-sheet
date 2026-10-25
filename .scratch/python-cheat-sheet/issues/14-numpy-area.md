# 14: NumPy Area: arrays, axes, vectorised functions and simulations

**What to build:** The NumPy Area stops being planned and gets real content, written for Students who know basic Python and now need NumPy for statistics work: matrices, axes, vectorised functions, sample statistics and reproducible simulations. Decided with the Author:

- **Topics**, in this Topic order: Arrays (`arrays`), Indexing (`indexing`), a new Topic *Array maths* (`array-maths`, Polish *Działania na tablicach*, glyph `a*2`), Aggregates (`aggregates`) and Random (`random`). The existing Polish Topic titles stay: Tablice, Indeksowanie, Agregacje, Losowanie. Random moves to the end, after Aggregates.
- **Entries** (26), with these English titles; the Polish titles are the agent's:
  - **Arrays:** Creating arrays; Ranges (`arange`, `linspace`); Zeros, ones and full; Shape and dtype; Two-dimensional arrays (matrices from nested lists, `np.zeros((r, c))`, `reshape` and similar: Students must learn to make 2D matrices); Reshaping.
  - **Indexing:** Indexing and slicing; Rows and columns (`a[i, j]`, `a[:, j]`); Boolean masks; Changing values through a mask.
  - **Array maths:** Element-wise arithmetic, with a Pitfall: `list * 2` repeats the list while `array * 2` doubles each value; Maths functions (`sqrt`, `exp`, `log`); Comparisons; Broadcasting; Functions that work on whole arrays: a function written with NumPy operations (e.g. the normal density) takes an array and returns the result for every element. Its Pitfall shows what breaks vectorisation (`math.exp` or an `if` on an array) with the real error as an expected-error Output, and points to `np.where`.
  - **Aggregates:** Sum, mean, min and max, with a Pitfall about NumPy 2 scalars showing as `np.float64(...)` inside lists or dicts; Standard deviation and variance, with a Pitfall that the default `ddof=0` is the population formula, so use `ddof=1` for a sample; Along an axis, on a students × tests matrix, with a Pitfall that `axis=0` collapses the rows and gives one result per column; Median and percentiles; Where the minimum and maximum are (`argmin`, `argmax`); Counting and proportions with a mask (`mask.sum()`, `mask.mean()`).
  - **Random:** A generator with a seed, with a Pitfall about the legacy `np.random.seed` / `np.random.rand` style of older tutorials; Uniform numbers and integers; Normal samples; Choosing and shuffling (`choice`, with probabilities); Simulating an experiment (e.g. the proportion of two-dice rolls summing to 7).
- **Reproducibility:** every random example uses `rng = np.random.default_rng(<fixed seed>)`, never the legacy global API, so Outputs are the same on every build.
- **Printing:** the authoring guide gets a rule that a single NumPy number is printed on its own or in an f-string (rounding long decimals where needed), never inside a list or dict; the Pitfall above shows why.
- **Links between Areas:** two-way See-also links where a Python Basics idea has a NumPy counterpart, at least Lists' *Summaries* ↔ *Sum, mean, min and max*; *List comprehensions* ↔ *Element-wise arithmetic*; *Counting occurrences* ↔ *Counting and proportions with a mask*; Functions' *Defining and calling* ↔ *Functions that work on whole arrays*.
- **Topic order inside the Area:** a Topic comes after what its examples rely on. Earlier Topics use `print` and `np.array` freely; Arrays prefers a non-random matrix over `rng`, or links to Random.

Conventions from tickets 12 and 13 apply: Outputs show values, not English sentences; inline code is the same in both Languages; a blank line follows a compound block so examples paste into the `python` REPL; "Polish term (English term)" at first mention.

**Blocked by:** None (can start immediately).

**Status:** resolved

- [x] The NumPy Area is no longer planned and has the five Topics in the decided Topic order, with the Polish Topic titles above and the glyph `a*2` for Array maths.
- [x] The 26 Entries exist with exactly the decided English titles, each with Polish, and the six Pitfalls named above.
- [x] Every random example uses `np.random.default_rng` with a fixed seed; none uses the legacy global API, except the Pitfall that warns about it.
- [x] Single NumPy numbers are printed on their own or in an f-string, never inside a list or dict, and the authoring guide has that rule.
- [x] The four pairs of two-way See-also links between Python Basics and NumPy exist.
- [x] Every example runs alone with `uv run python` in an empty folder: stdout matches the Output, no warnings on stderr apart from expected errors, and it pastes into the REPL.
- [x] `uv run cheatsheet build` and `uv run pytest` pass.
- [x] The NumPy Topics were looked at on the Map, the Trail and the Topic pages in both Languages, including how matrix and broadcasting Outputs read.
- [x] The Comments list every Entry with its Polish title for the Author to skim.

## Comments

**Resolved** in PR brokenpumpernickel/python-cheat-sheet#PRNUM (https://github.com/brokenpumpernickel/python-cheat-sheet/pull/PRNUM). The NumPy Area is real: five Topics, 26 Entries, 11 Pitfalls (9 with code, 5 of them expected errors). Random moved from third to last in the Topic order, and the Area blurb now names matrices, sample statistics and simulations.

Every Entry, for the Author to skim (English / Polish):

- **Arrays** / *Tablice* (glyph `[[ ]]`)
  - *Creating arrays* / *Tworzenie tablic*
  - *Ranges* / *Zakresy*
  - *Zeros, ones and full* / *Zera, jedynki i full*
  - *Shape and dtype* / *Kształt i dtype*
  - *Two-dimensional arrays* / *Tablice dwuwymiarowe*: nested lists, `np.zeros((2, 3))`, `np.arange(1, 7).reshape(3, 2)`. Random matrices are in Random's *Uniform numbers and integers*, which this Entry links to.
  - *Reshaping* / *Zmiana kształtu*: `reshape`, `-1`, `.T` and `.flatten()`. The Output shows that `.T` is not a reshape.
- **Indexing** / *Indeksowanie* (glyph `a[i]`)
  - *Indexing and slicing* / *Indeksowanie i wycinanie*
  - *Rows and columns* / *Wiersze i kolumny*
  - *Boolean masks* / *Maski logiczne*
  - *Changing values through a mask* / *Zmiana wartości przez maskę*: `a[mask] = value` and `np.where`.
- **Array maths** / *Działania na tablicach* (glyph `a*2`, new)
  - *Element-wise arithmetic* / *Arytmetyka element po elemencie*
  - *Maths functions* / *Funkcje matematyczne*
  - *Comparisons* / *Porównania*: element-wise comparisons, `.any()`, `.all()`, `np.isclose`.
  - *Broadcasting* / *Rozgłaszanie (broadcasting)*: a row against a matrix, and a `(rows, 1)` column.
  - *Functions that work on whole arrays* / *Funkcje działające na całych tablicach*: the normal density on an array and on one number.
- **Aggregates** / *Agregacje* (glyph `.sum`)
  - *Sum, mean, min and max* / *Suma, średnia, minimum i maksimum*: same data as Lists' *Summaries*.
  - *Standard deviation and variance* / *Odchylenie standardowe i wariancja*
  - *Along an axis* / *Wzdłuż osi*: a students × tests matrix, written one row per line.
  - *Median and percentiles* / *Mediana i percentyle*
  - *Where the minimum and maximum are* / *Gdzie jest minimum i maksimum*
  - *Counting and proportions with a mask* / *Zliczanie i proporcje z maską*
- **Random** / *Losowanie* (glyph `rng`)
  - *A generator with a seed* / *Generator z ziarnem*: the Output prints the same three numbers twice from the same seed.
  - *Uniform numbers and integers* / *Rozkład jednostajny i liczby całkowite*: `uniform`, dice with `integers(1, 7, n)`, and a `(2, 5)` matrix.
  - *Normal samples* / *Próbki z rozkładu normalnego*
  - *Choosing and shuffling* / *Losowy wybór i tasowanie*: a biased coin with `p=`, `replace=False` and `permutation`.
  - *Simulating an experiment* / *Symulacja doświadczenia*: 100 000 rolls of two dice as a `(100_000, 2)` matrix, `sum(axis=1)` and a mask proportion, printed next to 6/36.

Pitfalls:

- **Decided with the Author:** `list * 2` (*Element-wise arithmetic*, shows `*` and `+` on a list); `if` on an array (*Functions that work on whole arrays*, `ValueError`, names `math.exp`'s `TypeError` and points to `np.where`); `np.float64(...)` inside a list and a dict (*Sum, mean, min and max*); `ddof=0` (*Standard deviation and variance*, prints the population value); `axis=0` (*Along an axis*, prose, since the example already shows both axes); the legacy `np.random.seed` style (*A generator with a seed*, prose, so no example runs the legacy API).
- **Added beyond the decision**, each a common mistake with a hard-to-read error or a silent wrong result: `np.zeros(2, 3)` without the inner parentheses (*Two-dimensional arrays*, `TypeError`); a slice is a view, so changing it changes the original (*Indexing and slicing*); `and` between masks (*Boolean masks*, `ValueError`); `np.nan` in an integer array (*Changing values through a mask*, `ValueError`); a one-value-per-row array that won't broadcast (*Broadcasting*, `ValueError`).

Other changes:

- **See also between Areas:** Lists' *Summaries* ↔ *Sum, mean, min and max*; *List comprehensions* ↔ *Element-wise arithmetic*; *Counting occurrences* ↔ *Counting and proportions with a mask*; Functions' *Defining and calling* ↔ *Functions that work on whole arrays*. One-way links from NumPy to Python Basics: *Creating arrays* → Lists' *Creating and indexing*, *Ranges* → Loops' *range*, *Indexing and slicing* → Lists' *Slicing*, *Boolean masks* → Conditionals' *Combining conditions*, *Sum, mean, min and max* → Strings' *f-strings*.
- **Authoring guide:** a "NumPy numbers are printed on their own" bullet under "Code example", and the seeding bullet now says to use a generator from `default_rng`, never the legacy `np.random.seed`.
- **Line length:** code lines are at most 43 characters (39 in a Pitfall), which is what fits in a two-column Topic page at 1280 px without scrolling sideways. Matrices are written one row per line, so they look like the Output.
- **Checked:** all 35 examples (26 Entries, 9 Pitfalls) ran alone with `uv run python` in an empty folder. Stdout matched the Output, and stderr was empty apart from the five expected errors, whose last line matched. Each was also fed line by line to `code.InteractiveConsole` like a REPL paste, with no `SyntaxError` and the same stdout. `uv run cheatsheet build` and `uv run pytest` pass. The Map, the Trail and the NumPy Topic pages were looked at in `uv run cheatsheet serve` in both Languages.

For the Author to check:

- The Polish, especially *Rozkład jednostajny i liczby całkowite* for "Uniform numbers and integers", and "rozgłaszanie (broadcasting)".
- The glyph `a*2` and the five extra Pitfalls.
- Four of the decided titles are longer than the guide's four words (*Changing values through a mask*, *Functions that work on whole arrays*, *Where the minimum and maximum are*, *Counting and proportions with a mask*). They were kept as decided.
- *Counting occurrences* now has four See-also links, one more than the guide's one to three, because the decided link to NumPy was added beside the three it had.
- A few Python Basics code lines are also longer than 43 characters and scroll sideways in two columns (e.g. Strings' *Number formats*). They weren't changed here.
