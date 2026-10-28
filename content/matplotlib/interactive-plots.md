---
title: Interactive plots
glyph: "(0,1)"
summary: "Plots driven by Jupyter widgets with interact: a slider, several sliders, dropdowns and checkboxes, the @interact decorator, sliders made explicitly, fixed values."
pl:
  title: Wykresy interaktywne
  summary: "Wykresy sterowane kontrolkami (widgets) Jupytera przez interact: suwak, kilka suwaków, listy rozwijane i pola wyboru, dekorator @interact, suwaki tworzone jawnie, stałe wartości."
---

## A slider with interact

PL: Suwak (slider) z interact

`interact(plot, mu=(-3.0, 3.0))` shows a slider from -3 to 3 and calls `plot` with its value, here the mean of a normal curve, again on every move. The function's default, `mu=0.0`, sets where the slider starts; without one, it starts in the middle. The `;` at the end keeps Jupyter from also printing the function `interact` returns.

PL: `interact(plot, mu=(-3.0, 3.0))` pokazuje suwak od -3 do 3 i wywołuje `plot` z jego wartością, tu średnią krzywej normalnej, przy każdym ruchu od nowa. Wartość domyślna funkcji, `mu=0.0`, ustala, gdzie suwak startuje; bez niej startuje w środku zakresu. Średnik `;` na końcu sprawia, że Jupyter nie wypisuje dodatkowo funkcji zwracanej przez `interact`.

```python
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact

def plot(mu=0.0):
    x = np.linspace(-6, 6, 200)
    y = np.exp(-(x - mu) ** 2 / 2)
    plt.figure(figsize=(6, 3.5))
    plt.plot(x, y / np.sqrt(2 * np.pi))
    plt.show()

interact(plot, mu=(-3.0, 3.0));
```

### Figure

A bell curve centred on x = 0, peaking at about 0.4, on an x-axis from −6 to 6.

PL: Krzywa dzwonowa o środku w x = 0, ze szczytem około 0,4, na osi x od −6 do 6.

### Pitfall

Whole numbers make a whole-number slider: `p=(0, 1)` gives only 0 or 1, so here the default 0.5 becomes 0. Write `(0.0, 1.0)`, or give a step: `(0, 1, 0.05)`.

PL: Liczby całkowite dają suwak liczb całkowitych: `p=(0, 1)` daje tylko 0 albo 1, więc tu domyślne 0.5 zamienia się w 0. Napisz `(0.0, 1.0)` albo podaj krok: `(0, 1, 0.05)`.

```python
import matplotlib.pyplot as plt
from ipywidgets import interact

def plot(p=0.5):
    plt.figure(figsize=(6, 3.5))
    plt.bar([0, 1], [1 - p, p])
    plt.ylim(0, 1)
    plt.show()

interact(plot, p=(0, 1));
```

### Figure

One wide bar at 0 reaching the top of a y-axis from 0 to 1, and no bar at all at 1.

PL: Jeden szeroki słupek w 0 sięgający szczytu osi y od 0 do 1, a w 1 nie ma żadnego słupka.

### See also

- functions/default-arguments
- plotting-distributions/a-pdf-curve

## Several sliders

PL: Kilka suwaków (sliders)

Give `interact` one keyword argument per slider, here the mean `mu` and the standard deviation `sigma` of a normal curve. Fix the axes inside the function with `plt.xlim` and `plt.ylim`, so every redraw has the same scale and you see the curve move and change shape.

PL: Podaj `interact` po jednym argumencie nazwanym (keyword argument) na każdy suwak, tu średnią `mu` i odchylenie standardowe `sigma` krzywej normalnej. Ustal osie w funkcji przez `plt.xlim` i `plt.ylim`, żeby każde przerysowanie miało tę samą skalę i żeby było widać, jak krzywa się przesuwa i zmienia kształt.

```python
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact

def plot(mu=0.0, sigma=1.0):
    x = np.linspace(-6, 6, 200)
    z = (x - mu) / sigma
    y = np.exp(-z ** 2 / 2)
    y = y / (sigma * np.sqrt(2 * np.pi))
    plt.figure(figsize=(6, 3.5))
    plt.plot(x, y)
    plt.xlim(-6, 6)
    plt.ylim(0, 0.85)
    plt.show()

interact(plot, mu=(-3.0, 3.0),
         sigma=(0.5, 3.0));
```

### Figure

A bell curve centred on x = 0 on fixed axes, x from −6 to 6 and y from 0 to 0.85; its peak of about 0.4 reaches less than half the height.

PL: Krzywa dzwonowa o środku w x = 0 na ustalonych osiach, x od −6 do 6 i y od 0 do 0,85; jej szczyt, około 0,4, nie sięga nawet połowy wysokości.

### Pitfall

Without `plt.xlim` and `plt.ylim` the axes are fitted to every new curve, so its peak always touches the top: as you move `sigma`, the curve seems to keep its height, and only the numbers on the y-axis change.

PL: Bez `plt.xlim` i `plt.ylim` osie dopasowują się do każdej nowej krzywej, więc jej szczyt zawsze sięga górnej krawędzi: gdy przesuwasz `sigma`, krzywa wydaje się mieć stałą wysokość, a zmieniają się tylko liczby na osi y.

### See also

- plotting-basics/axis-limits-and-a-grid
- plotting-distributions/comparing-parameters

## Dropdowns and checkboxes

PL: Listy rozwijane (dropdowns) i pola wyboru (checkboxes)

A list makes a dropdown, `True` or `False` a checkbox, and a string a text box. Here you choose the number of `bins` from `[10, 20, 50]` and switch `density` on or off for a histogram of 300 values drawn once, outside the function, so every redraw shows the same sample.

