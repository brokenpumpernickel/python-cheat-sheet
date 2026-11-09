---
title: Equations
glyph: "Eq"
summary: "Equations in SymPy: Eq and solve, solving an expression equal to 0, systems of equations, solving a formula for one symbol and numeric solutions."
pl:
  title: Równania
  summary: "Równania (equations) w SymPy: Eq i solve, rozwiązywanie wyrażenia równego 0, układy równań, wyznaczanie jednego symbolu ze wzoru i rozwiązania numeryczne."
---

## Equations with Eq

PL: Równania (equations) z Eq

`sp.Eq(left, right)` builds an equation, and `sp.solve(eq, x)` returns a list of its solutions for `x`. For `a*x**2 + b*x + c = 0` the two solutions are the quadratic formula's roots.

PL: `sp.Eq(left, right)` tworzy równanie, a `sp.solve(eq, x)` zwraca listę jego rozwiązań względem `x`. Dla `a*x**2 + b*x + c = 0` dwa rozwiązania to pierwiastki ze wzoru na równanie kwadratowe.

```python
import sympy as sp
sp.init_printing()

x, a, b, c = sp.symbols("x a b c")
eq = sp.Eq(a*x**2 + b*x + c, 0)
display(eq)
display(sp.solve(eq, x))
```

### Pitfall

`a*x**2 + b*x + c == 0` is `False`, not an equation, because `==` checks whether the two expressions are the same. Write `sp.Eq(a*x**2 + b*x + c, 0)`.

PL: `a*x**2 + b*x + c == 0` daje `False`, a nie równanie, bo `==` sprawdza, czy dwa wyrażenia są takie same. Napisz `sp.Eq(a*x**2 + b*x + c, 0)`.

```python
import sympy as sp
sp.init_printing()

x, a, b, c = sp.symbols("x a b c")
print(a*x**2 + b*x + c == 0)
```

### See also

- symbols/symbols

## Solving expr = 0

PL: Rozwiązywanie expr = 0

`sp.solve(expr, x)` with a bare expression, not an `Eq`, solves `expr = 0`. The roots stay exact, such as `sqrt(2)`, and complex roots like `I` are included unless `x` is declared `real=True`.

PL: `sp.solve(expr, x)` z samym wyrażeniem, a nie z `Eq`, rozwiązuje `expr = 0`. Pierwiastki zostają dokładne, np. `sqrt(2)`, a pierwiastki zespolone, takie jak `I`, są na liście, chyba że zadeklarujesz `x` z `real=True`.

```python
import sympy as sp
sp.init_printing()

x = sp.Symbol("x")
display(sp.solve(x**2 - 5*x + 6, x))
display(sp.solve(x**2 - 2, x))
display(sp.solve(x**2 + 1, x))
```

### See also

- symbols/assumptions

## Systems of equations

PL: Układy równań (systems of equations)

`sp.solve([eq1, eq2], [x, y])` solves a system of equations, each one an `Eq` or an expression equal to 0, and returns a dict from each symbol to its value. Read one value with `sol[x]`.

PL: `sp.solve([eq1, eq2], [x, y])` rozwiązuje układ równań, w którym każde równanie to `Eq` albo wyrażenie równe 0, i zwraca słownik (dict) z wartością dla każdego symbolu. Jedną wartość odczytasz przez `sol[x]`.

```python
import sympy as sp
sp.init_printing()

x, y = sp.symbols("x y")
sol = sp.solve([2*x + y, 3*x + 4*y + 1],
               [x, y])
display(sol)
display(sol[x])
```

## Solving for one symbol

PL: Wyznaczanie jednego symbolu

`sp.solve(eq, x)` solves a formula for whichever symbol you name, treating the others as known. Solving `z = (x - mu)/sigma` for `x` gives the value at `z` standard deviations from the mean, the way a normal quantile is found.

PL: `sp.solve(eq, x)` wyznacza ze wzoru ten symbol, który podasz, a pozostałe traktuje jako znane. Wyznaczenie `x` z `z = (x - mu)/sigma` daje wartość odległą o `z` odchyleń standardowych od średniej, tak jak wyznacza się kwantyl rozkładu normalnego.

```python
import sympy as sp
sp.init_printing()

x, z, mu = sp.symbols("x z mu")
sigma = sp.Symbol("sigma", positive=True)
eq = sp.Eq(z, (x - mu) / sigma)
sol = sp.solve(eq, x)
display(sol)
print(sol[0].subs({z: 2, mu: 100,
                   sigma: 15}))
```

### See also

- symbols/assumptions

## Numeric solutions

PL: Rozwiązania numeryczne

`sp.nsolve(expr, x, 1)` finds a decimal root of `expr = 0` near the starting guess `1`. Use it when no formula exists: `sp.solve(sp.cos(x) - x, x)` raises `NotImplementedError`.

PL: `sp.nsolve(expr, x, 1)` znajduje przybliżony, dziesiętny pierwiastek `expr = 0` blisko punktu startowego `1`. Użyj go, gdy rozwiązanie nie ma wzoru: `sp.solve(sp.cos(x) - x, x)` zgłasza `NotImplementedError`.

```python
import sympy as sp
sp.init_printing()

x = sp.Symbol("x")
r = sp.nsolve(sp.cos(x) - x, x, 1)
print(r)
print(sp.cos(r) - r)
```

### See also

- symbols/decimals-to-many-digits
