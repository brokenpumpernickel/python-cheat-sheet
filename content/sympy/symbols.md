---
title: Symbols and numbers
glyph: "Sym"
summary: "Symbols and exact numbers in SymPy: making symbols, assumptions, exact fractions, decimals to many digits and constants."
pl:
  title: Symbole i liczby
  summary: "Symbole (symbols) i liczby dokładne w SymPy: tworzenie symboli, założenia, dokładne ułamki, liczby dziesiętne z wieloma cyframi i stałe."
---

## Symbols

PL: Symbole (symbols)

`sp.Symbol("x")` makes one symbol and `sp.symbols("a b c")` several at once; arithmetic on them builds expressions. The Python variable and the symbol's name are separate: `w = sp.Symbol("omega")` is used as `w` but shows as ω, and a name like `"x_1"` shows as x₁.

PL: `sp.Symbol("x")` tworzy jeden symbol, a `sp.symbols("a b c")` kilka naraz; działania na nich budują wyrażenia (expressions). Zmienna Pythona i nazwa symbolu to dwie różne rzeczy: `w = sp.Symbol("omega")` używasz jako `w`, ale wyświetla się jako ω, a nazwa taka jak `"x_1"` wyświetla się jako x₁.

```python
import sympy as sp
sp.init_printing()

x = sp.Symbol("x")
a, b, c = sp.symbols("a b c")
display(a*x**2 + b*x + c)
w = sp.Symbol("omega")
x1 = sp.Symbol("x_1")
display(w * x1)
print(w * x1)
```

### See also

- variables/assigning-values

## Assumptions

PL: Założenia (assumptions)

Keyword arguments such as `integer=True` or `positive=True` tell SymPy what a symbol stands for, so it can simplify more. With `n` an integer, `sp.sin(sp.pi * n)` is `0`; with `a` positive, `sp.sqrt(a**2)` is `a`, while for any `a` it stays a square root.

PL: Argumenty nazwane, takie jak `integer=True` czy `positive=True`, mówią SymPy, co oznacza symbol, więc może uprościć więcej. Gdy `n` jest liczbą całkowitą, `sp.sin(sp.pi * n)` daje `0`; gdy `a` jest dodatnie, `sp.sqrt(a**2)` daje `a`, a dla dowolnego `a` zostaje pierwiastek.

```python
import sympy as sp
sp.init_printing()

n = sp.Symbol("n")
n_int = sp.Symbol("n", integer=True)
display(sp.sin(sp.pi * n))
display(sp.sin(sp.pi * n_int))
a = sp.Symbol("a")
a_pos = sp.Symbol("a", positive=True)
display(sp.sqrt(a**2))
display(sp.sqrt(a_pos**2))
```

### See also

- integrals/integrals-to-infinity
- differential-equations/solving-an-ode

## Exact numbers

PL: Liczby dokładne

`sp.Rational(10, 3)` is the exact fraction 10/3, and arithmetic on it stays exact, where Python's `10 / 3` is a rounded float. `sp.Integer(358)**987` keeps every one of its 2521 digits.

PL: `sp.Rational(10, 3)` to dokładny ułamek 10/3, czyli liczba wymierna (Rational), a działania na nim zostają dokładne, podczas gdy `10 / 3` w Pythonie to zaokrąglona liczba zmiennoprzecinkowa (float). `sp.Integer(358)**987` zachowuje wszystkie swoje 2521 cyfr.

```python
import sympy as sp
sp.init_printing()

print(10 / 3)
r = sp.Rational(10, 3)
display(r)
display(r + sp.Rational(1, 6))
big = sp.Integer(358)**987
print(len(str(big)))
```

### Pitfall

`1/3 * x` gives `0.333333333333333 x`, because Python divides `1/3` into a float before SymPy sees it. Write `x / 3` or `sp.Rational(1, 3) * x`.

PL: `1/3 * x` daje `0.333333333333333 x`, bo Python dzieli `1/3` na liczbę zmiennoprzecinkową (float), zanim SymPy to zobaczy. Napisz `x / 3` albo `sp.Rational(1, 3) * x`.

```python
import sympy as sp
sp.init_printing()

x = sp.Symbol("x")
display(1/3 * x)
```

## Decimals to many digits

PL: Liczby dziesiętne z wieloma cyframi

`r.evalf(30)` or `sp.N(r, 30)` turns an exact number into a decimal with 30 significant digits, and `sp.pi.evalf(40)` gives π to 40. For a decimal you type, `sp.Float("0.3", 30)` reads it from text, so every digit is exact.

PL: `r.evalf(30)` albo `sp.N(r, 30)` zamienia liczbę dokładną na dziesiętną z 30 cyframi znaczącymi, a `sp.pi.evalf(40)` daje π z 40 cyframi. Liczbę dziesiętną, którą wpisujesz, `sp.Float("0.3", 30)` odczytuje z tekstu jako liczbę zmiennoprzecinkową (Float), więc każda cyfra jest dokładna.

```python
import sympy as sp
sp.init_printing()

r = sp.Rational(10, 3)
print(r.evalf(30))
print(sp.N(r, 30))
print(sp.pi.evalf(40))
print(sp.Float("0.3", 30))
```

### Pitfall

`sp.Float(0.3, 30)` starts from the Python float `0.3`, which is already a little off in binary, so the extra digits show its error.

PL: `sp.Float(0.3, 30)` zaczyna od liczby zmiennoprzecinkowej (float) Pythona `0.3`, która w zapisie binarnym już jest trochę niedokładna, więc dodatkowe cyfry pokazują ten błąd.

```python
import sympy as sp
sp.init_printing()

print(sp.Float(0.3, 30))
```

### See also

- evaluating/decimal-values

## Constants

PL: Stałe

`sp.pi`, `sp.E`, `sp.I` (the imaginary unit) and `sp.oo` (infinity) are exact, so `sp.exp(sp.I * sp.pi)` gives exactly `-1`. The `math.pi` of Python is a float: `sp.sin(math.pi)` gives a tiny number, not `0`.

PL: `sp.pi`, `sp.E`, `sp.I` (jednostka urojona) i `sp.oo` (nieskończoność) są dokładne, więc `sp.exp(sp.I * sp.pi)` daje dokładnie `-1`. `math.pi` z Pythona to liczba zmiennoprzecinkowa (float): `sp.sin(math.pi)` daje bardzo małą liczbę, a nie `0`.

```python
import sympy as sp
sp.init_printing()

display(sp.exp(sp.I * sp.pi))
display(sp.cos(sp.pi / 6))
display(sp.sqrt(-4))
display(sp.log(sp.E**3))
display(sp.oo + 1)
```
