---
title: Subplots
glyph: "ax[ ]"
summary: "Several plots in one figure: plt.subplot(121), plots spanning columns, grids with plt.subplots, shared axes, size and layout."
pl:
  title: Podwykresy
  summary: "Podwykresy (subplots), czyli kilka wykresów na jednym rysunku: plt.subplot(121), wykresy na kilka kolumn, siatki z plt.subplots, wspólne osie, rozmiar i układ."
---

## Side-by-side plots with plt.subplot(121)

PL: Wykresy obok siebie z plt.subplot(121)

`plt.subplot(121)` splits the figure into 1 row and 2 columns and makes plot 1 the current one, so every `plt` call after it draws there until `plt.subplot(122)` moves to plot 2. The three digits are rows, columns and index, the same as `plt.subplot(1, 2, 1)`.

PL: `plt.subplot(121)` dzieli rysunek na 1 wiersz i 2 kolumny podwykresów (subplots) i ustawia wykres 1 jako bieżący, więc każde wywołanie `plt` po nim rysuje tam, dopóki `plt.subplot(122)` nie przejdzie do wykresu 2. Trzy cyfry to wiersze, kolumny i numer, tak samo jak `plt.subplot(1, 2, 1)`.

```python
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(6)  #| hide
plt.figure(figsize=(6, 3.5))
plt.subplot(121)
plt.hist(np.random.uniform(0, 1, 500))
plt.title("U(0, 1)")
plt.subplot(122)
plt.hist(np.random.normal(0, 1, 500))
plt.title("N(0, 1)")
plt.show()
```

### Figure

Two histograms side by side: on the left, U(0, 1), ten bars of similar height, between about 45 and 55; on the right, N(0, 1), a bell shape around 0.

PL: Dwa histogramy obok siebie: po lewej U(0, 1), dziesięć słupków podobnej wysokości, od około 45 do 55; po prawej N(0, 1), kształt dzwonu wokół 0.

## Plots spanning several columns

PL: Wykresy na kilka kolumn

Each `plt.subplot` call can split the figure its own way, so plots of different sizes share one figure. `plt.subplot(221)` and `plt.subplot(222)` are the top half of a 2 by 2 grid, and `plt.subplot(212)`, plot 2 of a 2 by 1 grid, is the bottom half across both columns.

PL: Każde wywołanie `plt.subplot` może dzielić rysunek po swojemu, więc podwykresy (subplots) różnej wielkości mieszczą się na jednym rysunku. `plt.subplot(221)` i `plt.subplot(222)` to górna połowa siatki 2 na 2, a `plt.subplot(212)`, czyli wykres 2 siatki 2 na 1, to dolna połowa przez obie kolumny.

```python
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(7)  #| hide
a = np.random.normal(0, 1, 200)
b = np.random.normal(0, 3, 200)
plt.figure(figsize=(6, 3.5))
plt.subplot(221)
plt.hist(a)
plt.title("a")
plt.subplot(222)
plt.hist(b)
plt.title("b")
plt.subplot(212)
plt.plot(b)
plt.plot(a)
plt.show()
```

### Figure

Two histograms side by side on top, a and b, both bell-shaped around 0, with b about three times as wide; below them one wide plot across both columns shows the 200 values of each sample in order, b swinging much further from 0 than a.

PL: U góry dwa histogramy obok siebie, a i b, oba w kształcie dzwonu wokół 0, przy czym b jest mniej więcej trzy razy szerszy; pod nimi jeden szeroki wykres przez obie kolumny pokazuje po kolei 200 wartości każdej próbki, a b oddala się od 0 znacznie bardziej niż a.

## A grid of plots with plt.subplots

PL: Siatka wykresów z plt.subplots

`fig, axes = plt.subplots(2, 2)` makes a figure with a 2 by 2 grid of plots and returns them as an array: `axes[0, 1]` is row 0, column 1, and `axes.flat` goes through them row by row. You then draw with each plot's own methods, such as `ax.hist`; `layout="constrained"` keeps the titles apart.

PL: `fig, axes = plt.subplots(2, 2)` tworzy rysunek z siatką 2 na 2 wykresów i zwraca je jako tablicę osi (Axes): `axes[0, 1]` to wiersz 0, kolumna 1, a `axes.flat` przechodzi po nich wierszami. Rysujesz potem metodami każdego wykresu, np. `ax.hist`; `layout="constrained"` rozsuwa tytuły.

```python
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(1)  #| hide
sizes = [10, 100, 1000, 10000]
fig, axes = plt.subplots(
    2, 2, figsize=(6, 3.5),
    layout="constrained")
for ax, n in zip(axes.flat, sizes):
    sample = np.random.normal(0, 1, n)
    ax.hist(sample, bins=20)
    ax.set_title(f"n = {n}")

plt.show()
```

### Figure

Four histograms of normal samples in a 2 by 2 grid, titled n = 10, n = 100, n = 1000 and n = 10000; the larger n, the smoother the bell shape.

