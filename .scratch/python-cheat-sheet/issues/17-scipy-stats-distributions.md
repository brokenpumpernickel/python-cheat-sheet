# 17: SciPy stats Area: distributions, their parameters, and plotting them

**What to build:** The SciPy stats Area stops being planned and gets its first real content: probability distributions with `scipy.stats`. That covers what a distribution object is, the two ways to give it parameters, the methods Students use (`pdf`, `pmf`, `cdf`, `sf`, `ppf`, `rvs`, `mean`, `std`, `interval`), the common continuous and discrete distributions with their parameters, and plotting them. The Author says Students are "really confused" by two things, so the content must make both clear:

1. **The two calling styles.** Students call methods on the distribution object with the parameters each time (`stats.uniform.rvs(loc=2, scale=3, size=5)`), and they also create a frozen distribution once (`U = stats.uniform(loc=2, scale=3)`) and then call `U.rvs(size=5)` with no `loc` or `scale`. They mix the two up.
2. **Plotting.** Students draw a random sample for a histogram, then use those same random points as `x` when they plot `pdf`, and get a mess.

Decided with the Author (every recommendation accepted):

- **Scope:** distributions only. The planned Topics *t-tests* and *Correlation* stay planned for a later ticket.
- **Setup:** add SciPy with `uv add scipy` (pinned in `uv.lock`) and add it to `EXAMPLE_LIBRARIES` in `cheatsheet/build.py`, so the footer shows its version next to NumPy and Matplotlib. Update the test that lists those versions (`test_meta_lists_the_versions_examples_ran_with`) and the authoring guide's "Libraries" line.
- **Imports:** always `from scipy import stats`, then `stats.norm`, `stats.uniform`, … This avoids clashes with names like `t` or `norm` in Students' own code. *A distribution object* mentions once that `from scipy.stats import norm` does the same, since Students will see it elsewhere.
- **Classic interface only:** use the `stats.norm` style that courses and answers online use. Don't teach or mention SciPy 1.15's newer class-based style (`stats.Normal(mu=..., sigma=...)`); a third style would add to the confusion.
- **The frozen style is the default:** apart from *Parameters in every call*, every example freezes the distribution first (`d = stats.norm(loc=170, scale=8)`) and then calls its methods. Say why once, in *A frozen distribution*: the parameters are given once, so they can't drift apart between `pdf`, `cdf` and `rvs`.
- **Randomness:** `rvs` always gets `random_state=rng` with `rng = np.random.default_rng(<seed>)`, the same habit as the NumPy Area.
- **Topics,** in this Topic order. The Area keeps hue 320. The planned Topic `distributions` (glyph `pdf`) becomes the first Topic; the three new ones get glyphs chosen per the authoring guide. `t-tests` and `correlation` stay planned, after them.
  1. Distributions (`distributions`, *Rozkłady*)
  2. Continuous distributions (`continuous-distributions`, *Rozkłady ciągłe*)
  3. Discrete distributions (`discrete-distributions`, *Rozkłady dyskretne*)
  4. Plotting distributions (`plotting-distributions`, *Wykresy rozkładów*)
