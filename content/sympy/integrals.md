---
title: Integrals and sums
glyph: "∫"
summary: "Integrals and sums in SymPy: indefinite and definite integrals, integrals to infinity, unevaluated integrals and finite and infinite sums."
pl:
  title: Całki i sumy
  summary: "Całki (integrals) i sumy w SymPy: całki nieoznaczone i oznaczone, całki do nieskończoności, całki nieobliczone oraz sumy skończone i nieskończone."
---

## Indefinite integrals

PL: Całki nieoznaczone (indefinite integrals)

`sp.integrate(expr, x)` gives an antiderivative of `expr`, with no constant of integration added. A result may hold a special function: `erf` is the error function, from which the normal distribution's CDF is built.

PL: `sp.integrate(expr, x)` daje funkcję pierwotną (antiderivative) `expr` bez dodanej stałej całkowania. Wynik może zawierać funkcję specjalną: `erf` to funkcja błędu (error function), z której zbudowana jest dystrybuanta rozkładu normalnego.

```python
import sympy as sp
sp.init_printing()

x = sp.Symbol("x")
display(sp.integrate(x**2 + sp.cos(x), x))
display(sp.integrate(sp.exp(-x**2), x))
```

### See also

- derivatives/derivatives

## Definite integrals

PL: Całki oznaczone (definite integrals)

`sp.integrate(expr, (x, -1, 1))` integrates `expr` from `-1` to `1` and gives an exact number. When that number holds a function such as `erf`, `.evalf()` turns it into a decimal.

PL: `sp.integrate(expr, (x, -1, 1))` całkuje `expr` od `-1` do `1` i daje dokładną liczbę. Gdy ta liczba zawiera funkcję taką jak `erf`, `.evalf()` zamienia ją na liczbę dziesiętną.

```python
import sympy as sp
sp.init_printing()

x = sp.Symbol("x")
display(sp.integrate(x**2, (x, -1, 1)))
f = sp.exp(-x**2)
area = sp.integrate(f, (x, -1, 1))
display(area)
print(area.evalf())
```

### See also

- symbols/decimals-to-many-digits
- evaluating/decimal-values

## Integrals to infinity

PL: Całki do nieskończoności

Use `-sp.oo` and `sp.oo` as limits for an improper integral. With `a` declared positive, the integral of `sp.exp(-a*x**2)` over the whole line is `sqrt(pi)/sqrt(a)`. The integral of `1/x**2` from `1` converges, while that of `1/x` diverges and gives `oo`.

PL: Jako granice całki niewłaściwej (improper integral) użyj `-sp.oo` i `sp.oo`. Gdy `a` jest zadeklarowane jako dodatnie, całka z `sp.exp(-a*x**2)` po całej prostej daje `sqrt(pi)/sqrt(a)`. Całka z `1/x**2` od `1` jest zbieżna, a całka z `1/x` jest rozbieżna i daje `oo`.

```python
import sympy as sp
sp.init_printing()

x = sp.Symbol("x")
a = sp.Symbol("a", positive=True)
f = sp.exp(-a*x**2)
display(sp.integrate(f, (x, -sp.oo, sp.oo)))
display(sp.integrate(1/x**2, (x, 1, sp.oo)))
display(sp.integrate(1/x, (x, 1, sp.oo)))
```

### Pitfall

Without `positive=True` on `a`, SymPy can't tell whether the integral converges, so it returns a `Piecewise`: the answer under a condition on `a`, and the integral left undone otherwise.

PL: Bez `positive=True` przy `a` SymPy nie wie, czy całka jest zbieżna, więc zwraca `Piecewise`: wynik z warunkiem na `a`, a w pozostałych przypadkach nieobliczoną całkę.

```python
import sympy as sp
sp.init_printing()

x, a = sp.symbols("x a")
f = sp.exp(-a*x**2)
r = sp.integrate(f, (x, -sp.oo, sp.oo))
display(r)
```

### See also

- symbols/assumptions
- symbols/constants
- probability/mean-and-variance

## Unevaluated integrals

PL: Całki nieobliczone (Integral)

`sp.Integral(expr, (x, 0, sp.oo))` keeps the integral as it is, so it shows the question; `.doit()` computes it. `sp.Eq(q, q.doit())` shows the question beside its answer.

PL: `sp.Integral(expr, (x, 0, sp.oo))` zostawia całkę (integral) bez obliczania, więc pokazuje samo pytanie; `.doit()` ją oblicza. `sp.Eq(q, q.doit())` pokazuje pytanie obok odpowiedzi.

```python
import sympy as sp
sp.init_printing()

x = sp.Symbol("x")
q = sp.Integral(x * sp.exp(-x),
                (x, 0, sp.oo))
display(q)
display(q.doit())
display(sp.Eq(q, q.doit()))
```

### See also

- equations/equations-with-eq

## Sums

PL: Sumy (Sum)

`sp.Sum(k**2, (k, 1, n))` is the sum for `k` from `1` to `n`, and `.doit()` finds its closed form; `sp.summation(...)` does both in one step. The infinite geometric series of `p**k` adds up to `1/(1 - p)` only when `abs(p) < 1`, so SymPy returns that condition with it.

PL: `sp.Sum(k**2, (k, 1, n))` to suma po `k` od `1` do `n`, a `.doit()` znajduje jej postać zwartą; `sp.summation(...)` robi oba kroki naraz. Nieskończony szereg geometryczny (geometric series) z `p**k` sumuje się do `1/(1 - p)` tylko wtedy, gdy `abs(p) < 1`, więc SymPy zwraca wynik razem z tym warunkiem.

```python
import sympy as sp
sp.init_printing()

k, n, p = sp.symbols("k n p")
s = sp.Sum(k**2, (k, 1, n))
display(s)
display(s.doit())
display(sp.Sum(p**k, (k, 0, sp.oo)).doit())
display(sp.summation(1/k**2, (k, 1, sp.oo)))
```

### See also

- symbols/constants
- probability/discrete-distributions
