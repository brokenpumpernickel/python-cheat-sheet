---
title: Algebra
glyph: "x²"
summary: Expressions shown as maths.
pl:
  title: Algebra
  summary: Wyrażenia pokazane jako wzory.
---

## Printed and displayed

PL: Wypisane i wyświetlone

`display(expr)` shows an expression as maths, in order with what `print` shows.

PL: `display(expr)` pokazuje wyrażenie jako wzór, w kolejności z tym, co pokazuje `print`.

```python
import sympy as sp
sp.init_printing()

x = sp.symbols("x")
print("expand")
display(sp.expand((x + 1)**2))
print("factor")
display(sp.factor(x**2 - 4))
```

## Collections

PL: Kolekcje

After `sp.init_printing()`, lists, dicts and tuples are maths too.

PL: Po `sp.init_printing()` listy, słowniki i krotki też są wzorami.

```python
import sympy as sp
sp.init_printing()

x = sp.symbols("x")
display(sp.solve(x**2 - 4, x))
display({x: 1})
display((x, 2))
```

## Plain display

PL: Zwykłe wyświetlanie

Without `sp.init_printing()`, `display(3)` shows text, as `print` does.

PL: Bez `sp.init_printing()` `display(3)` pokazuje tekst, tak jak `print`.

```python
print(1)
display(3)
print(2)
```

## Wide formula

PL: Szeroki wzór

A formula wider than the card scrolls inside its Output.

PL: Wzór szerszy niż karta przewija się w swoim Wyniku.

```python
import sympy as sp
sp.init_printing()

x = sp.symbols("x")
display(sp.expand((x + 1)**24))
```

### Pitfall

The error line still ends the Output, after the maths.

PL: Wiersz błędu nadal kończy Wynik, po wzorze.

```python raises=TypeError
import sympy as sp
sp.init_printing()

x = sp.symbols("x")
display(x / 2)
print("x" + 1)
```
