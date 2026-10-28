---
title: Scatter plots
glyph: "x, y"
summary: "One dot per pair of values: a basic scatter plot, colour and size by value, a fitted line."
pl:
  title: Wykresy punktowe
  summary: "Wykresy punktowe (scatter plots): jedna kropka na parę wartości — podstawowy wykres, kolor i rozmiar według wartości, dopasowana prosta."
---

## A scatter plot

PL: Wykres punktowy

`plt.scatter(x, y)` draws one dot for each pair `(x[i], y[i])` and joins nothing, so you see how two measurements go together. Here `y` grows with `x` plus random noise.

PL: `plt.scatter(x, y)` rysuje wykres punktowy (scatter plot): jedną kropkę dla każdej pary `(x[i], y[i])`, bez łączenia, więc widać, jak dwa pomiary zmieniają się razem. Tu `y` rośnie razem z `x`, z dodanym losowym szumem.

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(11)  #| show: rng = np.random.default_rng()
x = rng.uniform(0, 10, 50)
y = 2 * x + rng.normal(0, 3, 50)
plt.figure(figsize=(6, 3.5))
plt.scatter(x, y)
plt.show()
```

### Figure

Fifty dots spread from lower left to upper right in a loose band, rising from about 0 to about 20 as x goes from 0 to 10.

PL: Pięćdziesiąt kropek rozrzuconych luźnym pasem od lewego dołu do prawej góry, rosnących od około 0 do około 20, gdy x idzie od 0 do 10.

### See also

- random/uniform-numbers-and-integers
- heatmaps/a-2d-histogram-of-points
- plotting-basics/format-strings

## Colour and size by value

PL: Kolor i rozmiar według wartości

`c=values` colours each dot by its value through a colour map, and `s=sizes` sets each dot's area. `plt.colorbar()` adds the scale that tells which colour is which value; `label=` names it. Here both show `r`, a dot's distance from `(0, 0)`.

PL: `c=values` koloruje każdą kropkę według jej wartości przez mapę kolorów (colormap), a `s=sizes` ustala pole każdej kropki. `plt.colorbar()` dodaje pasek kolorów (colorbar) z ich wartościami; `label=` go opisuje. Tu oba pokazują `r`, odległość kropki od `(0, 0)`.

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(12)  #| show: rng = np.random.default_rng()
x = rng.normal(0, 1, 100)
y = rng.normal(0, 1, 100)
r = np.sqrt(x ** 2 + y ** 2)
plt.figure(figsize=(6, 3.5))
plt.scatter(x, y, c=r, s=20 + 30 * r)
plt.colorbar(label="r")
plt.show()
```

### Figure

A round cloud of dots around (0, 0): small and dark purple in the middle, larger and yellow towards the edge, with a colour bar labelled r from 0 to about 2.5.

PL: Okrągła chmura kropek wokół (0, 0): w środku małe i ciemnofioletowe, ku brzegom większe i żółte, z paskiem kolorów opisanym r od 0 do około 2,5.

## Adding a fitted line

PL: Dopasowana prosta

`a, b = np.polyfit(x, y, 1)` fits the least-squares line `y = a * x + b` and returns its slope and intercept. Plot it over the dots with `plt.plot` on two `x` values, since two points make a straight line.

PL: `a, b = np.polyfit(x, y, 1)` dopasowuje prostą metodą najmniejszych kwadratów (least squares) `y = a * x + b` i zwraca jej współczynnik kierunkowy (slope) i wyraz wolny (intercept). Narysuj ją na kropkach przez `plt.plot` dla dwóch wartości `x`, bo dwa punkty wyznaczają prostą.

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(11)  #| show: rng = np.random.default_rng()
x = rng.uniform(0, 10, 50)
y = 2 * x + 1 + rng.normal(0, 3, 50)
a, b = np.polyfit(x, y, 1)
print(f"{a:.2f} {b:.2f}")
xs = np.array([0, 10])
plt.figure(figsize=(6, 3.5))
plt.scatter(x, y)
plt.plot(xs, a * xs + b, color="red")
plt.show()
```

### Figure

Fifty dots in a loose band rising from lower left to upper right, with a red straight line running through the middle of the band.

PL: Pięćdziesiąt kropek luźnym pasem od lewego dołu do prawej góry i czerwona prosta biegnąca środkiem tego pasa.

### See also

- tuples/unpacking
