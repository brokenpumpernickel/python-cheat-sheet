# 21: Random numbers with the `np.random.*` functions, not generator objects

**What to build:** Every random example creates a generator, `rng = np.random.default_rng()`, and calls its methods (`rng.normal(...)`). The Author says this confuses Students, much like the visible seeds did (ticket 20), and it isn't how the lab works: Students call the `np.random.*` functions directly. So every example switches to `np.random.normal(...)`, `np.random.uniform(...)` and so on, seeded by a hidden `np.random.seed(...)`. That covers NumPy Random, Matplotlib (including Interactive plots) and SciPy stats.

Decided with the Author (every recommendation accepted):

- **Scope: every example**, not only NumPy Random. `default_rng` appears 45 times in 11 files today: `content/numpy/random.md`, the Matplotlib Topics (bar charts, heatmaps, histograms, interactive plots, plotting basics, scatter plots, subplots) and SciPy stats (distributions, discrete distributions, plotting distributions).
- **Hidden seeds** (ticket 20's markers):
  - The run code seeds with `np.random.seed(<n>)  #| hide`, and the shown code calls the functions with no seed.
  - In SciPy, `rvs` without `random_state` draws from NumPy's global generator, so the same hidden `np.random.seed` line fixes it. Every `random_state=rng  #| show: ...` line and hidden `rng = ...` line goes, leaving plain `d.rvs(size=...)`.
  - A hidden `import numpy as np` is still allowed when nothing shown uses NumPy.
- **Outputs change.** The legacy functions draw different numbers from `default_rng`, so every random Output changes.
  - Look again at every figure against its figure description, and fix the descriptions, Pitfall texts and explanations that quote values.
  - Pick seeds that give clear, typical-looking results, as the current ones do: e.g. the 2D histogram's tilted blob, the law-of-large-numbers line settling near 0.5, the sample-as-`x` zigzag.
  - Keep each example's numbers and sizes otherwise as they are.
- **NumPy Random Entries:**
  - *A generator with a seed* becomes **Setting a seed** (*Ustawianie ziarna*): `np.random.seed(42)` makes the numbers repeat on every run, and it fixes SciPy's `rvs` too.
    - The sentence that now calls `np.random.seed` the "older" style is reversed. Newer code writes `rng = np.random.default_rng(42)` and then `rng.normal(...)`, which works the same way. That sentence is the only mention of generators.
    - Renaming changes the Entry id, so update every See-also link to it.
  - The other Entries keep their titles and points. Write them with `np.random.rand` / `np.random.random`, `np.random.uniform`, `np.random.randint` (the high end is excluded, the existing Pitfall's point), `np.random.normal`, `np.random.choice`, `np.random.shuffle` / `np.random.permutation`, and `np.random.binomial` where a simulation needs it.
  - The Topic summary and the glyph (`rng`) are updated to match. The glyph could become e.g. `rand`; the agent decides.
- **SciPy *Reproducible samples*:**
  - Shows `np.random.seed(42)` before `rvs` (no markers: the seed is the point), with the same numbers on a second run.
  - Mentions `random_state=42` as the per-call alternative.
  - No generator objects. Keep its two-way See-also link with *Setting a seed*.
- **Prose:** reword anything that mentions `rng`, generators or `default_rng`, in explanations, Pitfalls, Topic summaries and figure descriptions. Keep the ticket 20 point where it is: a Student's numbers differ from the Output shown because the Output comes from one run.
- **Authoring guide:**
  - Reverse the rule "in NumPy always a generator from `default_rng`, never the legacy `np.random.seed`". Seed with a hidden `np.random.seed(<n>)  #| hide` line, and call the `np.random.*` functions.
  - Update the guide's own examples and the "Random data" line of the Figures section.
- **ADR 0006:** add a short note that the lab uses the `np.random.*` functions, so examples do too, seeded by a hidden `np.random.seed`.
- **Tests:** fixture content that uses `default_rng` may stay as it is. Change it only if the guide's rules or a test about randomness need it.

**Blocked by:** none. Ticket 22 (Sampling) waits for this one.

**Status:** resolved

- [x] No example in `content/` uses `default_rng` or `random_state=rng`, except the one sentence in *Setting a seed* and the `random_state=42` mention in *Reproducible samples*.
- [x] Every random example shows plain `np.random.*` / `rvs` calls, with its seed in a hidden `np.random.seed` line; *Setting a seed* and *Reproducible samples* show their seed.
- [x] *A generator with a seed* is now *Setting a seed*, with Polish, and every link to it works.
- [x] Every changed figure was looked at, and its description, plus any prose quoting values, matches the new Output.
- [x] The authoring guide and ADR 0006 describe the new rule.
- [x] Every changed example runs alone with `uv run python` in an empty folder with `MPLBACKEND=Agg` (with its hidden lines), with no warnings.
- [x] `uv run cheatsheet build` and `uv run pytest` pass. NumPy Random and a few Matplotlib and SciPy Topics were looked at in `uv run cheatsheet serve` in both Languages.
- [x] One session and one PR, which also adds this ticket and ticket 22.

## Comments

- **Change:** every random example in NumPy Random, the Matplotlib Topics (Plotting basics, Histograms, Bar charts, Scatter plots, Heatmaps, Subplots, Interactive plots) and SciPy stats (Distributions, Discrete distributions, Plotting distributions) now calls the `np.random.*` functions (`np.random.normal`, `np.random.uniform`, `np.random.randint`, `np.random.lognormal`, `np.random.choice`, `np.random.permutation`, `np.random.random`) and plain `d.rvs(size=...)`, seeded by a hidden `np.random.seed(<n>)  #| hide` line after the imports. No `#| show:` marker is left in `content/`. The only `default_rng` left is the one sentence in *Setting a seed* (in both Languages), and the only `random_state` is the `random_state=42` mention in *Reproducible samples*.
- **Renamed:** *A generator with a seed* / *Generator z ziarnem* is now *Setting a seed* / *Ustawianie ziarna* (`random/setting-a-seed`). Its See-also links from *Random samples with rvs* and *Reproducible samples* are updated, and its link back to *Reproducible samples* stays.
- **Figure descriptions changed** (both Languages): Bar charts *Bar chart of counts* (now 6 for face 5 to 15 for face 3), *A probability mass function* (tallest bar about 0.17), *Means with error bars* (B tallest at about 6, A about 5, C lowest at about 4); Interactive plots *Dropdowns and checkboxes* (about −2.4 to 2.8, tallest bar around 0) and *Holding a value fixed* (about 37 to 92); Subplots *Side-by-side plots with plt.subplot(121)* (uniform bars between about 45 and 55); Plotting distributions *A histogram with the pdf* (about 145 to 191). Every other figure was looked at against its description and still matches it.
- **Prose changed** (both Languages): NumPy Random's summary ("Random numbers with the np.random functions: …") and glyph (`rand`); *Setting a seed* (rewritten); every NumPy Random explanation that named `rng.*` methods; *Choosing and shuffling* also names `np.random.shuffle(x)`, which shuffles in place and returns `None`; *Discrete uniform distribution* ("as in `np.random.randint`"); *Reproducible samples* (rewritten).
- Decisions:
  - **Seeds** were searched for, not taken at random: each was checked in a script for a typical result (a sample mean and standard deviation close to the true ones, a bell-shaped histogram peaking at the centre, 7 heads of 10 at p = 0.7, the share of sevens within 0.0005 of 6/36, a coin-flip line that jumps early and settles near 0.5). Where a seed could also keep a figure description true (the log-bins histogram and its Pitfall, the 2D histogram, the B(10, 0.3) bars, the A histogram, Choosing bins, the coin flips, the zigzag Pitfall), that one was chosen, so those descriptions didn't change. *The @interact decorator* got a seed whose 50 values give clearly ragged bars, which is that Entry's point.
  - **Setting a seed** has no Pitfall now. The old Pitfall warned against `np.random.seed`; reversed, it is not a mistake Students make, so the "newer code writes `rng = np.random.default_rng(42)`…" sentence went into the explanation, which also keeps the ticket 20 point that the Student's numbers won't match the Output.
  - **Reproducible samples** seeds with `np.random.seed(42)`, draws two samples, seeds again and draws them again, so the Output shows that each call draws new numbers and the sequence repeats. `random_state=42` is mentioned in the explanation as the way to fix a single call.
  - Same draws: *Parameters in every call* and *A frozen distribution* still share a seed, so they print the same five values, as before; *A scatter plot* and *Adding a fitted line* share one too, as do *Logarithmic bins* and its Pitfall, and *A histogram with the pdf* and its Pitfall.
  - The `rvs` calls that were split over two lines for their markers are one line again (each within 43 characters).
  - Test fixtures were left as they are; no test is about randomness in `content/`.
- Every changed example (Entry and Pitfall, 38 in all) was run alone with `MPLBACKEND=Agg uv run python` in its own empty folder, with no warnings, and its figures were saved and looked at beside the old ones. The build's Outputs match those runs.
- `uv run cheatsheet build` and `uv run pytest` (237 tests) pass, run one after the other. In `uv run cheatsheet serve`, NumPy Random, SciPy Distributions, Bar charts and Histograms were checked in English and Polish: the shown code (no seed or marker outside the two Entries that show one), the Outputs, the figure descriptions and the See-also links to *Setting a seed*.
