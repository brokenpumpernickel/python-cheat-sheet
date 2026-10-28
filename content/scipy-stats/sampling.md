---
title: Sampling
glyph: "rvs"
summary: "Random samples with rvs: any distribution, a matrix of samples, statistics of many samples, probabilities by simulation, reproducible samples."
pl:
  title: Losowanie próby
  summary: "Losowanie próby (sampling) z rvs: dowolny rozkład, macierz prób, statystyki wielu prób, prawdopodobieństwa z symulacji, powtarzalne próby."
---

## Random samples with rvs

PL: Próba losowa z rvs

`d.rvs(size=n)` draws `n` random values from the distribution as a 1-D array, and the sample mean sits near the exact `d.mean()`. Every run draws a new sample, so your numbers will differ from the Output shown here, which comes from one run.

PL: `d.rvs(size=n)` losuje `n` wartości z rozkładu i zwraca je jako jednowymiarową tablicę (array), czyli próbę losową (random sample), której średnia leży blisko dokładnej średniej `d.mean()`. Każde uruchomienie losuje nową próbę, więc twoje liczby będą inne niż w pokazanym tu Wyniku, który pochodzi z jednego uruchomienia.

```python
import numpy as np  #| hide
from scipy import stats

np.random.seed(11)  #| hide
d = stats.norm(loc=170, scale=10)
sample = d.rvs(size=1000)
print(sample.shape)
print(sample[:4].round(1))
print(f"{sample.mean():.2f}", d.mean())
print(f"{sample.std(ddof=1):.2f}", d.std())
```

### See also

- random/normal-samples
- random/setting-a-seed
- plotting-distributions/a-histogram-with-the-pdf

## Sampling any distribution

PL: Losowanie z dowolnego rozkładu

Every distribution in `scipy.stats` has the same `rvs(size=n)`. A continuous one, such as `stats.norm` or `stats.uniform`, gives decimals (`float64`), and a discrete one, such as `stats.binom` or `stats.poisson`, gives whole numbers (`int64`).

PL: Każdy rozkład (distribution) w `scipy.stats` ma tę samą metodę `rvs(size=n)`. Rozkład ciągły, np. `stats.norm` albo `stats.uniform`, daje ułamki (`float64`), a rozkład dyskretny, np. `stats.binom` albo `stats.poisson`, daje liczby całkowite (`int64`).

```python
import numpy as np  #| hide
from scipy import stats

np.random.seed(3)  #| hide
heights = stats.norm(loc=170, scale=10)
U = stats.uniform(loc=2, scale=3)
coin = stats.binom(10, 0.5)
calls = stats.poisson(3)
for d in [heights, U, coin, calls]:
    sample = d.rvs(size=5)
    print(sample.dtype, sample.round(2))
```

### See also

- continuous-distributions/uniform-distribution
- discrete-distributions/poisson-distribution
- plotting-distributions/a-pmf-as-bars

## A matrix of samples

PL: Macierz prób

`d.rvs(size=(1000, 10))` gives a matrix with 1000 rows and 10 columns: 1000 repeats of a sample of 10, one sample per row. `samples[0]` is the first sample.

PL: `d.rvs(size=(1000, 10))` daje macierz (matrix) o 1000 wierszach i 10 kolumnach: 1000 powtórzeń próby losowej (random sample) liczności 10, po jednej próbie w każdym wierszu. `samples[0]` to pierwsza próba.

```python
import numpy as np  #| hide
from scipy import stats

np.random.seed(6)  #| hide
d = stats.norm(loc=170, scale=10)
samples = d.rvs(size=(1000, 10))
print(samples.shape)
print(samples[0].round(1))
print(samples[1].round(1))
```

### See also

- arrays/two-dimensional-arrays
- indexing/rows-and-columns
- random/uniform-numbers-and-integers

## Statistics of many samples

PL: Statystyki wielu prób

