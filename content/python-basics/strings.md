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

## Number formats

PL: Formaty liczb

`format(x, spec)` formats a number the way `f"{x:spec}"` does. In the table, `.2f` gives 2 decimals, `.3g` 3 significant digits, `10` a width of 10 (`010` pads with zeros), `,` a thousands separator, `%` a percentage and `e` scientific notation.

PL: `format(x, spec)` formatuje liczbę tak samo jak `f"{x:spec}"`. W tabeli `.2f` daje 2 miejsca po przecinku, `.3g` 3 cyfry znaczące, `10` szerokość 10 znaków (`010` dopełnia zerami), `,` separator tysięcy, `%` procent, a `e` notację wykładniczą (scientific notation).

```python
n = 1234.5678
p = 0.04567
for spec in [".2f", ".3g", "10.2f", "010.2f", ",.2f", ".1%", ".2e"]:
    print(f"{spec:8}{format(n, spec):14}{format(p, spec)}")
```

### See also

- loops/for-over-a-collection

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
