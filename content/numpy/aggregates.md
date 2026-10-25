---
title: Aggregates
glyph: ".sum"
summary: "Many values down to one: sum and mean, spread, along an axis, percentiles, positions, proportions."
pl:
  title: Agregacje
  summary: "Agregacje (aggregations): wiele wartości sprowadzonych do jednej — suma i średnia, rozrzut, wzdłuż osi, percentyle, położenia, proporcje."
---

## Sum, mean, min and max

PL: Suma, średnia, minimum i maksimum

`a.sum()`, `a.mean()`, `a.min()` and `a.max()` reduce an array to one number, and `np.sum(a)` and the other `np.` forms do the same. The result is a NumPy number such as `np.float64`, which prints like a plain one when you print it on its own.

PL: `a.sum()`, `a.mean()`, `a.min()` i `a.max()` sprowadzają tablicę (array) do jednej liczby, a `np.sum(a)` i inne formy z `np.` robią to samo. Wynik to liczba NumPy, np. `np.float64`, która wypisana osobno wygląda jak zwykła liczba.

```python
import numpy as np

data = np.array([4, 8, 15, 16, 23, 42])
print(data.sum(), data.mean())
print(data.min(), data.max())
```

### Pitfall

Inside a list or dict a NumPy number shows its type, as in `np.float64(18.0)`, because a container prints the `repr` of its items. Print the numbers on their own or in an f-string, or convert one with `float(x)`.

PL: Wewnątrz listy (list) lub słownika (dictionary) liczba NumPy pokazuje swój typ, np. `np.float64(18.0)`, bo kontener wypisuje `repr` swoich elementów. Wypisuj liczby osobno albo w f-stringu (f-string) lub zamień je przez `float(x)`.

```python
import numpy as np

data = np.array([4, 8, 15, 16, 23, 42])
print([data.min(), data.max()])
print({"mean": data.mean()})
```

### See also

- lists/summaries
- strings/f-strings

## Standard deviation and variance

PL: Odchylenie standardowe i wariancja

`a.std(ddof=1)` and `a.var(ddof=1)` are the sample standard deviation and variance, which divide by `n - 1` as in statistics courses. Without `ddof=1` NumPy divides by `n`, the population formula.

PL: `a.std(ddof=1)` i `a.var(ddof=1)` to odchylenie standardowe (standard deviation) i wariancja (variance) z próby, które dzielą przez `n - 1`, jak na zajęciach ze statystyki. Bez `ddof=1` NumPy dzieli przez `n`, czyli liczy wzór dla populacji.

```python
import numpy as np

heights = np.array([168, 175, 181])
print(f"{heights.std(ddof=1):.3f}")
print(f"{heights.var(ddof=1):.3f}")
```

### Pitfall

`heights.std()` with the default `ddof=0` is the population standard deviation, a little smaller than the sample one, and nothing warns you. Pass `ddof=1` for a sample.

PL: `heights.std()` z domyślnym `ddof=0` to odchylenie standardowe (standard deviation) populacji, trochę mniejsze niż z próby, i nic cię nie ostrzega. Dla próby podaj `ddof=1`.

```python
import numpy as np

heights = np.array([168, 175, 181])
print(f"{heights.std():.3f}")
```

## Along an axis

PL: Wzdłuż osi

On a matrix, `axis=0` aggregates down the rows and gives one result per column, and `axis=1` aggregates across the columns and gives one result per row. Without `axis` you get one number for the whole matrix.

PL: Na macierzy (matrix) `axis=0` agreguje w dół wierszy i daje jeden wynik na kolumnę, a `axis=1` agreguje w poprzek kolumn i daje jeden wynik na wiersz. Bez `axis` dostajesz jedną liczbę dla całej macierzy, bez podziału na osie (axes).

```python
import numpy as np

# rows: students, columns: tests
scores = np.array([[4, 5, 3],
                   [2, 4, 3],
                   [5, 5, 5],
                   [3, 2, 4]])
print(scores.mean(axis=0))
print(scores.mean(axis=1))
print(scores.max())
```

### Pitfall

`axis=0` names the axis that disappears: it collapses the rows, so `scores.mean(axis=0)` is one mean per test (column), not one per student. Count the results to check: one per column means `axis=0`.

PL: `axis=0` wskazuje oś (axis), która znika: zwija wiersze, więc `scores.mean(axis=0)` to jedna średnia na test (kolumnę), a nie na studenta. Policz wyniki, by sprawdzić: jeden na kolumnę oznacza `axis=0`.

### See also

- arrays/two-dimensional-arrays

## Median and percentiles

PL: Mediana i percentyle

`np.median(a)` is the middle value, and `np.percentile(a, q)` the value below which `q` percent of the data lie; a list of `q` values gives several at once. Both are functions only: there is no `a.median()`.

PL: `np.median(a)` to wartość środkowa, czyli mediana (median), a `np.percentile(a, q)` to percentyl (percentile), wartość, poniżej której leży `q` procent danych; lista wartości `q` daje kilka naraz. Obie są tylko funkcjami: nie ma `a.median()`.

```python
import numpy as np

times = np.array([12, 15, 11, 30, 14, 13])
print(np.median(times))
print(np.percentile(times, [25, 75]))
```

## Where the minimum and maximum are

PL: Gdzie jest minimum i maksimum

`a.argmin()` and `a.argmax()` give the index of the smallest and the largest value, the first one if there is a tie. Use that index to look up the matching value in another array.

PL: `a.argmin()` i `a.argmax()` dają indeks (index) najmniejszej i największej wartości, a przy remisie pierwszej z nich. Tym indeksem odczytasz pasującą wartość z innej tablicy (array).

```python
import numpy as np

names = np.array(["Ola", "Jan", "Ewa"])
scores = np.array([4.5, 3.0, 5.0])
best = scores.argmax()
print(best, names[best])
print(names[scores.argmin()])
```

## Counting and proportions with a mask

PL: Zliczanie i proporcje z maską

In arithmetic `True` counts as 1 and `False` as 0, so `mask.sum()` counts the values that meet a condition and `mask.mean()` gives their proportion.

PL: W rachunkach `True` liczy się jako 1, a `False` jako 0, więc `mask.sum()` zlicza wartości spełniające warunek, a `mask.mean()` daje ich proporcję, gdzie `mask` to maska logiczna (boolean mask).

```python
import numpy as np

rolls = np.array([3, 6, 3, 1, 6, 3, 5, 2])
sixes = rolls == 6
print(sixes.sum())
print(sixes.mean())
print((rolls >= 4).mean())
```

### See also

- indexing/boolean-masks
- dictionaries/counting-occurrences
