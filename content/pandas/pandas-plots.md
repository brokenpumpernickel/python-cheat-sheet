---
title: Plotting with pandas
glyph: ".plot"
summary: "Plots from a Series or DataFrame two ways, columns passed to plt or pandas' .plot(): a column against a distribution, line plots, bar charts of counts, scatter plots, histograms."
pl:
  title: Wykresy z pandas
  summary: "Wykresy z serii (Series) i ramki danych (DataFrame) na dwa sposoby, kolumny podane funkcjom plt albo .plot() z pandas: kolumna na tle rozkładu, liniowe, słupkowe z liczebnościami, punktowe i histogramy."
---

## Plotting columns with plt

PL: Wykresy kolumn przez plt

`plt.plot(df["year"], df["n"])`, `plt.scatter(df["height"], df["weight"])` and `plt.hist(df["score"], bins=20)` take columns as they are, and `.to_numpy()` gives plain arrays if you want them. When you already know Matplotlib this is often simpler than `.plot()`, the shortcut the next Entries show, which labels the axes with the column names. Here, on the left, the weight in kg against the height in cm of 200 students and, on the right, their scores.

PL: `plt.plot(df["year"], df["n"])`, `plt.scatter(df["height"], df["weight"])` i `plt.hist(df["score"], bins=20)` przyjmują kolumny takie, jakie są, a `.to_numpy()` daje zwykłe tablice (arrays), jeśli ich potrzebujesz. Gdy znasz już Matplotlib, to często prostsze niż `.plot()`, skrót pokazany w kolejnych hasłach, który opisuje osie nazwami kolumn. Tu po lewej waga w kg względem wzrostu w cm 200 studentów, a po prawej ich wyniki.

```python
import numpy as np  #| hide
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(7)  #| hide
height = np.random.normal(172, 9, 200).round(1)  #| hide
weight = (0.9 * (height - 100) + np.random.normal(0, 6, 200)).round(1)  #| hide
score = np.random.normal(70, 12, 200).clip(0, 100).round()  #| hide
pd.DataFrame({"height": height, "weight": weight, "score": score}).to_csv("students.csv", index=False)  #| hide
df = pd.read_csv("students.csv")
plt.figure(figsize=(6, 3.5))
plt.subplot(121)
plt.scatter(df["height"], df["weight"], s=10)
plt.xlabel("cm")
plt.ylabel("kg")
plt.subplot(122)
plt.hist(df["score"], bins=20)
plt.show()
```

### Figure

Two plots side by side. On the left, small dots in a loose band rising from lower left to upper right, x-axis labelled cm and y-axis kg; on the right, a histogram in a rough bell shape from about 35 to 100, tallest between 60 and 80.

PL: Dwa wykresy obok siebie. Po lewej małe kropki w luźnym pasie rosnącym od lewego dołu do prawej góry, oś x opisana jako cm, oś y jako kg; po prawej histogram w przybliżeniu w kształcie dzwonu od około 35 do 100, najwyższy między 60 a 80.

### See also

- plotting-basics/a-line-plot
- scatter-plots/a-scatter-plot
- histograms/a-histogram

## A column against a distribution

PL: Kolumna na tle rozkładu

`plt.hist(df["height"], bins=20, density=True)` draws a column on the scale of a pdf, and `plt.plot(x, stats.norm(m, s).pdf(x))` draws a normal curve over it, with `m` and `s` from the column's `.mean()` and `.std()`. Plot the curve on `x = np.linspace(...)` over the data's range, not on the column itself, which is unsorted. Here the x-axis shows the heights of 200 students in cm.

PL: `plt.hist(df["height"], bins=20, density=True)` rysuje kolumnę w skali gęstości (pdf), a `plt.plot(x, stats.norm(m, s).pdf(x))` rysuje na niej krzywą rozkładu normalnego (normal distribution), z `m` i `s` wziętymi z `.mean()` i `.std()` kolumny. Krzywą rysuj na `x = np.linspace(...)` w zakresie danych, a nie na samej kolumnie, która nie jest posortowana. Tu oś x pokazuje wzrost 200 studentów w cm.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

