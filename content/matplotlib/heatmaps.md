---
title: Heatmaps
glyph: "cmap"
summary: "A matrix drawn as coloured cells: imshow with a colour bar, row and column labels, colour maps and limits, values in the cells, a 2D histogram of points."
pl:
  title: Mapy ciepła
  summary: "Mapy ciepła (heatmaps), czyli macierz jako kolorowe komórki: imshow z paskiem kolorów, etykiety wierszy i kolumn, mapy kolorów i zakresy, wartości w komórkach, dwuwymiarowy histogram punktów."
---

## A matrix as a heatmap

PL: Macierz jako mapa ciepła

`plt.imshow(m)` draws a two-dimensional array as a grid of coloured cells, one per value, with row 0 at the top. `plt.colorbar()` shows which colour stands for which value. Here the rows are 5 students and the columns 8 test scores.

PL: `plt.imshow(m)` rysuje tablicę dwuwymiarową jako mapę ciepła (heatmap): siatkę kolorowych komórek, po jednej na wartość, z wierszem 0 na górze. `plt.colorbar()` pokazuje, który kolor oznacza jaką wartość. Tu wiersze to 5 studentów, a kolumny to 8 wyników testów.

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(13)  #| show: rng = np.random.default_rng()
scores = rng.integers(40, 101, (5, 8))
plt.figure(figsize=(6, 3.5))
plt.imshow(scores)
plt.colorbar()
plt.show()
```

### Figure

A grid of 5 rows and 8 columns of coloured squares, from dark purple for about 40 to yellow for 100, with no clear pattern, and a colour bar beside it.

PL: Siatka 5 wierszy i 8 kolumn kolorowych kwadratów, od ciemnofioletowych dla około 40 do żółtych dla 100, bez wyraźnego wzoru, z paskiem kolorów obok.

### See also

- arrays/two-dimensional-arrays

## Labelling rows and columns

PL: Etykiety wierszy i kolumn

The cells sit at positions 0, 1, 2, … on both axes, so `plt.xticks(range(n), labels)` names the columns and `plt.yticks(range(m), labels)` the rows. Here the columns are the grades 2 to 5 and the rows the groups A, B and C, with how many students got each grade.

PL: Komórki leżą w pozycjach 0, 1, 2, … na obu osiach, więc `plt.xticks(range(n), labels)` nazywa kolumny, a `plt.yticks(range(m), labels)` wiersze, przez etykiety znaczników osi (ticks). Tu kolumny to oceny od 2 do 5, a wiersze to grupy A, B i C, z liczbą studentów, którzy dostali każdą ocenę.

```python
import numpy as np
import matplotlib.pyplot as plt

counts = np.array([[3, 8, 10, 4],
                   [6, 9, 7, 3],
                   [1, 5, 12, 7]])
plt.figure(figsize=(6, 3.5))
plt.imshow(counts)
plt.xticks(range(4), ["2", "3", "4", "5"])
plt.yticks(range(3), ["A", "B", "C"])
plt.colorbar()
plt.show()
```

### Figure

A grid of 3 rows labelled A, B and C and 4 columns labelled 2 to 5, with a colour bar; the brightest cell is row C, column 4, and row C, column 2 is the darkest.

PL: Siatka 3 wierszy opisanych A, B i C i 4 kolumn opisanych od 2 do 5, z paskiem kolorów; najjaśniejsza komórka to wiersz C, kolumna 4, a najciemniejsza to wiersz C, kolumna 2.

## Colour maps and fixed limits

PL: Mapy kolorów i stałe zakresy

`cmap="coolwarm"` picks the colour map, and `vmin=` and `vmax=` fix the values at its two ends instead of the data's own minimum and maximum. For a correlation matrix from `np.corrcoef`, `vmin=-1, vmax=1` puts 0 at the neutral middle colour.

PL: `cmap="coolwarm"` wybiera mapę kolorów (colormap), a `vmin=` i `vmax=` ustalają wartości na jej dwóch końcach zamiast minimum i maksimum danych. Dla macierzy korelacji (correlation matrix) z `np.corrcoef` `vmin=-1, vmax=1` stawia 0 w neutralnym środkowym kolorze.

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(14)  #| show: rng = np.random.default_rng()
x = rng.normal(0, 1, 200)
y = x + rng.normal(0, 1, 200)
z = -x + rng.normal(0, 0.5, 200)
r = np.corrcoef([x, y, z])
plt.figure(figsize=(6, 3.5))
plt.imshow(r, cmap="coolwarm",
           vmin=-1, vmax=1)
plt.xticks(range(3), ["x", "y", "z"])
plt.yticks(range(3), ["x", "y", "z"])
plt.colorbar()
plt.show()
```

