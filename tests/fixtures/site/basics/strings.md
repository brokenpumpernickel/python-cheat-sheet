---
title: Strings
glyph: '"Aa"'
summary: Text.
pl:
  title: Napisy
  summary: Tekst.
---

## Joining

PL: Łączenie

`+` joins two strings.

PL: `+` łączy dwa napisy.

```python
print("ab" + "cd")
```

### Pitfall

`+` adds no space between the strings.

PL: `+` nie dodaje spacji między napisami.

### See also

- numbers/addition

## Mixing types

PL: Mieszanie typów

A string and a number don't join with `+`; convert the number with `str()` first.

PL: Napis i liczba nie łączą się przez `+`; najpierw zamień liczbę przez `str()`.

```python raises=TypeError
print("total: " + str(3))
print("total: " + 3)
```

## Repeating

PL: Powtarzanie

`"ha" * n` repeats a string `n` times.

PL: `"ha" * n` powtarza napis `n` razy.

```python
import random

rng = random.Random(4)  #| show: rng = random.Random()
print("ha" * rng.randint(2, 4))
```
