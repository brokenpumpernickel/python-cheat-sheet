---
title: Simplifying expressions
glyph: "(x+1)"
summary: "Building and reshaping SymPy expressions: functions, expanding and factoring, simplify, collecting terms and partial fractions."
pl:
  title: Upraszczanie wyrażeń
  summary: "Budowanie i przekształcanie wyrażeń (expressions) SymPy: funkcje, rozwijanie i rozkład na czynniki, simplify, grupowanie wyrazów i ułamki proste."
---

## Building expressions

PL: Budowanie wyrażeń (expressions)

Arithmetic on symbols, such as `3*x**2 + 2*x + 1`, builds an expression. For functions use SymPy's own, `sp.sin`, `sp.exp`, `sp.sqrt` and `sp.log`, which keep their argument symbolic.

PL: Działania na symbolach, np. `3*x**2 + 2*x + 1`, budują wyrażenie. Do funkcji używaj tych z SymPy, `sp.sin`, `sp.exp`, `sp.sqrt` i `sp.log`, które zostawiają argument w postaci symbolicznej.

```python
import sympy as sp
sp.init_printing()

x, a = sp.symbols("x a")
display(3*x**2 + 2*x + 1)
display(sp.exp(-a*x**2))
display(sp.sin(x) / sp.sqrt(x))
display(sp.log(x**2 + 1))
```

### Pitfall

`np.sin(x)` and `math.sin(x)` work on numbers only, so on a Symbol they raise `TypeError`; use `sp.sin(x)`.

PL: `np.sin(x)` i `math.sin(x)` działają tylko na liczbach, więc na symbolu (Symbol) zgłaszają `TypeError`; użyj `sp.sin(x)`.

```python raises=TypeError
import numpy as np
import sympy as sp
sp.init_printing()

x = sp.Symbol("x")
print(np.sin(x))
```

### See also

- array-maths/maths-functions
- evaluating/functions-for-numpy

## Expanding and factoring

PL: Rozwinięcie (expand) i rozkład na czynniki (factor)

`sp.expand(expr)` multiplies out every bracket and power, and `sp.factor(expr)` goes back, writing a polynomial as a product of factors.

PL: `sp.expand(expr)` wymnaża wszystkie nawiasy i potęgi, a `sp.factor(expr)` robi odwrotnie: zapisuje wielomian jako iloczyn czynników.

```python
import sympy as sp
sp.init_printing()

x = sp.Symbol("x")
display(sp.expand((x + 1)**3))
display(sp.factor(x**2 - 5*x + 6))
a, b = sp.symbols("a b")
display(sp.factor(a**2 - b**2))
```

## simplify

PL: Upraszczanie (simplify)

`sp.simplify(expr)` tries many rules and returns the simplest form it finds, such as `1` for `sin(x)**2 + cos(x)**2`. It can be slow on big expressions, and its result is hard to predict; when you know the form you want, `sp.expand` or `sp.factor` says exactly that.

PL: `sp.simplify(expr)` próbuje wielu reguł i zwraca najprostszą postać, jaką znajdzie, np. `1` dla `sin(x)**2 + cos(x)**2`. Na dużych wyrażeniach bywa wolne, a jego wynik trudno przewidzieć; gdy wiesz, jakiej postaci chcesz, `sp.expand` albo `sp.factor` mówi dokładnie to.

```python
import sympy as sp
sp.init_printing()

x = sp.Symbol("x")
e = sp.sin(x)**2 + sp.cos(x)**2
display(sp.simplify(e))
f = (x**2 - 1) / (x - 1)
display(f)
display(sp.simplify(f))
```

## Collecting terms

PL: Grupowanie wyrazów (collect)

`sp.collect(expr, x)` groups the terms by powers of `x`, so every power appears once with its coefficient. `sp.apart(expr)` splits a fraction of polynomials into partial fractions.

PL: `sp.collect(expr, x)` grupuje wyrazy według potęg `x`, więc każda potęga pojawia się raz ze swoim współczynnikiem. `sp.apart(expr)` rozkłada iloraz wielomianów na ułamki proste (partial fractions).

```python
import sympy as sp
sp.init_printing()

x, a, b = sp.symbols("x a b")
expr = a*x**2 + b*x + 2*x**2 + 3*x
display(sp.collect(expr, x))
display(sp.apart(1 / (x * (x + 1))))
```
