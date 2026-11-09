---
title: Differential equations
glyph: "y''"
summary: "Ordinary differential equations in SymPy: unknown functions and their derivatives, dsolve, initial conditions and using the solution."
pl:
  title: Równania różniczkowe
  summary: "Równania różniczkowe zwyczajne (ordinary differential equations) w SymPy: funkcje niewiadome i ich pochodne, dsolve, warunki początkowe i korzystanie z rozwiązania."
---

## Functions and their derivatives

PL: Funkcje i ich pochodne (derivatives)

`x = sp.Function("x")` makes an unknown function, and `x(t)` is that function of the symbol `t`. `x(t).diff(t)` is its derivative and `x(t).diff(t, t)` its second derivative, left unevaluated because `x` is unknown.

PL: `x = sp.Function("x")` tworzy funkcję niewiadomą (Function), a `x(t)` to ta funkcja symbolu `t`. `x(t).diff(t)` to jej pochodna, a `x(t).diff(t, t)` druga pochodna; obie zostają niewyliczone, bo funkcja `x` jest nieznana.

```python
import sympy as sp
sp.init_printing()

t = sp.Symbol("t")
x = sp.Function("x")
display(x(t))
display(x(t).diff(t))
display(x(t).diff(t, t))
```

### See also

- derivatives/derivatives

## Solving an ODE

PL: Rozwiązywanie równania różniczkowego (ODE)

`sp.dsolve(ode, x(t))` solves a differential equation written with `sp.Eq` for the function `x(t)`; the general solution has constants `C1`, `C2`. Here it is the harmonic oscillator, with `omega` declared `positive=True` so the answer comes in sines and cosines rather than complex exponentials.

PL: `sp.dsolve(ode, x(t))` rozwiązuje równanie różniczkowe zapisane przez `sp.Eq` względem funkcji `x(t)`; rozwiązanie ogólne ma stałe `C1`, `C2`. Tutaj to oscylator harmoniczny, a `omega` ma `positive=True`, więc wynik wychodzi w sinusach i cosinusach zamiast w zespolonych funkcjach wykładniczych.

```python
import sympy as sp
sp.init_printing()

t = sp.Symbol("t")
w = sp.Symbol("omega", positive=True)
x = sp.Function("x")
ode = sp.Eq(x(t).diff(t, t), -w**2 * x(t))
display(ode)
display(sp.dsolve(ode, x(t)))
```

### See also

- symbols/assumptions
- equations/equations-with-eq

## Initial conditions

PL: Warunki początkowe (initial conditions)

`ics={x(0): x0, ...}` passes initial conditions to `sp.dsolve`, which then finds `C1` and `C2`. The starting velocity x′(0) is written `x(t).diff(t).subs(t, 0)`: take the derivative first, then put in `t = 0`.

PL: `ics={x(0): x0, ...}` przekazuje do `sp.dsolve` warunki początkowe, z których wyznacza on `C1` i `C2`. Prędkość początkową x′(0) zapisuje się jako `x(t).diff(t).subs(t, 0)`: najpierw pochodna, potem podstawienie `t = 0`.

```python
import sympy as sp
sp.init_printing()

t = sp.Symbol("t")
w = sp.Symbol("omega", positive=True)
x0, v0 = sp.symbols("x_0 v_0")
x = sp.Function("x")
ode = sp.Eq(x(t).diff(t, t), -w**2 * x(t))
ics = {x(0): x0,
       x(t).diff(t).subs(t, 0): v0}
display(sp.dsolve(ode, x(t), ics=ics))
```

## Using the solution

PL: Korzystanie z rozwiązania

`sp.dsolve` returns an equation `x(t) = ...`, and `res.rhs` is its right-hand side, the formula itself. Put numbers in with `.subs(w, sp.pi)` and turn the formula into a NumPy function with `sp.lambdify(t, ...)`.

PL: `sp.dsolve` zwraca równanie `x(t) = ...`, a `res.rhs` to jego prawa strona (right-hand side), czyli sam wzór. Liczby wstawisz przez `.subs(w, sp.pi)`, a wzór zamienisz w funkcję NumPy przez `sp.lambdify(t, ...)`.

```python
import numpy as np
import sympy as sp
sp.init_printing()

t = sp.Symbol("t")
w = sp.Symbol("omega", positive=True)
x = sp.Function("x")
ode = sp.Eq(x(t).diff(t, t), -w**2 * x(t))
ics = {x(0): 2, x(t).diff(t).subs(t, 0): 0}
res = sp.dsolve(ode, x(t), ics=ics)
display(res)
display(res.rhs)
f = sp.lambdify(t, res.rhs.subs(w, sp.pi))
print(f(np.array([0, 1, 2])))
```

### See also

- evaluating/substituting-values
- evaluating/functions-for-numpy
- sympy-plots/plotting-with-lambdify
