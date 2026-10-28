---
title: DataFrames
glyph: "df"
summary: "Tables with named columns: building one from a dictionary, columns as Series, shape, column types and printing."
pl:
  title: Ramki danych
  summary: "Ramki danych (DataFrames), czyli tabele z nazwanymi kolumnami: tworzenie ze słownika, kolumny jako serie, kształt, typy kolumn i wypisywanie."
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
