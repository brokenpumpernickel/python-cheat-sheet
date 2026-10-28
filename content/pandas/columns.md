---
title: Changing columns
glyph: "df[]="
summary: "Adding and cleaning columns: computing from other columns, text methods, text to numbers, apply, map, renaming and dropping."
pl:
  title: Zmiana kolumn
  summary: "Dodawanie i czyszczenie kolumn ramki danych (DataFrame): obliczanie z innych kolumn, metody tekstowe, tekst na liczby, apply, map, zmiana nazw i usuwanie."
---

## A column from other columns

PL: Kolumna z innych kolumn

`df["hours"] = df["seconds"] / 3600` computes a value for every row at once, with no loop, and stores it as a new column at the end of the table. Columns combine row by row, as in `df["km"] / df["hours"]`; assigning to an existing name replaces that column.

PL: `df["hours"] = df["seconds"] / 3600` oblicza wartość dla wszystkich wierszy naraz, bez pętli (loop), i zapisuje ją jako nową kolumnę na końcu tabeli. Kolumny łączą się wiersz po wierszu, jak w `df["km"] / df["hours"]`; przypisanie do istniejącej nazwy zastępuje tę kolumnę.

```python
import pandas as pd

df = pd.DataFrame({
    "runner": ["Ala", "Jan", "Ewa"],
    "km": [10, 21, 10],
    "seconds": [2880, 7560, 3600],
})
df["hours"] = df["seconds"] / 3600
df["speed"] = df["km"] / df["hours"]
print(df)
```

### See also

- dataframes/a-column-is-a-series
- array-maths/element-wise-arithmetic

## Text methods

PL: Metody tekstowe

`.str` gives every value of a text column the string methods: `.str.strip()` trims spaces, `.str.lower()` makes letters lowercase, `.str.replace("_", " ")` swaps text, and `.str.len()` gives each length. Each returns a new column, so chain them and assign the result back.

PL: `.str` daje każdej wartości kolumny tekstowej metody napisów (string methods): `.str.strip()` obcina spacje, `.str.lower()` zamienia litery na małe, `.str.replace("_", " ")` podmienia tekst, a `.str.len()` podaje długość każdej wartości. Każda zwraca nową kolumnę, więc łącz je w łańcuch i przypisz wynik z powrotem.

```python
import pandas as pd

df = pd.DataFrame({
    "city": [" Kraków", "NOWY_SĄCZ "],
})
city = df["city"].str.strip().str.lower()
df["city"] = city.str.replace("_", " ")
print(df)
print(df["city"].str.len())
```

### See also

- strings/cleaning-and-splitting
- filtering/text-that-contains

## Text to numbers

PL: Tekst na liczby

A number written with thousands commas, `"1,863,056"`, is text. Remove the commas with `.str.replace(",", "")` and convert with `.astype(int)`. `pd.to_numeric(col, errors="coerce")` converts what it can and turns the rest, such as `"unknown"`, into `NaN`.

PL: Liczba zapisana z przecinkami tysięcy, `"1,863,056"`, jest tekstem. Usuń przecinki przez `.str.replace(",", "")` i zamień tekst na liczby przez `.astype(int)`. `pd.to_numeric(col, errors="coerce")` zamienia to, co potrafi, a resztę, taką jak `"unknown"`, zamienia na `NaN`, czyli brakującą wartość (missing value).

```python
import pandas as pd

df = pd.DataFrame({
    "population": ["1,863,056", "804,237"],
    "area": ["517.2", "unknown"],
})
pop = df["population"].str.replace(",", "")
df["population"] = pop.astype(int)
df["area"] = pd.to_numeric(
    df["area"], errors="coerce")
print(df)
print(df.dtypes)
```

### See also

- dataframes/column-types
- missing-values/finding-missing-values

## A function on each value

PL: Funkcja na każdej wartości

`df["score"].apply(grade)` calls your function on each value of the column and collects what it returns into a new column. Pass the function's name without brackets: `apply(grade)`, not `apply(grade())`.

PL: `df["score"].apply(grade)` wywołuje twoją funkcję (function) dla każdej wartości kolumny i zbiera to, co zwraca, w nową kolumnę. Podaj samą nazwę funkcji bez nawiasów: `apply(grade)`, a nie `apply(grade())`.

