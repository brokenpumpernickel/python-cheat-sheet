---
title: Lists
glyph: "[ ]"
summary: "Ordered, changeable sequences: indexing, slicing, sorting."
pl:
  title: Listy
  summary: "Listy (lists): uporządkowane, modyfikowalne sekwencje — indeksowanie, wycinanie, sortowanie."
---

## Creating and indexing

PL: Tworzenie i indeksowanie

A list holds items in order inside `[]`. Indexing starts at 0, and negative indexes count from the end.

PL: Lista (list) przechowuje elementy po kolei w `[]`. Indeksy (indexes) zaczynają się od 0, a ujemne liczą od końca.

```python
data = [3, 1, 4, 1, 5]
print(data[0])
print(data[-1])
print(len(data))
```

## Slicing

PL: Wycinanie (slicing)

`data[start:stop]` takes a part of a list; `stop` is not included. Leave either one out to go to the start or end; add `:step` to skip items.

PL: `data[start:stop]` wybiera fragment listy (list); `stop` nie wchodzi do wyniku. Pomiń jedno z nich, aby sięgnąć do początku lub końca; dodaj `:step`, aby przeskakiwać elementy.

```python
data = [10, 20, 30, 40, 50]
print(data[1:3])
print(data[:2])
print(data[::2])
```

## Adding and removing

PL: Dodawanie i usuwanie

`.append()` adds one item at the end, `.extend()` adds several, and `.pop()` removes and returns an item (the last one by default).

PL: `.append()` dodaje jeden element na końcu listy (list), `.extend()` dodaje kilka, a `.pop()` usuwa i zwraca element (domyślnie ostatni).

```python
data = [1, 2]
data.append(3)
data.extend([4, 5])
last = data.pop()
print(data, last)
```

## Sorting

PL: Sortowanie

`sorted(x)` returns a new sorted list; `x.sort()` sorts the list in place and returns `None`.

PL: `sorted(x)` zwraca nową posortowaną listę (list); `x.sort()` sortuje listę w miejscu (in place) i zwraca `None`.

```python
data = [3, 1, 2]
print(sorted(data, reverse=True))
data.sort()
print(data)
```

### Pitfall

`data = data.sort()` replaces your list with `None`.

PL: `data = data.sort()` zastępuje twoją listę wartością `None`.

```python
data = [3, 1, 2]
data = data.sort()
print(data)
```

### See also

- functions/lambda

## List comprehensions

PL: Wyrażenia listowe (list comprehensions)

`[expression for item in collection]` builds a new list in one line. Add `if condition` at the end to keep only some items.

PL: `[expression for item in collection]` buduje nową listę (list) w jednej linii. Dodaj na końcu `if condition`, aby zostawić tylko niektóre elementy.

```python
data = [1, 2, 3, 4, 5, 6]
print([x ** 2 for x in data])
print([x for x in data if x % 2 == 0])
```

### See also

- loops/for-over-a-collection

## Summaries

PL: Podsumowania

`len`, `sum`, `min` and `max` work on any list of numbers. Together they give quick descriptive statistics.

PL: `len`, `sum`, `min` i `max` działają na każdej liście (list) liczb. Razem dają szybkie statystyki opisowe.

```python
data = [4, 8, 15, 16, 23, 42]
print(len(data), sum(data), min(data), max(data))
print(sum(data) / len(data))
```
