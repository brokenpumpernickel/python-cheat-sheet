---
title: Derivatives and limits
glyph: "diff"
summary: "Derivatives and limits of SymPy expressions: diff, higher and partial derivatives, one-sided limits and Taylor series."
pl:
  title: Pochodne i granice
  summary: "Pochodne (derivatives) i granice (limits) wyrażeń SymPy: diff, pochodne wyższych rzędów i cząstkowe, granice jednostronne i szereg Taylora."
---

## Derivatives

PL: Pochodne (derivatives)

`expr.diff(x)` and `sp.diff(expr, x)` are the same: the derivative of `expr` with respect to `x`. Other symbols, such as `a` here, are treated as constants.

PL: `expr.diff(x)` i `sp.diff(expr, x)` robią to samo: liczą pochodną `expr` względem `x`. Inne symbole, jak tu `a`, są traktowane jako stałe.

```python
import sympy as sp
sp.init_printing()

x, a = sp.symbols("x a")
f = sp.exp(-a*x**2)
display(f.diff(x))
display(sp.diff(f, x))
display(sp.diff(x**3 + 2*x, x))
```

### See also

- expressions/building-expressions
- evaluating/substituting-values

## Higher derivatives

PL: Pochodne wyższych rzędów (higher derivatives)

`expr.diff(x, x)` or `expr.diff(x, 2)` differentiates twice, and `expr.diff(x, 10)` gives the 10th derivative without writing `x` ten times.

PL: `expr.diff(x, x)` albo `expr.diff(x, 2)` różniczkuje dwa razy, a `expr.diff(x, 10)` daje pochodną 10. rzędu bez pisania `x` dziesięć razy.

```python
import sympy as sp
sp.init_printing()

x, a = sp.symbols("x a")
f = sp.exp(-a*x**2)
display(f.diff(x, x))
display(f.diff(x, 2))
display(sp.sin(2*x).diff(x, 10))
```

### See also

- differential-equations/functions-and-their-derivatives
- probability/moment-generating-functions

## Partial derivatives

PL: Pochodne cząstkowe (partial derivatives)

For a function of several symbols, `f.diff(x)` is the partial derivative with respect to `x`, and `f.diff(x, y)` differentiates by `x`, then by `y`.

PL: Dla funkcji kilku symboli `f.diff(x)` to pochodna cząstkowa względem `x`, a `f.diff(x, y)` różniczkuje najpierw po `x`, potem po `y`.

```python
import sympy as sp
sp.init_printing()

x, y = sp.symbols("x y")
f = x**2 * y + sp.sin(x*y)
display(f.diff(x))
display(f.diff(y))
display(f.diff(x, y))
```

## Limits

PL: Granice (limits)

`sp.limit(expr, x, x0)` is the limit of `expr` as `x` goes to `x0`, which may be `sp.oo`. `dir="+"` takes the one-sided limit from the right, and `dir="-"` from the left.

PL: `sp.limit(expr, x, x0)` to granica `expr`, gdy `x` dąży do `x0`, którym może być też `sp.oo`. `dir="+"` liczy granicę jednostronną z prawej strony, a `dir="-"` z lewej.

```python
import sympy as sp
sp.init_printing()

x = sp.Symbol("x")
display(sp.limit(sp.sin(x)/x, x, 0))
display(sp.limit((1 + 1/x)**x, x, sp.oo))
display(sp.limit(1/x, x, 0, dir="+"))
display(sp.limit(1/x, x, 0, dir="-"))
```

### Pitfall

Without `dir`, `sp.limit` approaches from the right only, so `sp.limit(1/x, x, 0)` gives ∞ although `1/x` has no limit at 0.

PL: Bez `dir` funkcja `sp.limit` dąży do punktu tylko z prawej strony, więc `sp.limit(1/x, x, 0)` daje ∞, choć `1/x` nie ma granicy w 0.

```python
import sympy as sp
sp.init_printing()

x = sp.Symbol("x")
display(sp.limit(1/x, x, 0))
```

### See also

- symbols/constants

## Taylor series

PL: Szereg Taylora (Taylor series)

`sp.series(expr, x, x0, n)` expands `expr` around `x0` up to, but not including, `x**n`, and ends with an O term for the rest. `.removeO()` drops it, leaving a polynomial you can compute with.

PL: `sp.series(expr, x, x0, n)` rozwija `expr` wokół `x0` aż do `x**n`, bez niego, i kończy wyrazem O, który oznacza resztę. `.removeO()` go usuwa i zostaje wielomian, na którym można dalej liczyć.

```python
import sympy as sp
sp.init_printing()

x = sp.Symbol("x")
s = sp.series(sp.exp(x), x, 0, 5)
display(s)
display(s.removeO())
display(sp.series(sp.cos(x), x, 0, 6))
```