np.random.seed(7)  #| hide
height = np.random.normal(172, 9, 200).round(1)  #| hide
weight = (0.9 * (height - 100) + np.random.normal(0, 6, 200)).round(1)  #| hide
score = np.random.normal(70, 12, 200).clip(0, 100).round()  #| hide
pd.DataFrame({"height": height, "weight": weight, "score": score}).to_csv("students.csv", index=False)  #| hide
df = pd.read_csv("students.csv")
m = df["height"].mean()
s = df["height"].std()
x = np.linspace(df["height"].min(),
                df["height"].max(), 200)
plt.figure(figsize=(6, 3.5))
plt.hist(df["height"], bins=20, density=True)
plt.plot(x, stats.norm(m, s).pdf(x))
plt.show()
```

### Figure

Twenty uneven bars in a rough bell shape from about 151 to 193, with a smooth bell curve drawn over them that peaks near 172 at about 0.045; one bar near 168 rises well above it.

PL: Dwadzieścia nierównych słupków układa się w dzwon od około 151 do 193, a nałożona na nie gładka krzywa dzwonowa ma szczyt blisko 172, na wysokości około 0,045; jeden słupek przy 168 wyraźnie ją przewyższa.

### See also

- plotting-distributions/a-histogram-with-the-pdf
- histograms/density-with-a-pdf-on-top
- exploring/column-statistics

## A line plot of a Series

PL: Wykres liniowy serii

`df.groupby("year").size()` counts the rows of each year, and `.plot()` draws it as a line with the index, the years, on the x-axis. Here `sightings.csv` has one row per sighting, so the y-axis shows sightings per year; `plt.xlabel`, `plt.ylabel` and `plt.grid(ls="--")` work as on any plot.

PL: `df.groupby("year").size()` zlicza wiersze z każdego roku, a `.plot()` rysuje wynik jako linię, z indeksem (index), czyli latami, na osi x. Tu `sightings.csv` ma jeden wiersz na obserwację, więc oś y pokazuje liczbę obserwacji w roku; `plt.xlabel`, `plt.ylabel` i `plt.grid(ls="--")` działają jak na każdym wykresie.

```python
import numpy as np  #| hide
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(3)  #| hide
year = np.random.choice(np.arange(2014, 2025), 400, p=np.arange(1, 12) / 66)  #| hide
shape = np.random.choice(list("○□△◇"), 400, p=[0.4, 0.3, 0.2, 0.1])  #| hide
minutes = (np.random.exponential(1, 400) * pd.Series(shape).map({"○": 12, "□": 5, "△": 9, "◇": 15})).round(1)  #| hide
pd.DataFrame({"year": year, "shape": shape, "minutes": minutes}).to_csv("sightings.csv", index=False)  #| hide
df = pd.read_csv("sightings.csv")
plt.figure(figsize=(6, 3.5))
df.groupby("year").size().plot()
plt.xlabel("t")
plt.ylabel("n")
plt.grid(ls="--")
plt.show()
```

### Figure

A line over the years 2014 to 2024 on a dashed grid, x-axis labelled t and y-axis n, rising unevenly from under 10 to about 60.

PL: Linia dla lat od 2014 do 2024 na tle kreskowanej siatki, oś x opisana jako t, oś y jako n, rosnąca nierówno od poniżej 10 do około 60.

### See also

- plotting-basics/a-line-plot
- plotting-basics/axis-limits-and-a-grid
- grouping/group-sizes

## Bar charts of counts

PL: Wykresy słupkowe liczebności

`df["shape"].value_counts().plot(kind="bar")` draws one bar per value, most frequent first, here the sightings of each shape. A per-group mean from `groupby` comes in group order, so sort it first, as on the right for the mean minutes per shape. `rot=0` keeps the labels upright, and `plt.xlabel("")` drops the column name pandas writes under the bars.

PL: `df["shape"].value_counts().plot(kind="bar")` rysuje wykres słupkowy (bar chart): jeden słupek na wartość, od najczęstszej, tu liczbę obserwacji każdego kształtu. Średnia w grupach z `groupby` jest w kolejności grup, więc najpierw ją posortuj, jak po prawej dla średniej liczby minut na kształt. `rot=0` zostawia etykiety poziomo, a `plt.xlabel("")` usuwa nazwę kolumny, którą pandas wpisuje pod słupkami.

```python
import numpy as np  #| hide
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(3)  #| hide
year = np.random.choice(np.arange(2014, 2025), 400, p=np.arange(1, 12) / 66)  #| hide
shape = np.random.choice(list("○□△◇"), 400, p=[0.4, 0.3, 0.2, 0.1])  #| hide
minutes = (np.random.exponential(1, 400) * pd.Series(shape).map({"○": 12, "□": 5, "△": 9, "◇": 15})).round(1)  #| hide
pd.DataFrame({"year": year, "shape": shape, "minutes": minutes}).to_csv("sightings.csv", index=False)  #| hide
df = pd.read_csv("sightings.csv")
counts = df["shape"].value_counts()
means = df.groupby("shape")["minutes"].mean()
plt.figure(figsize=(6, 3.5))
plt.subplot(121)
counts.plot(kind="bar", rot=0)
plt.xlabel("")
plt.subplot(122)
means.sort_values().plot(kind="bar", rot=0)
plt.xlabel("")
plt.show()
```

### Figure

Two bar charts side by side, with a circle, a square, a triangle and a diamond under the bars. On the left the counts fall from the circle, about 155, to the diamond, about 35; on the right the mean minutes rise from the square, about 6, through the triangle and the diamond to the circle, about 13.

PL: Dwa wykresy słupkowe obok siebie, pod słupkami koło, kwadrat, trójkąt i romb. Po lewej liczebności maleją od koła, około 155, do rombu, około 35; po prawej średnie minuty rosną od kwadratu, około 6, przez trójkąt i romb do koła, około 13.

### See also

- exploring/value-counts
- bar-charts/bar-chart-of-counts
- subplots/side-by-side-plots-with-plt-subplot-121

## A scatter plot of two columns

PL: Wykres punktowy dwóch kolumn

`df.plot(kind="scatter", x="height", y="weight")` draws one dot per row, with the two named columns on the axes. A DataFrame's `.plot` starts a figure of its own, so give it the size there with `figsize=`. Here `students.csv` holds the height in cm and the weight in kg of 200 students, and `plt.xlabel` and `plt.ylabel` replace the column names pandas puts on the axes.

PL: `df.plot(kind="scatter", x="height", y="weight")` rysuje wykres punktowy (scatter plot): jedną kropkę na wiersz, z dwiema podanymi kolumnami na osiach. Metoda `.plot` ramki danych (DataFrame) zaczyna własny rysunek, więc rozmiar podaj w niej przez `figsize=`. Tu `students.csv` zawiera wzrost w cm i wagę w kg 200 studentów, a `plt.xlabel` i `plt.ylabel` zastępują nazwy kolumn, które pandas wpisuje na osiach.

```python
import numpy as np  #| hide
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(7)  #| hide
height = np.random.normal(172, 9, 200).round(1)  #| hide
weight = (0.9 * (height - 100) + np.random.normal(0, 6, 200)).round(1)  #| hide
score = np.random.normal(70, 12, 200).clip(0, 100).round()  #| hide
pd.DataFrame({"height": height, "weight": weight, "score": score}).to_csv("students.csv", index=False)  #| hide
df = pd.read_csv("students.csv")
df.plot(kind="scatter", x="height",
        y="weight", figsize=(6, 3.5))
