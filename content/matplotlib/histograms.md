---
title: Histograms
glyph: "hist"
summary: "How a sample is spread: counting into bins, choosing bins, logarithmic bins, density with a PDF, comparing two samples."
pl:
  title: Histogramy
  summary: "Histogramy (histograms), czyli rozkład próby: zliczanie w przedziałach, wybór przedziałów, przedziały logarytmiczne, gęstość z krzywą PDF, porównanie dwóch próbek."
---

## A histogram

PL: Histogram

`plt.hist(data)` splits the range of `data` into equal bins and draws one bar per bin, as tall as the number of values that fall in it. Without `bins=` there are 10 bins. Here the x-axis shows 500 heights and the y-axis how many fall in each bin.

PL: `plt.hist(data)` dzieli zakres `data` na równe przedziały (bins) i rysuje jeden słupek na przedział, tak wysoki, ile wartości do niego wpada. Bez `bins=` przedziałów jest 10. Tu oś x pokazuje 500 wzrostów, a oś y, ile z nich wpada do każdego przedziału.

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(7)  #| show: rng = np.random.default_rng()
heights = rng.normal(170, 10, 500)
plt.figure(figsize=(6, 3.5))
plt.hist(heights)
plt.show()
```

### Figure

Ten bars forming a bell shape that peaks around 170, with counts falling away on both sides, from about 140 to 195.

PL: Dziesięć słupków w kształcie dzwonu ze szczytem około 170, z liczebnościami malejącymi w obie strony, od około 140 do 195.

### See also

- random/normal-samples
- heatmaps/a-2d-histogram-of-points

## Choosing bins

PL: Wybór przedziałów

`bins=30` sets the number of bins: too few hide the shape, too many make it noisy. An array of edges sets them exactly, so `np.arange(0, 101, 10)` gives one bin per 10 points; `edgecolor="black"` outlines the bars.

PL: `bins=30` ustala liczbę przedziałów (bins): za mało ukrywa kształt, za dużo daje szum. Tablica granic ustala je dokładnie, więc `np.arange(0, 101, 10)` daje jeden przedział na każde 10 punktów; `edgecolor="black"` obrysowuje słupki.

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(2)  #| show: rng = np.random.default_rng()
scores = rng.normal(65, 12, 200)
edges = np.arange(0, 101, 10)
plt.figure(figsize=(6, 3.5))
plt.hist(scores, bins=edges,
         edgecolor="black")
plt.show()
```

### Figure

Outlined bars, each 10 points wide, on an axis from 0 to 100: the bin from 60 to 70 is the tallest, the bins on either side of it are equal, and the bins below 30 are empty.

PL: Obrysowane słupki, każdy o szerokości 10 punktów, na osi od 0 do 100: najwyższy jest przedział od 60 do 70, przedziały po obu jego stronach są równe, a przedziały poniżej 30 są puste.

### Pitfall

Values outside the edges are left out without any warning: with `bins=np.arange(0, 101, 10)`, a score of 105 is in no bar.

PL: Wartości spoza granic przedziałów są pomijane bez ostrzeżenia: przy `bins=np.arange(0, 101, 10)` wynik 105 nie trafia do żadnego słupka.

### See also

- arrays/ranges

## Logarithmic bins

PL: Przedziały logarytmiczne

Data spread over several powers of 10, such as reaction times or incomes, need bins that widen as the values grow. `np.logspace(-1, 3, 41)` gives 41 edges from 0.1 to 1000 (start and stop are the powers of 10, -1 and 3), and `plt.xscale("log")` spaces the x-axis by powers of 10, so the bars come out equally wide.

PL: Dane rozciągnięte na kilka rzędów wielkości, np. czasy reakcji czy dochody, potrzebują przedziałów (bins), które rosną razem z wartościami. `np.logspace(-1, 3, 41)` daje 41 granic od 0,1 do 1000 (początek i koniec to wykładniki potęg 10, czyli -1 i 3), a `plt.xscale("log")` rysuje oś x w skali logarytmicznej (log scale), więc słupki mają równą szerokość.

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(8)  #| show: rng = np.random.default_rng()
times = rng.lognormal(3, 1, 1000)
edges = np.logspace(-1, 3, 41)
plt.figure(figsize=(6, 3.5))
plt.hist(times, bins=edges,
         edgecolor="black")
