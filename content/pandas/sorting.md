---
title: Sorting
glyph: "sort"
summary: "Putting rows in order: sort_values by one or several columns, descending order, nlargest and nsmallest, the row with the largest value, and sort_index."
pl:
  title: Sortowanie
  summary: "Ustawianie wierszy ramki danych (DataFrame) w kolejności: sort_values po jednej lub kilku kolumnach, kolejność malejąca, nlargest i nsmallest, wiersz z największą wartością i sort_index."
---

## sort_values

PL: sort_values

`df.sort_values("score")` returns a new DataFrame with the rows from the smallest score to the largest, each row keeping its index label. `df` itself stays in its order, so assign the result to keep it.

PL: `df.sort_values("score")` zwraca nową ramkę danych (DataFrame) z wierszami od najmniejszego wyniku do największego, a każdy wiersz zachowuje swoją etykietę (label) w indeksie. Samo `df` zostaje w swojej kolejności, więc przypisz wynik, aby go zachować.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa", "Olek"],
    "score": [72, 85, 90, 64],
})
by_score = df.sort_values("score")
print(by_score)
print(df)
```

### See also

- lists/sorting

## Descending, and by several columns

PL: Malejąco i po kilku kolumnach

`ascending=False` sorts from the largest value. `by=["group", "score"]` sorts by `group`, then by `score` within each group, and a list such as `ascending=[True, False]` gives each column its own direction.

PL: `ascending=False` sortuje od największej wartości. `by=["group", "score"]` sortuje według `group`, a w każdej grupie według `score`, a lista, np. `ascending=[True, False]`, ustala kierunek osobno dla każdej kolumny.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa",
             "Olek", "Iga"],
    "group": ["A", "B", "A", "B", "A"],
    "score": [72, 85, 90, 64, 78],
})
print(df.sort_values(
    "score", ascending=False))
print(df.sort_values(
    by=["group", "score"],
    ascending=[True, False]))
```

## nlargest and nsmallest

PL: nlargest i nsmallest

`df.nlargest(3, "score")` gives the 3 rows with the largest scores, largest first, and `df.nsmallest(2, "score")` the 2 rows with the smallest, smallest first. It is shorter than sorting and then taking `head()`.

PL: `df.nlargest(3, "score")` daje 3 wiersze z największymi wynikami, od największego, a `df.nsmallest(2, "score")` 2 wiersze z najmniejszymi, od najmniejszego. To krócej niż sortowanie, a potem `head()`.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa",
             "Olek", "Iga"],
    "score": [72, 85, 90, 64, 78],
})
print(df.nlargest(3, "score"))
print(df.nsmallest(2, "score"))
```

### See also

- exploring/head-and-tail

## The row with the largest value

PL: Wiersz z największą wartością

`df["score"].idxmax()` gives the index label of the largest score, so `df.loc[best]` is that whole row and `df.loc[best, "name"]` one value from it. It is a label, not a position, so use it with `loc`, not `iloc`; `idxmin()` does the same for the smallest.

PL: `df["score"].idxmax()` daje etykietę (label) w indeksie największego wyniku, więc `df.loc[best]` to cały ten wiersz, a `df.loc[best, "name"]` jedna wartość z niego. To etykieta, a nie pozycja (position), więc używaj jej z `loc`, a nie z `iloc`; `idxmin()` robi to samo dla najmniejszej wartości.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa", "Olek"],
    "score": [72, 85, 90, 64],
})
best = df["score"].idxmax()
print(best)
print(df.loc[best])
print(df.loc[best, "name"])
```

### See also

- aggregates/where-the-minimum-and-maximum-are
- selecting/a-single-value

## sort_index

PL: sort_index

`df.sort_index()` sorts the rows by their index labels, which puts a table back in its first order after `sort_values`. On an index of names, as after `set_index("name")`, it sorts them alphabetically.

PL: `df.sort_index()` sortuje wiersze według ich etykiet (labels) w indeksie (index), co przywraca tabeli pierwotną kolejność po `sort_values`. Na indeksie z imionami, np. po `set_index("name")`, sortuje je alfabetycznie.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Jan", "Ewa", "Ala", "Olek"],
    "score": [72, 85, 90, 64],
})
by_score = df.sort_values("score")
print(by_score.sort_index())
by_name = df.set_index("name")
print(by_name.sort_index())
```

### See also

- selecting/a-single-value