PL: Lista daje listę rozwijaną, `True` lub `False` pole wyboru, a napis pole tekstowe (text box). Tu wybierasz liczbę przedziałów `bins` z `[10, 20, 50]` i włączasz lub wyłączasz `density` dla histogramu 300 wartości wylosowanych raz, poza funkcją, więc każde przerysowanie pokazuje tę samą próbę.

```python
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact

np.random.seed(4)  #| hide
data = np.random.normal(0, 1, 300)

def plot(bins=10, density=False):
    plt.figure(figsize=(6, 3.5))
    plt.hist(data, bins=bins,
             density=density)
    plt.show()

interact(plot, bins=[10, 20, 50],
         density=False);
```

### Figure

Ten bars in a rough bell shape from about −2.4 to 2.8; the tallest, around 0, holds about 70 values.

PL: Dziesięć słupków w przybliżeniu w kształcie dzwonu, od około −2,4 do 2,8; najwyższy, wokół 0, mieści około 70 wartości.

### See also

- histograms/choosing-bins
- histograms/density-with-a-pdf-on-top

## The @interact decorator

PL: Dekorator (decorator) @interact

`@interact(n=(10, 1000, 10))` written above `def` makes the slider and shows the plot at once, with no separate `interact(...)` call; the third number is the step. Here the histogram shows the first `n` of 1000 values, and the larger `n`, the closer it comes to the normal curve drawn on top: the law of large numbers.

PL: `@interact(n=(10, 1000, 10))` napisane nad `def` od razu tworzy suwak (slider) i pokazuje wykres, bez osobnego wywołania `interact(...)`; trzecia liczba to krok. Tu histogram pokazuje pierwsze `n` z 1000 wartości, a im większe `n`, tym bliżej mu do narysowanej na nim krzywej normalnej: to prawo wielkich liczb (law of large numbers).

```python
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact

np.random.seed(222)  #| hide
data = np.random.normal(0, 1, 1000)
x = np.linspace(-4, 4, 200)
c = np.sqrt(2 * np.pi)

@interact(n=(10, 1000, 10))
def plot(n=50):
    plt.figure(figsize=(6, 3.5))
    plt.hist(data[:n], bins=20,
             range=(-4, 4), density=True)
    plt.plot(x, np.exp(-x ** 2 / 2) / c)
    plt.ylim(0, 0.8)
    plt.show()
```

### Figure

A smooth bell curve on an x-axis from −4 to 4 over a histogram of 50 values, all between −2 and 2; the bars are ragged, some well above the curve and some below it.

PL: Gładka krzywa dzwonowa na osi x od −4 do 4 nad histogramem 50 wartości, wszystkich między −2 a 2; słupki są nierówne, jedne wyraźnie powyżej krzywej, inne poniżej.

### See also

- indexing/indexing-and-slicing
- plotting-distributions/a-histogram-with-the-pdf

## Sliders made explicitly

PL: Suwaki (sliders) tworzone jawnie

`widgets.FloatSlider(min=..., max=..., step=..., value=..., description="σ")` makes a slider you set up fully, and `interact` uses it as it is: it starts at its `value`, not at the function's default. `continuous_update=False` redraws only when you let go of the slider, so a slow plot doesn't lag behind it.

PL: `widgets.FloatSlider(min=..., max=..., step=..., value=..., description="σ")` tworzy suwak, który ustawiasz w całości sam, a `interact` używa go bez zmian: suwak startuje od swojego `value`, a nie od wartości domyślnej funkcji. `continuous_update=False` przerysowuje wykres dopiero po puszczeniu suwaka, więc wolny wykres nie zostaje w tyle.

```python
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets import interact

def plot(sigma):
    x = np.linspace(-6, 6, 200)
    y = np.exp(-(x / sigma) ** 2 / 2)
    c = sigma * np.sqrt(2 * np.pi)
    plt.figure(figsize=(6, 3.5))
    plt.plot(x, y / c)
    plt.ylim(0, 0.85)
    plt.show()

slider = widgets.FloatSlider(
    min=0.5, max=3.0, step=0.1,
    value=1.5, description="σ",
    continuous_update=False)
interact(plot, sigma=slider);
```

### Figure

A wide, low bell curve centred on x = 0, peaking at about 0.27 on a y-axis from 0 to 0.85, and nearly flat at x = ±5.

PL: Szeroka, niska krzywa dzwonowa o środku w x = 0, ze szczytem około 0,27 na osi y od 0 do 0,85, prawie płaska przy x = ±5.

### See also

- plotting-basics/several-lines-and-a-legend
- plotting-distributions/a-pdf-curve

## Holding a value fixed

PL: Ustalona wartość

`fixed(scores)` passes `scores` to the function's `data` argument as it is, with no control for it, so one function can plot any sample. Without `fixed`, `interact` turns the array into a dropdown of its values.

PL: `fixed(scores)` przekazuje `scores` do argumentu `data` funkcji bez zmian i bez kontrolki (widget), więc jedna funkcja narysuje dowolną próbę. Bez `fixed` `interact` zamienia tablicę w listę rozwijaną (dropdown) jej wartości.

```python
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, fixed

def plot(data, bins=20):
    plt.figure(figsize=(6, 3.5))
    plt.hist(data, bins=bins)
    plt.show()

np.random.seed(7)  #| hide
scores = np.random.normal(65, 12, 200)
interact(plot, data=fixed(scores),
         bins=(5, 50));
```

### Figure

Twenty bars from about 37 to 92 in a rough bell shape around 65, with ragged tops.

PL: Dwadzieścia słupków od około 37 do 92, w przybliżeniu w kształcie dzwonu wokół 65, o nierównych wierzchołkach.

### See also

- random/normal-samples
- histograms/a-histogram