On a matrix of samples, one per row, `samples.mean(axis=1)` gives one mean per sample, here 1000 sample means. They vary less than single values: their standard deviation is close to σ/√n, the standard error, here 10/√10 ≈ 3.16.

PL: Na macierzy (matrix) prób, po jednej w wierszu, `samples.mean(axis=1)` daje jedną średnią na próbę, tu 1000 średnich z próby. Zmieniają się mniej niż pojedyncze wartości: ich odchylenie standardowe (standard deviation) jest bliskie σ/√n, czyli błędowi standardowemu (standard error), tu 10/√10 ≈ 3,16.

```python
import numpy as np
from scipy import stats

np.random.seed(6)  #| hide
d = stats.norm(loc=170, scale=10)
samples = d.rvs(size=(1000, 10))
means = samples.mean(axis=1)
print(means.shape)
print(means[:4].round(1))
print(f"{means.std(ddof=1):.2f}")
print(f"{d.std() / np.sqrt(10):.2f}")
```

### Pitfall

`samples.mean(axis=0)` gives one mean per column, 10 values, not one per sample: each mixes 1000 different samples, so all of them sit close to 170 and nothing warns you. Count the results: one per sample means `axis=1`.

PL: `samples.mean(axis=0)` daje jedną średnią na kolumnę, 10 wartości, a nie jedną na próbę: każda miesza 1000 różnych prób, więc wszystkie leżą blisko 170 i nic cię nie ostrzega. Policz wyniki: jeden na próbę oznacza `axis=1`.

```python
import numpy as np  #| hide
from scipy import stats

np.random.seed(6)  #| hide
d = stats.norm(loc=170, scale=10)
samples = d.rvs(size=(1000, 10))
means = samples.mean(axis=0)
print(means.shape)
print(means.round(1))
```

### See also

- aggregates/along-an-axis
- aggregates/standard-deviation-and-variance
- random/simulating-an-experiment

## Estimating probabilities by simulation

PL: Szacowanie prawdopodobieństw symulacją

`sample > 2` is a mask of `True` and `False`, so `(sample > 2).mean()` is the share of the sample above 2: an estimate of P(X > 2), close to the exact `d.sf(2)` and closer the larger the sample. Join conditions with `&`, each in its own parentheses.

PL: `sample > 2` to maska logiczna (boolean mask) z `True` i `False`, więc `(sample > 2).mean()` to odsetek próby powyżej 2: oszacowanie P(X > 2), bliskie dokładnemu `d.sf(2)`, i to tym bliższe, im większa próba. Warunki łącz przez `&`, każdy we własnych nawiasach.

```python
import numpy as np  #| hide
from scipy import stats

np.random.seed(12)  #| hide
d = stats.norm()
sample = d.rvs(size=100_000)
print((sample > 2).mean())
print(f"{d.sf(2):.5f}")
inside = (sample > -1) & (sample < 1)
print(inside.mean())
print(f"{d.cdf(1) - d.cdf(-1):.5f}")
```

### See also

- aggregates/counting-and-proportions-with-a-mask
- random/simulating-an-experiment
- distributions/density-and-probabilities

## Reproducible samples

PL: Powtarzalne próby

`np.random.seed(42)` before `d.rvs(size=n)` gives the same samples on every run, so others can check your results: each call draws new numbers, but after the same seed the whole sequence repeats. To fix a single call instead, pass `random_state=42`.

PL: `np.random.seed(42)` przed `d.rvs(size=n)` daje te same próby przy każdym uruchomieniu, więc inni mogą sprawdzić twoje wyniki: każde wywołanie losuje nowe liczby, ale po tym samym ziarnie (seed) cały ich ciąg się powtarza. Żeby ustalić tylko jedno wywołanie, podaj `random_state=42`.

```python
import numpy as np
from scipy import stats

die = stats.randint(1, 7)
np.random.seed(42)
print(die.rvs(size=5))
print(die.rvs(size=5))
np.random.seed(42)
print(die.rvs(size=5))
print(die.rvs(size=5))
```

### See also

- random/setting-a-seed
