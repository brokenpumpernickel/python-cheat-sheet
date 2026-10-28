---
title: Grouping
glyph: "group"
summary: "Statistics per group with groupby: group sizes, means, several statistics, named aggregations, two keys, the latest row per group and the largest groups."
pl:
  title: Grupowanie
  summary: "Grupowanie (grouping) przez groupby i statystyki w grupach: liczebności grup, średnie, kilka statystyk naraz, nazwane agregacje, dwa klucze, najnowszy wiersz w grupie i największe grupy."
---

## Group sizes

PL: Liczebności grup

`df.groupby("group").size()` splits the rows by the values of `group` and counts the rows in each group. The result is a Series indexed by the groups in sorted order, while `value_counts()` puts the largest group first.

PL: `df.groupby("group").size()` dzieli wiersze według wartości kolumny `group`, czyli grupuje je (grouping), i zlicza wiersze w każdej grupie. Wynikiem jest seria (Series) z grupami jako indeksem (index), posortowanymi po nazwie, a `value_counts()` stawia największą grupę na początku.

```python
import pandas as pd

df = pd.DataFrame({
    "group": ["A", "B", "B", "A", "B", "B"],
})
print(df.groupby("group").size())
print(df["group"].value_counts())
```

### See also

- exploring/value-counts

## A column's mean per group

PL: Średnia kolumny w grupach

`df.groupby("group")["score"].mean()` gives the mean score of each group, one value per group. Any column statistic works the same way: `.median()`, `.std()`, `.min()`, `.max()`, `.sum()` or `.count()`.

PL: `df.groupby("group")["score"].mean()` daje średni wynik każdej grupy, jedną wartość na grupę. Tak samo działa każda statystyka kolumny: `.median()`, `.std()`, `.min()`, `.max()`, `.sum()` czy `.count()`, liczona osobno w każdej grupie (grouping).

```python
import pandas as pd

df = pd.DataFrame({
    "group": ["A", "B", "B", "A", "B", "B"],
    "score": [72, 85, 90, 64, 78, 70],
})
print(df.groupby("group")["score"].mean())
print(df.groupby("group")["score"].max())
```

### See also

- exploring/column-statistics
- aggregates/along-an-axis

## Several statistics with agg

PL: Kilka statystyk przez agg

`.agg(["mean", "std", "count"])` on one column gives a table with one column per statistic. A dictionary, `.agg({"score": "mean", "height": "median"})`, gives each column its own statistic. As for a whole column, `"std"` divides by `n - 1`.

PL: `.agg(["mean", "std", "count"])` na jednej kolumnie daje tabelę z jedną kolumną na statystykę; to agregacja (aggregation) kilkoma funkcjami naraz. Słownik, `.agg({"score": "mean", "height": "median"})`, daje każdej kolumnie jej własną statystykę. Tak jak dla całej kolumny, `"std"` dzieli przez `n - 1`.

```python
import pandas as pd

df = pd.DataFrame({
    "group": ["A", "B", "B", "A", "B", "B"],
    "score": [72, 85, 90, 64, 78, 70],
    "height": [165, 181, 168, 178, 161, 176]
})
groups = df.groupby("group")
stats = ["mean", "std", "count"]
print(groups["score"].agg(stats).round(2))
print(groups.agg({"score": "mean",
                  "height": "median"}))
```

### See also

- exploring/column-statistics
- aggregates/standard-deviation-and-variance

## Named aggregations

PL: Nazwane agregacje

`.agg(mean_score=("score", "mean"), n=("score", "size"))` names the result's columns yourself: each keyword is a new column's name, and its pair gives the column to use and the statistic. `"size"` counts every row of the group, `"count"` only the values that aren't missing.

PL: `.agg(mean_score=("score", "mean"), n=("score", "size"))` to nazwane agregacje (named aggregations): sam nadajesz nazwy kolumnom wyniku. Każdy argument to nazwa nowej kolumny, a jego para podaje kolumnę i statystykę. `"size"` zlicza wszystkie wiersze grupy, a `"count"` tylko wartości, których nie brakuje.

```python
import pandas as pd

df = pd.DataFrame({
    "group": ["A", "B", "B", "A", "B", "B"],
    "score": [72, 85, 90, 64, 78, 70],
})
result = df.groupby("group").agg(
    mean_score=("score", "mean"),
    n=("score", "size"),
)
print(result)
```

