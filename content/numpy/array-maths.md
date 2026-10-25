---
title: Array maths
glyph: "a*2"
summary: "Maths on every value at once: arithmetic, maths functions, comparisons, broadcasting, functions on whole arrays."
pl:
  title: Działania na tablicach
  summary: "Działania na tablicach (arrays) bez pętli: arytmetyka, funkcje matematyczne, porównania, rozgłaszanie (broadcasting), funkcje na całych tablicach."
---

## Element-wise arithmetic

PL: Arytmetyka element po elemencie

`+`, `-`, `*`, `/` and `**` act on every value of an array, with no loop. Between two arrays of the same shape they pair the values up position by position.

PL: `+`, `-`, `*`, `/` i `**` działają na każdej wartości tablicy (array) element po elemencie (element-wise), bez pętli. Między dwiema tablicami o tym samym kształcie (shape) łączą wartości w pary, pozycja po pozycji.

```python
import numpy as np

x = np.array([1, 2, 3, 4])
y = np.array([10, 20, 30, 40])
print(x * 2)
print(x ** 2)
print(x + y)
print(y / x)
```

### Pitfall

On a plain list `*` and `+` don't do arithmetic: `data * 2` repeats the list and `data + other` joins two lists. Turn the list into an array with `np.array(data)` first.

PL: Na zwykłej liście (list) `*` i `+` nie liczą: `data * 2` powtarza listę, a `data + other` łączy dwie listy. Najpierw zamień listę w tablicę przez `np.array(data)`.

```python
data = [1, 2, 3]
print(data * 2)
print(data + [10, 20, 30])
```

### See also

- lists/list-comprehensions

## Maths functions

PL: Funkcje matematyczne

`np.sqrt`, `np.exp`, `np.log` and `np.abs` apply to every value and return a new array; `np.log` is the natural logarithm. `a.round(2)` rounds every value to two decimal places.

PL: `np.sqrt`, `np.exp`, `np.log` i `np.abs` działają na każdej wartości i zwracają nową tablicę (array); `np.log` to logarytm naturalny. `a.round(2)` zaokrągla każdą wartość do dwóch miejsc po przecinku.

```python
import numpy as np

x = np.array([1.0, 4.0, 9.0])
print(np.sqrt(x))
print(np.log(x).round(3))
print(np.exp(np.array([0, 1, 2])).round(2))
print(np.abs(np.array([-2, 3, -5])))
```

## Comparisons

PL: Porównania

`a == b`, `a < b` and the other comparisons work value by value and give an array of `True` and `False`. `.all()` asks whether every value is `True` and `.any()` whether at least one is; `np.isclose(a, b)` compares decimals with a small tolerance.

PL: `a == b`, `a < b` i inne porównania działają wartość po wartości i dają tablicę (array) `True` i `False`. `.all()` sprawdza, czy wszystkie wartości to `True`, a `.any()`, czy choć jedna; `np.isclose(a, b)` porównuje ułamki z małą tolerancją.

```python
import numpy as np

a = np.array([0.1 + 0.2, 0.5, 1.0])
b = np.array([0.3, 0.5, 2.0])
print(a == b)
print(np.isclose(a, b))
print((a < b).any(), (a < b).all())
```

### See also

- indexing/boolean-masks

## Broadcasting

PL: Rozgłaszanie (broadcasting)

When shapes differ, NumPy stretches the smaller array to fit: a single number goes with every value, and a row of `cols` values goes with every row of a `(rows, cols)` matrix. To go with every column instead, give it the shape `(rows, 1)`.

PL: Gdy kształty (shapes) się różnią, NumPy rozciąga mniejszą tablicę, by pasowała, czyli stosuje rozgłaszanie (broadcasting): pojedyncza liczba trafia do każdej wartości, a wiersz `cols` wartości do każdego wiersza macierzy (matrix) `(rows, cols)`. Aby trafiła do każdej kolumny, nadaj jej kształt `(rows, 1)`.

```python
import numpy as np

scores = np.array([[4, 5, 3],
                   [2, 4, 4]])
bonus = np.array([1, 0, 2])
print(scores + bonus)
weights = np.array([[10], [100]])
print(scores * weights)
```

### Pitfall

A one-dimensional array always lines up with the columns, so one value per row (shape `(2,)` against `(2, 3)`) raises a `ValueError`. Make it a column first with `row_bonus.reshape(-1, 1)`.

PL: Tablica jednowymiarowa zawsze dopasowuje się do kolumn, więc jedna wartość na wiersz (kształt `(2,)` wobec `(2, 3)`) zgłasza `ValueError`. Najpierw zamień ją w kolumnę przez `row_bonus.reshape(-1, 1)`.

```python raises=ValueError
import numpy as np

scores = np.array([[4, 5, 3],
                   [2, 4, 4]])
row_bonus = np.array([1, 2])
print(scores + row_bonus)
```

### See also

- arrays/reshaping

## Functions that work on whole arrays

PL: Funkcje działające na całych tablicach

A function written with NumPy operations takes a whole array and returns the result for every value, with no loop; this is called vectorisation. The normal density below gives one height per `x`, and still works on a single number.

PL: Funkcja napisana z operacji NumPy przyjmuje całą tablicę (array) i zwraca wynik dla każdej wartości, bez pętli; to wektoryzacja (vectorisation). Gęstość (density) rozkładu normalnego poniżej daje jedną wysokość na każde `x` i nadal działa na pojedynczej liczbie.

```python
import numpy as np

def normal_pdf(x, mu=0.0, sigma=1.0):
    z = (x - mu) / sigma
    c = sigma * np.sqrt(2 * np.pi)
    return np.exp(-z ** 2 / 2) / c

x = np.array([-1.0, 0.0, 1.0, 2.0])
print(normal_pdf(x).round(4))
print(f"{normal_pdf(0.5):.4f}")
```

### Pitfall

`if` and the `math` module handle one number at a time, so on an array `if x < 0:` raises `ValueError` and `math.exp(x)` raises `TypeError`. Write the choice as `np.where(x < 0, 0.0, np.exp(-x))` and use `np.exp`.

PL: `if` i moduł (module) `math` obsługują jedną liczbę naraz, więc na tablicy `if x < 0:` zgłasza `ValueError`, a `math.exp(x)` zgłasza `TypeError`. Zapisz wybór jako `np.where(x < 0, 0.0, np.exp(-x))` i użyj `np.exp`.

```python raises=ValueError
import numpy as np

def exp_pdf(x):
    if x < 0:
        return 0.0
    return np.exp(-x)

x = np.array([-1.0, 0.0, 1.0])
print(exp_pdf(x))
```

### See also

- functions/defining-and-calling
- indexing/changing-values-through-a-mask
