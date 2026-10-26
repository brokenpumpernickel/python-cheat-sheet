---
title: Distributions
glyph: "pdf"
summary: "Distributions in scipy.stats: objects, parameters, frozen distributions, probabilities, quantiles, samples and summaries."
pl:
  title: Rozkłady
  summary: "Rozkłady (distributions) w scipy.stats: obiekty, parametry, rozkłady zamrożone, prawdopodobieństwa, kwantyle, próbki i podsumowania."
---

## A distribution object

PL: Obiekt rozkładu

`stats.norm` is an object, not a function: you call its methods, such as `stats.norm.cdf(1.96)` or `stats.norm.pdf(0)`. Without parameters they use the standard normal distribution N(0, 1). `from scipy.stats import norm` gives the same object under the name `norm`.

PL: `stats.norm` to obiekt rozkładu (distribution), a nie funkcja: wywołujesz jego metody (methods), np. `stats.norm.cdf(1.96)` albo `stats.norm.pdf(0)`. Bez parametrów używają standardowego rozkładu normalnego (standard normal distribution) N(0, 1). `from scipy.stats import norm` daje ten sam obiekt pod nazwą `norm`.

```python
from scipy import stats

print(stats.norm.mean(), stats.norm.std())
print(f"{stats.norm.pdf(0):.4f}")
print(f"{stats.norm.cdf(1.96):.4f}")
```

## Parameters in every call

PL: Parametry w każdym wywołaniu

Each method also takes the distribution's parameters: `stats.uniform.rvs(loc=2, scale=3, size=5, random_state=rng)` draws five values from U(2, 5). Every call to `pdf`, `cdf` or `rvs` needs the same `loc` and `scale` again; leave them out and it quietly uses `loc=0` and `scale=1`.

PL: Każda metoda przyjmuje też parametry rozkładu: `stats.uniform.rvs(loc=2, scale=3, size=5, random_state=rng)` losuje pięć wartości z U(2, 5). Każde wywołanie `pdf`, `cdf` czy `rvs` potrzebuje znowu tych samych `loc` i `scale`; pomiń je, a metoda po cichu użyje `loc=0` i `scale=1`.

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(7)
sample = stats.uniform.rvs(
    loc=2, scale=3, size=5,
    random_state=rng)
print(sample.round(2))
x = 3.5
print(stats.uniform.pdf(x, loc=2, scale=3))
print(stats.uniform.cdf(x, loc=2, scale=3))
print(stats.uniform.cdf(x))
```

## A frozen distribution

PL: Rozkład zamrożony

Calling the distribution object with parameters, `U = stats.uniform(loc=2, scale=3)`, gives a new, *frozen* distribution that keeps them, so `U.rvs(size=5, random_state=rng)`, `U.pdf(x)` and `U.cdf(x)` take no `loc` or `scale`. The rest of this cheat sheet uses this style: you give the parameters once, so they can't drift apart between `pdf`, `cdf` and `rvs`.

PL: Wywołanie obiektu rozkładu z parametrami, `U = stats.uniform(loc=2, scale=3)`, daje nowy rozkład zamrożony (frozen distribution), który je zapamiętuje, więc `U.rvs(size=5, random_state=rng)`, `U.pdf(x)` i `U.cdf(x)` nie potrzebują `loc` ani `scale`. Dalej w tej ściągawce używamy tego stylu: parametry podajesz raz, więc nie mogą się rozjechać między `pdf`, `cdf` i `rvs`.

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(7)
U = stats.uniform(loc=2, scale=3)
sample = U.rvs(size=5, random_state=rng)
print(sample.round(2))
x = 3.5
print(U.pdf(x))
print(U.cdf(x))
```

### Pitfall

Passing `loc=` or `scale=` again to a frozen distribution's method raises `TypeError`, because its parameters are already fixed; for new parameters, freeze a new distribution.

PL: Ponowne podanie `loc=` lub `scale=` metodzie rozkładu zamrożonego (frozen distribution) zgłasza `TypeError`, bo jego parametry są już ustalone; dla nowych parametrów zamroź nowy rozkład.

```python raises=TypeError
from scipy import stats

U = stats.uniform(loc=2, scale=3)
print(U.cdf(3.5))
print(U.cdf(3.5, loc=0, scale=10))
```

## Density and probabilities

PL: Gęstość i prawdopodobieństwa