## The group as an index or as a column

PL: Grupa jako indeks albo kolumna

The result of `groupby` has the groups as its index, so `means.loc["B"]` picks one group's value. `means.reset_index()` turns the groups back into an ordinary column and numbers the rows from 0, which you need before joining or saving the table.

PL: Wynik `groupby` ma grupy jako indeks (index), więc `means.loc["B"]` wybiera wartość jednej grupy. `means.reset_index()` zamienia grupy z powrotem w zwykłą kolumnę i numeruje wiersze od 0; tego potrzebujesz przed łączeniem albo zapisem tabeli.

```python
import pandas as pd

df = pd.DataFrame({
    "group": ["A", "B", "B", "A", "B", "B"],
    "score": [72, 85, 90, 64, 78, 70],
})
means = df.groupby("group")["score"].mean()
print(means.index)
print(means.loc["B"])
print(means.reset_index())
```

### See also

- merging/merge-on-a-shared-column

## Grouping by two columns

PL: Grupowanie po dwóch kolumnach

`df.groupby(["group", "sex"])` makes one group for each pair of values. The result has a two-level index, so `means.loc[("B", "F")]` picks one pair, and `reset_index()` turns both levels into columns.

PL: `df.groupby(["group", "sex"])` tworzy jedną grupę dla każdej pary wartości, czyli grupuje (grouping) po dwóch kluczach. Wynik ma dwupoziomowy indeks (MultiIndex), więc `means.loc[("B", "F")]` wybiera jedną parę, a `reset_index()` zamienia oba poziomy w kolumny.

```python
import pandas as pd

df = pd.DataFrame({
    "group": ["A", "B", "B", "A", "B", "B"],
    "sex": ["F", "M", "F", "M", "F", "M"],
    "score": [72, 85, 90, 64, 78, 70],
})
by_pair = df.groupby(["group", "sex"])
means = by_pair["score"].mean()
print(means)
print(means.loc[("B", "F")])
print(means.reset_index())
```

## The latest row per group

PL: Najnowszy wiersz w grupie

`df.sort_values("year", ascending=False)` puts the newest rows first, so `.groupby("state").first()` then gives each state's latest row. `.first()` takes each column's first value that isn't missing, so where the latest row has a gap, that value comes from an older row.

PL: `df.sort_values("year", ascending=False)` ustawia najnowsze wiersze na początku, więc grupowanie (grouping) przez `.groupby("state").first()` daje potem najnowszy wiersz każdego stanu. `.first()` bierze w każdej kolumnie pierwszą wartość, której nie brakuje, więc jeśli w najnowszym wierszu jest luka, ta wartość pochodzi ze starszego wiersza.

```python
import pandas as pd

df = pd.DataFrame({
    "state": ["TX", "CA", "TX", "NY", "CA"],
    "year": [2003, 2011, 2014, 2009, 1998],
    "shape": ["disk", "light", "light",
              "disk", "oval"],
})
newest = df.sort_values("year",
                        ascending=False)
print(newest.groupby("state").first())
```

## Keeping the largest groups

PL: Tylko największe grupy

`df.groupby("shape").size().nlargest(2)` gives the two largest groups, and its `.index` their names; `df["shape"].isin(top)` then keeps only the rows of those groups. `sizes.sort_values(ascending=False)[:2]` finds the same two groups.

PL: Po grupowaniu (grouping) `df.groupby("shape").size().nlargest(2)` daje dwie największe grupy, a `.index` wyniku ich nazwy; `df["shape"].isin(top)` zostawia potem tylko wiersze tych grup. `sizes.sort_values(ascending=False)[:2]` znajduje te same dwie grupy.

```python
import pandas as pd

df = pd.DataFrame({
    "shape": ["light", "disk", "light",
              "oval", "disk", "cigar",
              "light", "fireball"],
    "year": [2001, 2003, 2004, 2005,
             2007, 2008, 2010, 2012],
})
sizes = df.groupby("shape").size()
print(sizes.nlargest(2))
top = sizes.nlargest(2).index
print(df[df["shape"].isin(top)])
```
