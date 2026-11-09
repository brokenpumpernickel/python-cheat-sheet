---
title: Probability with SymPy
glyph: "E(X)"
summary: "Probability by hand and with sympy.stats: normalising a pdf, mean and variance, discrete distributions, moment generating functions and random variables."
pl:
  title: Prawdopodobieństwo w SymPy
  summary: "Prawdopodobieństwo ręcznie i z sympy.stats: normowanie gęstości (pdf), wartość oczekiwana i wariancja, rozkłady dyskretne, funkcje tworzące momenty (moment generating functions) i zmienne losowe (random variables)."
---

## Normalising a pdf

PL: Normowanie gęstości (pdf)

A pdf integrates to 1, so write it with an unknown constant `c`, integrate it over its whole range with `sp.integrate(f, (x, a, b))`, and solve `total - 1` for `c`. `sp.solve` returns a list of solutions, so `[0]` takes the only one; `sp.oo` is the end of a range to infinity.

PL: Gęstość (pdf) całkuje się do 1, więc zapisz ją z nieznaną stałą `c`, scałkuj po całym zakresie przez `sp.integrate(f, (x, a, b))` i rozwiąż `total - 1` względem `c`. `sp.solve` zwraca listę rozwiązań, więc `[0]` bierze jedyne z nich; `sp.oo` to koniec zakresu sięgającego nieskończoności.

```python
import sympy as sp
sp.init_printing()

x, c = sp.symbols("x c")
f = c * (1 - x**2)
total = sp.integrate(f, (x, -1, 1))
display(total)
c0 = sp.solve(total - 1, c)[0]
display(f.subs(c, c0))
g = c * x * sp.exp(-2*x)
total = sp.integrate(g, (x, 0, sp.oo))
display(sp.solve(total - 1, c))
```

### See also

- plotting-distributions/probability-as-an-area

## Mean and variance

PL: Wartość oczekiwana i wariancja

E[X] is the integral of `x*f`, and Var(X) = E[X²] − E[X]². Give parameters `positive=True`: with a plain `lam`, SymPy can't tell that the exponential pdf's integrals converge, and returns a `Piecewise` with the condition instead of `1/lam`.

PL: E[X], czyli wartość oczekiwana (expected value), to całka z `x*f`, a wariancja (variance) Var(X) = E[X²] − E[X]². Nadaj parametrom `positive=True`: przy zwykłym `lam` SymPy nie wie, że całki z gęstości (pdf) rozkładu wykładniczego są zbieżne, i zamiast `1/lam` zwraca `Piecewise` z warunkiem.

```python
import sympy as sp
sp.init_printing()

x = sp.Symbol("x")
lam = sp.Symbol("lambda", positive=True)
f = lam * sp.exp(-lam*x)
mean = sp.integrate(x*f, (x, 0, sp.oo))
ex2 = sp.integrate(x**2*f, (x, 0, sp.oo))
display(mean)
display(ex2)
display(ex2 - mean**2)
```

### See also

- symbols/assumptions
- distributions/mean-spread-and-intervals

## Discrete distributions

PL: Rozkłady dyskretne

For a pmf, `sp.Sum(k * pmf, (k, 0, sp.oo)).doit()` adds the series, here for a Poisson pmf with mean `mu`; make `k` `integer=True, nonnegative=True`. Check what `doit()` returns: the variance needs `sp.simplify`, and a geometric sum with a symbol `p` comes back as a `Piecewise`, so here `p` is a number.

PL: Dla funkcji prawdopodobieństwa (pmf) `sp.Sum(k * pmf, (k, 0, sp.oo)).doit()` sumuje szereg, tu dla rozkładu Poissona ze średnią `mu`; nadaj `k` założenia `integer=True, nonnegative=True`. Sprawdź, co zwraca `doit()`: wariancja (variance) potrzebuje `sp.simplify`, a suma geometryczna z symbolem `p` wraca jako `Piecewise`, więc tu `p` to liczba.

```python
import sympy as sp
sp.init_printing()

k = sp.Symbol("k", integer=True,
              nonnegative=True)
mu = sp.Symbol("mu", positive=True)
pmf = mu**k * sp.exp(-mu) / sp.factorial(k)
mean = sp.Sum(k*pmf, (k, 0, sp.oo)).doit()
ek2 = sp.Sum(k**2*pmf, (k, 0, sp.oo)).doit()
display(mean)
display(sp.simplify(ek2 - mean**2))
p = sp.Rational(1, 4)
geo = k * p * (1 - p)**k
display(sp.Sum(geo, (k, 0, sp.oo)).doit())
```

