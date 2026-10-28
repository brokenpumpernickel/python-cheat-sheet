---
title: Random
glyph: "rand"
summary: "Random numbers with the np.random functions: seeds, uniform and normal samples, choosing, simulations."
pl:
  title: Losowanie
  summary: "Liczby losowe (random numbers) z funkcji np.random: ziarno, próbki jednostajne i normalne, losowy wybór, symulacje."
---

## Setting a seed

PL: Ustawianie ziarna

`np.random.seed(42)` makes the numbers drawn after it the same on every run, SciPy's `rvs` included, so others can check your results; without it, as in the other examples here, your numbers won't match the Output shown. Newer code writes `rng = np.random.default_rng(42)` and then `rng.normal(...)`, which works the same way.

PL: `np.random.seed(42)` ustawia ziarno (seed), więc liczby losowane po nim, także przez `rvs` z SciPy, są te same przy każdym uruchomieniu i inni mogą sprawdzić twoje wyniki; bez ziarna, jak w pozostałych przykładach, twoje liczby nie będą zgodne z pokazanym Wynikiem. W nowszym kodzie spotkasz `rng = np.random.default_rng(42)`, a potem `rng.normal(...)`; działa to tak samo.

```python
import numpy as np

np.random.seed(42)
print(np.random.random(3))
np.random.seed(42)
print(np.random.random(3))
```

### See also

- distributions/reproducible-samples

## Uniform numbers and integers

PL: Rozkład jednostajny i liczby całkowite

`np.random.uniform(low, high, n)` gives `n` decimals spread evenly between `low` and `high`. `np.random.randint(low, high, n)` gives whole numbers and leaves `high` out, so a die is `np.random.randint(1, 7, n)`; a shape `(rows, cols)` in place of `n` gives a matrix.

PL: `np.random.uniform(low, high, n)` daje `n` ułamków z rozkładu jednostajnego (uniform distribution) między `low` a `high`. `np.random.randint(low, high, n)` daje liczby całkowite i pomija `high`, więc kostka to `np.random.randint(1, 7, n)`; kształt (shape) `(rows, cols)` zamiast `n` daje macierz (matrix).

```python
import numpy as np

np.random.seed(3)  #| hide
print(np.random.uniform(0, 10, 3).round(2))
print(np.random.randint(1, 7, 10))
print(np.random.randint(1, 7, (2, 5)))
```

### See also

- arrays/two-dimensional-arrays
- scatter-plots/a-scatter-plot
- discrete-distributions/discrete-uniform-distribution

## Normal samples

PL: Próbki z rozkładu normalnego

`np.random.normal(loc, scale, size)` draws from a normal distribution with mean `loc` and standard deviation `scale`. The sample mean and standard deviation come close to them, and closer as the sample grows.

PL: `np.random.normal(loc, scale, size)` losuje z rozkładu normalnego (normal distribution) o średniej `loc` i odchyleniu standardowym (standard deviation) `scale`. Średnia i odchylenie standardowe z próby są im bliskie, a tym bliższe, im większa próba.

```python
import numpy as np

np.random.seed(3)  #| hide
heights = np.random.normal(170, 10, size=1000)
print(heights[:4].round(1))
print(f"{heights.mean():.2f}")
print(f"{heights.std(ddof=1):.2f}")
```

### See also

- aggregates/standard-deviation-and-variance
- histograms/a-histogram
- distributions/random-samples-with-rvs

## Choosing and shuffling

PL: Losowy wybór i tasowanie

`np.random.choice(values, size)` picks from `values` with replacement, unless you pass `replace=False`, and `p=[...]` gives each value its probability. `np.random.permutation(values)` returns a shuffled copy, while `np.random.shuffle(x)` shuffles `x` in place and returns `None`.

PL: `np.random.choice(values, size)` losuje z `values` ze zwracaniem (with replacement), chyba że podasz `replace=False`, a `p=[...]` nadaje każdej wartości jej prawdopodobieństwo. `np.random.permutation(values)` zwraca potasowaną kopię, a `np.random.shuffle(x)` tasuje `x` w miejscu i zwraca `None`.

```python
import numpy as np

np.random.seed(3)  #| hide
coin = ["H", "T"]
print(np.random.choice(coin, 10, p=[0.7, 0.3]))
names = ["Ola", "Jan", "Ewa", "Ala"]
print(np.random.choice(names, 2, replace=False))
print(np.random.permutation(names))
```

## Simulating an experiment

PL: Symulacja doświadczenia

Simulate many trials at once: draw a matrix with one row per trial, combine each row with `axis=1`, and take the proportion of successes with a mask. With enough trials it comes close to the exact probability, here 6/36 for two dice summing to 7.

PL: Symuluj wiele prób naraz: wylosuj macierz (matrix) z jednym wierszem na próbę, połącz każdy wiersz przez `axis=1` i policz odsetek sukcesów maską logiczną (boolean mask). Przy dużej liczbie prób wynik zbliża się do dokładnego prawdopodobieństwa, tu 6/36 dla sumy 7 na dwóch kostkach.

```python
import numpy as np

np.random.seed(4)  #| hide
rolls = np.random.randint(1, 7, (100_000, 2))
totals = rolls.sum(axis=1)
print(rolls[:3])
print((totals == 7).mean())
print(f"{6 / 36:.5f}")
```

### See also

- aggregates/along-an-axis
- aggregates/counting-and-proportions-with-a-mask
- bar-charts/a-probability-mass-function