plt.xlabel("cm")
plt.ylabel("kg")
plt.show()
```

### Figure

Two hundred dots in a loose band rising from lower left to upper right, x-axis labelled cm from about 150 to 192, y-axis kg from about 38 to 94.

PL: Dwieście kropek w luźnym pasie rosnącym od lewego dołu do prawej góry, oś x opisana jako cm od około 150 do 192, oś y jako kg od około 38 do 94.

### See also

- scatter-plots/a-scatter-plot
- exploring/correlation-with-corr

## A histogram of a column

PL: Histogram kolumny

`df["score"].plot(kind="hist", bins=20)` draws a histogram of one column, here the scores of 200 students, with the counts on the y-axis, which pandas labels `Frequency`; `plt.ylabel("n")` replaces it. `df.hist(bins=20, figsize=(6, 3.5))` draws one histogram per numeric column instead, each titled with its column name, in a figure of its own.

PL: `df["score"].plot(kind="hist", bins=20)` rysuje histogram jednej kolumny, tu wyników 200 studentów, z liczebnościami na osi y, którą pandas opisuje jako `Frequency`; `plt.ylabel("n")` zastępuje ten opis. `df.hist(bins=20, figsize=(6, 3.5))` rysuje za to po jednym histogramie na każdą kolumnę liczbową, z nazwą kolumny w tytule, na osobnym rysunku.

```python
import numpy as np  #| hide
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(7)  #| hide
height = np.random.normal(172, 9, 200).round(1)  #| hide
weight = (0.9 * (height - 100) + np.random.normal(0, 6, 200)).round(1)  #| hide
score = np.random.normal(70, 12, 200).clip(0, 100).round()  #| hide
pd.DataFrame({"height": height, "weight": weight, "score": score}).to_csv("students.csv", index=False)  #| hide
df = pd.read_csv("students.csv")
plt.figure(figsize=(6, 3.5))
df["score"].plot(kind="hist", bins=20)
plt.ylabel("n")
plt.show()
```

### Figure

Bars in a rough bell shape from about 35 to 100, tallest between 60 and 80, with the y-axis labelled n.

PL: Słupki w przybliżeniu w kształcie dzwonu od około 35 do 100, najwyższe między 60 a 80; oś y opisana jako n.

### Pitfall

`df.hist()` makes a figure of its own, as a DataFrame's `.plot()` does, so a `plt.figure(figsize=(6, 3.5))` before it stays empty, which Jupyter shows as `<Figure size 600x350 with 0 Axes>`, and the histograms come out at the default size, 6.4 by 4.8 inches. Pass `figsize=(6, 3.5)` to `df.hist` instead.

PL: `df.hist()` tworzy własny rysunek, tak jak `.plot()` ramki danych (DataFrame), więc `plt.figure(figsize=(6, 3.5))` przed nim zostaje pusty, co Jupyter pokazuje jako `<Figure size 600x350 with 0 Axes>`, a histogramy mają rozmiar domyślny, 6,4 na 4,8 cala. Zamiast tego podaj `figsize=(6, 3.5)` w `df.hist`.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(5)  #| hide
df = pd.DataFrame({
    "A": np.random.normal(60, 10, 200),
    "B": np.random.normal(75, 8, 200)})
plt.figure(figsize=(6, 3.5))
df.hist(bins=20)
plt.show()
```