### See also

- discrete-distributions/poisson-distribution
- symbols/assumptions

## Moment generating functions

PL: Funkcje tworzące momenty

M(t) = E[e^(tX)] is the integral of `sp.exp(t*x) * f`; `conds="none"` drops its convergence condition, t < λ, and `sp.simplify` tidies the result, which otherwise gives `nan` at `t = 0`. The n-th moment is `M.diff(t, n).subs(t, 0)`, so the first two give the mean and variance of *Mean and variance*.

PL: Funkcja tworząca momenty (moment generating function) M(t) = E[e^(tX)] to całka z `sp.exp(t*x) * f`; `conds="none"` pomija warunek zbieżności tej całki, t < λ, a `sp.simplify` porządkuje wynik, który inaczej daje `nan` w `t = 0`. n-ty moment to `M.diff(t, n).subs(t, 0)`, więc dwa pierwsze dają wartość oczekiwaną i wariancję z hasła *Wartość oczekiwana i wariancja*.

```python
import sympy as sp
sp.init_printing()

x, t = sp.symbols("x t")
lam = sp.Symbol("lambda", positive=True)
f = lam * sp.exp(-lam*x)
g = sp.exp(t*x) * f
M = sp.integrate(g, (x, 0, sp.oo),
                 conds="none")
M = sp.simplify(M)
display(M)
m1 = M.diff(t).subs(t, 0)
m2 = M.diff(t, 2).subs(t, 0)
display(m1)
display(m2 - m1**2)
```

## Distributions in sympy.stats

PL: Rozkłady w sympy.stats

`X = Normal("X", mu, sigma)` makes a random variable, and `E(X)`, `variance(X)`, `density(X)(x)` and `P(X > mu)` give exact results. With numbers for the parameters, `P(Z > 1).evalf()` turns an exact probability into a decimal.

PL: `X = Normal("X", mu, sigma)` tworzy zmienną losową (random variable), a `E(X)`, `variance(X)`, `density(X)(x)` i `P(X > mu)` dają dokładne wyniki. Gdy parametry są liczbami, `P(Z > 1).evalf()` zamienia dokładne prawdopodobieństwo na liczbę dziesiętną.

```python
import sympy as sp
from sympy.stats import (Normal, E, P,
                         variance, density)
sp.init_printing()

x, mu = sp.symbols("x mu")
sigma = sp.Symbol("sigma", positive=True)
X = Normal("X", mu, sigma)
display(E(X))
display(variance(X))
display(density(X)(x))
display(P(X > mu))
Z = Normal("Z", 0, 1)
print(P(Z > 1).evalf())
```

### Pitfall

`E` and `P` need the random variable `X`, not a plain Symbol `x`: `E(x**2)` quietly returns `x**2`, and `P(x > 1)` raises `ValueError`.

PL: `E` i `P` potrzebują zmiennej losowej (random variable) `X`, a nie zwykłego symbolu (Symbol) `x`: `E(x**2)` po cichu zwraca `x**2`, a `P(x > 1)` zgłasza `ValueError`.

```python raises=ValueError
import sympy as sp
from sympy.stats import Normal, E, P
sp.init_printing()

x = sp.Symbol("x")
X = Normal("X", 0, 1)
display(E(x**2))
display(P(x > 1))
```

### See also

- distributions/a-distribution-object
- distributions/mean-spread-and-intervals

## Moment generating functions in sympy.stats

PL: Funkcje tworzące momenty w sympy.stats

`moment_generating_function(X)` returns M as a function of `t`; for `Exponential("Y", lam)` it matches the one integrated by hand. `moment(Y, n)` or `E(Y**n)` gives a moment directly.

PL: `moment_generating_function(X)` zwraca funkcję tworzącą momenty (moment generating function) M jako funkcję `t`; dla `Exponential("Y", lam)` zgadza się z tą scałkowaną ręcznie. `moment(Y, n)` albo `E(Y**n)` daje moment wprost.

```python
import sympy as sp
from sympy.stats import (
    Normal, Exponential, E, moment,
    moment_generating_function)
sp.init_printing()

t, mu = sp.symbols("t mu")
sigma = sp.Symbol("sigma", positive=True)
lam = sp.Symbol("lambda", positive=True)
X = Normal("X", mu, sigma)
display(moment_generating_function(X)(t))
Y = Exponential("Y", lam)
display(moment_generating_function(Y)(t))
display(moment(Y, 3))
display(E(Y**2))
```
