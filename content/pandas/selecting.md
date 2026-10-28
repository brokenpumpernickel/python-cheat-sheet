---
title: Selecting
glyph: "df[ ]"
summary: "Picking parts of a table: columns with [], rows by position with iloc, rows and columns by label with loc, single values and row slices."
pl:
  title: Wybieranie
  summary: "Wybieranie części ramki danych (DataFrame): kolumny przez [], wiersze według pozycji z iloc, wiersze i kolumny według etykiet z loc, pojedyncze wartości i wycinki wierszy."
---

## One column or several

PL: Jedna kolumna lub kilka

`df["score"]` gives one column as a Series, and `df[["name", "score"]]`, with a list inside the brackets, gives a DataFrame with the listed columns in the order of the list.

PL: `df["score"]` daje jedną kolumnę jako serię (Series), a `df[["name", "score"]]`, z listą w nawiasach, daje ramkę danych (DataFrame) z wymienionymi kolumnami w kolejności z listy.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa"],
    "group": ["A", "B", "A"],
    "score": [72, 85, 90],
})
print(df["score"])
print(df[["name", "score"]])
```

### Pitfall

`df["name", "score"]` without the inner brackets looks for one column named by the pair `("name", "score")`, so it raises `KeyError`.

PL: `df["name", "score"]` bez wewnętrznych nawiasów szuka jednej kolumny o nazwie będącej parą `("name", "score")`, więc zgłasza `KeyError`.

```python raises=KeyError
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa"],
    "score": [72, 85, 90],
})
print(df["name", "score"])
```

### See also

- dataframes/a-column-is-a-series
- exploring/correlation-with-corr

## Rows by position with iloc

PL: Wiersze według pozycji z iloc

`df.iloc[0]` gives the first row as a Series, and `df.iloc[3:5]` the rows at positions 3 and 4, since the slice stops before its end, as a list slice does. A second slice picks columns by position: `df.iloc[3:5, :2]` keeps the first two.

PL: `df.iloc[0]` daje pierwszy wiersz jako serię (Series), a `df.iloc[3:5]` wiersze na pozycjach (positions) 3 i 4, bo wycinek (slice) kończy się przed swoim końcem, tak jak wycinek listy. Drugi wycinek wybiera kolumny według pozycji: `df.iloc[3:5, :2]` zostawia pierwsze dwie.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa",
             "Olek", "Iga", "Tom"],
    "score": [72, 85, 90, 64, 78, 85],
    "age": [19, 22, 20, 21, 19, 23],
})
print(df.iloc[0])
print(df.iloc[3:5])
print(df.iloc[3:5, :2])
```

### See also

- lists/slicing
- indexing/rows-and-columns

## Rows and columns by label with loc

PL: Wiersze i kolumny według etykiet z loc

`df.loc[3]` gives the row whose index label is 3, and `df.loc[3:5, "score"]` the `score` values of the rows labelled 3 to 5. Columns go by name, and a slice of names such as `"name":"score"` keeps the columns from `name` to `score`, both included. Here the labels are the default 0 to 5.

PL: `df.loc[3]` daje wiersz, którego etykieta (label) w indeksie (index) to 3, a `df.loc[3:5, "score"]` wartości `score` z wierszy o etykietach od 3 do 5. Kolumny wybierasz po nazwie, a wycinek (slice) nazw, np. `"name":"score"`, zostawia kolumny od `name` do `score`, łącznie z obiema. Tutaj etykiety to domyślne liczby od 0 do 5.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa",
             "Olek", "Iga", "Tom"],
    "score": [72, 85, 90, 64, 78, 85],
    "age": [19, 22, 20, 21, 19, 23],
})
print(df.loc[3])
print(df.loc[3:5, "score"])
print(df.loc[3:5, "name":"score"])
```

### Pitfall

A `loc` slice includes its end label and an `iloc` slice stops before its end position, so `df.loc[3:5]` gives 3 rows and `df.iloc[3:5]` only 2.

PL: Wycinek w `loc` obejmuje swoją końcową etykietę, a wycinek w `iloc` kończy się przed końcową pozycją, więc `df.loc[3:5]` daje 3 wiersze, a `df.iloc[3:5]` tylko 2.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa",
             "Olek", "Iga", "Tom"],
    "score": [72, 85, 90, 64, 78, 85],
})
print(df.loc[3:5])
print(df.iloc[3:5])
```

## A single value

PL: Pojedyncza wartość

`df.loc["Ewa", "score"]` gives one value by row label and column name, and `df.iloc[2, 1]` the same value by position: row 2, column 1. `set_index("name")` makes the names the row labels, so here labels and positions differ.

PL: `df.loc["Ewa", "score"]` daje jedną wartość według etykiety (label) wiersza i nazwy kolumny, a `df.iloc[2, 1]` tę samą wartość według pozycji (position): wiersz 2, kolumna 1. `set_index("name")` robi z imion etykiety wierszy, więc tutaj etykiety i pozycje się różnią.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa"],
    "group": ["A", "B", "A"],
    "score": [72, 85, 90],
}).set_index("name")
print(df)
print(df.loc["Ewa", "score"])
print(df.iloc[2, 1])
```

### See also

- indexing/rows-and-columns
- sorting/sort-index

## Row slices with df[3:5]

PL: Wycinki wierszy przez df[3:5]

A slice inside the brackets, as in `df[3:5]`, picks rows by position, like `df.iloc[3:5]`, while a name inside them picks a column.

PL: Wycinek (slice) w nawiasach, jak w `df[3:5]`, wybiera wiersze według pozycji (position), tak jak `df.iloc[3:5]`, a nazwa w nawiasach wybiera kolumnę.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa",
             "Olek", "Iga", "Tom"],
    "score": [72, 85, 90, 64, 78, 85],
})
print(df[3:5])
print(df[:2])
```

### Pitfall

`df[3]` without a colon looks for a column named `3`, not for row 3, so it raises `KeyError`. Use `df.iloc[3]` for one row.

PL: `df[3]` bez dwukropka szuka kolumny o nazwie `3`, a nie wiersza 3, więc zgłasza `KeyError`. Jeden wiersz wybierzesz przez `df.iloc[3]`.

```python raises=KeyError
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa",
             "Olek", "Iga", "Tom"],
    "score": [72, 85, 90, 64, 78, 85],
})
print(df[3])
```

### See also

- lists/slicing
