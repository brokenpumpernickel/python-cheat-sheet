---
title: Sets
glyph: "{ }"
summary: "Unique values and set operations: union, intersection, difference."
pl:
  title: Zbiory
  summary: "Zbiory (sets): unikalne wartości i operacje na zbiorach — suma, iloczyn, różnica."
---

## Unique values

PL: Unikalne wartości

A set keeps each value only once and has no order. `set(data)` is a quick way to drop duplicates from a list.

PL: Zbiór (set) przechowuje każdą wartość tylko raz i nie ma kolejności. `set(data)` to szybki sposób na usunięcie duplikatów z listy (list).

```python
rolls = [3, 6, 3, 1, 6, 6]
print(set(rolls))
print(len(set(rolls)))
```

### Pitfall

`{}` is an empty **dictionary**, not an empty set. For an empty set, write `set()`.

PL: `{}` to pusty **słownik** (dictionary), a nie pusty zbiór. Pusty zbiór zapisz jako `set()`.

## Set operations

PL: Operacje na zbiorach

`A | B` is the union, `A & B` the intersection and `A - B` the difference of two sets, as with events in probability.

PL: `A | B` to suma (union), `A & B` iloczyn (intersection), a `A - B` różnica (difference) dwóch zbiorów (sets), tak jak w działaniach na zdarzeniach w rachunku prawdopodobieństwa.

```python
A = {1, 2, 3, 4}
B = {3, 4, 5}
print(A | B)
print(A & B)
print(A - B)
```
