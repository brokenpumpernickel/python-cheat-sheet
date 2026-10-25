---
title: Tuples
glyph: "( )"
summary: "Fixed, unchangeable groups of values: unpacking and zip."
pl:
  title: Krotki
  summary: "Krotki (tuples): stałe, niezmienne grupy wartości — rozpakowywanie i zip."
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

## zip

PL: zip

`zip(xs, ys)` pairs up items from several lists by position, giving one tuple per position. It stops at the end of the shortest list.

PL: `zip(xs, ys)` łączy w pary elementy kilku list (lists) według pozycji i daje jedną krotkę (tuple) na każdą pozycję. Kończy się wraz z najkrótszą listą.

```python
xs = [1, 2, 3]
ys = [2.1, 3.9, 6.2]
print(list(zip(xs, ys)))
for x, y in zip(xs, ys):
    print(x, y)
```

### See also

- loops/for-over-a-collection
