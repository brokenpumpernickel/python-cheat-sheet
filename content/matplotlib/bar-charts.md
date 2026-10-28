---
title: Bar charts
glyph: "bar"
summary: "One bar per value or group: counts, a probability mass function, means with error bars."
pl:
  title: Wykresy słupkowe
  summary: "Wykresy słupkowe (bar charts): jeden słupek na wartość lub grupę — liczebności, funkcja prawdopodobieństwa, średnie ze słupkami błędów."
---

## Bar chart of counts

PL: Wykres słupkowy liczebności

`plt.bar(x, heights)` draws one bar per value of `x`, which may be numbers or strings. `np.unique(data, return_counts=True)` gives each distinct value and how often it appears, ready to plot. Here the x-axis shows the faces of a die and the y-axis how often each came up in 60 rolls.

PL: `plt.bar(x, heights)` rysuje wykres słupkowy (bar chart): jeden słupek na każdą wartość `x`, a mogą to być liczby lub napisy. `np.unique(data, return_counts=True)` daje każdą różną wartość i liczbę jej wystąpień, gotowe do wykresu. Tu oś x pokazuje oczka kostki, a oś y, ile razy każde wypadło w 60 rzutach.

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(8)  #| show: rng = np.random.default_rng()
rolls = rng.integers(1, 7, 60)
faces, counts = np.unique(
    rolls, return_counts=True)
plt.figure(figsize=(6, 3.5))
plt.bar(faces, counts)
plt.show()
```

### Figure

Six bars for the faces 1 to 6 of uneven height, from 6 for face 5 to 17 for face 3.

PL: Sześć słupków dla oczek od 1 do 6 o nierównej wysokości, od 6 dla oczka 5 do 17 dla oczka 3.

### See also

- collections/counting-with-counter

## A probability mass function

PL: Funkcja prawdopodobieństwa

A probability mass function gives each value of a discrete variable its probability, so the bars add up to 1. Here the heights are the share of 10 000 simulated rolls of two dice that gave each sum, and `plt.xticks(values)` puts a tick under every bar.

PL: Funkcja prawdopodobieństwa (probability mass function) przypisuje każdej wartości zmiennej dyskretnej jej prawdopodobieństwo, więc słupki sumują się do 1. Tu wysokości to odsetek z 10 000 symulowanych rzutów dwiema kostkami, które dały daną sumę, a `plt.xticks(values)` stawia znacznik osi (tick) pod każdym słupkiem.

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(9)  #| show: rng = np.random.default_rng()
rolls = rng.integers(1, 7, (10_000, 2))
sums = rolls.sum(axis=1)
values, counts = np.unique(
    sums, return_counts=True)
plt.figure(figsize=(6, 3.5))
plt.bar(values, counts / len(sums))
plt.xticks(values)
plt.show()
```

### Figure

Eleven bars for the sums 2 to 12 forming a triangle: rising evenly to the tallest bar at 7, about 0.16, then falling evenly.

PL: Jedenaście słupków dla sum od 2 do 12 układa się w trójkąt: równo rosną do najwyższego słupka przy 7, około 0,16, a potem równo maleją.

### See also

- random/simulating-an-experiment
- plotting-distributions/a-pmf-as-bars

## Means with error bars

PL: Średnie ze słupkami błędów

`yerr=` adds an error bar to each bar, and `capsize=4` gives it short caps. A common choice is the standard error of the mean, the standard deviation over `np.sqrt(n)`; here three groups of 20 measurements are the columns of `data`.

PL: `yerr=` dodaje do każdego słupka słupek błędu (error bar), a `capsize=4` daje mu krótkie poprzeczki. Często jest to błąd standardowy średniej (standard error of the mean), czyli odchylenie standardowe podzielone przez `np.sqrt(n)`; tu trzy grupy po 20 pomiarów to kolumny `data`.

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(10)  #| show: rng = np.random.default_rng()
data = rng.normal([5, 6, 4], 1.5, (20, 3))
means = data.mean(axis=0)
sd = data.std(axis=0, ddof=1)
sem = sd / np.sqrt(len(data))
groups = ["A", "B", "C"]
plt.figure(figsize=(6, 3.5))
plt.bar(groups, means, yerr=sem, capsize=4)
plt.show()
```

### Figure

Three bars, A, B and C, each with a short capped error bar on top; A and B are close, at about 5 and 5.5, and C is clearly lower, below 3.5.

PL: Trzy słupki, A, B i C, każdy z krótkim słupkiem błędu z poprzeczkami na górze; A i B są bliskie, około 5 i 5,5, a C jest wyraźnie niższy, poniżej 3,5.

### See also

- aggregates/standard-deviation-and-variance
- aggregates/along-an-axis
