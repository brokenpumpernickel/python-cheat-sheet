---
title: Strings
glyph: '"Aa"'
summary: "Text: f-strings, formatting numbers, cleaning and splitting."
pl:
  title: Napisy
  summary: "Napisy (strings): tekst — f-stringi, formatowanie liczb, czyszczenie i dzielenie."
---

## f-strings

PL: f-stringi

Put `f` before the quotes and write expressions in `{}`. After a colon you can format a number: `.3f` for 3 decimals, `.1%` for a percentage.

PL: Postaw `f` przed cudzysłowem napisu (string) i wpisz wyrażenia w `{}`. Po dwukropku sformatujesz liczbę: `.3f` to 3 miejsca po przecinku, `.1%` to procent.

```python
n = 120
p = 0.04567
rate = 0.8731
print(f"n = {n}, p = {p:.3f}")
print(f"rate = {rate:.1%}")
```

### Pitfall

Adding a number to a string with `+` raises `TypeError`. Use an f-string, or convert the number with `str()`.

PL: Dodanie liczby do napisu przez `+` zgłasza `TypeError`. Użyj f-stringa albo zamień liczbę na napis funkcją `str()`.

```python raises=TypeError
n = 120
print("n = " + n)
```

## Cleaning and splitting

PL: Czyszczenie i dzielenie

`.strip()` removes whitespace from both ends of a string, and `.split(sep)` breaks it into a list of pieces at each `sep`. The pieces are still strings.

PL: `.strip()` usuwa białe znaki z obu końców napisu (string), a `.split(sep)` dzieli go na listę (list) kawałków w każdym miejscu `sep`. Kawałki nadal są napisami.

```python
line = "  12,15,9 \n"
parts = line.strip().split(",")
print(parts)
print([int(p) for p in parts])
```

### See also

- lists/list-comprehensions
- loops/for-over-a-collection