### Figure

A 3 by 3 grid for x, y and z with a colour bar from −1 in blue to 1 in red: the diagonal is dark red, x and y are light red, and z against x and y is blue.

PL: Siatka 3 na 3 dla x, y i z z paskiem kolorów od −1 na niebiesko do 1 na czerwono: przekątna jest ciemnoczerwona, x z y jasnoczerwone, a z z x i y niebieskie.

## Values in the cells

PL: Wartości w komórkach

`plt.text(j, i, value)` writes text at column `j` and row `i`: the column comes first, because it is the x position. Loop over the cells, and keep the text readable with a light colour map, here `"Blues"` with `vmax` above the largest count.

PL: `plt.text(j, i, value)` wypisuje tekst w kolumnie `j` i wierszu `i`: kolumna jest pierwsza, bo to pozycja x. Przejdź pętlą po komórkach i zadbaj o czytelny tekst jasną mapą kolorów (colormap), tu `"Blues"` z `vmax` powyżej największej liczebności.

```python
import numpy as np
import matplotlib.pyplot as plt

counts = np.array([[3, 8, 10, 4],
                   [6, 9, 7, 3],
                   [1, 5, 12, 7]])
plt.figure(figsize=(6, 3.5))
plt.imshow(counts, cmap="Blues", vmax=20)
plt.xticks(range(4), ["2", "3", "4", "5"])
plt.yticks(range(3), ["A", "B", "C"])
for i in range(3):
    for j in range(4):
        plt.text(j, i, counts[i, j],
                 ha="center", va="center")

plt.show()
```

### Figure

The grid of grades 2 to 5 by groups A, B and C in shades of blue, each cell showing its count in the middle; the darkest cell holds 12 and the lightest 1.

PL: Siatka ocen od 2 do 5 dla grup A, B i C w odcieniach niebieskiego, każda komórka z liczebnością pośrodku; najciemniejsza komórka ma 12, a najjaśniejsza 1.

### See also

- indexing/rows-and-columns
- loops/range

## A 2D histogram of points

PL: Dwuwymiarowy histogram punktów

`plt.hist2d(x, y, bins=40)` splits the plane into a 40 by 40 grid, counts the points in each square and colours the square by its count, with `plt.colorbar()` giving the counts. It shows where points crowd together when a scatter plot of thousands of them is one solid blot. Unlike `plt.imshow`, the axes show the values of `x` and `y`, with `y` growing upwards. `rasterized=True` stores the grid as one picture in a vector file such as SVG or PDF, so the file stays small and no thin seams show between the squares.

PL: `plt.hist2d(x, y, bins=40)` dzieli płaszczyznę na siatkę 40 na 40, liczy punkty w każdym kwadracie i koloruje go według tej liczby, a `plt.colorbar()` podaje liczebności. Taki histogram dwuwymiarowy (2D histogram) pokazuje, gdzie punkty się skupiają, gdy wykres punktowy tysięcy punktów jest jedną plamą. Inaczej niż w `plt.imshow` osie pokazują wartości `x` i `y`, a `y` rośnie w górę. `rasterized=True` zapisuje siatkę jako jeden obrazek w pliku wektorowym, takim jak SVG czy PDF, więc plik pozostaje mały, a między kwadratami nie widać cienkich szczelin.

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(18)  #| show: rng = np.random.default_rng()
x = rng.normal(10, 2, 20000)
y = x + rng.normal(0, 1.5, 20000)
plt.figure(figsize=(6, 3.5))
plt.hist2d(x, y, bins=40,
           rasterized=True)
plt.colorbar()
plt.show()
```

### Figure

A dark purple rectangle with a bright oval blob tilted from lower left to upper right, yellow at its centre near x = 10, y = 10 and fading to purple at its edges, with a colour bar of counts.

PL: Ciemnofioletowy prostokąt z jasną owalną plamą nachyloną od lewego dołu do prawej góry, żółtą w środku przy x = 10, y = 10 i przechodzącą w fiolet na brzegach, z paskiem kolorów pokazującym liczebności.

### See also

- scatter-plots/a-scatter-plot
- histograms/a-histogram
