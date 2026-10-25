---
title: Conditionals
glyph: "if"
summary: "Choosing what runs: if / elif / else and combining conditions."
pl:
  title: Warunki
  summary: "Instrukcje warunkowe (conditionals): wybór kodu do wykonania — if / elif / else i łączenie warunków."
---

## if / elif / else

PL: if / elif / else

Python checks each condition from the top and runs only the first block whose condition is true; `else` runs when none is. Indentation marks which lines belong to a block.

PL: Python sprawdza warunki od góry i wykonuje tylko pierwszy blok, którego warunek jest prawdziwy; `else` działa, gdy żaden nie jest. Wcięcie (indentation) wyznacza, które linie należą do bloku.

```python
p = 0.03
if p < 0.01:
    stars = "**"
elif p < 0.05:
    stars = "*"
else:
    stars = "ns"

print(stars)
```

## Combining conditions

PL: Łączenie warunków

Combine conditions with `and`, `or` and `not`. Comparisons can be chained: `0 <= x <= 1`.

PL: Warunki łączysz operatorami logicznymi (logical operators) `and`, `or` i `not`. Porównania (comparisons) można łączyć w łańcuch: `0 <= x <= 1`.

```python
x = 0.7
print(0 <= x <= 1)
print(x > 0.5 and x < 0.9)
print(not x > 0.5)
```

### Pitfall

`if x == 1 or 2:` is always true, because `2` on its own counts as true. Write `x == 1 or x == 2`, or `x in (1, 2)`.

PL: `if x == 1 or 2:` jest zawsze prawdziwe, bo samo `2` liczy się jako prawda. Napisz `x == 1 or x == 2` albo `x in (1, 2)`.
