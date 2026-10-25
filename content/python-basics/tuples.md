---
title: Tuples
glyph: "( )"
summary: "Fixed, unchangeable groups of values: creating and unpacking."
pl:
  title: Krotki
  summary: "Krotki (tuples): stałe, niezmienne grupy wartości — tworzenie i rozpakowywanie."
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
