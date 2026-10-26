---
title: Plotting distributions
glyph: "f(x)"
summary: "Drawing distributions with Matplotlib: a pdf curve, a histogram with the pdf, a pmf as bars, the cdf, comparing parameters."
pl:
  title: Wykresy rozkładów
  summary: "Wykresy rozkładów (distributions) w Matplotlib: krzywa gęstości, histogram z gęstością, funkcja prawdopodobieństwa jako słupki, dystrybuanta, porównanie parametrów."
---

## A pdf curve

PL: Krzywa gęstości

Plot a pdf on a grid of `x` values that you choose: `x = np.linspace(d.ppf(0.001), d.ppf(0.999), 200)` gives 200 evenly spaced, sorted points that cover all but 0.2% of the distribution, and `plt.plot(x, d.pdf(x))` joins them into a smooth curve. Here the x-axis shows heights and the y-axis their density.

PL: Gęstość (pdf) rysuj na wybranej przez ciebie siatce wartości `x`: `x = np.linspace(d.ppf(0.001), d.ppf(0.999), 200)` daje 200 równo rozmieszczonych, posortowanych punktów, które obejmują cały rozkład poza 0,2%, a `plt.plot(x, d.pdf(x))` łączy je w gładką krzywą. Tu oś x pokazuje wzrost, a oś y jego gęstość.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

d = stats.norm(loc=170, scale=8)
x = np.linspace(d.ppf(0.001),
                d.ppf(0.999), 200)
plt.figure(figsize=(6, 3.5))
plt.plot(x, d.pdf(x))
plt.show()
```

### Figure

A smooth bell curve from about 145 to 195, peaking at 170 at a height of about 0.05.

PL: Gładka krzywa w kształcie dzwonu od około 145 do 195, ze szczytem przy 170 na wysokości około 0,05.

### See also

- plotting-basics/a-line-plot
- arrays/ranges

## A histogram with the pdf

PL: Histogram z gęstością

Draw the sample with `plt.hist(sample, density=True)` and the pdf over it on a `linspace` grid. `density=True` scales the bars so their total area is 1, the same scale as the pdf; without it the bars show counts and the curve lies flat along the bottom.

PL: Narysuj próbkę przez `plt.hist(sample, density=True)`, a na niej gęstość (pdf) na siatce z `linspace`. `density=True` skaluje słupki tak, by ich łączne pole wynosiło 1, czyli do skali gęstości; bez niego słupki pokazują liczebności, a krzywa leży płasko przy dolnej krawędzi.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(12)
d = stats.norm(loc=170, scale=8)
sample = d.rvs(size=500, random_state=rng)
x = np.linspace(d.ppf(0.001),
                d.ppf(0.999), 200)
plt.figure(figsize=(6, 3.5))
plt.hist(sample, bins=25, density=True)
plt.plot(x, d.pdf(x))
plt.show()
```

### Figure

Twenty-five bars in a rough bell shape around 170, from about 147 to 192, with a smooth bell curve drawn over them that follows their tops, peaking near 0.05.

PL: Dwadzieścia pięć słupków układa się w nierówny dzwon wokół 170, od około 147 do 192, a nałożona na nie gładka krzywa dzwonowa biegnie po ich wierzchołkach, ze szczytem blisko 0,05.

### Pitfall

`plt.plot(sample, d.pdf(sample))` uses the random, unsorted sample as `x`, so the line jumps back and forth between the points and scribbles a zigzag mess over the histogram. Plot the pdf on a sorted `linspace` grid instead.

PL: `plt.plot(sample, d.pdf(sample))` używa losowej, nieposortowanej próbki jako `x`, więc linia skacze tam i z powrotem między punktami i zamazuje histogram zygzakami. Zamiast tego rysuj gęstość na posortowanej siatce z `linspace`.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(12)
d = stats.norm(loc=170, scale=8)
sample = d.rvs(size=500,
               random_state=rng)
plt.figure(figsize=(6, 3.5))
plt.hist(sample, bins=25,
         density=True)
plt.plot(sample, d.pdf(sample))
plt.show()
```

### Figure

The same histogram covered by a tangle of straight lines that zigzag back and forth between points on the bell curve, filling the whole area under it.

PL: Ten sam histogram przykryty plątaniną prostych linii, które zygzakiem skaczą tam i z powrotem między punktami krzywej dzwonowej i wypełniają cały obszar pod nią.

### See also

- histograms/density-with-a-pdf-on-top
- distributions/random-samples-with-rvs

## A pmf as bars

PL: Funkcja prawdopodobieństwa jako słupki

For a discrete distribution put one bar at each whole number: `k = np.arange(0, 11)` and `plt.bar(k, d.pmf(k))`. Beside them, `np.bincount(sample, minlength=11) / n` gives a sample's relative frequencies; here B(10, 0.3) and 200 draws from it.

PL: Funkcję prawdopodobieństwa (pmf) rozkładu dyskretnego rysuj jako słupki, po jednym na każdą liczbę całkowitą: `k = np.arange(0, 11)` i `plt.bar(k, d.pmf(k))`. Obok nich `np.bincount(sample, minlength=11) / n` daje częstości względne (relative frequencies) próbki; tu B(10, 0.3) i 200 losowań z niego.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(3)
d = stats.binom(10, 0.3)
n = 200
sample = d.rvs(size=n, random_state=rng)
freq = np.bincount(sample, minlength=11)
k = np.arange(0, 11)
plt.figure(figsize=(6, 3.5))
plt.bar(k - 0.2, d.pmf(k), width=0.4,
        label="P(X = k)")
plt.bar(k + 0.2, freq / n, width=0.4,
        label="n = 200")
plt.xticks(k)
plt.legend()
plt.show()
```

