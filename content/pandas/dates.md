---
title: Dates
glyph: ".dt"
summary: "Date columns: text to dates, dates from a CSV file, parts of a date with .dt, time between dates, filtering by date, and grouping by month or year."
pl:
  title: Daty
  summary: "Kolumny z datami (dates): tekst na daty, daty z pliku CSV, części daty przez akcesor .dt (.dt accessor), czas między datami, filtrowanie po dacie oraz grupowanie po miesiącu lub roku."
---

## Text to dates

PL: Tekst na daty

`pd.to_datetime(df["iso"])` turns ISO dates such as `"2026-10-28"` into a `datetime64` column. Polish dates such as `"28.10.2026"` need `format="%d.%m.%Y"` (or `dayfirst=True`), since without it `"04.03.2026"` reads as April 3. `errors="coerce"` turns text it can't read, such as `"unknown"`, into `NaT`, a missing date.

PL: `pd.to_datetime(df["iso"])` zamienia daty (dates) w formacie ISO, takie jak `"2026-10-28"`, na kolumnę typu `datetime64`. Polskie daty, takie jak `"28.10.2026"`, wymagają `format="%d.%m.%Y"` (albo `dayfirst=True`), bo bez tego `"04.03.2026"` wczytuje się jako 3 kwietnia. `errors="coerce"` zamienia tekst, którego nie da się odczytać, taki jak `"unknown"`, na `NaT`, czyli brakującą datę (missing value).

```python
import pandas as pd

df = pd.DataFrame({
    "iso": ["2026-10-28", "2026-11-03"],
    "polish": ["28.10.2026", "03.11.2026"],
    "messy": ["2026-12-01", "unknown"],
})
df["iso"] = pd.to_datetime(df["iso"])
df["polish"] = pd.to_datetime(
    df["polish"], format="%d.%m.%Y")
df["messy"] = pd.to_datetime(
    df["messy"], errors="coerce")
print(df)
print(df.dtypes)
```

### See also

- columns/text-to-numbers
- missing-values/finding-missing-values
- text-columns/cleaning-text

## Dates from a CSV file

PL: Daty z pliku CSV

`pd.read_csv` reads dates as text, so name the date columns in `parse_dates=["date"]` to get dates straight away. Here `sightings.csv` has the header `date,shape` and three rows like `2024-03-04,disk`; for Polish dates add `date_format="%d.%m.%Y"`.

PL: `pd.read_csv` wczytuje daty (dates) jako tekst, więc podaj kolumny z datami w `parse_dates=["date"]`, aby od razu dostać daty. Tutaj `sightings.csv` ma nagłówek `date,shape` i trzy wiersze w rodzaju `2024-03-04,disk`; dla polskich dat dodaj `date_format="%d.%m.%Y"`.

```python
with open("sightings.csv", "w", encoding="utf-8") as f: f.write("date,shape\n2024-03-04,disk\n2024-03-18,light\n2024-04-02,disk\n")  #| hide
import pandas as pd

print(pd.read_csv("sightings.csv").dtypes)
df = pd.read_csv("sightings.csv",
                 parse_dates=["date"])
print(df)
print(df.dtypes)
```

### See also

- csv-files/reading-a-csv-file
- csv-files/semicolons-and-decimal-commas

## Parts of a date

PL: Części daty

`.dt` gives a date column's parts: `.dt.year`, `.dt.month`, `.dt.day` and `.dt.day_of_week`, where 0 is Monday and 6 is Sunday. `.dt.day_name()` gives the day's name in English; its `locale=` depends on the languages installed on the computer, so don't rely on it.

PL: Akcesor `.dt` (.dt accessor) daje części kolumny z datami: `.dt.year`, `.dt.month`, `.dt.day` i `.dt.day_of_week`, gdzie 0 to poniedziałek, a 6 to niedziela. `.dt.day_name()` podaje nazwę dnia po angielsku; jej `locale=` zależy od języków zainstalowanych na komputerze, więc nie polegaj na nim.

```python
import pandas as pd

df = pd.DataFrame({
    "date": ["2024-03-04", "2024-03-16",
             "2025-01-01"],
})
df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day
df["weekday"] = df["date"].dt.day_of_week
print(df)
print(df["date"].dt.day_name())
```

