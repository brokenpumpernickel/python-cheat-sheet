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

**Status:** resolved

- [x] The Sampling Topic exists in the decided place, with its Polish title and a distinct glyph, and the six Entries with the decided English titles, each with Polish, including the `axis=0` Pitfall.
- [x] *Random samples with rvs* and *Reproducible samples* live only in Sampling, every link to them works, and Distributions points to Sampling.
- [x] Examples follow ticket 21's style, with hidden seeds; Outputs show what the explanations promise.
- [x] See-also links connect Sampling with NumPy Aggregates and Random, and with Plotting distributions.
- [x] Every example runs alone with `uv run python` in an empty folder (with its hidden lines), with no warnings, and pastes into the REPL.
- [x] `uv run cheatsheet build` and `uv run pytest` pass; the Topic was looked at on the Map and its page in both Languages in `uv run cheatsheet serve`.
- [x] The Comments list every Entry with its Polish title.
- [x] One session and one PR.

## Comments

- **Topic:** `content/scipy-stats/sampling.md`, *Sampling* / *Losowanie próby*, glyph `rvs`, between *Discrete distributions* and *Plotting distributions* in the SciPy stats Topic order. Summary: "Random samples with rvs: any distribution, a matrix of samples, statistics of many samples, probabilities by simulation, reproducible samples." / "Losowanie próby (sampling) z rvs: dowolny rozkład, macierz prób, statystyki wielu prób, prawdopodobieństwa z symulacji, powtarzalne próby."
- **Entries** (English / Polish):
  - *Random samples with rvs* / *Próba losowa z rvs* (moved, `sampling/random-samples-with-rvs`)
  - *Sampling any distribution* / *Losowanie z dowolnego rozkładu*
  - *A matrix of samples* / *Macierz prób*
  - *Statistics of many samples* / *Statystyki wielu prób*, with the `axis=0` Pitfall
  - *Estimating probabilities by simulation* / *Szacowanie prawdopodobieństw symulacją*
  - *Reproducible samples* / *Powtarzalne próby* (moved, `sampling/reproducible-samples`)
- **Moved Entries:** gone from Distributions. Links updated: NumPy Random's *Setting a seed* and *Normal samples*, and Plotting distributions' *A histogram with the pdf* (no Matplotlib Entry linked to them). Distributions' summary drops "samples" in both Languages, and *Density and probabilities* gains a sentence, "To draw random values from the distribution instead, use `d.rvs(size=n)`.", with a See-also link to `sampling/random-samples-with-rvs`.
- **Links:** *Statistics of many samples* ↔ Aggregates' *Along an axis* (both ways); *Estimating probabilities by simulation* → Aggregates' *Counting and proportions with a mask* (one way, as the ticket says; that Entry already has four links); *Random samples with rvs* ↔ *A histogram with the pdf*; NumPy Random's *Normal samples*, *Setting a seed*, *Uniform numbers and integers* and *Simulating an experiment* are linked from Sampling. Every Sampling Entry has at most three links.
- Decisions:
  - **"Próba", not "próbka":** the Polish Topic title is *Losowanie próby*, so the Polish text uses "próba losowa (random sample)" throughout, and the moved Entries' Polish titles changed from *Próbki losowe z rvs* / *Powtarzalne próbki* to *Próba losowa z rvs* / *Powtarzalne próby*. The English titles and ids are as decided. NumPy Random's "próbki" were left as they are.
  - **Random samples with rvs** now also prints `sample.shape`, `d.mean()` and `d.std()` beside the sample's, to show the 1-D array and the sample mean near `d.mean()` (same seed, 11, so the sample is unchanged).
  - **Sampling any distribution** prints each sample's `dtype` with it (`float64` for `norm` and `uniform`, `int64` for `binom` and `poisson`), so the Output shows decimals versus whole numbers.
  - **A matrix of samples**, **Statistics of many samples** and its Pitfall share seed 6 and N(170, 10²): the 1000 sample means have a standard deviation of 3.14 against σ/√n = 3.16, and the Pitfall's 10 column means all sit between 169.8 and 170.6, a plausible-looking wrong answer.
  - **Estimating probabilities by simulation** uses N(0, 1) and 100 000 values (seed 12): 0.0227 against `d.sf(2)` = 0.02275, plus P(−1 < X < 1) with `&`, 0.68297 against 0.68269.
  - Seeds were searched for in a script, picking typical results. Text Outputs only; no figures.
- All seven examples (six Entries and the Pitfall) were run alone with `uv run python -W default` in their own empty folders, with no warnings; the build's Outputs match those runs. The one compound block (the `for` loop) is last in its example, so it pastes into the REPL.
- `uv run cheatsheet build` and `uv run pytest` (237 tests) pass, run one after the other. In `uv run cheatsheet serve` the `rvs` bubble shows on the SciPy stats island, and the Sampling page was read in English and Polish: no seed shown except in *Reproducible samples*, Outputs as above, See-also links working, Previous stop *Discrete distributions* and Next stop *Plotting distributions*.