### Figure

Pairs of bars for k = 0 to 10 with a legend, P(X = k) and n = 200: both rise to the tallest pair at 3, about 0.27 and 0.29, then fall to almost nothing from 7 up, and each sample bar stays close to its partner.

PL: Pary słupków dla k od 0 do 10 z legendą P(X = k) i n = 200: obie serie rosną do najwyższej pary przy 3, około 0,27 i 0,29, a od 7 w górę spadają prawie do zera, przy czym każdy słupek próbki jest bliski swojej parze.

### See also

- bar-charts/a-probability-mass-function
- discrete-distributions/binomial-distribution

## The cdf

PL: Dystrybuanta

A continuous cdf is a smooth curve, `plt.plot(x, z.cdf(x))`. A discrete one jumps at each whole number and is flat in between, so draw it with `plt.step(k, coin.cdf(k), where="post")`, which holds each value until the next `k`.

PL: Dystrybuanta (cdf) rozkładu ciągłego to gładka krzywa, `plt.plot(x, z.cdf(x))`. Dystrybuanta rozkładu dyskretnego skacze przy każdej liczbie całkowitej i jest płaska pomiędzy nimi, więc rysuj ją przez `plt.step(k, coin.cdf(k), where="post")`, które trzyma każdą wartość aż do następnego `k`.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

z = stats.norm()
x = np.linspace(-3, 3, 200)
coin = stats.binom(10, 0.5)
k = np.arange(0, 11)
plt.figure(figsize=(6, 3.5))
plt.subplot(121)
plt.plot(x, z.cdf(x))
plt.title("N(0, 1)")
plt.subplot(122)
plt.step(k, coin.cdf(k), where="post")
plt.xticks(range(0, 11, 2))
plt.title("B(10, 0.5)")
plt.show()
```

### Figure

Two plots side by side: on the left, N(0, 1), a smooth S-shaped curve rising from 0 to 1 between −3 and 3; on the right, B(10, 0.5), a staircase rising from 0 to 1 over 0 to 10, with the biggest steps around 5.

PL: Dwa wykresy obok siebie: po lewej N(0, 1), gładka krzywa w kształcie litery S rosnąca od 0 do 1 między −3 a 3; po prawej B(10, 0.5), schodki rosnące od 0 do 1 na odcinku od 0 do 10, z największymi stopniami wokół 5.

### See also

- subplots/side-by-side-plots-with-plt-subplot-121
- distributions/density-and-probabilities

## Comparing parameters

PL: Porównanie parametrów

Loop over the parameter values and draw one pdf curve for each on the same `x` grid, with a `label` such as `f"df = {df}"` for `plt.legend()`. Here the chi-squared distribution with 2, 4 and 8 degrees of freedom: the larger `df`, the further right and the flatter the curve.

PL: Przejdź pętlą po wartościach parametru i dla każdej narysuj krzywą gęstości (pdf) na tej samej siatce `x`, z etykietą `label`, np. `f"df = {df}"`, dla `plt.legend()`. Tu rozkład chi-kwadrat z 2, 4 i 8 stopniami swobody (degrees of freedom): im większe `df`, tym krzywa leży dalej w prawo i jest bardziej płaska.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

x = np.linspace(0, 20, 200)
plt.figure(figsize=(6, 3.5))
for df in [2, 4, 8]:
    d = stats.chi2(df)
    plt.plot(x, d.pdf(x),
             label=f"df = {df}")

plt.legend()
plt.show()
```

### Figure

Three curves for x from 0 to 20 with a legend, df = 2, df = 4 and df = 8: the df = 2 curve falls from 0.5 at 0, df = 4 peaks near 2 at about 0.18, and df = 8 peaks near 6 at about 0.11, with a long tail to the right.

PL: Trzy krzywe dla x od 0 do 20 z legendą df = 2, df = 4 i df = 8: krzywa df = 2 opada od 0,5 przy 0, df = 4 ma szczyt blisko 2 na wysokości około 0,18, a df = 8 ma szczyt blisko 6 na wysokości około 0,11 i długi ogon w prawo.

### See also

- plotting-basics/several-lines-and-a-legend
- continuous-distributions/chi-squared-distribution
