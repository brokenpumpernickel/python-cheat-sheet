---
title: Tuples
glyph: "( )"
summary: "Fixed, unchangeable groups of values: creating and unpacking, one-element tuples."
pl:
  title: Krotki
  summary: "Krotki (tuples): stałe, niezmienne grupy wartości — tworzenie i rozpakowywanie, krotki jednoelementowe."
---

## Unpacking

PL: Rozpakowywanie (unpacking)

A tuple is a fixed group of values in `()`. Unpacking assigns its items to separate names in one line: `x, y = point`.

PL: Krotka (tuple) to stała grupa wartości w `()`. Rozpakowywanie przypisuje jej elementy do osobnych nazw w jednej linii: `x, y = point`.

```python
point = (2.5, -1.0)
x, y = point
print(x, y)
```

### Pitfall

A tuple can't be changed after it is created, so `point[0] = 3` raises `TypeError`. Use a list if the items need to change.

PL: Krotki nie można zmienić po utworzeniu, więc `point[0] = 3` zgłasza `TypeError`. Jeśli elementy mają się zmieniać, użyj listy (list).

```python raises=TypeError
point = (2.5, -1.0)
point[0] = 3
```

### See also

- loops/looping-with-zip

## One-element tuples

PL: Jednoelementowe krotki (tuples)

A tuple with one item needs a comma after it: `(30,)`. The comma makes the tuple, not the brackets, which is why NumPy shows the shape of a one-dimensional array as `(3,)`.

PL: Krotka z jednym elementem potrzebuje przecinka po nim: `(30,)`. To przecinek tworzy krotkę, a nie nawiasy, dlatego NumPy pokazuje kształt jednowymiarowej tablicy jako `(3,)`.

```python
sizes = (30,)
print(sizes, len(sizes))
print(type(sizes))
```

### Pitfall

Without the comma the brackets only group, so `(30)` is the number `30`, and `len(sizes)` raises `TypeError`.

PL: Bez przecinka nawiasy tylko grupują, więc `(30)` to liczba `30`, a `len(sizes)` zgłasza `TypeError`.

```python raises=TypeError
sizes = (30)
print(sizes, type(sizes))
print(len(sizes))
```

### See also

- arrays/shape-and-dtype
