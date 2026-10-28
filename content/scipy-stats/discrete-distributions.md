---
title: Discrete distributions
glyph: "binom"
summary: "Distributions of counts, with pmf instead of pdf: binomial and Bernoulli, Poisson, geometric, discrete uniform."
pl:
  title: Rozkłady dyskretne
  summary: "Rozkłady dyskretne (discrete distributions), czyli rozkłady liczebności z pmf zamiast pdf: dwumianowy i Bernoulliego, Poissona, geometryczny, dyskretny jednostajny."
---

## Binomial distribution

PL: Rozkład dwumianowy

`stats.binom(n, p)` counts the successes in `n` independent trials, each a success with probability `p`, and `pmf(k)` gives P(X = k). Bernoulli is the case `n=1`: one trial, with the values 0 and 1, also available as `stats.bernoulli(p)`.

PL: `stats.binom(n, p)` to rozkład dwumianowy (binomial distribution): liczba sukcesów w `n` niezależnych próbach, z których każda kończy się sukcesem z prawdopodobieństwem `p`, a `pmf(k)` daje P(X = k). Rozkład Bernoulliego (Bernoulli distribution) to przypadek `n=1`: jedna próba o wartościach 0 i 1, dostępny też jako `stats.bernoulli(p)`.

```python
import numpy as np
from scipy import stats

coin = stats.binom(10, 0.5)
k = np.arange(0, 11)
print(coin.pmf(k).round(3))
print(coin.mean(), coin.var())
print(f"{coin.cdf(3):.4f}")
one = stats.binom(1, 0.3)
print(one.pmf([0, 1]))
```

### Pitfall

A discrete distribution has no `.pdf`, only `.pmf`, so `coin.pdf(5)` raises `AttributeError`.

PL: Rozkład dyskretny (discrete distribution) nie ma `.pdf`, tylko `.pmf`, więc `coin.pdf(5)` zgłasza `AttributeError`.

```python raises=AttributeError
from scipy import stats

coin = stats.binom(10, 0.5)
print(f"{coin.pmf(5):.4f}")
print(coin.pdf(5))
```

### See also

- plotting-distributions/a-pmf-as-bars

## Poisson distribution

PL: Rozkład Poissona

`stats.poisson(mu)` counts events in a fixed interval when they happen `mu` times on average; its values are 0, 1, 2, … with no upper limit, and its mean and variance both equal `mu`. For a discrete distribution `sf(k)` is P(X > k), so `calls.sf(5)` is the probability of 6 or more.

PL: `stats.poisson(mu)` to rozkład Poissona (Poisson distribution): liczba zdarzeń w ustalonym przedziale, gdy zdarzają się średnio `mu` razy; przyjmuje wartości 0, 1, 2, … bez górnej granicy, a jego średnia i wariancja są równe `mu`. W rozkładzie dyskretnym `sf(k)` to P(X > k), więc `calls.sf(5)` to prawdopodobieństwo 6 lub więcej.

```python
import numpy as np
from scipy import stats

calls = stats.poisson(3)
k = np.arange(0, 8)
print(calls.pmf(k).round(3))
print(calls.mean(), calls.var())
print(f"{calls.sf(5):.4f}")
```

## Geometric distribution

PL: Rozkład geometryczny

`stats.geom(p)` counts the trials up to and including the first success, so its values start at 1, not 0, and its mean is `1/p`: waiting for a six takes 6 rolls on average. For the failures before the first success, use `stats.geom(p, loc=-1)`.

PL: `stats.geom(p)` to rozkład geometryczny (geometric distribution): liczba prób aż do pierwszego sukcesu włącznie, więc jego wartości zaczynają się od 1, a nie od 0, a średnia wynosi `1/p`: na szóstkę czekasz średnio 6 rzutów. Liczbę porażek przed pierwszym sukcesem daje `stats.geom(p, loc=-1)`.

```python
import numpy as np
from scipy import stats

six = stats.geom(1 / 6)
k = np.arange(0, 6)
print(six.pmf(k).round(3))
print(f"{six.mean():.1f}")
print(f"{six.cdf(6):.4f}")
```

## Discrete uniform distribution

PL: Dyskretny rozkład jednostajny

`stats.randint(low, high)` gives every whole number from `low` to `high - 1` the same probability. `high` is not included, as in `np.random.randint`, so a die is `stats.randint(1, 7)`.

PL: `stats.randint(low, high)` to dyskretny rozkład jednostajny (discrete uniform distribution): każda liczba całkowita od `low` do `high - 1` ma to samo prawdopodobieństwo. `high` nie jest wliczane, tak jak w `np.random.randint`, więc kostka to `stats.randint(1, 7)`.

```python
import numpy as np
from scipy import stats

np.random.seed(1)  #| hide
die = stats.randint(1, 7)
print(die.pmf(np.arange(0, 8)).round(3))
print(die.mean())
print(die.rvs(size=10))
```

### See also

- random/uniform-numbers-and-integers