### Pitfall

`.dt` works only on a date column, so on dates still stored as text, as after `pd.read_csv` without `parse_dates`, it raises `AttributeError`. Convert the column with `pd.to_datetime` first.

PL: `.dt` działa tylko na kolumnie z datami, więc na datach zapisanych jeszcze jako tekst, jak po `pd.read_csv` bez `parse_dates`, zgłasza `AttributeError`. Najpierw zamień kolumnę przez `pd.to_datetime`.

```python raises=AttributeError
import pandas as pd

df = pd.DataFrame({
    "date": ["2024-03-04", "2024-03-16"],
})
print(df["date"].dtype)
print(df["date"].dt.year)
```

### See also

- dataframes/column-types
- text-columns/the-str-accessor

## Time between dates

PL: Czas między datami

Subtracting two date columns, `df["end"] - df["start"]`, gives a Timedelta, the time between the dates, in each row, and `.dt.days` turns it into whole days. Adding `pd.Timedelta(days=7)` to a date column moves every date a week on.

PL: Odjęcie dwóch kolumn z datami, `df["end"] - df["start"]`, daje w każdym wierszu różnicę czasu (Timedelta), czyli czas między datami, a `.dt.days` zamienia ją na pełne dni. Dodanie `pd.Timedelta(days=7)` do kolumny z datami przesuwa każdą datę o tydzień.

```python
import pandas as pd

df = pd.DataFrame({
    "start": ["2024-03-04", "2024-03-18"],
    "end": ["2024-03-11", "2024-04-02"],
})
df["start"] = pd.to_datetime(df["start"])
df["end"] = pd.to_datetime(df["end"])
df["took"] = df["end"] - df["start"]
df["days"] = df["took"].dt.days
print(df)
week = pd.Timedelta(days=7)
print(df["end"] + week)
```

### See also

- columns/a-column-from-other-columns

## Filtering by date

PL: Filtrowanie po dacie

A date column compares with a date written as text, so `df[df["date"] >= "2024-03-01"]` keeps the rows from 1 March 2024 on. `.between("2024-03-01", "2024-03-31")` keeps a range and includes both ends.

PL: Kolumnę z datami (dates) można porównać z datą zapisaną jako tekst, więc `df[df["date"] >= "2024-03-01"]` zostawia wiersze od 1 marca 2024. `.between("2024-03-01", "2024-03-31")` zostawia zakres dat razem z oboma końcami.

```python
import pandas as pd

df = pd.DataFrame({
    "date": ["2024-02-27", "2024-03-04",
             "2024-03-31", "2024-04-02"],
    "shape": ["oval", "disk",
              "light", "disk"],
})
df["date"] = pd.to_datetime(df["date"])
print(df[df["date"] >= "2024-03-01"])
march = df["date"].between(
    "2024-03-01", "2024-03-31")
print(df[march])
```

### See also

- filtering/a-boolean-mask
- filtering/combining-conditions

## Grouping by month or year

PL: Grupowanie po miesiącu lub roku

`df.groupby(df["date"].dt.year)` groups the rows by year, here with `.size()` to count them. `.dt.to_period("M")` turns each date into its month, such as `2024-03`, so grouping by it gives one value per month, here the mean of `minutes`.

PL: `df.groupby(df["date"].dt.year)` grupuje wiersze po roku (grouping), tutaj z `.size()`, aby je zliczyć. `.dt.to_period("M")` zamienia każdą datę na jej miesiąc, taki jak `2024-03`, więc grupowanie po nim daje jedną wartość na miesiąc, tutaj średnią z `minutes`.

```python
import pandas as pd

df = pd.DataFrame({
    "date": ["2023-11-20", "2024-03-04",
             "2024-03-18", "2024-04-02",
             "2024-04-09"],
    "minutes": [5, 12, 3, 8, 10],
})
df["date"] = pd.to_datetime(df["date"])
print(df.groupby(df["date"].dt.year).size())
month = df["date"].dt.to_period("M")
print(df.groupby(month)["minutes"].mean())
```

### See also

- grouping/group-sizes
- grouping/a-column-s-mean-per-group
- pandas-plots/a-line-plot-of-a-series
