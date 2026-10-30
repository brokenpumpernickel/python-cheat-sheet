---
title: DataFrames
glyph: "df"
summary: "Tables with named columns: building one from a dictionary, columns as Series and NumPy arrays, shape, column types and printing."
pl:
  title: Ramki danych
  summary: "Ramki danych (DataFrames), czyli tabele z nazwanymi kolumnami: tworzenie ze słownika, kolumny jako serie i tablice NumPy, kształt, typy kolumn i wypisywanie."
---

## A DataFrame from a dictionary

PL: Ramka danych ze słownika

`pd.DataFrame({"name": [...], "score": [...]})` builds a table with one column per dictionary key, in the order of the keys. Every list must have the same length, one value per row, and pandas numbers the rows from 0.

PL: `pd.DataFrame({"name": [...], "score": [...]})` tworzy ramkę danych (DataFrame), czyli tabelę z jedną kolumną na każdy klucz słownika, w kolejności kluczy. Każda lista musi mieć tę samą długość, jedną wartość na wiersz, a pandas numeruje wiersze od 0.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa", "Olek"],
    "group": ["A", "B", "A", "B"],
    "score": [72, 85, 90, 64],
})
print(df)
```

### See also

- dictionaries/creating-and-accessing

## A column is a Series

PL: Kolumna to seria

`df["score"]` gives one column as a `Series`: its values with the same index as the table, its name and its dtype. Most column maths, such as `.mean()`, works on a Series.

PL: `df["score"]` daje jedną kolumnę jako serię (Series): jej wartości z tym samym indeksem (index) co tabela, jej nazwę i typ danych (dtype). Większość obliczeń na kolumnach, takich jak `.mean()`, działa na serii.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa"],
    "score": [72, 85, 90],
})
print(df["score"])
print(type(df["score"]))
```

## Columns as NumPy arrays

PL: Kolumny jako tablice NumPy

`df["score"].to_numpy()` gives one column as a 1-D NumPy array, and `df[["height", "weight"]].to_numpy()` a 2-D array with one row per row of the table. The older `.values` still works, but `.to_numpy()` is the recommended way. NumPy functions such as `np.percentile` take the array, but `np.std` divides by `n` unless you pass `ddof=1`, while pandas' `.std()` divides by `n - 1`.

PL: `df["score"].to_numpy()` daje jedną kolumnę jako jednowymiarową tablicę NumPy (NumPy array), a `df[["height", "weight"]].to_numpy()` tablicę dwuwymiarową, z jednym wierszem na każdy wiersz tabeli. Starsze `.values` nadal działa, ale zalecane jest `.to_numpy()`. Tablicę przyjmują funkcje NumPy, takie jak `np.percentile`, tylko że `np.std` dzieli przez `n`, jeśli nie podasz `ddof=1`, a `.std()` w pandas dzieli przez `n - 1`.

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "height": [165.5, 180.0, 172.5, 158.0],
    "weight": [58.0, 77.5, 70.0, 52.5],
    "score": [72, 85, 90, 64],
})
scores = df["score"].to_numpy()
print(scores)
print(df[["height", "weight"]].to_numpy())
print(np.percentile(scores, 90))
print(round(np.std(scores, ddof=1), 2))
print(round(df["score"].std(), 2))
```

### Pitfall

`df.to_numpy()` on a table with a text column gives one array of dtype `object`, so `a.sum(axis=0)` glues the names together and `a.mean(axis=0)` fails with a `TypeError` about `str`. Select the number columns before `.to_numpy()`.

PL: `df.to_numpy()` na tabeli z kolumną tekstową daje jedną tablicę o typie `object`, więc `a.sum(axis=0)` skleja imiona, a `a.mean(axis=0)` kończy się wyjątkiem `TypeError`, który mówi o `str`. Przed `.to_numpy()` wybierz kolumny z liczbami.

```python raises=TypeError
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa"],
    "score": [72, 85, 90],
})
a = df.to_numpy()
print(a.dtype)
print(a.sum(axis=0))
print(a.mean(axis=0))
```

### See also

- aggregates/median-and-percentiles
- exploring/column-statistics
- columns/text-to-numbers

## Shape, columns and index

PL: Kształt, kolumny i indeks

`df.shape` is the tuple `(rows, columns)`, and `len(df)` is the number of rows. `df.columns` holds the column names and `df.index` the row labels, here the numbers 0 to 3.

PL: `df.shape` to krotka (tuple) `(rows, columns)`, czyli liczba wierszy i kolumn, a `len(df)` to liczba wierszy. `df.columns` zawiera nazwy kolumn, a `df.index` etykiety wierszy, czyli indeks (index), tutaj liczby od 0 do 3.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa", "Olek"],
    "score": [72, 85, 90, 64],
})
print(df.shape)
print(len(df))
print(df.columns)
print(df.index)
```

### See also

- arrays/shape-and-dtype

## Column types

PL: Typy kolumn

`df.dtypes` lists each column's type: `int64` and `float64` for numbers, `str` for text. `df["score"].astype("float64")` returns the column converted to another type, so assign it back to change the table.

PL: `df.dtypes` wypisuje typ każdej kolumny (dtype): `int64` i `float64` dla liczb, `str` dla tekstu. `df["score"].astype("float64")` zwraca kolumnę zamienioną na inny typ, więc przypisz ją z powrotem, aby zmienić tabelę.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa"],
    "height": [165.5, 180.0, 172.5],
    "score": [72, 85, 90],
})
print(df.dtypes)
df["score"] = df["score"].astype("float64")
print(df.dtypes)
```

### Pitfall

`df["score"].astype("float64")` on its own line changes nothing: it returns a new column and leaves `df` as it was.

PL: `df["score"].astype("float64")` w osobnej linii niczego nie zmienia: zwraca nową kolumnę, a `df` zostaje bez zmian.

```python
import pandas as pd

df = pd.DataFrame({"score": [72, 85, 90]})
df["score"].astype("float64")
print(df.dtypes)
```

### See also

- arrays/shape-and-dtype

## Printing a DataFrame

PL: Wypisywanie ramki danych

`print(df)` prints the whole table as text, and `print(df.head(3))` only its first 3 rows. In Jupyter a bare `df` or `df.head()` on the last line of a cell shows a formatted table instead; this cheat sheet prints, so its Outputs are text.

PL: `print(df)` wypisuje całą ramkę danych (DataFrame) jako tekst, a `print(df.head(3))` tylko jej pierwsze 3 wiersze. W Jupyterze samo `df` lub `df.head()` w ostatniej linii komórki pokazuje zamiast tego sformatowaną tabelę; ta ściągawka używa `print`, więc jej Wyniki są tekstem.

```python
import pandas as pd

df = pd.DataFrame({
    "group": ["A", "B", "A", "B", "A"],
    "score": [72, 85, 90, 64, 78],
})
print(df)
print(df.head(3))
```

### See also

- exploring/head-and-tail
