---
title: Plotting basics
glyph: "/\\"
summary: Line and bar charts.
pl:
  title: Podstawy wykresów
  summary: Wykresy liniowe i słupkowe.
---

## Shown and open figures

PL: Pokazane i otwarte wykresy

`plt.show()` shows the figures drawn so far; a figure still open at the end is shown too.

PL: `plt.show()` pokazuje dotąd narysowane wykresy; wykres otwarty na końcu też jest pokazany.

```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3], [1, 4, 9])
plt.show()

fig, ax = plt.subplots()
ax.bar(["a", "b"], [3, 5])
print("two figures")
```

### Figure

A line rising ever faster through three points, then two bars, the second taller.

PL: Linia rosnąca coraz szybciej przez trzy punkty, potem dwa słupki, drugi wyższy.

## Closed figures

PL: Zamknięte wykresy

A figure closed with `plt.close()` is not shown.

PL: Wykres zamknięty przez `plt.close()` nie jest pokazany.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2])
plt.close(fig)
print("no figure")
```

### Pitfall

A figure drawn before an error is still shown.

PL: Wykres narysowany przed błędem i tak jest pokazany.

```python raises=ValueError
import matplotlib.pyplot as plt

plt.plot([1, 2], [1, 4])
print(int("two"))
```

### Figure

A straight line rising between two points.

PL: Prosta linia rosnąca między dwoma punktami.