### Figure

Two bell-shaped histograms side by side on a grid, titled A and B, in a figure taller than the others on this page; A peaks around 60 and B around 75.

PL: Dwa histogramy w kształcie dzwonu obok siebie na tle siatki, z tytułami A i B, na rysunku wyższym niż pozostałe na tej stronie; A ma szczyt około 60, a B około 75.

### See also

- histograms/a-histogram
- histograms/choosing-bins

## Pandas plots are Matplotlib plots

PL: Wykresy pandas to wykresy Matplotlib

A Series' `.plot()` draws on the current figure, so `plt.figure` before it and `plt.title`, `plt.xlabel` or `plt.show()` after it work as usual. A DataFrame's `.plot()` starts a new figure unless you pass `ax=`: `df.plot(ax=ax)` draws on a plot from `fig, ax = plt.subplots(figsize=(6, 3.5))`, one line per column, and the `ax.` methods add to it. Here `A` and `B` are two random walks.

PL: `.plot()` serii (Series) rysuje na bieżącym rysunku, więc `plt.figure` przed nim oraz `plt.title`, `plt.xlabel` czy `plt.show()` po nim działają jak zwykle. `.plot()` ramki danych (DataFrame) zaczyna nowy rysunek, chyba że podasz `ax=`: `df.plot(ax=ax)` rysuje na wykresie z `fig, ax = plt.subplots(figsize=(6, 3.5))`, po jednej linii na kolumnę, a metody `ax.` dodają do niego resztę. Tu `A` i `B` to dwa błądzenia losowe (random walks).

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(8)  #| hide
a = np.random.normal(0, 1, 50).cumsum()
b = np.random.normal(0, 1, 50).cumsum()
df = pd.DataFrame({"A": a, "B": b})
fig, ax = plt.subplots(figsize=(6, 3.5))
df.plot(ax=ax)
ax.axhline(0, color="gray", linestyle="--")
ax.set_xlabel("t")
plt.show()
```

### Figure

Two jagged lines over t = 0 to 49 with a legend, A and B, and a grey dashed horizontal line at 0; both wander between about −5 and 5 and cross several times.

PL: Dwie poszarpane linie dla t od 0 do 49 z legendą A i B oraz szara kreskowana pozioma linia na 0; obie błądzą między około −5 a 5 i kilka razy się przecinają.

### See also

- subplots/a-grid-of-plots-with-plt-subplots
- plotting-basics/axis-labels-and-a-title
- pandas-plots/plotting-columns-with-plt