```python
import pandas as pd

def grade(score):
    if score >= 90:
        return 5
    if score >= 50:
        return 3
    return 2

df = pd.DataFrame({"score": [92, 64, 41]})
df["grade"] = df["score"].apply(grade)
print(df)
```

### See also

- functions/defining-and-calling
- conditionals/if-elif-else

## Mapping values with a dictionary

PL: Zamiana wartości słownikiem

`df["group"].map({"A": "control", "B": "treatment"})` replaces each value with the value it has in the dictionary. A value that isn't a key, here `"C"`, becomes `NaN`, so check the result for gaps.

PL: `df["group"].map({"A": "control", "B": "treatment"})` zamienia każdą wartość na wartość, którą ma w słowniku (dictionary). Wartość, której nie ma wśród kluczy, tutaj `"C"`, staje się `NaN`, więc sprawdź, czy w wyniku nie ma braków.

```python
import pandas as pd

df = pd.DataFrame({
    "id": [1, 2, 3, 4],
    "group": ["A", "B", "A", "C"],
})
arms = {"A": "control", "B": "treatment"}
df["arm"] = df["group"].map(arms)
print(df)
```

### See also

- dictionaries/creating-and-accessing
- missing-values/finding-missing-values

## Renaming columns

PL: Zmiana nazw kolumn

`df.rename(columns={"Exam Score": "score"})` returns the table with the named columns renamed, so assign it back. To clean every name at once, assign to `df.columns` the names passed through `.str` methods; the brackets let you write one method per line.

PL: `df.rename(columns={"Exam Score": "score"})` zwraca tabelę ze zmienionymi nazwami wskazanych kolumn, więc przypisz ją z powrotem. Aby oczyścić wszystkie nazwy naraz, przypisz do `df.columns` nazwy przepuszczone przez metody `.str`; nawiasy pozwalają zapisać jedną metodę w linii.

```python
import pandas as pd

df = pd.DataFrame({
    "Height.cm": [165.0, 180.5],
    "Weight.kg": [58.5, 77.0],
    "Exam Score": [72, 85],
})
df = df.rename(
    columns={"Exam Score": "score"})
print(list(df.columns))
df.columns = (
    df.columns
    .str.lower()
    .str.replace(".", "_")
)
print(df)
```

### See also

- dataframes/shape-columns-and-index

## Dropping columns

PL: Usuwanie kolumn

`df.drop(columns=["seconds"])` returns a new DataFrame without the listed columns, and `df` keeps them. Assign the result, `df = df.drop(columns=[...])`, to change `df`.

PL: `df.drop(columns=["seconds"])` zwraca nową ramkę danych (DataFrame) bez wymienionych kolumn, a `df` je zachowuje. Przypisz wynik, `df = df.drop(columns=[...])`, aby zmienić `df`.

```python
import pandas as pd

df = pd.DataFrame({
    "runner": ["Ala", "Jan", "Ewa"],
    "seconds": [2880, 7560, 3600],
    "hours": [0.8, 2.1, 1.0],
})
short = df.drop(columns=["seconds"])
print(short)
print(list(df.columns))
```

### Pitfall

Changing a column of a filtered table, as in `df[df["score"] < 50]["score"] = 50`, changes a temporary copy, so `df` stays as it was and pandas 3 only warns with `ChainedAssignmentError`. Pick the rows and the column in one step: `df.loc[df["score"] < 50, "score"] = 50`.

PL: Zmiana kolumny w przefiltrowanej tabeli, jak w `df[df["score"] < 50]["score"] = 50`, zmienia tymczasową kopię, więc `df` zostaje bez zmian, a pandas 3 tylko ostrzega o przypisaniu łańcuchowym (chained assignment) przez `ChainedAssignmentError`. Wybierz wiersze i kolumnę w jednym kroku: `df.loc[df["score"] < 50, "score"] = 50`.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa"],
    "score": [45, 85, 30],
})
df[df["score"] < 50]["score"] = 50
print(df)
df.loc[df["score"] < 50, "score"] = 50
print(df)
```

### See also

- dataframes/column-types
- selecting/rows-and-columns-by-label-with-loc
- filtering/a-column-of-the-matching-rows