plt.xscale("log")
plt.show()
```

### Figure

Outlined bars of equal width on a logarithmic x-axis from 0.1 to 1000, forming a bell shape that peaks around 20; there are no bars below 1.

PL: Obrysowane słupki równej szerokości na logarytmicznej osi x od 0,1 do 1000, układające się w kształt dzwonu ze szczytem około 20; poniżej 1 nie ma słupków.

### Pitfall

With `plt.xscale("log")` but equal-width bins, such as `bins=40`, the first bin swallows most of the data and the rest shrink to slivers on the right. Give the bins with `np.logspace`.

PL: Przy `plt.xscale("log")`, ale przedziałach równej szerokości, np. `bins=40`, pierwszy przedział połyka większość danych, a reszta kurczy się do wąskich pasków po prawej. Podaj przedziały przez `np.logspace`.

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(8)  #| show: rng = np.random.default_rng()
times = rng.lognormal(3, 1, 1000)
plt.figure(figsize=(6, 3.5))
plt.hist(times, bins=40,
         edgecolor="black")
plt.xscale("log")
plt.show()
```

### Figure

On a logarithmic x-axis, one very wide bar from about 1 to 14 holding over 350 values, then ever narrower and shorter bars to the right, down to thin slivers past 100.

PL: Na logarytmicznej osi x jeden bardzo szeroki słupek od około 1 do 14 z ponad 350 wartościami, a dalej w prawo coraz węższe i niższe słupki, aż do cienkich pasków za 100.

### See also

- arrays/ranges

## Density with a PDF on top

PL: Gęstość z krzywą PDF

`density=True` scales the bars so their total area is 1, which puts the histogram on the same scale as a probability density function drawn on top with `plt.plot`. To mark the mean, add `plt.axvline(data.mean())`.

PL: `density=True` skaluje słupki tak, by ich łączne pole wynosiło 1, więc histogram ma tę samą skalę co funkcja gęstości prawdopodobieństwa (PDF, probability density function) narysowana na nim przez `plt.plot`. Średnią zaznaczysz przez `plt.axvline(data.mean())`.

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(4)  #| show: rng = np.random.default_rng()
data = rng.normal(0, 1, 1000)
x = np.linspace(-4, 4, 200)
c = np.sqrt(2 * np.pi)
pdf = np.exp(-x ** 2 / 2) / c
plt.figure(figsize=(6, 3.5))
plt.hist(data, bins=30, density=True)
plt.plot(x, pdf)
plt.show()
```

### Figure

Thirty bars in a bell shape around 0, with the smooth normal curve drawn over them and following their tops closely, peaking near 0.4.

PL: Trzydzieści słupków w kształcie dzwonu wokół 0 i nałożona na nie gładka krzywa normalna, która ściśle biegnie po ich wierzchołkach, ze szczytem blisko 0,4.

### See also

- plotting-basics/horizontal-and-vertical-lines
- array-maths/functions-that-work-on-whole-arrays
- plotting-distributions/a-histogram-with-the-pdf

## Comparing two samples

PL: Porównanie dwóch próbek

`alpha=0.5` makes the bars half transparent, so two histograms on the same axes both stay visible where they overlap. Give both the same bin edges so the bars line up, and a `label` each for `plt.legend()`.

PL: `alpha=0.5` ustawia słupkom przezroczystość (transparency) 50%, więc dwa histogramy na tych samych osiach są widoczne także tam, gdzie się nakładają. Daj obu te same granice przedziałów, żeby słupki się pokrywały, i każdemu `label` dla `plt.legend()`.

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(6)  #| show: rng = np.random.default_rng()
a = rng.normal(0, 1, 500)
b = rng.normal(1, 1, 500)
edges = np.linspace(-4, 5, 37)
plt.figure(figsize=(6, 3.5))
plt.hist(a, bins=edges, alpha=0.5,
         label="μ = 0")
plt.hist(b, bins=edges, alpha=0.5,
         label="μ = 1")
plt.legend()
plt.show()
```

### Figure

Two see-through bell-shaped histograms with a legend, μ = 0 and μ = 1; the second is the same shape shifted one unit to the right, and they overlap in the middle.

PL: Dwa półprzezroczyste histogramy w kształcie dzwonu z legendą μ = 0 i μ = 1; drugi ma ten sam kształt przesunięty o jedną jednostkę w prawo, a w środku się nakładają.
