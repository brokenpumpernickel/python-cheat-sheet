---
title: collections
glyph: "Ctr"
summary: "Ready-made containers from the collections module: counting with Counter, most common values."
pl:
  title: collections
  summary: "Gotowe kontenery z modułu (module) collections: zliczanie z Counter, najczęstsze wartości."
---

## Counting with Counter

PL: Zliczanie z Counter

`Counter(data)` from the `collections` module counts how often each value appears and works like a dictionary of counts. Reading a value that never appears gives `0` instead of raising `KeyError`.

PL: `Counter(data)` z modułu (module) `collections` zlicza, ile razy pojawia się każda wartość, i działa jak słownik (dictionary) liczników. Odczyt wartości, która się nie pojawia, daje `0` zamiast zgłosić `KeyError`.

```python
from collections import Counter

rolls = [3, 6, 3, 1, 6, 6]
counts = Counter(rolls)
print(counts)
print(counts[6], counts[2])
```

### See also

- dictionaries/counting-occurrences
- dictionaries/grouping-with-defaultdict

## Most common values

PL: Najczęstsze wartości

`counts.most_common(n)` gives the `n` most frequent values with their counts, as `(value, count)` tuples, most frequent first. `counts.total()` adds up all the counts.

PL: `counts.most_common(n)` daje `n` najczęstszych wartości z ich licznikami jako krotki (tuples) `(value, count)`, od najczęstszej. `counts.total()` sumuje wszystkie liczniki.

```python
from collections import Counter

answers = ["yes", "no", "yes", "maybe", "yes", "no"]
counts = Counter(answers)
print(counts.most_common(2))
print(counts.total())
```
