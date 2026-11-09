---
title: Matrices
glyph: "Mat"
summary: "Exact, symbolic matrices in SymPy: making a matrix, the matrix product, transpose and inverse, determinants, eigenvalues and eigenvectors."
pl:
  title: Macierze
  summary: "Dokładne, symboliczne macierze (matrices) w SymPy: tworzenie macierzy, iloczyn macierzy, transpozycja i odwrotność, wyznaczniki, wartości i wektory własne."
---

## Making a matrix

PL: Tworzenie macierzy (matrix)

`sp.Matrix([[...], [...]])` makes a matrix from a list of rows, and its entries may be symbols: `V0 * sp.Matrix(...)` multiplies every entry by `V0`. `M.shape` is `(rows, cols)`, `M[0, 1]` is one entry, and `sp.eye(3)` is the 3×3 identity matrix.

PL: `sp.Matrix([[...], [...]])` tworzy macierz z listy wierszy, a jej elementami mogą być symbole: `V0 * sp.Matrix(...)` mnoży każdy element przez `V0`. `M.shape` to `(rows, cols)`, `M[0, 1]` to jeden element, a `sp.eye(3)` to macierz jednostkowa 3×3.

```python
import sympy as sp
sp.init_printing()

V0 = sp.Symbol("V_0")
M = V0 * sp.Matrix([[0, 1, 0],
                    [1, 0, 1],
                    [0, 1, 0]])
display(M)
print(M.shape)
display(M[0, 1])
display(sp.eye(3))
```

### See also

- arrays/two-dimensional-arrays

## Matrix arithmetic

PL: Działania na macierzach

`M * N` is the matrix product, rows times columns, `M.T` is the transpose and `M.inv()` the inverse. The inverse stays exact, with fractions such as `3/2` instead of `1.5`.

PL: `M * N` to iloczyn macierzy (matrix product), wiersze razy kolumny, `M.T` to transpozycja (transpose), a `M.inv()` macierz odwrotna (inverse). Macierz odwrotna zostaje dokładna, z ułamkami takimi jak `3/2` zamiast `1.5`.

```python
import sympy as sp
sp.init_printing()

M = sp.Matrix([[1, 2], [3, 4]])
N = sp.Matrix([[0, 1], [1, 0]])
display(M * N)
display(M.T)
display(M.inv())
```

### Pitfall

On a NumPy array `*` multiplies element by element, but on a SymPy `Matrix` it is the matrix product, so the same numbers give different results. For the matrix product of arrays write `a @ a`.

PL: Na tablicy (array) NumPy `*` mnoży element po elemencie, ale na macierzy SymPy (`Matrix`) to iloczyn macierzy, więc te same liczby dają różne wyniki. Iloczyn macierzy dla tablic zapiszesz jako `a @ a`.

```python
import numpy as np
import sympy as sp
sp.init_printing()

a = np.array([[1, 2], [3, 4]])
print(a * a)
M = sp.Matrix([[1, 2], [3, 4]])
display(M * M)
```

### See also

- array-maths/element-wise-arithmetic
- arrays/two-dimensional-arrays

## Determinants

PL: Wyznaczniki (determinants)

`M.det()` gives the determinant of a square matrix, as a formula when the entries are symbols. The matrix is invertible exactly where the determinant isn't `0`: here for every `x` except `±1/√2`.

PL: `M.det()` daje wyznacznik macierzy kwadratowej, jako wzór, gdy elementy są symbolami. Macierz jest odwracalna dokładnie tam, gdzie wyznacznik nie jest `0`: tutaj dla każdego `x` poza `±1/√2`.

```python
import sympy as sp
sp.init_printing()

a, b, c, d = sp.symbols("a b c d")
display(sp.Matrix([[a, b], [c, d]]).det())
x = sp.Symbol("x")
M = sp.Matrix([[1, x, 0],
               [x, 1, x],
               [0, x, 1]])
display(M.det())
```

## Eigenvalues and eigenvectors

PL: Wartości i wektory własne (eigenvalues, eigenvectors)

`M.eigenvals()` gives a dict from each eigenvalue to its multiplicity. `M.eigenvects()` gives a list of triples: the eigenvalue, its multiplicity and a list of its eigenvectors. For this matrix the eigenvalues are `0` and `±√2 V0`.

PL: `M.eigenvals()` zwraca słownik (dict), który każdej wartości własnej przypisuje jej krotność. `M.eigenvects()` zwraca listę trójek: wartość własna, jej krotność i lista jej wektorów własnych. Dla tej macierzy wartości własne to `0` i `±√2 V0`.

```python
import sympy as sp
sp.init_printing()

V0 = sp.Symbol("V_0")
M = V0 * sp.Matrix([[0, 1, 0],
                    [1, 0, 1],
                    [0, 1, 0]])
display(M.eigenvals())
for triple in M.eigenvects():
    display(triple)
```
