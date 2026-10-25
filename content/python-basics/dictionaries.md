---
title: Dictionaries
glyph: "{k:v}"
summary: "Looking values up by key: access, updating, looping, counting."
pl:
  title: Słowniki
  summary: "Słowniki (dictionaries): wartości wyszukiwane po kluczu — odczyt, aktualizacja, pętle, zliczanie."
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

## Looping over items

PL: Pętla po elementach

`for key, value in d.items():` gives each key together with its value. `.keys()` and `.values()` give only the keys or only the values.

PL: `for key, value in d.items():` daje każdy klucz (key) razem z jego wartością (value). `.keys()` i `.values()` dają tylko klucze albo tylko wartości.

```python
sample = {"mean": 4.2, "sd": 1.1}
for key, value in sample.items():
    print(key, value)

print(list(sample.values()))
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
