---
title: Exploring data
glyph: ".info"
summary: "A first look at a table: head and tail, info, describe, column statistics, counts, distinct values and correlation."
pl:
  title: Przeglądanie danych
  summary: "Pierwsze spojrzenie na ramkę danych (DataFrame): head i tail, info, describe, statystyki kolumn, zliczenia, różne wartości i korelacja."
---

## head and tail

PL: head i tail

`df.head()` gives the first 5 rows and `df.tail()` the last 5; pass a number for another count, as in `df.tail(2)`. Here `students.csv` holds 8 students with their name, group, height, weight and score.

PL: `df.head()` daje pierwsze 5 wierszy, a `df.tail()` ostatnie 5; podaj liczbę, aby dostać inną liczbę wierszy, jak w `df.tail(2)`. Tutaj `students.csv` zawiera 8 studentów z ich imieniem, grupą, wzrostem, wagą i wynikiem.

```python
with open("students.csv", "w", encoding="utf-8") as f: f.write("name,group,height,weight,score\nAla,A,165.0,58.5,72\nJan,B,180.5,77.0,85\nEwa,A,172.0,68.0,90\nOlek,B,178.0,74.0,64\nIga,A,160.5,57.5,78\nTom,B,183.0,81.5,85\nOla,A,168.5,60.0,91\nPiotr,A,175.5,64.0,58\n")  #| hide
import pandas as pd

df = pd.read_csv("students.csv")
print(df.head())
print(df.tail(2))
```

### See also

- dataframes/printing-a-dataframe
- csv-files/reading-a-csv-file

## info()

PL: info()

`df.info()` prints the number of rows and, for each column, its non-null count and dtype, so you see at once which columns have missing values or were read as text. It prints by itself, without `print`. The memory line at the end can differ between computers and pandas versions.

PL: `df.info()` wypisuje liczbę wierszy, a dla każdej kolumny liczbę wartości niepustych (non-null) i typ danych (dtype), więc od razu widać, w których kolumnach brakuje wartości albo które wczytały się jako tekst. Wypisuje się sama, bez `print`. Wiersz z pamięcią na końcu może się różnić między komputerami i wersjami pandas.

```python
with open("students.csv", "w", encoding="utf-8") as f: f.write("name,group,height,weight,score\nAla,A,165.0,58.5,72\nJan,B,180.5,77.0,85\nEwa,A,172.0,68.0,90\nOlek,B,178.0,74.0,64\nIga,A,160.5,57.5,78\nTom,B,183.0,81.5,85\nOla,A,168.5,60.0,91\nPiotr,A,175.5,64.0,58\n")  #| hide
import pandas as pd

df = pd.read_csv("students.csv")
df.info()
```

### See also

- dataframes/column-types

## describe()

PL: describe()

`df.describe()` gives the count, mean, standard deviation, minimum, quartiles and maximum of every numeric column. `df.describe(include="all")` adds the text columns, with the number of distinct values, the most common one and its count; `NaN` marks the statistics that don't apply to a column. `.round(2)` keeps the table narrow.

PL: `df.describe()` podaje liczbę wartości, średnią, odchylenie standardowe (standard deviation), minimum, kwartyle (quartiles) i maksimum każdej kolumny liczbowej. `df.describe(include="all")` dodaje kolumny tekstowe z liczbą różnych wartości, najczęstszą z nich i jej liczbą; `NaN` oznacza statystyki, które nie pasują do danej kolumny. `.round(2)` zaokrągla liczby, więc tabela jest węższa.

```python
with open("students.csv", "w", encoding="utf-8") as f: f.write("name,group,height,weight,score\nAla,A,165.0,58.5,72\nJan,B,180.5,77.0,85\nEwa,A,172.0,68.0,90\nOlek,B,178.0,74.0,64\nIga,A,160.5,57.5,78\nTom,B,183.0,81.5,85\nOla,A,168.5,60.0,91\nPiotr,A,175.5,64.0,58\n")  #| hide
import pandas as pd

df = pd.read_csv("students.csv")
print(df.describe().round(2))
print(df.describe(include="all").round(2))
```

### See also

- aggregates/median-and-percentiles

## Column statistics

PL: Statystyki kolumn

A column has the methods `.mean()`, `.median()`, `.std()`, `.quantile(0.9)`, `.min()` and `.max()`. pandas' `.std()` divides by `n - 1` (`ddof=1`), the sample standard deviation, while NumPy's `a.std()` divides by `n` unless you pass `ddof=1`.

