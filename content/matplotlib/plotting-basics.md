---
title: Plotting basics
glyph: "plt"
summary: "Line plots with plt: labels and a title, legends, colours and styles, limits, reference lines, saving."
pl:
  title: Podstawy wykresów
  summary: "Wykresy liniowe (line plots) z plt: opisy osi i tytuł, legenda, kolory i style, zakresy, linie odniesienia, zapis do pliku."
---

## A line plot

PL: Wykres liniowy

`plt.plot(x, y)` joins the points `(x, y)` with straight lines, so many points from `np.linspace` make a smooth curve. `plt.figure(figsize=(6, 3.5))` starts a figure 6 by 3.5 inches, and `plt.show()` shows it.

PL: `plt.plot(x, y)` łączy punkty `(x, y)` odcinkami, więc wiele punktów z `np.linspace` daje gładką krzywą. `plt.figure(figsize=(6, 3.5))` zaczyna rysunek (figure) o wymiarach 6 na 3,5 cala, a `plt.show()` go pokazuje.

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)
plt.figure(figsize=(6, 3.5))
plt.plot(x, np.sin(x))
plt.show()
```

### Figure

A sine wave from x = 0 to 10, swinging between −1 and 1 a little over one and a half times.

PL: Sinusoida od x = 0 do 10, wahająca się między −1 a 1 nieco ponad półtora raza.

### See also

- arrays/ranges
- array-maths/maths-functions

## Axis labels and a title

PL: Opisy osi i tytuł

`plt.xlabel(text)` and `plt.ylabel(text)` describe the axes, and `plt.title(text)` names the plot. Here the x-axis shows `x`, the y-axis the density `f(x)` of the standard normal distribution, and the title is `N(0, 1)`.

PL: `plt.xlabel(text)` i `plt.ylabel(text)` opisują osie (axis labels), a `plt.title(text)` nadaje wykresowi tytuł. Tu oś x pokazuje `x`, oś y gęstość `f(x)` standardowego rozkładu normalnego, a tytuł to `N(0, 1)`.

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-4, 4, 200)
c = np.sqrt(2 * np.pi)
plt.figure(figsize=(6, 3.5))
plt.plot(x, np.exp(-x ** 2 / 2) / c)
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("N(0, 1)")
plt.show()
```

### Figure

A bell curve titled N(0, 1), peaking at about 0.4 at x = 0, with the x-axis labelled x and the y-axis f(x).

PL: Krzywa dzwonowa z tytułem N(0, 1), ze szczytem około 0,4 w x = 0; oś x opisana jako x, oś y jako f(x).

## Several lines and a legend

PL: Kilka linii i legenda

Every `plt.plot` call adds one more line to the same figure. Give each one a name with `label=...`, and `plt.legend()` lists the names beside their line styles.

PL: Każde wywołanie `plt.plot` dodaje kolejną linię do tego samego wykresu. Nazwij każdą przez `label=...`, a `plt.legend()` wyświetli legendę (legend) z nazwami obok stylów linii.

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-5, 5, 200)
plt.figure(figsize=(6, 3.5))
for s in [0.5, 1, 2]:
    y = np.exp(-(x / s) ** 2 / 2)
    y = y / (s * np.sqrt(2 * np.pi))
    plt.plot(x, y, label=f"σ = {s}")

plt.legend()
plt.show()
```

### Figure

Three bell curves centred on 0, with a legend for σ = 0.5, σ = 1 and σ = 2; the smaller σ, the taller and narrower the curve.

PL: Trzy krzywe dzwonowe o środku w 0 i legenda dla σ = 0,5, σ = 1 i σ = 2; im mniejsze σ, tym krzywa wyższa i węższa.

### See also

- loops/for-over-a-collection
- strings/f-strings

## Colours, markers and line styles

PL: Kolory, znaczniki i style linii

`color=` sets a line's colour, `marker=` puts a symbol on every point (`"o"` dots, `"s"` squares) and `linestyle=` draws it dashed (`"--"`) or dotted (`":"`). A short format string sets all three at once: `"gs:"` is green squares on a dotted line.

PL: `color=` ustawia kolor linii, `marker=` stawia znacznik (marker) w każdym punkcie (`"o"` kropki, `"s"` kwadraty), a `linestyle=` rysuje ją kreskowaną (`"--"`) lub kropkowaną (`":"`). Krótki napis formatu (format string) ustawia wszystkie trzy naraz: `"gs:"` to zielone kwadraty na kropkowanej linii.

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(1, 11)
plt.figure(figsize=(6, 3.5))
plt.plot(x, x ** 2, color="red",
         marker="o")
plt.plot(x, 10 * x, color="black",
         linestyle="--")
plt.plot(x, 5 * x, "gs:")
plt.show()
```

