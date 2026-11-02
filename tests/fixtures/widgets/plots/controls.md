---
title: Controls
glyph: "~"
summary: Jupyter widgets.
pl:
  title: Kontrolki
  summary: Kontrolki Jupytera.
---

## Every control

PL: Każda kontrolka

`interact` makes a control for each argument; the function's defaults set where they start.

PL: `interact` tworzy kontrolkę dla każdego argumentu; wartości domyślne funkcji ustawiają, gdzie startują.

```python
import matplotlib.pyplot as plt
from ipywidgets import interact


def plot(mu=1.0, n=10, kind="b", show=True,
         name="x"):
    plt.figure(figsize=(6, 3.5))
    plt.plot([0, 1], [mu, n])
    plt.show()


interact(plot, mu=(-3.0, 3.0),
         n=(0, 100, 5), kind=["a", "b"],
         show=True, name="x")
```

### Figure

A straight line rising between two points.

PL: Prosta linia rosnąca między dwoma punktami.

## Nested containers

PL: Zagnieżdżone kontenery

Boxes inside boxes are walked in order; Output widgets are left out.

PL: Pudełka w pudełkach są przechodzone po kolei; widżety Output są pomijane.

```python
import ipywidgets as widgets
from IPython.display import display

box = widgets.Checkbox(value=False,
                       description="a")
row = widgets.HBox([box, widgets.Output()])
k = widgets.IntSlider(min=1, max=9, value=3,
                      description="k")
display(widgets.VBox([row, k]))
print("shown")
```

### Pitfall

A slider made explicitly keeps its own description.

PL: Suwak utworzony jawnie zachowuje swój opis.

```python
import ipywidgets as widgets
from ipywidgets import interact

def show(value):
    print(value)


s = widgets.FloatSlider(
    min=0, max=2, step=0.1, value=0.5,
    description="σ")
interact(show, value=s)
```
