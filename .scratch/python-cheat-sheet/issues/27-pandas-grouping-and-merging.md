# 27: pandas Grouping and Joining tables Topics

**What to build:** Two pandas Topics that ticket 24 left planned. **Grouping** covers `groupby` with sizes, means, several statistics, named aggregations, two keys, the first row per group, and keeping the largest groups. **Joining tables** covers `merge` and `concat`. They are the last analysis steps of the lab notebook, where the UFO sightings per state are joined with a second table.

Decided with the Author (every recommendation accepted). The English titles are decided; the Polish titles are the agent's.

- **Grouping** (`grouping`). The Entries:
  - **Group sizes:** `df.groupby("group").size()`.
  - **A column's mean per group:** `df.groupby("group")["score"].mean()`.
  - **Several statistics with agg:** `agg(["mean", "std", "count"])` on one column, and `agg({"score": "mean", "height": "median"})`.
  - **Named aggregations:** `agg(mean_score=("score", "mean"), n=("score", "size"))`.
  - **The group as an index or as a column:**
    - The result's index is the groups, so `result.loc["A"]` picks one.
    - `reset_index()` makes the group a column again.
  - **Grouping by two columns:** `groupby(["group", "sex"])`, the two-level index it gives, and `reset_index()`.
  - **The latest row per group:** `df.sort_values("year", ascending=False).groupby("state").first()`, as in the notebook.
  - **Keeping the largest groups:**
    - `top = df.groupby("shape").size().nlargest(3).index`, then `df[df["shape"].isin(top)]`.
    - Use `nlargest` rather than the notebook's `sort_values(ascending=False)[:5]`, or show both if it reads better.
- **Joining tables** (`merging`). The Entries:
  - **merge on a shared column:** `pd.merge(a, b, on="state")` or `a.merge(b, on="state")`.
  - **Different column names:** `left_on="location_state", right_on="State"`, and that both columns stay.
  - **Keeping unmatched rows:** `how="left"`, and the NaN it gives.
    - **Pitfall:** the default inner join quietly drops the rows with no match. Compare `len` before and after.
  - **Stacking rows with concat:** `pd.concat([a, b])`, and `ignore_index=True` to renumber.
- **Style:** as ticket 24 decided for the pandas Area. Small made-up tables, e.g. states with counts and populations, built inside each example. No `us` package.
- **Links:**
  - Ticket 25's *Counting and proportions with a mask*, *Sorting* and *isin* Entries (parallel: list them under Links to add later).
  - Ticket 26's *Missing values* (for the NaN after a left join; parallel: list it under Links to add later).
  - SciPy stats Sampling's *Statistics of many samples* or NumPy Aggregates' *Along an axis*, where a per-group statistic echoes them.
  - At most three per Entry. No links into planned Topics.

Conventions from tickets 12–24 apply:
- Outputs show values, not English sentences.
- A blank line follows a compound block.
- "Polish term (English term)" at first mention, e.g. "grupowanie (grouping)", "agregacja (aggregation)", "złączenie (join)".

**Running in parallel:** tickets 25–28 run at the same time, each in its own session and PR, all starting from `main` after ticket 24.
- **Edit only your own Topic files.** Make back-links (a See-also added to an Entry outside your Topics) only where the ticket asks for them, and keep them few. Two PRs editing the same Entry would conflict.
- **Link only to Entries that are on `main` or in your own Topics.** The other parallel tickets' Topics are still planned on `main`, and a link into a planned Topic fails the build.
- **List the links you'd add into the other parallel tickets' Topics** under a **Links to add later** heading in the Comments, as `your-topic/entry → other-topic/entry`. They're added in one pass after all four PRs are merged.
- **If `main` moves:** If another of these PRs is merged first and yours then conflicts, bring your branch up to date with `main` and resolve it. Don't push to a merged PR's branch.

