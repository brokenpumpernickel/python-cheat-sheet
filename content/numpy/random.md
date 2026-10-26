---
title: Random
glyph: "rng"
summary: "Reproducible random numbers: a seeded generator, uniform and normal samples, choosing, simulations."
pl:
  title: Losowanie
  summary: "Powtarzalne liczby losowe (random numbers): generator z ziarnem, próbki jednostajne i normalne, losowy wybór, symulacje."
---

## A generator with a seed

PL: Generator z ziarnem

`rng = np.random.default_rng(42)` makes a random generator, and every random number comes from its methods, such as `rng.random(n)`. The same seed gives the same numbers on every run, so others can check your results; leave the seed out and each run differs.

PL: `rng = np.random.default_rng(42)` tworzy generator liczb losowych (random number generator), a każda liczba losowa pochodzi z jego metod, np. `rng.random(n)`. To samo ziarno (seed) daje te same liczby przy każdym uruchomieniu, więc inni mogą sprawdzić twoje wyniki; bez ziarna każde uruchomienie daje inne.

```python
import numpy as np

rng = np.random.default_rng(42)
print(rng.random(3))
rng = np.random.default_rng(42)
print(rng.random(3))
```

### Pitfall

Older tutorials use `np.random.seed(42)` with `np.random.rand()` or `np.random.normal()`. That legacy style shares one hidden global state, so any other code that draws numbers changes yours; make a generator with `default_rng` and use its methods instead.

PL: Starsze poradniki używają `np.random.seed(42)` z `np.random.rand()` lub `np.random.normal()`. Ten przestarzały styl dzieli jeden ukryty stan globalny, więc każdy inny kod, który losuje, zmienia twoje liczby; zamiast tego utwórz generator przez `default_rng` i używaj jego metod.

## Uniform numbers and integers

PL: Rozkład jednostajny i liczby całkowite

`rng.uniform(low, high, n)` gives `n` decimals spread evenly between `low` and `high`. `rng.integers(low, high, n)` gives whole numbers and leaves `high` out, so a die is `rng.integers(1, 7, n)`; a shape `(rows, cols)` in place of `n` gives a matrix.

PL: `rng.uniform(low, high, n)` daje `n` ułamków z rozkładu jednostajnego (uniform distribution) między `low` a `high`. `rng.integers(low, high, n)` daje liczby całkowite i pomija `high`, więc kostka to `rng.integers(1, 7, n)`; kształt (shape) `(rows, cols)` zamiast `n` daje macierz (matrix).

```python
import numpy as np

rng = np.random.default_rng(1)
print(rng.uniform(0, 10, 3).round(2))
print(rng.integers(1, 7, 10))
print(rng.integers(1, 7, (2, 5)))
```

### See also

- arrays/two-dimensional-arrays
- scatter-plots/a-scatter-plot
- discrete-distributions/discrete-uniform-distribution

## Normal samples

PL: Próbki z rozkładu normalnego

`rng.normal(loc, scale, size)` draws from a normal distribution with mean `loc` and standard deviation `scale`. The sample mean and standard deviation come close to them, and closer as the sample grows.

PL: `rng.normal(loc, scale, size)` losuje z rozkładu normalnego (normal distribution) o średniej `loc` i odchyleniu standardowym (standard deviation) `scale`. Średnia i odchylenie standardowe z próby są im bliskie, a tym bliższe, im większa próba.

```python
import numpy as np

rng = np.random.default_rng(7)
heights = rng.normal(170, 10, size=1000)
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

`rng.choice(values, size)` picks from `values` with replacement, unless you pass `replace=False`, and `p=[...]` gives each value its probability. `rng.permutation(values)` returns a shuffled copy.

PL: `rng.choice(values, size)` losuje z `values` ze zwracaniem (with replacement), chyba że podasz `replace=False`, a `p=[...]` nadaje każdej wartości jej prawdopodobieństwo. `rng.permutation(values)` zwraca potasowaną kopię.

```python
import numpy as np

rng = np.random.default_rng(3)
coin = ["H", "T"]
print(rng.choice(coin, 10, p=[0.7, 0.3]))
names = ["Ola", "Jan", "Ewa", "Ala"]
print(rng.choice(names, 2, replace=False))
print(rng.permutation(names))
```

## Simulating an experiment

PL: Symulacja doświadczenia

Simulate many trials at once: draw a matrix with one row per trial, combine each row with `axis=1`, and take the proportion of successes with a mask. With enough trials it comes close to the exact probability, here 6/36 for two dice summing to 7.

PL: Symuluj wiele prób naraz: wylosuj macierz (matrix) z jednym wierszem na próbę, połącz każdy wiersz przez `axis=1` i policz odsetek sukcesów maską logiczną (boolean mask). Przy dużej liczbie prób wynik zbliża się do dokładnego prawdopodobieństwa, tu 6/36 dla sumy 7 na dwóch kostkach.

```python
import numpy as np

rng = np.random.default_rng(2024)
rolls = rng.integers(1, 7, (100_000, 2))
totals = rolls.sum(axis=1)
print(rolls[:3])
print((totals == 7).mean())
print(f"{6 / 36:.5f}")
```

### See also

- aggregates/along-an-axis
- aggregates/counting-and-proportions-with-a-mask
- bar-charts/a-probability-mass-function