### Figure

Three lines over x = 1 to 10: red dots on a curve rising ever faster, a black dashed straight line, and green squares on a dotted, less steep straight line.

PL: Trzy linie dla x od 1 do 10: czerwone kropki na krzywej rosnącej coraz szybciej, czarna kreskowana prosta i zielone kwadraty na kropkowanej, łagodniejszej prostej.

## Axis limits and a grid

PL: Zakresy osi i siatka

`plt.xlim(low, high)` and `plt.ylim(low, high)` fix the range each axis shows, and `plt.grid(True)` draws grid lines. Here the share of heads after `n` coin flips settles near 0.5 on a y-axis from 0 to 1; `cumsum` counts the heads so far.

PL: `plt.xlim(low, high)` i `plt.ylim(low, high)` ustalają zakres (limits) każdej osi, a `plt.grid(True)` rysuje siatkę (grid). Tu odsetek orłów po `n` rzutach monetą ustala się blisko 0,5 na osi y od 0 do 1; `cumsum` liczy dotychczasowe orły.

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(3)
flips = rng.integers(0, 2, 500)
n = np.arange(1, 501)
plt.figure(figsize=(6, 3.5))
plt.plot(n, flips.cumsum() / n)
plt.xlim(0, 500)
plt.ylim(0, 1)
plt.grid(True)
plt.show()
```

### Figure

A jagged line over n = 1 to 500 on a grid, jumping around at first and then settling close to 0.5, on a y-axis from 0 to 1.

PL: Poszarpana linia dla n od 1 do 500 na tle siatki, na początku skacze, potem ustala się blisko 0,5; oś y od 0 do 1.

### See also

- random/uniform-numbers-and-integers

## Horizontal and vertical lines

PL: Linie poziome i pionowe

`plt.axhline(y)` draws a horizontal line across the whole plot at height `y`, and `plt.axvline(x)` a vertical one at `x`, to mark a threshold or the mean. They take `color` and `linestyle` like `plt.plot`; `plt.plot(scores)` alone puts the values at x = 0, 1, 2, ….

PL: `plt.axhline(y)` rysuje poziomą linię przez cały wykres na wysokości `y`, a `plt.axvline(x)` pionową w `x`, np. dla progu albo średniej. Przyjmują `color` i `linestyle` jak `plt.plot`; samo `plt.plot(scores)` stawia wartości w x = 0, 1, 2, ….

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(5)
scores = rng.normal(70, 8, 30)
plt.figure(figsize=(6, 3.5))
plt.plot(scores, marker="o")
plt.axhline(scores.mean(), color="red")
plt.axvline(scores.argmax(), color="gray",
            linestyle="--")
plt.show()
```

### Figure

Thirty points joined by a zigzag line between about 55 and 85, a red horizontal line across the plot at their mean, and a grey dashed vertical line through the highest point.

PL: Trzydzieści punktów połączonych zygzakiem między około 55 a 85, czerwona pozioma linia przez cały wykres na wysokości ich średniej i szara kreskowana pionowa linia przez najwyższy punkt.

### See also

- aggregates/where-the-minimum-and-maximum-are
- aggregates/sum-mean-min-and-max

## Saving a figure

PL: Zapisywanie wykresu

`plt.savefig("name.png")` writes the figure to a file in the current folder, and the extension picks the format: `.png`, `.pdf` or `.svg`. `dpi=` sets how many pixels per inch a PNG gets.

PL: `plt.savefig("name.png")` zapisuje wykres do pliku w bieżącym folderze, a rozszerzenie wybiera format: `.png`, `.pdf` lub `.svg`. `dpi=` ustala, ile pikseli na cal dostaje plik PNG.

```python
import os
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)
plt.figure(figsize=(6, 3.5))
plt.plot(x, np.sqrt(x))
plt.savefig("sqrt.png", dpi=150)
print(os.path.exists("sqrt.png"))
plt.show()
```

### Figure

A curve rising steeply from 0 and then flattening, reaching about 3.2 at x = 10.

PL: Krzywa, która rośnie stromo od 0, a potem się wypłaszcza, dochodząc do około 3,2 w x = 10.

### Pitfall

In a script, call `plt.savefig` before `plt.show()`. Once the figure has been shown it is closed, so a `savefig` after `show` saves a new, empty figure.

PL: W skrypcie wywołaj `plt.savefig` przed `plt.show()`. Pokazany wykres zostaje zamknięty, więc `savefig` po `show` zapisuje nowy, pusty wykres.