- **Entries** (22), with these English titles; the Polish titles are the agent's:
  - **Distributions:**
    - A distribution object: `stats.norm` is an object, not a function, and its methods take the parameters. Shown on the standard normal with no parameters, e.g. `stats.norm.cdf(1.96)`.
    - Parameters in every call: `stats.uniform.rvs(loc=2, scale=3, size=5, random_state=rng)`, and `pdf` / `cdf` with the same `loc` and `scale` repeated.
    - A frozen distribution: `U = stats.uniform(loc=2, scale=3)`, then `U.rvs(size=5, random_state=rng)`, `U.pdf(x)` and `U.cdf(x)`. Use the same seed and parameters as the previous Entry, so the Output matches it. The explanation names the term: calling the distribution object with parameters gives a new, *frozen* distribution. **Pitfall:** passing `loc=` or `scale=` again to a frozen distribution's method raises `TypeError`.
    - Density and probabilities: `pdf` (continuous) or `pmf` (discrete), `cdf` for P(X ≤ x), and `sf` for P(X > x), i.e. `1 - cdf`.
    - Quantiles with ppf: the inverse of `cdf`, e.g. `stats.norm().ppf(0.975)` ≈ 1.96, critical values.
    - Random samples with rvs: `size=` and `random_state=rng`. Link both ways to NumPy Random's *Normal samples*.
    - Mean, spread and intervals: `d.mean()`, `d.std()`, `d.var()`, `d.interval(0.95)`.
  - **Continuous distributions:**
    - Shape, loc and scale: every continuous distribution is a standard one moved by `loc` and stretched by `scale`; shape parameters such as `df` come first, before `loc` and `scale`.
    - Normal distribution: `stats.norm(loc=μ, scale=σ)`. `scale` is the standard deviation, not the variance (explanation or Pitfall).
    - Uniform distribution: U(a, b) is `stats.uniform(loc=a, scale=b - a)`. **Pitfall:** `stats.uniform(2, 5)` is U(2, 7), not U(2, 5).
    - Exponential distribution: rate λ is `stats.expon(scale=1/λ)`. Say plainly that SciPy wants the scale, not the rate.
    - Student's t distribution: `stats.t(df)`; heavier tails than the normal, approaching it as `df` grows. The later t-tests Topic will rely on it.
    - Chi-squared distribution: `stats.chi2(df)`.
  - **Discrete distributions:**
    - Binomial distribution: `stats.binom(n, p)`; Bernoulli is the case `n=1`. **Pitfall:** a discrete distribution has no `.pdf`, only `.pmf` (`AttributeError`).
    - Poisson distribution: `stats.poisson(mu)`.
    - Geometric distribution: `stats.geom(p)` counts the trials up to and including the first success, so its values start at 1.
    - Discrete uniform distribution: `stats.randint(low, high)`; `high` is not included (a die is `stats.randint(1, 7)`).
  - **Plotting distributions** (each draws a figure):
    - A pdf curve: `x = np.linspace(d.ppf(0.001), d.ppf(0.999), 200)` and `plt.plot(x, d.pdf(x))`. The explanation says that `x` is an evenly spaced, sorted grid chosen by you.
    - A histogram with the pdf: a sample from `d.rvs(...)` drawn with `plt.hist(sample, density=True)`, with `d.pdf(x)` on a `linspace` grid over it. Say why `density=True`: it makes the bars' area 1, so they match the pdf's scale. **Pitfall, with code and figure:** `plt.plot(sample, d.pdf(sample))` uses the random, unsorted sample as `x`, so the line zigzags back and forth across the plot. This is the exact mistake the Author describes; the figure must show the mess, and the text says to plot the pdf on a `linspace` grid instead.
    - A pmf as bars: `k = np.arange(...)` and `plt.bar(k, d.pmf(k))`, with a sample's relative frequencies beside or over it.
    - The cdf: a continuous cdf as a curve and a discrete one as steps (`plt.step(..., where="post")`).
    - Comparing parameters: several pdf curves of one distribution with different parameters, and a legend with language-neutral labels such as `σ = 1`.
- **Figures** follow ticket 16's rules: one figure per example with `plt.figure(figsize=(6, 3.5))`, the default style, `plt.show()` at the end, the `plt` style, language-neutral text in the figure, and a figure description in both Languages for every figure (including the Pitfall's).
- **Links:** two-way See-also links with Matplotlib Histograms' *Density with a PDF on top* and NumPy Random's *Normal samples* (and other NumPy or Matplotlib Entries where natural). At most three links per Entry.

Conventions from tickets 12–16 apply: Outputs show values, not English sentences; inline code is the same in both Languages; a blank line follows a compound block so examples paste into the `python` REPL; "Polish term (English term)" at first mention, e.g. "rozkład zamrożony (frozen distribution)", "kwantyl (quantile)", "dystrybuanta (cdf)", "gęstość (pdf)"; NumPy numbers are printed on their own or in f-strings, rounded where needed.

**Blocked by:** none. Tickets 14 and 16 (NumPy and Matplotlib) are merged, and the See-also links point at them.

**Status:** resolved

- [x] SciPy is installed with uv and pinned, it is in `EXAMPLE_LIBRARIES`, the footer shows its version, and the tests and authoring guide are updated to match.
- [x] The SciPy stats Area is no longer planned and has the four Topics above in this Topic order, followed by the planned *t-tests* and *Correlation*, with hue 320, the Polish Topic titles above and a distinct glyph for each Topic.
- [x] The 22 Entries exist with the decided English titles, each with Polish, including the Pitfalls named above (`loc=` again on a frozen distribution, `stats.uniform(2, 5)`, `.pdf` on a discrete distribution, the sample used as `x`).
- [x] Examples use `from scipy import stats` and the classic interface; every example except *Parameters in every call* freezes the distribution first; `rvs` always gets a seeded `default_rng` as `random_state`.
- [x] Every figure follows ticket 16's figure rules and has a description in both Languages; the sample-as-`x` Pitfall's figure visibly shows the zigzag mess.
- [x] Two-way See-also links connect the new Entries with the related NumPy and Matplotlib Entries.
- [x] Every example runs alone with `uv run python` in an empty folder with `MPLBACKEND=Agg`, with no warnings on stderr, and pastes into the REPL.
- [x] `uv run cheatsheet build` and `uv run pytest` pass.
- [x] The new Topics were looked at on the Map, the Trail and the Topic pages in both Languages in `uv run cheatsheet serve`.
- [x] The Comments list every Entry with its Polish title and figure description for the Author to skim.
- [x] One session and one PR, which also adds this ticket file.