**Blocked by:** 24 (resolved, PR #35).

**Status:** resolved

- [x] Grouping and Joining tables are written (no longer planned), each with a summary in both Languages, and the decided Entries with their English titles and Polish.
- [x] The inner-join Pitfall is there.
- [x] Every example runs alone with `uv run python` in an empty folder, with no warnings, and pastes into the REPL.
- [x] `uv run cheatsheet build` and `uv run pytest` pass. Both pages were looked at in both Languages in `uv run cheatsheet serve`.
- [x] The Comments list every Entry with its Polish title, plus any decisions made on the way.
- [x] One session and one PR.

## Comments

- Resolved by PR #38: https://github.com/brokenpumpernickel/python-cheat-sheet/pull/38.
- **Topics** (English / Polish, glyph kept):
  - `grouping`: *Grouping* / *Grupowanie*, `group`. Summary: "Statistics per group with groupby: group sizes, means, several statistics, named aggregations, two keys, the latest row per group and the largest groups." / "Grupowanie (grouping) przez groupby i statystyki w grupach: liczebności grup, średnie, kilka statystyk naraz, nazwane agregacje, dwa klucze, najnowszy wiersz w grupie i największe grupy."
  - `merging`: *Joining tables* / *Łączenie tabel*, `merge`. Summary: "Two tables into one: merge on a shared column or on columns with different names, keeping unmatched rows, and stacking rows with concat." / "Dwie tabele w jedną: złączenie (join) przez merge po wspólnej kolumnie lub po kolumnach o różnych nazwach, zachowanie wierszy bez dopasowania i sklejanie wierszy przez concat."
- **Entries** (English / Polish):
  - Grouping:
    - *Group sizes* / *Liczebności grup*: `size()` beside `value_counts()`, to show sorted groups against largest first
    - *A column's mean per group* / *Średnia kolumny w grupach* (Entry id `a-column-s-mean-per-group`)
    - *Several statistics with agg* / *Kilka statystyk przez agg*
    - *Named aggregations* / *Nazwane agregacje*
    - *The group as an index or as a column* / *Grupa jako indeks albo kolumna*
    - *Grouping by two columns* / *Grupowanie po dwóch kolumnach*
    - *The latest row per group* / *Najnowszy wiersz w grupie*
    - *Keeping the largest groups* / *Tylko największe grupy*
  - Joining tables:
    - *merge on a shared column* / *merge po wspólnej kolumnie*
    - *Different column names* / *Różne nazwy kolumn*
    - *Keeping unmatched rows* / *Zachowanie wierszy bez dopasowania*, with the inner-join Pitfall (`4 3`, then the table without `AK`)
    - *Stacking rows with concat* / *Sklejanie wierszy przez concat*
- **Links:** *Group sizes* → Exploring's *value_counts*; *A column's mean per group* → *Column statistics* and NumPy Aggregates' *Along an axis*; *Several statistics with agg* → *Column statistics* and Aggregates' *Standard deviation and variance* (the `n - 1`); *The group as an index or as a column* ↔ *merge on a shared column*. SciPy Sampling's *Statistics of many samples* was left out: *Along an axis* is the closer echo, and it already links there. No back-links outside these two Topics.
- **Links to add later** (into ticket 25's and 26's Topics):
  - `grouping/group-sizes → filtering/counting-and-proportions-with-a-mask`
  - `grouping/the-latest-row-per-group → sorting/descending-and-by-several-columns`
  - `grouping/keeping-the-largest-groups → filtering/isin`
  - `grouping/keeping-the-largest-groups → sorting/nlargest-and-nsmallest`
  - `merging/keeping-unmatched-rows → missing-values/finding-missing-values`
  - `merging/different-column-names → columns/dropping-columns`
- Decisions:
  - **Titles kept as decided** although three run past the guide's four words (*The group as an index or as a column*, *A column's mean per group*, *merge on a shared column*); ticket 24's *A DataFrame from a dictionary* already does the same.
  - **Data:** the Grouping Entries share one six-row students table (groups A×2, B×4, so `size()` and `value_counts()` order differently; `sex` added for two keys), with only the columns each Entry needs. The notebook-like Entries use small UFO tables (state, year, shape). Joining tables uses sightings and populations (in millions) for CA, TX and NY; the unmatched row is `AK`. All built inline.
  - **Keeping the largest groups** uses `nlargest(2)` on five shapes rather than `nlargest(3)`, so the filter visibly drops rows (5 of 8 kept). It prints the sizes, then the rows; the notebook's `sort_values(ascending=False)[:2]` is named in the explanation as the same thing.
  - **The latest row per group** says that `.first()` takes each column's first non-missing value, so a gap is filled from an older row. The example has no gap; that would need Missing values first.
  - **Different column names** also prints `joined.drop(columns="State")`, since both key columns staying is the point and dropping the copy is the next thing Students do.
  - **merge on a shared column** prints `pd.merge(...)` and checks that `a.merge(...)` `.equals` it, rather than printing the same table twice; `b` lists the states in another order, to show that order doesn't matter.
  - **Polish terms:** grupowanie (grouping), agregacja (aggregation), nazwane agregacje (named aggregations), złączenie (join), złączenie lewostronne (left join), złączenie wewnętrzne (inner join), sklejanie (concatenation), dwupoziomowy indeks (MultiIndex).
  - **Line length:** code boxes at 1280 px fit 44 characters (45 scrolls), so every shown line keeps to 44. That is why several examples wrap their lists and calls, the agg Entry names `groups` and the list of statistics, and its last DataFrame line has no trailing comma.
- All 13 examples (12 Entries and 1 Pitfall) were run alone with `uv run python -W default` in their own empty folders: no warnings. Each was also pasted line by line into `code.InteractiveConsole`: no errors.
- `uv run cheatsheet build` and `uv run pytest` (248 tests) pass, run one after the other. Both pages were checked in English and Polish with a Playwright script through `uv run python` against `uv run cheatsheet serve`: no code box scrolls sideways, no console errors; on the Trail, Grouping follows Exploring data (the planned Topics are skipped) and Joining tables leads on to Matplotlib's Plotting basics.
