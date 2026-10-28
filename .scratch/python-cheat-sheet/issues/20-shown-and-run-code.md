# 20: Shown code and run code: `#| show:` and `#| hide` line markers, and no visible seeds

**What to build:** Today an Entry's code block is both what the page shows and what the build runs. The Author wants the two to be able to differ, so that:

1. Examples stop showing seeds. Students find passing a generator to `rvs` (`random_state=rng`) confusing, and it isn't the workflow the lab uses: they call `rvs` and `default_rng()` without a seed and get new numbers each run. The build still needs a seed, so Outputs stay the same from build to build. It should run seeded code while showing unseeded code, with no patching of NumPy or any other library.
2. Later Entries can show things the build can't or shouldn't do, e.g. loading a file from the web, while the build loads a local copy.

Decided with the Author:

- **One code block, with marker comments at the end of a line.** The build runs the block as written. The page shows it with the marked lines changed:
  - `code  #| show: <shown code>`: runs `code`, shows `<shown code>` in its place, with the line's indentation kept.
  - `code  #| hide`: runs `code`, and the line isn't shown at all.
  - Unmarked lines run exactly as shown. That's why it's per line, not a second hidden block: the Output can't quietly drift from the code beside it, and nothing has to be edited twice.

  For example:

  ```python
  rng = np.random.default_rng(7)  #| show: rng = np.random.default_rng()
  sample = d.rvs(size=1000, random_state=rng)  #| show: sample = d.rvs(size=1000)
  open("scores.csv", "w").write("72,45,88\n")  #| hide
  data = np.loadtxt("scores.csv", delimiter=",")  #| show: data = np.loadtxt("https://example.org/scores.csv", delimiter=",")
  ```

  The marker is the last `  #| ` (two or more spaces, `#|`, a space) on the line. The space before it is not part of either the run code or the shown code.
