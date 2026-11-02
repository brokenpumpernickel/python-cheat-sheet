---
title: Charts
glyph: "/\\"
summary: Line charts.
pl:
  title: Diagramy
  summary: Wykresy liniowe.
---

## Line chart

PL: Wykres liniowy

`plt.plot(x, y)` draws a line through the points.

PL: `plt.plot(x, y)` rysuje linię przez punkty.

```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3], [1, 4, 9])
plt.show()
print("one figure")
```

### Figure

A line rising ever faster through three points.

PL: Linia rosnąca coraz szybciej przez trzy punkty.

## Interactive chart

PL: Wykres interaktywny

`interact(plot, mu=(-3.0, 3.0))` makes a slider for `mu`; the function's default is where it starts.

PL: `interact(plot, mu=(-3.0, 3.0))` tworzy suwak (slider) dla `mu`; wartość domyślna funkcji ustawia, gdzie startuje.

```python
import matplotlib.pyplot as plt
from ipywidgets import interact


def plot(mu=1.0, n=10, kind="b", show=True,
         grid=False, name="x"):
    plt.figure(figsize=(6, 3.5))
    plt.plot([0, 1], [mu, n / 10])
    plt.grid(grid)
    plt.show()


interact(plot, mu=(-3.0, 3.0),
         n=(0, 100, 5), kind=["a", "b"],
         show=True, grid=False, name="x")
```

### Figure

A flat line between two points.

PL: Płaska linia między dwoma punktami.