PL: Cztery histogramy próbek z rozkładu normalnego w siatce 2 na 2, z tytułami n = 10, n = 100, n = 1000 i n = 10000; im większe n, tym gładszy kształt dzwonu.

### Pitfall

`plt.title`, `plt.xlabel` and the like draw on the current plot only, which is the last one made, so here both titles land on the right plot. On a plot from `plt.subplots` use its methods: `ax.set_title`, `ax.set_xlabel`, `ax.set_ylabel`, `ax.set_xlim`, `ax.set_ylim`.

PL: `plt.title`, `plt.xlabel` i podobne rysują tylko na bieżącym wykresie, czyli ostatnio utworzonym, więc tu oba tytuły trafiają na prawy wykres. Na wykresie z `plt.subplots` użyj jego metod: `ax.set_title`, `ax.set_xlabel`, `ax.set_ylabel`, `ax.set_xlim`, `ax.set_ylim`.

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(
    1, 2, figsize=(6, 3.5))
axes[0].plot([1, 2, 3])
plt.title("a")
axes[1].plot([3, 2, 1])
plt.title("b")
plt.show()
```

### Figure

Two plots side by side, a line rising on the left and a line falling on the right; only the right plot has a title, b, and the left one has none.

PL: Dwa wykresy obok siebie, rosnąca linia po lewej i malejąca po prawej; tytuł b ma tylko prawy wykres, lewy nie ma żadnego.

### See also

- loops/looping-with-zip

## Shared axes

PL: Wspólne osie

`sharex=True` gives all the plots the same x-axis range, and `sharey=True` the same y-axis range, so you can compare them by eye. Here two samples with different means and spreads sit one above the other on one x scale.

PL: `sharex=True` daje wszystkim wykresom ten sam zakres osi x, a `sharey=True` ten sam zakres osi y, więc porównasz je na oko dzięki wspólnym osiom (shared axes). Tu dwie próbki o różnych średnich i rozrzutach stoją jedna nad drugą na jednej skali x.

```python
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(17)  #| hide
a = np.random.normal(0, 1, 500)
b = np.random.normal(2, 2, 500)
fig, axes = plt.subplots(
    2, 1, sharex=True, figsize=(6, 3.5))
axes[0].hist(a, bins=30)
axes[1].hist(b, bins=30)
plt.show()
```

### Figure

Two histograms stacked on one shared x-axis: the top one narrow and centred on 0, the bottom one about twice as wide and centred on 2.

PL: Dwa histogramy jeden nad drugim na wspólnej osi x: górny wąski, ze środkiem w 0, dolny mniej więcej dwa razy szerszy, ze środkiem w 2.

## Figure size and layout

PL: Rozmiar i układ rysunku

`figsize=(width, height)` sets the figure's size in inches, both in `plt.figure` and in `plt.subplots`. `layout="constrained"` makes room for every title, axis label and colour bar so nothing overlaps.

PL: `figsize=(width, height)` ustala rozmiar rysunku w calach, zarówno w `plt.figure`, jak i w `plt.subplots`. `layout="constrained"` robi miejsce na każdy tytuł, opis osi i pasek kolorów, żeby nic na siebie nie nachodziło; to układ (layout) rysunku.

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2, 100)
fig, axes = plt.subplots(
    2, 2, figsize=(6, 3.5),
    layout="constrained")
for k, ax in enumerate(axes.flat):
    ax.plot(x, x ** k)
    ax.set_title(f"k = {k}")
    ax.set_xlabel("x")

plt.show()
```

### Figure

A 2 by 2 grid of curves titled k = 0 to k = 3, each with its x-axis labelled x, all neatly spaced: a flat line, a straight line, and two curves rising ever faster.

PL: Siatka 2 na 2 krzywych z tytułami od k = 0 do k = 3, każda z osią x opisaną jako x, wszystko równo rozmieszczone: pozioma linia, prosta i dwie krzywe rosnące coraz szybciej.

### Pitfall

Without `layout="constrained"`, a grid of plots keeps its default spacing, so the x labels of the top row run into the titles of the bottom row.

PL: Bez `layout="constrained"` siatka wykresów zachowuje domyślne odstępy, więc opisy osi x górnego rzędu nachodzą na tytuły dolnego.

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2, 100)
fig, axes = plt.subplots(
    2, 2, figsize=(6, 3.5))
for k, ax in enumerate(axes.flat):
    ax.plot(x, x ** k)
    ax.set_title(f"k = {k}")
    ax.set_xlabel("x")

plt.show()
```

### Figure

The same 2 by 2 grid squeezed together: the x labels and tick numbers of the top row overlap the titles k = 2 and k = 3 of the bottom row.

PL: Ta sama siatka 2 na 2, ściśnięta: opisy osi x i liczby na osiach górnego rzędu nachodzą na tytuły k = 2 i k = 3 dolnego rzędu.

### See also

- loops/enumerate