- **Everywhere the code appears**: the page, the Copy button, syntax highlighting and the search index all use the shown code. The build runs the run code. `generated/content.json` keeps `code` as the shown code; add `run` only if something needs it.
- **Entry and Pitfall code** both support the markers.
- **Validation** (`ContentError`, in the guide's validation table):
  - An unknown `#|` marker, e.g. `#| hidden` or `#|show:x`. Message: say that only `#| show: <code>` and `#| hide` exist.
  - `#| show:` with nothing after it.
  - A block whose lines are all hidden.

  The build can't check that a `show:` line means the same as its run line. The guide says so, and says to use the markers only for seeds and data sources, never to change what the example does.
- **New ADR** `docs/adr/0006-...`: an Output may come from code that differs from the shown code, only on marked lines, and only for things like seeds and data sources. It records why line markers rather than a hidden second block, and why not patching libraries in the kernel. It refines ADR 0002/0003.
- **Seeds hidden everywhere.** Apply the markers to every example that seeds randomness:
  - NumPy and Matplotlib (including Interactive plots): show `rng = np.random.default_rng()`, keeping the seed only in the run code.
  - SciPy stats: show `rvs(...)` without `random_state`. A line that only creates `rng` for it becomes `#| hide`, and so does `import numpy as np` if nothing shown uses it.
  - **Keep each run line as it is now**, so every Output stays exactly the same and the figure descriptions stay true. Check this by comparing `generated/content.json` before and after; only `code` should change, apart from the new Entry.
  - **Where the seed is the point, it stays visible**: NumPy Random's *A generator with a seed*, and the new SciPy Entry below.
- **New SciPy Entry** in Distributions, after *Random samples with rvs*: **Reproducible samples**; the Polish title is the agent's.
  - `random_state=42` makes `rvs` give the same numbers on every run, and passing a seeded `np.random.default_rng(42)` gives a reproducible stream of samples. No markers in this one.
  - See-also links both ways with NumPy Random's *A generator with a seed*.
- **Prose:** reword explanations, Pitfalls and Topic summaries that talk about the seeds or `random_state=rng` they no longer show. For example:
  - *Parameters in every call* and *A frozen distribution* in SciPy, which mention `random_state=rng` and "the same seed".
  - *Random samples with rvs*.
  - NumPy Random's summary ("Reproducible random numbers: a seeded generator…").

  Where it helps, say that a Student's numbers will differ from the Output shown, because the Output comes from one run.
- **Authoring guide:**
  - A section on the markers, with the rules above.
  - Rewrite the "Same Output on every build" rule: seed in the run code with `#| show:`, show the unseeded form.
  - Update the "Random data" line of the Figures section.
  - Add the new validation rows.
- **Tests:** content-build tests for the shown vs run code (marked lines, indentation, hidden lines, Pitfall code) and for each new validation error. A browser test that the page and the Copy button give the shown code. The existing fixtures' Outputs are unchanged.

**Blocked by:** none. Ticket 19 (Interactive plots, PR brokenpumpernickel/python-cheat-sheet#29) is merged, so its examples are included.

**Status:** resolved

- [x] The build runs the marked code and the page, Copy, highlighting and search use the shown code, for Entry and Pitfall code.
- [x] Unknown markers, an empty `#| show:` and an all-hidden block fail the build with clear messages, listed in the guide's validation table.
- [x] ADR 0006 records the decision.
- [x] Every example except NumPy's *A generator with a seed* and SciPy's *Reproducible samples* shows no seed and no `random_state`, and every Output is unchanged (content.json compared before and after).
- [x] *Reproducible samples* exists in SciPy Distributions with Polish and two-way See-also links.
- [x] Prose and summaries no longer refer to seeds the code doesn't show.
- [x] The authoring guide describes the markers and the new randomness rule.
- [x] Tests cover the above; `uv run cheatsheet build` and `uv run pytest` pass; a few changed Topics were looked at in `uv run cheatsheet serve` in both Languages, including Copy.
- [x] One session and one PR, which also adds this ticket file.

## Comments

- Resolved by the PR that adds this ticket (link added below once it is open).
- **Mechanism:** `cheatsheet/content.py` splits each code block into shown code (`code` in `generated/content.json`, used by the page, Copy, highlighting and search) and run code, which `cheatsheet/build.py` runs and then drops from the data, so `content.json` has no `run` field. The site needed no change.
- **Entries whose code changed** (34; every Output, error, figure and widget list is identical to a fresh build from `main`, compared field by field):
  - NumPy Random: *Uniform numbers and integers*, *Normal samples*, *Choosing and shuffling*, *Simulating an experiment*.
  - Matplotlib Plotting basics: *Format strings*, *Axis limits and a grid*, *Horizontal and vertical lines*. Histograms: *A histogram*, *Choosing bins*, *Logarithmic bins* (and its Pitfall), *Density with a PDF on top*, *Comparing two samples*. Bar charts: *Bar chart of counts*, *A probability mass function*, *Means with error bars*. Scatter plots: *A scatter plot*, *Colour and size by value*, *Adding a fitted line*. Heatmaps: *A matrix as a heatmap*, *Colour maps and fixed limits*, *A 2D histogram of points*. Subplots: *Side-by-side plots with plt.subplot(121)*, *Plots spanning several columns*, *A grid of plots with plt.subplots*, *Shared axes*. Interactive plots: *Dropdowns and checkboxes*, *The @interact decorator*, *Holding a value fixed*.
  - SciPy stats Distributions: *Parameters in every call*, *A frozen distribution*, *Random samples with rvs*. Discrete distributions: *Discrete uniform distribution*. Plotting distributions: *A histogram with the pdf* (and its Pitfall), *A pmf as bars*.
- **New Entry:** *Reproducible samples* / *Powtarzalne próbki*, after *Random samples with rvs*, with two-way See-also links to NumPy's *A generator with a seed*. It rolls a die (`stats.randint(1, 7)`) so its lines stay within the 43 characters the SciPy examples keep to; Output `[4 5 3 5 5]` twice, then two different rows from one `default_rng(42)`.
- **Prose changed:** NumPy Random's summary ("Random numbers from a generator: seeds, …" / "Liczby losowe (random numbers) z generatora: ziarno, …") and *A generator with a seed*, which now says the other examples leave the seed out, so the Student's numbers won't match the Output. *Parameters in every call* and *A frozen distribution* drop `random_state=rng`; *Random samples with rvs* says each run draws a new sample, so the Student's numbers differ from the Output shown.
- Decisions:
  - **Marker parsing:** the marker is the last `#|` that starts a word on the line. It is valid only after two or more spaces with code before it, as `#| hide` or `#| show: <code>`; anything else (`#| hidden`, `#|show:x`, one space, a `#|` line with no code) is the "unknown marker" error. The run code is the line before the marker, with the trailing spaces removed.
  - **Blank lines at the top** of the shown code, left by hidden lines (a hidden `import numpy as np` followed by a blank line), are dropped. Other blank lines stay.
  - **Multi-line `rvs` calls** keep their run lines: the line with `size=` gets `#| show:` with the closing parenthesis, and the `random_state=rng)` line is hidden, so the shown call keeps its old line breaks.
  - `import numpy as np` is hidden in *Parameters in every call*, *A frozen distribution* and *Random samples with rvs*, where nothing shown uses `np`; it stays wherever `np` is still used.
  - The guide's Figures section says the figure description describes the figure on the page, which comes from the seeded run, so the existing descriptions stay as they are.
  - The ADR is `docs/adr/0006-shown-code-may-differ-on-marked-lines.md`.
- Tests: `tests/fixtures/markers` (hidden line, `#| show:` with indentation, three spaces before a marker, a Pitfall with a marker, a hidden first line), four invalid fixtures for the new errors, a browser test that the page and Copy give the shown code (a new *Repeating* Entry in the site fixture's Strings), and a search test that the run-only seed isn't indexed.
- `uv run cheatsheet build` and `uv run pytest` (237 tests) pass, run one after the other. In `uv run cheatsheet serve`, *Random samples with rvs*, *Reproducible samples*, *A frozen distribution*, NumPy Random and *A histogram* were checked in English and Polish: the shown code, Copy (it put the shown code on the clipboard and said "Copied!"), the See-also links both ways, and `search.json`, which has no `#|` and no seed outside the two Entries that show one.
