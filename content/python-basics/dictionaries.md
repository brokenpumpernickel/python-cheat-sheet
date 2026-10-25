---
title: Dictionaries
glyph: "{k:v}"
summary: "Looking values up by key: access, updating, keys and values, looping, counting, grouping."
pl:
  title: Słowniki
  summary: "Słowniki (dictionaries): wartości wyszukiwane po kluczu — odczyt, aktualizacja, klucze i wartości, pętle, zliczanie, grupowanie."
---

## Creating and accessing

PL: Tworzenie i odczyt

A dictionary maps keys to values inside `{}`. Look a value up with `d[key]`; `len(d)` counts the keys.

PL: Słownik (dictionary) przypisuje kluczom (keys) wartości (values) w `{}`. Wartość odczytasz przez `d[key]`; `len(d)` liczy klucze.

```python
sample = {"mean": 4.2, "sd": 1.1, "n": 30}
print(sample["mean"])
print(len(sample))
```

## Missing keys

PL: Brakujące klucze

`d[key]` raises `KeyError` if the key isn't there. `d.get(key, default)` returns `default` instead.

PL: `d[key]` zgłasza `KeyError`, jeśli takiego klucza (key) nie ma w słowniku (dictionary). `d.get(key, default)` zwraca wtedy `default`.

```python raises=KeyError
sample = {"mean": 4.2}
print(sample.get("sd", 0.0))
print(sample["sd"])
```

## Adding and updating

PL: Dodawanie i aktualizacja

`d[key] = value` adds the key if it's new and replaces its value if it already exists.

PL: `d[key] = value` dodaje klucz (key), jeśli jest nowy, a jeśli już istnieje, zastępuje jego wartość.

```python
sample = {"n": 30}
sample["mean"] = 4.2
sample["n"] = 31
print(sample)
```

## Keys and values

PL: Klucze i wartości

`d.keys()` gives the keys and `d.values()` the values, in the order they were added. Wrap one in `list()` to get a list, or pass it straight to a function such as `sum()`.

PL: `d.keys()` daje klucze (keys), a `d.values()` wartości (values), w kolejności dodawania. Obejmij je `list()`, żeby dostać listę (list), albo przekaż od razu do funkcji takiej jak `sum()`.

```python
counts = {"heads": 7, "tails": 3}
print(list(counts.keys()))
print(list(counts.values()))
print(sum(counts.values()))
```

### Pitfall

`in` checks the keys only, so `7 in counts` is `False`. To look for a value, write `7 in counts.values()`.

PL: `in` sprawdza tylko klucze, więc `7 in counts` daje `False`. Żeby szukać wśród wartości, napisz `7 in counts.values()`.

## Looping over items

PL: Pętla po elementach

`for key, value in d.items():` gives each key together with its value, as a pair you unpack into two names.

PL: `for key, value in d.items():` daje każdy klucz (key) razem z jego wartością (value) jako parę; rozpakowanie (unpacking) przypisuje ją dwóm nazwom.

```python
sample = {"mean": 4.2, "sd": 1.1}
for key, value in sample.items():
    print(key, value)
```

### See also

- loops/for-over-a-collection
- tuples/unpacking

## Counting occurrences

PL: Zliczanie wystąpień

`counts[x] = counts.get(x, 0) + 1` counts in a dictionary how often each value appears, starting from 0 the first time a value is seen.

PL: `counts[x] = counts.get(x, 0) + 1` zlicza w słowniku (dictionary), ile razy pojawia się każda wartość, zaczynając od 0, gdy wartość pojawia się pierwszy raz.

```python
rolls = [3, 6, 3, 1, 6, 6]
counts = {}
for roll in rolls:
    counts[roll] = counts.get(roll, 0) + 1

print(counts)
```

### See also

- dictionaries/missing-keys
- loops/for-over-a-collection
- collections/counting-with-counter

## Grouping with defaultdict

PL: Grupowanie z defaultdict

`defaultdict(list)` from the `collections` module is a dictionary that creates a missing key with an empty list the first time you use it, so `groups[key].append(x)` works without checking. `defaultdict(int)` starts missing counts at `0`.

PL: `defaultdict(list)` z modułu (module) `collections` to słownik (dictionary), który przy pierwszym użyciu brakującego klucza tworzy go z pustą listą (list), więc `groups[key].append(x)` działa bez sprawdzania. `defaultdict(int)` zaczyna brakujące liczniki od `0`.

```python
from collections import defaultdict

measurements = [("A", 4.1), ("B", 3.8), ("A", 4.5), ("B", 3.9)]
groups = defaultdict(list)
for group, value in measurements:
    groups[group].append(value)

print(dict(groups))
```

### Pitfall

Even reading a missing key adds it, so a typo such as `groups["C"]` quietly creates a new empty group instead of raising `KeyError`.

PL: Nawet odczyt brakującego klucza go dodaje, więc literówka taka jak `groups["C"]` po cichu tworzy nową pustą grupę zamiast zgłosić `KeyError`.

```python
from collections import defaultdict

groups = defaultdict(list)
print(groups["C"])
print(dict(groups))
```

### See also

- loops/for-over-a-collection
- tuples/unpacking
