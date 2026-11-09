---
title: Plotting with SymPy
glyph: "plot"
summary: "Plots of SymPy expressions: sp.plot for a quick curve, several curves at once, and lambdify with plt for everything Matplotlib can do."
pl:
  title: Wykresy w SymPy
  summary: "Wykresy (plots) wyrażeń SymPy: sp.plot do szybkiej krzywej, kilka krzywych naraz oraz lambdify z plt, gdy potrzebujesz wszystkiego, co daje Matplotlib."
---

## A plot with sp.plot

PL: Wykres z sp.plot

`sp.plot(expr, (x, -3, 3))` draws an expression straight from SymPy for `x` from -3 to 3, with the axes through zero and labelled `x` and `f(x)`; `size=(6, 3.5)` sets its size in inches. Keep the result in a name such as `p`, or Jupyter prints the plot object under the figure.

PL: `sp.plot(expr, (x, -3, 3))` rysuje wyrażenie prosto z SymPy dla `x` od -3 do 3, z osiami przechodzącymi przez zero i opisanymi `x` i `f(x)`; `size=(6, 3.5)` ustawia jego rozmiar w calach. Zachowaj wynik pod nazwą, np. `p`, bo inaczej Jupyter wypisze pod rysunkiem obiekt wykresu (plot).

```python
import sympy as sp
sp.init_printing()

x = sp.Symbol("x")
expr = x**3 - 3*x
p = sp.plot(expr, (x, -3, 3), size=(6, 3.5))
```

### Figure

A cubic curve from x = −3 to 3 on axes crossing at zero: it rises to a peak of 2 at x = −1, falls to a dip of −2 at x = 1, then climbs steeply to 18.

PL: Krzywa trzeciego stopnia od x = −3 do 3 na osiach przecinających się w zerze: rośnie do szczytu 2 w x = −1, spada do dołka −2 w x = 1, a potem stromo wspina się do 18.

## Several curves

PL: Kilka krzywych

`sp.plot(e1, e2, (x, a, b))` draws several expressions over the same range, each in its own colour, and `legend=True` adds a legend that names each curve by its expression.

PL: `sp.plot(e1, e2, (x, a, b))` rysuje kilka wyrażeń na tym samym przedziale, każde w innym kolorze, a `legend=True` dodaje legendę (legend), która podpisuje każdą krzywą jej wyrażeniem.

```python
import sympy as sp
sp.init_printing()

x = sp.Symbol("x")
p = sp.plot(sp.sin(x), sp.cos(x),
            (x, 0, 2*sp.pi),
            legend=True, size=(6, 3.5))
```

### Figure

One full period of sin(x) and cos(x) from x = 0 to 2π, with a legend: sin starts at 0 and cos at 1, both swing between −1 and 1, and they cross twice.

PL: Jeden pełny okres sin(x) i cos(x) od x = 0 do 2π, z legendą: sin zaczyna od 0, a cos od 1, oba wahają się między −1 a 1 i przecinają się dwa razy.

## Plotting with lambdify

PL: Wykres z lambdify

`f = sp.lambdify(x, expr)` gives a NumPy function, and `plt.plot(xs, f(xs))` on a `np.linspace` grid draws it with Matplotlib. This is the usual way when the plot needs Matplotlib's options, data beside the curve or subplots; here it is the normal density over a histogram of 500 samples.

PL: `f = sp.lambdify(x, expr)` daje funkcję dla NumPy, a `plt.plot(xs, f(xs))` na siatce z `np.linspace` rysuje ją w Matplotlib. To zwykły sposób, gdy wykres potrzebuje opcji Matplotlib, danych obok krzywej albo kilku wykresów (subplots); tutaj to gęstość rozkładu normalnego na histogramie 500 próbek.

```python
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
sp.init_printing()
np.random.seed(1)  #| hide

x = sp.Symbol("x")
expr = sp.exp(-x**2 / 2) / sp.sqrt(2*sp.pi)
f = sp.lambdify(x, expr)
xs = np.linspace(-4, 4, 200)
data = np.random.normal(size=500)
plt.figure(figsize=(6, 3.5))
plt.hist(data, bins=30, density=True)
plt.plot(xs, f(xs))
plt.show()
```

### Figure

A histogram of 500 samples, bell-shaped around 0, with the smooth normal density curve on top of it, peaking at about 0.4.

PL: Histogram 500 próbek, dzwonowaty wokół 0, a na nim gładka krzywa gęstości rozkładu normalnego ze szczytem około 0,4.

### See also

- evaluating/functions-for-numpy
- plotting-basics/a-line-plot
- arrays/ranges
