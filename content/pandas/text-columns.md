---
title: Text columns
glyph: ".str"
summary: "Text in a column through the .str accessor: cleaning, splitting, searching, lengths, slices and counts."
pl:
  title: Kolumny tekstowe
  summary: "Tekst w kolumnie przez akcesor .str (.str accessor): czyszczenie, dzielenie, wyszukiwanie, długości, wycinki i zliczanie."
---

## The .str accessor

PL: Akcesor .str

A column of text has no `.lower()` of its own: `df["city"].str.lower()` applies the string method to every value and returns a new column. The methods after `.str` have the same names as Python's string methods, and a missing value stays `NaN`.

PL: Kolumna tekstowa nie ma własnej metody `.lower()`: `df["city"].str.lower()` wywołuje tę metodę napisów (string method) dla każdej wartości i zwraca nową kolumnę. Metody po akcesorze `.str` (.str accessor) mają te same nazwy co metody napisów w Pythonie, a brakująca wartość zostaje `NaN`.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa"],
    "city": ["Kraków", None, "GDAŃSK"],
})
df["city"] = df["city"].str.lower()
print(df)
print("GDAŃSK".lower())
```

### Pitfall

`df["city"].lower()` without `.str` raises `AttributeError`, because the method belongs to each value, not to the column.

PL: `df["city"].lower()` bez `.str` zgłasza `AttributeError`, bo ta metoda należy do każdej wartości, a nie do kolumny.

```python raises=AttributeError
import pandas as pd

df = pd.DataFrame({
    "city": ["Kraków", "GDAŃSK"],
})
print(df["city"].lower())
```

### See also

- strings/cleaning-and-splitting
- dataframes/a-column-is-a-series
- dates/parts-of-a-date

## Cleaning text

PL: Czyszczenie tekstu

`.str.strip()` trims spaces at both ends, `.str.replace("_", " ")` swaps text, and `.str.title()` capitalises each word (`.str.lower()` makes it all lowercase). Each returns a new column, so chain them and assign the result back; differently typed names then become one value.

PL: `.str.strip()` obcina spacje z obu końców, `.str.replace("_", " ")` podmienia tekst, a `.str.title()` zaczyna każde słowo wielką literą (`.str.lower()` zamienia wszystkie na małe). Każda metoda zwraca nową kolumnę, więc łącz je w łańcuch i przypisz wynik z powrotem; różnie wpisane nazwy stają się wtedy jedną wartością.

```python
import pandas as pd

df = pd.DataFrame({
    "city": [" Kraków", "KRAKÓW",
             "nowy_sącz ", "Nowy Sącz"],
})
print(df["city"].nunique())
df["city"] = (
    df["city"]
    .str.strip()
    .str.replace("_", " ")
    .str.title()
)
print(df["city"].value_counts())
```

### See also

- strings/cleaning-and-splitting
- columns/text-to-numbers
- exploring/value-counts

## Splitting text

PL: Dzielenie tekstu

`.str.split(" ")` splits every value into a list of parts. `.str[0]` then picks the first part of each list, and `expand=True` puts the parts in separate columns, which you can assign to new column names.

PL: `.str.split(" ")` dzieli każdą wartość na listę (list) części. `.str[0]` wybiera potem pierwszą część każdej listy, a `expand=True` umieszcza części w osobnych kolumnach, które możesz przypisać do nowych nazw kolumn.

```python
import pandas as pd

df = pd.DataFrame({
    "student": ["Kowalski Jan",
                "Nowak Ala",
                "Wiśniewska Ewa"],
})
parts = df["student"].str.split(" ")
print(parts)
print(parts.str[0])
df[["surname", "name"]] = (
    df["student"].str.split(" ", expand=True))
print(df)
```

### See also

- strings/cleaning-and-splitting
- lists/creating-and-indexing
- selecting/one-column-or-several

## Searching text

PL: Wyszukiwanie tekstu

`.str.contains("exam")` is `True` where the text contains `exam` anywhere, and `.str.startswith(...)` and `.str.endswith(...)` only at the start or the end. `case=False` makes `contains` ignore case, which the other two always match, and `na=False` makes a missing value `False`, so the mask works in `df[mask]`.

PL: `.str.contains("exam")` daje `True`, gdy tekst zawiera `exam` w dowolnym miejscu, a `.str.startswith(...)` i `.str.endswith(...)` tylko na początku lub na końcu. `case=False` sprawia, że `contains` nie rozróżnia wielkości liter, które dwie pozostałe metody zawsze rozróżniają, a `na=False` zamienia brakującą wartość na `False`, więc maska logiczna (boolean mask) działa w `df[mask]`.

```python
import pandas as pd

df = pd.DataFrame({
    "file": ["exam_2024.csv", "Exam_2025.CSV",
             "notes.txt", None],
})
f = df["file"]
df["exam"] = f.str.contains(
    "exam", case=False, na=False)
df["starts"] = f.str.startswith("exam", na=False)
df["csv"] = f.str.endswith(".csv", na=False)
print(df)
```

### Pitfall

`.str.contains` reads its pattern as a regular expression, where `.` means any character, so `.str.contains(".")` is `True` for every value; pass `regex=False` to search for the text as written. `.str.replace` is the other way round: plain text unless you pass `regex=True`.

PL: `.str.contains` czyta swój wzorzec jako wyrażenie regularne (regular expression), w którym `.` oznacza dowolny znak, więc `.str.contains(".")` daje `True` dla każdej wartości; podaj `regex=False`, aby szukać tekstu dokładnie tak, jak jest zapisany. `.str.replace` działa odwrotnie: czyta zwykły tekst, chyba że podasz `regex=True`.

```python
import pandas as pd

df = pd.DataFrame({
    "grade": ["3.5", "4", "4.5", "5"],
})
print(df["grade"].str.contains("."))
```

### See also

- filtering/text-that-contains
- filtering/a-boolean-mask
- missing-values/finding-missing-values

## Lengths, slices and counts

PL: Długości, wycinki i zliczanie

`.str.len()` gives the number of characters in each value, `.str[:3]` slices each value as you slice a string, and `.str.count("a")` counts how often `a` appears. Like `contains`, `count` reads its pattern as a regular expression.

PL: `.str.len()` podaje liczbę znaków każdej wartości, `.str[:3]` wycina fragment każdej wartości tak, jak wycinasz (slicing) fragment napisu, a `.str.count("a")` zlicza, ile razy pojawia się `a`. Podobnie jak `contains`, `count` czyta swój wzorzec jako wyrażenie regularne (regular expression).

```python
import pandas as pd

df = pd.DataFrame({
    "city": ["Warszawa", "Łódź", "Gdańsk"],
})
df["length"] = df["city"].str.len()
df["code"] = df["city"].str[:3]
df["a_count"] = df["city"].str.count("a")
print(df)
```

### See also

- lists/slicing
