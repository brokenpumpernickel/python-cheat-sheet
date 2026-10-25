---
title: Arrays
glyph: "[[ ]]"
summary: "Collections of numbers of one type: creating, ranges, shape and dtype, matrices, reshaping."
pl:
  title: Tablice
  summary: "Tablice (arrays): zbiory liczb jednego typu — tworzenie, zakresy, kształt i dtype, macierze, zmiana kształtu."
---

## Creating arrays

PL: Tworzenie tablic

`np.array(data)` turns a list into an array, NumPy's collection of numbers that all share one type. Load NumPy with `import numpy as np`; a printed array has no commas between its values.

PL: `np.array(data)` zamienia listę w tablicę (array), czyli zbiór liczb NumPy, które mają wspólny typ. NumPy wczytasz przez `import numpy as np`; wypisana tablica nie ma przecinków między wartościami.

```python
import numpy as np

scores = np.array([4.5, 3.5, 5.0, 4.0])
print(scores)
print(type(scores))
```

### See also

- lists/creating-and-indexing

## Ranges

PL: Zakresy

`np.arange(start, stop, step)` works like `range` but returns an array and takes decimal steps; `stop` is not included. `np.linspace(start, stop, num)` gives `num` evenly spaced values and includes `stop`.

PL: `np.arange(start, stop, step)` działa jak `range`, ale zwraca tablicę (array) i przyjmuje krok z ułamkiem; `stop` nie wchodzi do wyniku. `np.linspace(start, stop, num)` daje `num` równo rozłożonych wartości i obejmuje `stop`.

```python
import numpy as np

print(np.arange(0, 10, 2))
print(np.arange(0, 1, 0.25))
print(np.linspace(0, 1, 5))
```

### See also

- loops/range

## Zeros, ones and full

PL: Zera, jedynki i full

`np.zeros(n)` and `np.ones(n)` make an array of `n` zeros or ones, and `np.full(n, value)` fills one with any value. Zeros and ones are decimals unless you pass `dtype=int`.

PL: `np.zeros(n)` i `np.ones(n)` tworzą tablicę (array) z `n` zer lub jedynek, a `np.full(n, value)` wypełnia ją dowolną wartością. Zera i jedynki są ułamkami, chyba że podasz `dtype=int`.

```python
import numpy as np

print(np.zeros(3))
print(np.ones(4, dtype=int))
print(np.full(3, 7.5))
```

## Shape and dtype

PL: Kształt i dtype

`a.shape` is the size along each dimension as a tuple, `a.ndim` the number of dimensions and `a.size` the number of values. `a.dtype` is the type every value shares: one decimal among integers makes the whole array `float64`.

PL: `a.shape` to rozmiar w każdym wymiarze jako krotka (tuple), `a.ndim` to liczba wymiarów, a `a.size` liczba wartości. `a.dtype` to typ danych (dtype) wspólny dla wszystkich wartości: jeden ułamek wśród liczb całkowitych zmienia całą tablicę w `float64`.

```python
import numpy as np

a = np.array([1, 2, 3.5])
print(a.shape, a.ndim, a.size)
print(a.dtype)
print(np.array([1, 2, 3]).dtype)
```

## Two-dimensional arrays

PL: Tablice dwuwymiarowe

Nested lists in `np.array` make a matrix, one inner list per row, with the shape `(rows, cols)`. `np.zeros`, `np.ones` and `np.full` take that shape as a tuple, and `np.arange(n).reshape(rows, cols)` fills a matrix row by row.

PL: Zagnieżdżone listy w `np.array` tworzą macierz (matrix), jedna wewnętrzna lista na wiersz, o kształcie (shape) `(rows, cols)`. `np.zeros`, `np.ones` i `np.full` przyjmują ten kształt jako krotkę (tuple), a `np.arange(n).reshape(rows, cols)` wypełnia macierz wiersz po wierszu.

```python
import numpy as np

m = np.array([[1, 2, 3], [4, 5, 6]])
print(m)
print(m.shape)
print(np.zeros((2, 3)))
print(np.arange(1, 7).reshape(3, 2))
```

### Pitfall

`np.zeros(2, 3)` without the inner parentheses raises a `TypeError` about a data type, because the second argument is the `dtype`, not the number of columns.

PL: `np.zeros(2, 3)` bez wewnętrznych nawiasów zgłasza `TypeError` o typie danych, bo drugi argument to `dtype`, a nie liczba kolumn.

```python raises=TypeError
import numpy as np

print(np.zeros(2, 3))
```

### See also

- random/uniform-numbers-and-integers

## Reshaping

PL: Zmiana kształtu

`a.reshape(rows, cols)` gives the same values in a new shape, filled row by row, and `-1` lets NumPy work out one of the sizes. `m.T` swaps rows and columns, which is not the same as reshaping, and `m.flatten()` turns a matrix back into one row.

PL: `a.reshape(rows, cols)` daje te same wartości w nowym kształcie (shape), wypełnionym wiersz po wierszu, a `-1` pozwala NumPy wyliczyć jeden z rozmiarów. `m.T` zamienia wiersze z kolumnami (transpose), co nie jest tym samym co zmiana kształtu, a `m.flatten()` zamienia macierz z powrotem w jeden wiersz.

```python
import numpy as np

a = np.arange(6)
m = a.reshape(2, 3)
print(m)
print(a.reshape(-1, 2))
print(m.T)
print(m.flatten())
```
