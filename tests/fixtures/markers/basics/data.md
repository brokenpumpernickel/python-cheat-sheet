---
title: Data
glyph: "csv"
summary: Loading data.
pl:
  title: Dane
  summary: Wczytywanie danych.
---

## Loading data

PL: Wczytywanie danych

The page shows a download; the build reads a file it writes first.

PL: Strona pokazuje pobieranie; build czyta plik, który najpierw zapisuje.

```python
open("scores.csv", "w").write("72,45,88\n")  #| hide
with open("scores.csv") as file:
    scores = [int(s) for s in file.read().split(",")]  #| show: scores = fetch("https://x.org/s.csv")
print(max(scores))
```

### Pitfall

A missing key raises `KeyError`.

PL: Brakujący klucz zgłasza `KeyError`.

```python raises=KeyError
counts = {"heads": 2}   #| show: counts = {"heads": 0}
print(counts["heads"])
counts["tails"] += 1
```

## Hidden import

PL: Ukryty import

A hidden first line leaves no blank line at the top.

PL: Ukryta pierwsza linia nie zostawia pustej linii na górze.

```python
import math  #| hide

print(round(math.pi, 2))  #| show: print(round(3.14159, 2))
```