PL: Kolumna ma metody `.mean()`, `.median()`, `.std()`, `.quantile(0.9)`, `.min()` i `.max()`. W pandas `.std()` dzieli przez `n - 1` (`ddof=1`), czyli liczy odchylenie standardowe (standard deviation) z próby, a w NumPy `a.std()` dzieli przez `n`, jeśli nie podasz `ddof=1`.

```python
with open("students.csv", "w", encoding="utf-8") as f: f.write("name,group,height,weight,score\nAla,A,165.0,58.5,72\nJan,B,180.5,77.0,85\nEwa,A,172.0,68.0,90\nOlek,B,178.0,74.0,64\nIga,A,160.5,57.5,78\nTom,B,183.0,81.5,85\nOla,A,168.5,60.0,91\nPiotr,A,175.5,64.0,58\n")  #| hide
import pandas as pd

df = pd.read_csv("students.csv")
score = df["score"]
print(score.mean(), score.median())
print(f"{score.std():.3f}")
print(f"{score.quantile(0.9):.1f}")
print(score.min(), score.max())
```

### See also

- aggregates/sum-mean-min-and-max
- aggregates/standard-deviation-and-variance
- aggregates/median-and-percentiles

## value_counts

PL: value_counts

`df["group"].value_counts()` counts how often each value appears in a column, most frequent first. With `normalize=True` it gives proportions that add up to 1 instead.

PL: `df["group"].value_counts()` zlicza, ile razy każda wartość pojawia się w kolumnie, od najczęstszej. Z `normalize=True` daje zamiast tego proporcje, które sumują się do 1.

```python
with open("students.csv", "w", encoding="utf-8") as f: f.write("name,group,height,weight,score\nAla,A,165.0,58.5,72\nJan,B,180.5,77.0,85\nEwa,A,172.0,68.0,90\nOlek,B,178.0,74.0,64\nIga,A,160.5,57.5,78\nTom,B,183.0,81.5,85\nOla,A,168.5,60.0,91\nPiotr,A,175.5,64.0,58\n")  #| hide
import pandas as pd

df = pd.read_csv("students.csv")
group = df["group"]
print(group.value_counts())
print(group.value_counts(normalize=True))
```

### See also

- collections/counting-with-counter
- aggregates/counting-and-proportions-with-a-mask

## unique and nunique

PL: unique i nunique

`df["score"].unique()` returns the distinct values of a column in the order they first appear, and `.nunique()` counts them. Here two students have the same score, so there are 7 distinct scores among 8 students.

PL: `df["score"].unique()` zwraca różne wartości kolumny w kolejności, w jakiej pojawiają się po raz pierwszy, a `.nunique()` je zlicza. Tutaj dwoje studentów ma ten sam wynik, więc wśród 8 studentów jest 7 różnych wyników.

```python
with open("students.csv", "w", encoding="utf-8") as f: f.write("name,group,height,weight,score\nAla,A,165.0,58.5,72\nJan,B,180.5,77.0,85\nEwa,A,172.0,68.0,90\nOlek,B,178.0,74.0,64\nIga,A,160.5,57.5,78\nTom,B,183.0,81.5,85\nOla,A,168.5,60.0,91\nPiotr,A,175.5,64.0,58\n")  #| hide
import pandas as pd

df = pd.read_csv("students.csv")
print(df["score"].unique())
print(df["score"].nunique(), len(df))
print(df["group"].nunique())
```

### See also

- sets/unique-values

## Correlation with corr()

PL: Korelacja z corr()

`df[["height", "weight"]].corr()` gives the Pearson correlation of every pair of the chosen columns as a table, with 1 on the diagonal; the double brackets pick several columns. `df["height"].corr(df["weight"])` gives a single pair as one number.

PL: `df[["height", "weight"]].corr()` podaje współczynnik korelacji (correlation) Pearsona dla każdej pary wybranych kolumn jako tabelę z 1 na przekątnej; podwójne nawiasy wybierają kilka kolumn. `df["height"].corr(df["weight"])` daje jedną parę jako pojedynczą liczbę.

```python
with open("students.csv", "w", encoding="utf-8") as f: f.write("name,group,height,weight,score\nAla,A,165.0,58.5,72\nJan,B,180.5,77.0,85\nEwa,A,172.0,68.0,90\nOlek,B,178.0,74.0,64\nIga,A,160.5,57.5,78\nTom,B,183.0,81.5,85\nOla,A,168.5,60.0,91\nPiotr,A,175.5,64.0,58\n")  #| hide
import pandas as pd

df = pd.read_csv("students.csv")
print(df[["height", "weight"]].corr())
r = df["height"].corr(df["weight"])
print(f"{r:.3f}")
```

### See also

- selecting/one-column-or-several
- heatmaps/colour-maps-and-fixed-limits