## Comments

**Resolved** in the PR that adds this ticket file. The SciPy stats Area is no longer planned: four Topics, 22 Entries and 7 figures (6 Entries and 1 Pitfall), each figure with a description in English and Polish, followed by the planned *t-tests* and *Correlation*. SciPy 1.18.1 is pinned in `uv.lock` and shows in the footer next to NumPy and Matplotlib. The Area blurb now names what it covers.

Every Entry with its Polish title, and the English figure description where there is a figure (the Polish descriptions say the same):

- **Distributions** / *Rozkłady* (glyph `pdf`)
  - *A distribution object* / *Obiekt rozkładu*
  - *Parameters in every call* / *Parametry w każdym wywołaniu*
  - *A frozen distribution* / *Rozkład zamrożony* (Pitfall with code: `loc=` again raises `TypeError`)
  - *Density and probabilities* / *Gęstość i prawdopodobieństwa*
  - *Quantiles with ppf* / *Kwantyle z ppf*
  - *Random samples with rvs* / *Próbki losowe z rvs*
  - *Mean, spread and intervals* / *Średnia, rozrzut i przedziały*
- **Continuous distributions** / *Rozkłady ciągłe* (glyph `norm`)
  - *Shape, loc and scale* / *Kształt, loc i scale*
  - *Normal distribution* / *Rozkład normalny* (Pitfall with code: `scale=var` gives a variance of 16 for 4)
  - *Uniform distribution* / *Rozkład jednostajny* (Pitfall with code: `stats.uniform(2, 5)` runs from 2.0 to 7.0)
  - *Exponential distribution* / *Rozkład wykładniczy*
  - *Student's t distribution* / *Rozkład t Studenta*
  - *Chi-squared distribution* / *Rozkład chi-kwadrat*
- **Discrete distributions** / *Rozkłady dyskretne* (glyph `binom`)
  - *Binomial distribution* / *Rozkład dwumianowy* (Pitfall with code: `coin.pdf(5)` raises `AttributeError`)
  - *Poisson distribution* / *Rozkład Poissona*
  - *Geometric distribution* / *Rozkład geometryczny*
  - *Discrete uniform distribution* / *Dyskretny rozkład jednostajny*
- **Plotting distributions** / *Wykresy rozkładów* (glyph `f(x)`)
  - *A pdf curve* / *Krzywa gęstości*: A smooth bell curve from about 145 to 195, peaking at 170 at a height of about 0.05.
  - *A histogram with the pdf* / *Histogram z gęstością*: Twenty-five bars in a rough bell shape around 170, from about 147 to 192, with a smooth bell curve drawn over them that follows their tops, peaking near 0.05. Pitfall: The same histogram covered by a tangle of straight lines that zigzag back and forth between points on the bell curve, filling the whole area under it.
  - *A pmf as bars* / *Funkcja prawdopodobieństwa jako słupki*: Pairs of bars for k = 0 to 10 with a legend, P(X = k) and n = 200: both rise to the tallest pair at 3, about 0.27 and 0.29, then fall to almost nothing from 7 up, and each sample bar stays close to its partner.
  - *The cdf* / *Dystrybuanta*: Two plots side by side: on the left, N(0, 1), a smooth S-shaped curve rising from 0 to 1 between −3 and 3; on the right, B(10, 0.5), a staircase rising from 0 to 1 over 0 to 10, with the biggest steps around 5.
  - *Comparing parameters* / *Porównanie parametrów*: Three curves for x from 0 to 20 with a legend, df = 2, df = 4 and df = 8: the df = 2 curve falls from 0.5 at 0, df = 4 peaks near 2 at about 0.18, and df = 8 peaks near 6 at about 0.11, with a long tail to the right.

Decisions made while writing:

- **A distribution object** calls methods on `stats.norm` itself with no parameters (`stats.norm.cdf(1.96)`, as the ticket's Entry list says), so it is a second Entry besides *Parameters in every call* that doesn't freeze. With no parameters there is nothing to freeze. Every other example freezes first, including inline ones such as `stats.t(df)` in a loop.
- **The two calling styles:** *Parameters in every call* and *A frozen distribution* use the same seed (7) and parameters, and both Outputs start with `[3.88 4.69 4.33 2.68 2.9 ]`, `0.333…` and `0.5`. *Parameters in every call* also prints `stats.uniform.cdf(x)` without `loc` and `scale`, which quietly gives `1.0` from U(0, 1): the drift the frozen style prevents. The frozen Pitfall prints a working `U.cdf(3.5)` before the `TypeError`.
- **Comparing parameters** uses the chi-squared distribution with `df = 2, 4, 8`, not normal curves with `σ = …`, because Matplotlib's *Several lines and a legend* already draws normal curves for σ = 0.5, 1 and 2. The labels are language-neutral (`df = 2`).
- **The cdf** draws N(0, 1) and B(10, 0.5) side by side with `plt.subplot(121)` and `plt.subplot(122)`, titled with those names, so the curve and the steps each get a fitting x-axis.
- **A histogram with the pdf** and its Pitfall use the same 500 values (seed 12, 25 bins), so the Pitfall's figure is the Entry's histogram with the zigzag tangle over it.
- **Random samples with rvs** uses seed 7 and `stats.norm(loc=170, scale=10)`, like NumPy's *Normal samples*, and gives the same first values `[170. 173. 167.3 161.1]`. The text doesn't claim this, since it depends on how SciPy draws.
- **Exponential distribution** says in the explanation that SciPy wants the scale, the mean 1/λ, rather than the rate; it has no Pitfall.
- **Poisson distribution** notes that for a discrete distribution `sf(k)` is P(X > k), so `calls.sf(5)` is "6 or more", because that off-by-one is easy to miss.
- **Polish terms:** rozkład zamrożony (frozen distribution), gęstość (pdf), funkcja prawdopodobieństwa (pmf), dystrybuanta (cdf), funkcja przeżycia (survival function), kwantyl (quantile), wartości krytyczne (critical values), parametry kształtu (shape parameters), intensywność (rate), stopnie swobody (degrees of freedom), cięższe ogony (heavier tails). Numbers in Polish prose use the decimal comma (1,96); code stays as it is.
- **Links into the planned t-tests Topic** (from *Student's t distribution* and *Quantiles with ppf*) are left for the ticket that writes it.

Other changes:

- **See also, two-way:** *Random samples with rvs* ↔ Random's *Normal samples*; *A histogram with the pdf* ↔ Histograms' *Density with a PDF on top*; *Discrete uniform distribution* ↔ Random's *Uniform numbers and integers*; *A pmf as bars* ↔ Bar charts' *A probability mass function*; *Comparing parameters* ↔ Plotting basics' *Several lines and a legend*. One-way: *Random samples with rvs* → *A generator with a seed*; *Mean, spread and intervals* → *Standard deviation and variance*; *Normal distribution* → *Normal samples*; *Uniform distribution* → *Uniform numbers and integers*; *A pdf curve* → *A line plot* and Arrays' *Ranges*; *The cdf* → *Side-by-side plots with plt.subplot(121)*. Within the Area, links join the Distributions Entries to the Continuous, Discrete and Plotting Entries that show them. The NumPy and Matplotlib edits touch only See-also lists, and no Entry has more than three links.
- **Setup:** `uv add scipy`; `EXAMPLE_LIBRARIES` gains `"SciPy": "scipy"`; `test_meta_lists_the_versions_examples_ran_with` expects it; the authoring guide's Libraries line says "NumPy, Matplotlib and SciPy".
- **Checked:** all 27 examples (22 Entries, 5 Pitfalls with code) ran alone with `uv run python` in an empty folder with `MPLBACKEND=Agg`, each figure also rendered to SVG; stderr was empty apart from Agg's "non-interactive" notice, and the two `raises=` examples ended in the marked error. Each was also fed line by line to `code.InteractiveConsole` like a REPL paste, with the same printed lines. Code lines are at most 43 characters (39 in a Pitfall). `uv run cheatsheet build` and `uv run pytest` (210 tests) pass. Every figure was looked at against its description. The Map, the Trail and the Topic pages were looked at in `uv run cheatsheet serve` in both Languages, and the Pitfall figure's accessible name was the Polish description with `?lang=pl`.