`d.pdf(x)` gives the density of a continuous distribution at `x`, and `d.pmf(k)` the probability P(X = k) of a discrete one. `d.cdf(x)` gives P(X ≤ x), and `d.sf(x)` gives P(X > x), the same as `1 - d.cdf(x)`.

PL: `d.pdf(x)` daje gęstość (pdf) rozkładu ciągłego w punkcie `x`, a `d.pmf(k)` daje funkcję prawdopodobieństwa (pmf), czyli P(X = k), rozkładu dyskretnego. `d.cdf(x)` to dystrybuanta (cdf), P(X ≤ x), a `d.sf(x)` to funkcja przeżycia (survival function), P(X > x), czyli to samo co `1 - d.cdf(x)`.

```python
from scipy import stats

d = stats.norm(loc=170, scale=8)
print(f"{d.pdf(170):.4f}")
print(f"{d.cdf(180):.4f}")
print(f"{d.sf(180):.4f}")
print(f"{1 - d.cdf(180):.4f}")
coin = stats.binom(10, 0.5)
print(f"{coin.pmf(5):.4f}")
```

### See also

- discrete-distributions/binomial-distribution
- plotting-distributions/the-cdf

## Quantiles with ppf

PL: Kwantyle z ppf

`d.ppf(q)` is the inverse of `cdf`: it gives the quantile, the value `x` with P(X ≤ x) = `q`. That is how you get critical values: `stats.norm().ppf(0.975)` is the 1.96 of a 95% interval, and `stats.t(df).ppf(0.975)` is its counterpart for the t distribution.

PL: `d.ppf(q)` to odwrotność `cdf`: daje kwantyl (quantile), czyli wartość `x`, dla której P(X ≤ x) = `q`. Tak otrzymasz wartości krytyczne (critical values): `stats.norm().ppf(0.975)` to 1,96 z przedziału 95%, a `stats.t(df).ppf(0.975)` to jej odpowiednik dla rozkładu t.

```python
from scipy import stats

z = stats.norm()
print(f"{z.ppf(0.975):.3f}")
print(f"{z.cdf(z.ppf(0.975)):.3f}")
t9 = stats.t(df=9)
print(f"{t9.ppf(0.975):.3f}")
heights = stats.norm(loc=170, scale=8)
print(f"{heights.ppf(0.9):.1f}")
```

### See also

- continuous-distributions/student-s-t-distribution
- plotting-distributions/a-pdf-curve

## Random samples with rvs

PL: Próbki losowe z rvs

`d.rvs(size=n, random_state=rng)` draws `n` random values from the distribution as an array. Pass a generator from `rng = np.random.default_rng(seed)` as `random_state`, so the sample is the same on every run.

PL: `d.rvs(size=n, random_state=rng)` losuje `n` wartości z rozkładu i zwraca je jako tablicę (array). Jako `random_state` podaj generator z `rng = np.random.default_rng(seed)`, żeby próbka (sample) była taka sama przy każdym uruchomieniu.

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(7)
d = stats.norm(loc=170, scale=10)
sample = d.rvs(size=1000, random_state=rng)
print(sample[:4].round(1))
print(f"{sample.mean():.2f}")
print(f"{sample.std(ddof=1):.2f}")
```

### See also

- random/normal-samples
- random/a-generator-with-a-seed
- plotting-distributions/a-histogram-with-the-pdf

## Mean, spread and intervals

PL: Średnia, rozrzut i przedziały

`d.mean()`, `d.std()` and `d.var()` give the distribution's exact mean, standard deviation and variance, not estimates from a sample. `d.interval(0.95)` returns the two values that hold the middle 95% of the probability, with 2.5% cut off at each end.

PL: `d.mean()`, `d.std()` i `d.var()` dają dokładną średnią, odchylenie standardowe (standard deviation) i wariancję (variance) rozkładu, a nie oszacowania z próby. `d.interval(0.95)` zwraca dwie wartości, między którymi leży środkowe 95% prawdopodobieństwa, z 2,5% odciętymi na każdym końcu.

```python
from scipy import stats

d = stats.norm(loc=170, scale=8)
print(d.mean(), d.std(), d.var())
low, high = d.interval(0.95)
print(f"{low:.1f} {high:.1f}")
print(f"{d.ppf(0.025):.1f}")
```

### See also

- aggregates/standard-deviation-and-variance
