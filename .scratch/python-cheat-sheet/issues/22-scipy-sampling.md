# 22: SciPy stats Sampling Topic

**What to build:** Students often need to draw samples from a distribution, but `rvs` examples are scattered across the SciPy stats Entries, and nothing on the Map says "sampling". A new Topic, **Sampling**, gathers it: drawing samples from any distribution, 1-D and 2-D arrays of samples, aggregating over an axis (a repeat of NumPy's *Along an axis*, with SciPy), and estimating probabilities by simulation.

Decided with the Author (every recommendation accepted):

- **Where:** a new Topic, `sampling`, **Sampling** (*Losowanie próby*), in the SciPy stats Topic order after *Discrete distributions* and before *Plotting distributions*. Choose a distinct glyph per the authoring guide.
- **It takes over the sampling Entries.** *Random samples with rvs* and *Reproducible samples* move from Distributions into Sampling, as its first and last Entries.
  - Their ids become `sampling/...`, so update every See-also link to them (in SciPy, NumPy, Matplotlib).
  - Distributions keeps its methods overview. *Density and probabilities*, or another fitting Entry, says that `rvs` draws samples, with a See-also link to Sampling.
  - Update Distributions' Topic summary in both Languages.
- **Entries** (6), with these English titles; the Polish titles are the agent's:
  - **Random samples with rvs** (moved): `d.rvs(size=n)` gives a 1-D array, and its sample mean sits near `d.mean()`.
  - **Sampling any distribution:** the same `rvs(size=...)` on a normal, a uniform, a binomial and a Poisson distribution, and what each gives back: decimals or whole numbers.
  - **A matrix of samples:** `size=(1000, 10)` is 1000 repeats of a sample of 10, one per row.
  - **Statistics of many samples:**
    - `samples.mean(axis=1)` gives the 1000 sample means. Their standard deviation is close to σ/√n, the standard error.
    - **Pitfall:** `axis=0` gives one value per column (10 values), not one per sample.
    - See-also links both ways with NumPy Aggregates' *Along an axis*.
  - **Estimating probabilities by simulation:** `(sample > 2).mean()` estimates P(X > 2), next to the exact `d.sf(2)`. See-also link with NumPy Aggregates' *Counting and proportions with a mask*.
  - **Reproducible samples** (moved), as ticket 21 leaves it.
- **Style:** as ticket 21 leaves the SciPy Topics.
  - Frozen distributions, `from scipy import stats`, and `rvs` with no `random_state`, seeded by a hidden `np.random.seed(<n>)  #| hide` (ticket 20's markers).
  - NumPy numbers printed on their own or in f-strings, rounded where needed.
  - Text Outputs mostly. If an Entry draws a figure, it follows ticket 16's figure rules and gets a figure description in both Languages.
- **Links:** See-also links with Plotting distributions' *A histogram with the pdf*, and with NumPy Random and Aggregates Entries where natural. At most three per Entry.

Conventions from tickets 12–21 apply: Outputs show values, not English sentences; a blank line follows a compound block; "Polish term (English term)" at first mention, e.g. "próba losowa (random sample)", "błąd standardowy (standard error)".

**Blocked by:** 21 (Random numbers with the `np.random.*` functions), because both edit the SciPy stats files and this Topic is written in ticket 21's style.

**Status:** ready-for-agent

- [ ] The Sampling Topic exists in the decided place, with its Polish title and a distinct glyph, and the six Entries with the decided English titles, each with Polish, including the `axis=0` Pitfall.
- [ ] *Random samples with rvs* and *Reproducible samples* live only in Sampling, every link to them works, and Distributions points to Sampling.
- [ ] Examples follow ticket 21's style, with hidden seeds; Outputs show what the explanations promise.
- [ ] See-also links connect Sampling with NumPy Aggregates and Random, and with Plotting distributions.
- [ ] Every example runs alone with `uv run python` in an empty folder (with its hidden lines), with no warnings, and pastes into the REPL.
- [ ] `uv run cheatsheet build` and `uv run pytest` pass; the Topic was looked at on the Map and its page in both Languages in `uv run cheatsheet serve`.
- [ ] The Comments list every Entry with its Polish title.
- [ ] One session and one PR.

## Comments
