---
title: Lists
glyph: "[ ]"
summary: Ordered sequences.
pl:
  title: Listy
  summary: Uporządkowane sekwencje.
---

## Slicing

PL: Wycinanie (slicing)

`data[start:stop]` takes a *part* of a list.

PL: `data[start:stop]` wybiera *fragment* listy.

```python
data = [10, 20, 30, 40]
print(data[1:3])
print(data[::2])
```

## Sorting

PL: Sortowanie

`sorted(x)` returns a new list.

PL: `sorted(x)` zwraca nową listę.

```python
print(sorted([3, 1, 2]))
```

### Pitfall

`data = data.sort()` replaces your list with `None`.

PL: `data = data.sort()` zastępuje listę wartością `None`.

```python
data = [3, 1, 2]
data = data.sort()
print(data)
```

### See also

- lists/slicing
- lists/missing-items

## Missing items

PL: Brakujące elementy

Indexing past the end raises an error.

PL: Indeks poza końcem listy zgłasza błąd.

```python raises=IndexError
data = [1, 2]
print(data[0])
print(data[5])
```
