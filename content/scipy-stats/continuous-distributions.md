---
title: Continuous distributions
glyph: "norm"
summary: "Continuous distributions and their parameters: shape, loc and scale, normal, uniform, exponential, t and chi-squared."
pl:
  title: Rozkłady ciągłe
  summary: "Rozkłady ciągłe (continuous distributions) i ich parametry: kształt, loc i scale, rozkład normalny, jednostajny, wykładniczy, t i chi-kwadrat."
---

## Shape, loc and scale

PL: Kształt, loc i scale

Every continuous distribution is a standard one, moved by `loc` and stretched by `scale`: X = `loc` + `scale` · Z. Shape parameters, such as the `df` of `stats.t`, come first, before `loc` and `scale`, so `stats.t(5, 10, 2)` is `stats.t(df=5, loc=10, scale=2)`.

PL: Każdy rozkład ciągły (continuous distribution) to rozkład standardowy przesunięty o `loc` i rozciągnięty o `scale`: X = `loc` + `scale` · Z. Parametry kształtu (shape parameters), np. `df` w `stats.t`, są pierwsze, przed `loc` i `scale`, więc `stats.t(5, 10, 2)` to `stats.t(df=5, loc=10, scale=2)`.

```python
from scipy import stats

z = stats.norm()
d = stats.norm(loc=10, scale=2)
print(f"{d.ppf(0.9):.3f}")
print(f"{10 + 2 * z.ppf(0.9):.3f}")
t1 = stats.t(5, 10, 2)
t2 = stats.t(df=5, loc=10, scale=2)
print(t1.ppf(0.9) == t2.ppf(0.9))
```

### See also

- plotting-distributions/comparing-parameters

## Normal distribution

PL: Rozkład normalny

`stats.norm(loc=μ, scale=σ)` is the normal distribution N(μ, σ²): `loc` is its mean and `scale` its standard deviation. About 68% of the probability lies within one σ of the mean, and 95% within 1.96σ.

PL: `stats.norm(loc=μ, scale=σ)` to rozkład normalny (normal distribution) N(μ, σ²): `loc` to jego średnia, a `scale` odchylenie standardowe (standard deviation). Około 68% prawdopodobieństwa leży w odległości do jednego σ od średniej, a 95% do 1,96σ.

```python
from scipy import stats

iq = stats.norm(loc=100, scale=15)
print(iq.mean(), iq.std())
print(f"{iq.cdf(115) - iq.cdf(85):.4f}")
print(f"{iq.sf(130):.4f}")
```

### Pitfall

`scale` is the standard deviation, not the variance: `stats.norm(loc=0, scale=4)` written for a variance of 4 has a variance of 16. Write `scale=2`, or `scale=np.sqrt(var)`.

PL: `scale` to odchylenie standardowe, a nie wariancja (variance): `stats.norm(loc=0, scale=4)` napisane dla wariancji 4 ma wariancję 16. Napisz `scale=2` albo `scale=np.sqrt(var)`.

```python
from scipy import stats

var = 4
d = stats.norm(loc=0, scale=var)
print(d.std(), d.var())
```

### See also

- random/normal-samples
- plotting-distributions/a-pdf-curve

## Uniform distribution

PL: Rozkład jednostajny

U(a, b) is `stats.uniform(loc=a, scale=b - a)`: `loc` is the lower end and `scale` the width of the interval, not its upper end. The density is 1/(b − a) between `a` and `b`, and 0 outside.

PL: U(a, b) to `stats.uniform(loc=a, scale=b - a)`: `loc` to dolny koniec, a `scale` szerokość przedziału, a nie jego górny koniec. Gęstość rozkładu jednostajnego (uniform distribution) wynosi 1/(b − a) między `a` i `b` oraz 0 poza nimi.

```python
from scipy import stats

a, b = 2, 5
U = stats.uniform(loc=a, scale=b - a)
print(U.ppf(0), U.ppf(1))
print(f"{U.pdf(3):.4f}")
print(U.pdf(6))
print(U.mean(), U.cdf(4.25))
```

### Pitfall

`stats.uniform(2, 5)` is U(2, 7), not U(2, 5): the second number is the width `scale`, not the upper end.

PL: `stats.uniform(2, 5)` to U(2, 7), a nie U(2, 5): druga liczba to szerokość `scale`, a nie górny koniec.

```python
from scipy import stats

U = stats.uniform(2, 5)
print(U.ppf(0), U.ppf(1))
```

### See also

- random/uniform-numbers-and-integers

## Exponential distribution

PL: Rozkład wykładniczy

An exponential distribution with rate λ is `stats.expon(scale=1/λ)`. SciPy wants the scale, which is the mean 1/λ, not the rate λ: with 2 events an hour, the wait in hours is `stats.expon(scale=1/2)`, half an hour on average.

PL: Rozkład wykładniczy (exponential distribution) z intensywnością (rate) λ to `stats.expon(scale=1/λ)`. SciPy chce skali, czyli średniej 1/λ, a nie intensywności λ: przy 2 zdarzeniach na godzinę czas oczekiwania w godzinach to `stats.expon(scale=1/2)`, średnio pół godziny.

```python
from scipy import stats

lam = 2
wait = stats.expon(scale=1 / lam)
print(wait.mean(), wait.std())
print(f"{wait.cdf(0.5):.4f}")
print(f"{wait.sf(1):.4f}")
```

## Student's t distribution

PL: Rozkład t Studenta

`stats.t(df)` is Student's t distribution with `df` degrees of freedom, the one t-tests use. It is bell-shaped like N(0, 1) but has heavier tails, so its critical values are larger, and it comes closer to the normal as `df` grows.

PL: `stats.t(df)` to rozkład t Studenta (Student's t distribution) z `df` stopniami swobody (degrees of freedom), ten, którego używają testy t. Ma kształt dzwonu jak N(0, 1), ale cięższe ogony (heavier tails), więc jego wartości krytyczne są większe, i zbliża się do rozkładu normalnego, gdy `df` rośnie.

```python
from scipy import stats

for df in [2, 10, 30, 1000]:
    t = stats.t(df)
    print(df, f"{t.ppf(0.975):.3f}")

z = stats.norm()
print("z", f"{z.ppf(0.975):.3f}")
```

### See also

- distributions/quantiles-with-ppf

## Chi-squared distribution

PL: Rozkład chi-kwadrat

`stats.chi2(df)` is the chi-squared distribution with `df` degrees of freedom, the distribution of a sum of `df` squared N(0, 1) values. It takes only values from 0 up, is skewed to the right, and has mean `df` and variance `2 * df`.

PL: `stats.chi2(df)` to rozkład chi-kwadrat (chi-squared distribution) z `df` stopniami swobody (degrees of freedom), czyli rozkład sumy `df` kwadratów wartości z N(0, 1). Przyjmuje tylko wartości od 0 w górę, jest prawostronnie skośny (right-skewed) i ma średnią `df` oraz wariancję `2 * df`.

```python
from scipy import stats

c = stats.chi2(4)
print(c.mean(), c.var())
print(f"{c.ppf(0.95):.3f}")
print(f"{c.sf(10):.4f}")
```

### See also

- plotting-distributions/comparing-parameters
