---
title: Saving and loading
glyph: ".npy"
summary: "Arrays in files: text and CSV with savetxt, loadtxt and genfromtxt, binary .npy and .npz files."
pl:
  title: Zapis i odczyt
  summary: "Tablice (arrays) w plikach: tekst i CSV przez savetxt, loadtxt i genfromtxt, binarne pliki .npy i .npz."
---

## Text files with savetxt and loadtxt

PL: Pliki tekstowe z savetxt i loadtxt

`np.savetxt("data.txt", a, fmt="%.2f")` writes an array as text, one row per line with spaces between the values, or one value per line for a 1-D array; `fmt` sets how each number is written. `np.loadtxt("data.txt")` reads it back as an array of floats.

PL: `np.savetxt("data.txt", a, fmt="%.2f")` zapisuje tablicę (array) jako tekst, jeden wiersz w linii z wartościami rozdzielonymi spacjami, a dla tablicy 1-D jedną wartość w linii; `fmt` ustala, jak zapisać każdą liczbę. `np.loadtxt("data.txt")` odczytuje ją z powrotem jako tablicę liczb zmiennoprzecinkowych (floats).

```python
import numpy as np

a = np.array([[1.5, 2.0],
              [3.25, 4.0]])
np.savetxt("data.txt", a, fmt="%.2f")
with open("data.txt", encoding="utf-8") as f:
    print(f.read())

print(np.loadtxt("data.txt"))
```

### See also

- files/reading-numbers-from-a-file
- arrays/two-dimensional-arrays

## CSV files

PL: Pliki CSV

`scores.csv` starts with the header `name,math,physics`, then one row per student: `delimiter=","` splits at the commas, `skiprows=1` skips the header and `usecols=(1, 2)` keeps the numeric columns. Pass `encoding="utf-8"` as you do to `open`, or on Windows a header with Polish letters raises `UnicodeDecodeError`.

PL: Plik (file) `scores.csv` zaczyna się nagłówkiem `name,math,physics`, a potem ma jeden wiersz na studenta: `delimiter=","` dzieli wiersze przy przecinkach, `skiprows=1` pomija nagłówek, a `usecols=(1, 2)` zostawia kolumny z liczbami. Podaj kodowanie (encoding) `encoding="utf-8"` tak jak przy `open`, bo inaczej w Windowsie nagłówek z polskimi literami zgłasza `UnicodeDecodeError`.

```python
with open("scores.csv", "w", encoding="utf-8") as f: f.write("name,math,physics\nAla,72,65\nJan,85,90\nEwa,90,78\n")  #| hide
import numpy as np

data = np.loadtxt(
    "scores.csv", delimiter=",",
    skiprows=1, usecols=(1, 2),
    encoding="utf-8")
print(data)
print(data.mean(axis=0).round(1))
```

### See also

- files/csv-files-with-the-csv-module
- aggregates/along-an-axis
- csv-files/reading-a-csv-file

## Columns as separate arrays

PL: Kolumny jako osobne tablice

`unpack=True` returns each column as its own array, so `x, y = np.loadtxt(...)` names them in one line, ready for `plt.scatter(x, y)`. Here `study.csv` has the header `hours,score` and four rows.

PL: `unpack=True` zwraca każdą kolumnę jako osobną tablicę (array), więc `x, y = np.loadtxt(...)` nazywa je w jednej linii, gotowe do `plt.scatter(x, y)`. Tutaj `study.csv` ma nagłówek `hours,score` i cztery wiersze.

```python
with open("study.csv", "w", encoding="utf-8") as f: f.write("hours,score\n1,52\n2,60\n3,71\n4,75\n")  #| hide
import numpy as np

x, y = np.loadtxt(
    "study.csv", delimiter=",",
    skiprows=1, unpack=True,
    encoding="utf-8")
print(x)
print(y)
```

### See also

- tuples/unpacking
- scatter-plots/a-scatter-plot

## Missing values with genfromtxt

PL: Brakujące wartości z genfromtxt

`np.genfromtxt` reads a file as `np.loadtxt` does, but turns empty fields into `nan`; it skips a header with `skip_header=1`. A mean over `nan` is `nan`, so use `np.nanmean`. Here `temps.csv` has the header `day,temp`, and day 2 has no temperature.

PL: `np.genfromtxt` czyta plik (file) tak jak `np.loadtxt`, ale puste pola zamienia na `nan`; nagłówek pomija przez `skip_header=1`. Średnia z `nan` to `nan`, więc użyj `np.nanmean`. Tutaj `temps.csv` ma nagłówek `day,temp`, a dzień 2 nie ma temperatury.

```python
with open("temps.csv", "w", encoding="utf-8") as f: f.write("day,temp\n1,12.5\n2,\n3,14.0\n")  #| hide
import numpy as np

t = np.genfromtxt(
    "temps.csv", delimiter=",",
    skip_header=1, usecols=1,
    encoding="utf-8")
print(t)
print(t.mean(), np.nanmean(t))
```

### Pitfall

`np.loadtxt` can't read an empty field, so on the same file it raises `ValueError`.

PL: `np.loadtxt` nie potrafi odczytać pustego pola, więc na tym samym pliku zgłasza `ValueError`.

```python raises=ValueError
with open("temps.csv", "w", encoding="utf-8") as f: f.write("day,temp\n1,12.5\n2,\n3,14.0\n")  #| hide
import numpy as np

t = np.loadtxt(
    "temps.csv", delimiter=",",
    skiprows=1, usecols=1,
    encoding="utf-8")
```

### See also

- indexing/changing-values-through-a-mask

## Binary files with save and load

PL: Pliki binarne z save i load

`np.save("a.npy", a)` writes an array to a binary `.npy` file, adding `.npy` to the name itself if it's missing, and `np.load("a.npy")` reads it back. Unlike a text file, it keeps the exact values and the dtype, and it is fast for large arrays.

PL: `np.save("a.npy", a)` zapisuje tablicę (array) do binarnego pliku `.npy`, sam dodając `.npy` do nazwy, jeśli go brakuje, a `np.load("a.npy")` odczytuje ją z powrotem. W przeciwieństwie do pliku tekstowego zachowuje dokładne wartości i typ danych (dtype) oraz działa szybko dla dużych tablic.

```python
import numpy as np

a = np.array([1/3, 2/3, 1.0])
np.save("a.npy", a)
b = np.load("a.npy")
print(b)
print(b.dtype, (b == a).all())
```

### See also

- arrays/shape-and-dtype

## Several arrays in an npz file

PL: Kilka tablic w pliku npz

`np.savez("data.npz", x=x, y=y)` saves several arrays in one file, each under its name. `d = np.load("data.npz")` opens it: `d.files` lists the names and `d["x"]` gives one array. For large arrays `np.savez_compressed` makes a smaller file.

PL: `np.savez("data.npz", x=x, y=y)` zapisuje kilka tablic (arrays) w jednym pliku, każdą pod jej nazwą. `d = np.load("data.npz")` go otwiera: `d.files` wypisuje nazwy, a `d["x"]` daje jedną tablicę. Dla dużych tablic `np.savez_compressed` tworzy mniejszy plik.

```python
import numpy as np

x = np.array([1, 2, 3])
y = np.array([2.1, 3.9, 6.2])
np.savez("data.npz", x=x, y=y)
d = np.load("data.npz")
print(d.files)
print(d["x"], d["y"])
```
