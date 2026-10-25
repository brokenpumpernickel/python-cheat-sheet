---
title: Indexing
glyph: "a[i]"
summary: "Picking values out of arrays: indexes and slices, rows and columns, boolean masks."
pl:
  title: Indeksowanie
  summary: "Indeksowanie (indexing) tablic: indeksy i wycinki, wiersze i kolumny, maski logiczne."
---

## Indexing and slicing

PL: Indeksowanie i wycinanie

`a[i]` and `a[start:stop:step]` work as on lists: indexes start at 0, negative ones count from the end, and `stop` is not included.

PL: `a[i]` i `a[start:stop:step]` działają jak na listach: indeksy (indexes) zaczynają się od 0, ujemne liczą od końca, a `stop` nie wchodzi do wyniku.

```python
import numpy as np

a = np.array([10, 20, 30, 40, 50])
print(a[0], a[-1])
print(a[1:4])
print(a[::2])
```

### Pitfall

A slice shares its values with the original array (it is a view), so changing the slice changes the original too. Take `a[:2].copy()` when you need a separate array.

PL: Wycinek (slice) dzieli wartości z oryginalną tablicą (jest widokiem, view), więc zmiana wycinka zmienia też oryginał. Użyj `a[:2].copy()`, gdy potrzebujesz osobnej tablicy.

```python
import numpy as np

a = np.array([10, 20, 30, 40, 50])
first = a[:2]
first[0] = 99
print(a)
```

### See also

- lists/slicing

## Rows and columns

PL: Wiersze i kolumny

`m[i, j]` is the value in row `i`, column `j`; `m[i]` is a whole row and `m[:, j]` a whole column, which comes out as a one-dimensional array. Slices work in both places, so `m[:2, 1:]` is a block.

PL: `m[i, j]` to wartość w wierszu `i` i kolumnie `j`; `m[i]` to cały wiersz, a `m[:, j]` cała kolumna, która wychodzi jako tablica (array) jednowymiarowa. Wycinki (slices) działają na obu miejscach, więc `m[:2, 1:]` to blok.

```python
import numpy as np

m = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])
print(m[1, 2])
print(m[0])
print(m[:, 1])
print(m[:2, 1:])
```

### See also

- arrays/two-dimensional-arrays
- heatmaps/values-in-the-cells

## Boolean masks

PL: Maski logiczne

A comparison such as `scores >= 4` gives a mask, an array of `True` and `False` with one value per score, and `scores[mask]` keeps the values where it is `True`. Combine conditions with `&` (and), `|` (or) and `~` (not), each condition in parentheses.

PL: Porównanie, np. `scores >= 4`, daje maskę logiczną (boolean mask), czyli tablicę `True` i `False` z jedną wartością na wynik, a `scores[mask]` zostawia wartości tam, gdzie jest `True`. Warunki łącz przez `&` (i), `|` (lub) i `~` (nie), każdy warunek w nawiasach.

```python
import numpy as np

scores = np.array([2, 5, 3, 4, 5, 1])
mask = scores >= 4
print(mask)
print(scores[mask])
print(scores[(scores > 1) & (scores < 5)])
```

### Pitfall

`and`, `or` and `not` need a single `True` or `False`, so between two masks they raise a `ValueError` about an ambiguous truth value. Use `&`, `|` and `~` instead.

PL: `and`, `or` i `not` potrzebują jednej wartości `True` lub `False`, więc między dwiema maskami zgłaszają `ValueError` o niejednoznacznej wartości logicznej. Użyj zamiast nich `&`, `|` i `~`.

```python raises=ValueError
import numpy as np

scores = np.array([2, 5, 3, 4, 5, 1])
mask = (scores > 1) and (scores < 5)
```

### See also

- array-maths/comparisons
- conditionals/combining-conditions

## Changing values through a mask

PL: Zmiana wartości przez maskę

`a[mask] = value` replaces only the values where the mask is `True`, in place. `np.where(mask, x, y)` instead returns a new array with `x` where the mask is `True` and `y` everywhere else.

PL: `a[mask] = value` zastępuje tylko wartości, gdzie maska logiczna (boolean mask) ma `True`, w miejscu (in place). `np.where(mask, x, y)` zwraca za to nową tablicę z `x` tam, gdzie maska ma `True`, i `y` wszędzie indziej.

```python
import numpy as np

scores = np.array([45, 102, 78, -3, 88])
scores[scores > 100] = 100
scores[scores < 0] = 0
print(scores)
print(np.where(scores >= 50, "ok", "fail"))
```

### Pitfall

An integer array can't hold `np.nan`, so marking missing values with it raises `ValueError`. Convert the array first with `scores = scores.astype(float)`.

PL: Tablica liczb całkowitych nie pomieści `np.nan`, więc oznaczanie nim brakujących wartości zgłasza `ValueError`. Najpierw zamień tablicę przez `scores = scores.astype(float)`.

```python raises=ValueError
import numpy as np

scores = np.array([45, -1, 78])
scores[scores < 0] = np.nan
```
