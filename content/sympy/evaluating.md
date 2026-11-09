---
title: Substituting and evaluating
glyph: "subs"
summary: "Putting values into SymPy expressions: substituting numbers and expressions, decimal values, and NumPy functions with lambdify."
pl:
  title: Podstawianie i obliczanie
  summary: "Podstawianie (substitution) wartości do wyrażeń SymPy: liczby i wyrażenia w miejsce symboli, wartości dziesiętne i funkcje dla NumPy z lambdify."
---

## Substituting values

PL: Podstawianie wartości (subs)

`expr.subs(a, 10)` puts `10` in place of the symbol `a` and returns a new expression. To substitute several symbols at once, pass a dict, `expr.subs({a: 10, x: 3})`; once every symbol has a value, the result is an exact number.

PL: `expr.subs(a, 10)` wstawia `10` w miejsce symbolu `a` i zwraca nowe wyrażenie. Kilka symboli naraz podstawisz, podając słownik (dict), `expr.subs({a: 10, x: 3})`; gdy każdy symbol ma już wartość, wynik jest dokładną liczbą.

```python
import sympy as sp
sp.init_printing()

x, a = sp.symbols("x a")
expr = a*x**2 + 2*x
display(expr.subs(a, 10))
display(expr.subs({a: 10, x: 3}))
```

### Pitfall

`subs` returns a new expression and leaves `expr` as it was, so a `subs` whose result you don't keep changes nothing.

PL: `subs` zwraca nowe wyrażenie, a `expr` zostawia bez zmian, więc `subs`, którego wyniku nie zachowasz, niczego nie zmienia.

```python
import sympy as sp
sp.init_printing()

x, a = sp.symbols("x a")
expr = a*x**2 + 2*x
expr.subs(a, 10)
display(expr)
```

## Substituting an expression

PL: Podstawianie wyrażenia

`expr.subs(x, y + 1)` puts a whole expression in place of `x`, as in a change of variables, and `expr.subs(x, x**2)` replaces every `x` with `x**2`. The result isn't multiplied out; use `sp.expand` when you want that.

PL: `expr.subs(x, y + 1)` wstawia całe wyrażenie (expression) w miejsce `x`, jak przy zamianie zmiennych, a `expr.subs(x, x**2)` zastępuje każde `x` przez `x**2`. Wynik nie jest wymnożony; użyj `sp.expand`, jeśli tego chcesz.

```python
import sympy as sp
sp.init_printing()

x, y = sp.symbols("x y")
expr = x**2 + 3*x
display(expr.subs(x, y + 1))
display(sp.expand(expr.subs(x, y + 1)))
display(expr.subs(x, x**2))
```

### See also

- expressions/expanding-and-factoring

## Decimal values

PL: Wartości dziesiętne

After `subs` the value stays exact, with `sin(30)` left as it is. `.evalf()` turns it into a decimal with 15 significant digits, and `.evalf(30)` or `sp.N(val, 30)` with 30. Here `res` is the 10th derivative of `sin(a*x)`, from `sp.diff(expr, x, 10)`.

PL: Po `subs` wartość zostaje dokładna, a `sin(30)` pozostaje w tej postaci. `.evalf()` zamienia ją na liczbę dziesiętną z 15 cyframi znaczącymi, a `.evalf(30)` albo `sp.N(val, 30)` z 30. Tutaj `res` to 10. pochodna `sin(a*x)`, z `sp.diff(expr, x, 10)`.

```python
import sympy as sp
sp.init_printing()

x, a = sp.symbols("x a")
res = sp.diff(sp.sin(a*x), x, 10)
display(res)
val = res.subs({a: 10, x: 3})
display(val)
print(val.evalf())
print(val.evalf(30))
print(sp.N(val, 30))
```

### See also

- symbols/decimals-to-many-digits

## Functions for NumPy

PL: Funkcje dla NumPy

`f = sp.lambdify(x, expr)` turns an expression into a Python function that computes it with NumPy, so `f` takes a whole array, such as one from `np.linspace`. With several symbols, pass them as a tuple, `sp.lambdify((x, a), expr)`, and give the values in the same order.

PL: `f = sp.lambdify(x, expr)` zamienia wyrażenie w funkcję (function) Pythona, która liczy je w NumPy, więc `f` przyjmuje całą tablicę (array), np. z `np.linspace`. Przy kilku symbolach podaj je jako krotkę (tuple), `sp.lambdify((x, a), expr)`, a wartości przekaż w tej samej kolejności.

```python
import numpy as np
import sympy as sp
sp.init_printing()

x, a = sp.symbols("x a")
xs = np.linspace(0, 2, 3)
f = sp.lambdify(x, sp.exp(-x**2 / 2))
print(f(xs))
g = sp.lambdify((x, a), a * sp.exp(-a*x))
print(g(xs, 2))
```

### See also

- sympy-plots/plotting-with-lambdify
- arrays/ranges
