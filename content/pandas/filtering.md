---
title: Filtering
glyph: "mask"
summary: "Keeping the rows that meet a condition: boolean masks, combining conditions, isin, text that contains a word, a column of the matching rows, and counting with a mask."
pl:
  title: Filtrowanie
  summary: "Zostawianie wierszy, które spełniają warunek: maski logiczne (boolean masks), łączenie warunków, isin, tekst zawierający słowo, kolumna pasujących wierszy i zliczanie maską."
---

## A boolean mask

PL: Maska logiczna

`df["score"] > 80` compares every value of the column and gives a Series of `True` and `False`, one per row, and `df[mask]` keeps the rows where the mask is `True`, with their index labels.

PL: `df["score"] > 80` porównuje każdą wartość kolumny i daje serię (Series) wartości `True` i `False`, po jednej na wiersz, czyli maskę logiczną (boolean mask), a `df[mask]` zostawia wiersze, w których maska ma `True`, z ich etykietami (labels) w indeksie.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa",
             "Olek", "Iga"],
    "score": [72, 85, 90, 64, 78],
})
mask = df["score"] > 80
print(mask)
print(df[mask])
```

### See also

- indexing/boolean-masks
- array-maths/comparisons

## Combining conditions

PL: Łączenie warunków

Combine masks row by row with `&` (and), `|` (or) and `~` (not), and put each comparison in parentheses, since `&` and `|` bind tighter than `>` and `==`.

PL: Maski łącz wiersz po wierszu przez `&` (i), `|` (lub) i `~` (nie), a każde porównanie umieść w nawiasach, bo `&` i `|` wiążą mocniej niż `>` i `==`.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa",
             "Olek", "Iga"],
    "group": ["A", "B", "A", "B", "A"],
    "score": [72, 85, 90, 64, 78],
})
in_a = df["group"] == "A"
print(df[in_a & (df["score"] > 75)])
print(df[~in_a | (df["score"] > 85)])
```

### Pitfall

`and`, `or` and `not` need a single `True` or `False`, so between two masks they raise a `ValueError` saying the truth value of a Series is ambiguous.

PL: `and`, `or` i `not` potrzebują jednej wartości `True` lub `False`, więc między dwiema maskami logicznymi (boolean masks) zgłaszają `ValueError` z informacją, że wartość logiczna serii (Series) jest niejednoznaczna.

```python raises=ValueError
import pandas as pd

df = pd.DataFrame({
    "group": ["A", "B", "A", "B", "A"],
    "score": [72, 85, 90, 64, 78],
})
in_a = df["group"] == "A"
high = df["score"] > 75
print(df[in_a and high])
```

### See also

- indexing/boolean-masks
- conditionals/combining-conditions

## isin

PL: isin

`df["group"].isin(["A", "C"])` is `True` for the rows whose value is in the list, which is shorter than joining `==` comparisons with `|`. `~` in front keeps the rows whose value is not in the list.

PL: `df["group"].isin(["A", "C"])` daje `True` dla wierszy, których wartość jest na liście, co jest krótsze niż łączenie porównań `==` przez `|`. `~` na początku zostawia wiersze, których wartości nie ma na liście.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa",
             "Olek", "Iga"],
    "group": ["A", "B", "C", "B", "D"],
})
chosen = df["group"].isin(["A", "C"])
print(df[chosen])
print(df[~chosen])
```

### See also

- sets/set-operations

## Text that contains

PL: Tekst, który zawiera

`df["comment"].str.contains("abduc", case=False)` is `True` for the rows whose text contains `abduc` in any mix of upper and lower case. `na=False` makes a missing comment count as `False`, so `df[mask]` works on a column with gaps in every pandas version.

PL: `df["comment"].str.contains("abduc", case=False)` daje `True` dla wierszy, których tekst zawiera `abduc`, pisane małymi lub wielkimi literami. `na=False` sprawia, że brakujący komentarz liczy się jako `False`, więc `df[mask]` działa na kolumnie z brakującymi wartościami (missing values) w każdej wersji pandas.

```python
import pandas as pd

df = pd.DataFrame({
    "year": [1997, 2004, 2011, 2019],
    "comment": [
        "Bright lights, then ABDUCTED",
        None,
        "Slow silver disk",
        "An abduction?",
    ],
})
mask = df["comment"].str.contains(
    "abduc", case=False, na=False)
print(mask)
print(df[mask])
```

### See also

- strings/cleaning-and-splitting

## A column of the matching rows

PL: Kolumna pasujących wierszy

`df.loc[mask, "name"]` gives only the `name` column of the rows where the mask is `True`, and you can loop over it as over a list. Any column statistic works on it too, such as `.mean()` of the matching scores.

PL: `df.loc[mask, "name"]` daje tylko kolumnę `name` z wierszy, w których maska logiczna (boolean mask) ma `True`, a po tej kolumnie możesz przejść pętlą jak po liście. Działają na niej też statystyki kolumn, np. `.mean()` pasujących wyników.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa",
             "Olek", "Iga"],
    "group": ["A", "B", "A", "B", "A"],
    "score": [72, 85, 90, 64, 78],
})
mask = df["group"] == "A"
for name in df.loc[mask, "name"]:
    print(name)

print(df.loc[mask, "score"].mean())
```

### See also

- selecting/rows-and-columns-by-label-with-loc
- loops/for-over-a-collection
- exploring/column-statistics

## Counting and proportions with a mask

PL: Zliczanie i proporcje z maską

`mask.sum()` counts the rows where the mask is `True`, since `True` counts as 1 and `False` as 0, and `mask.mean()` gives their proportion of all rows.

PL: `mask.sum()` zlicza wiersze, w których maska logiczna (boolean mask) ma `True`, bo `True` liczy się jako 1, a `False` jako 0, a `mask.mean()` daje ich proporcję wśród wszystkich wierszy.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa",
             "Olek", "Iga"],
    "score": [72, 45, 90, 38, 78],
})
passed = df["score"] >= 50
print(passed.sum())
print(passed.mean())
```

### See also

- aggregates/counting-and-proportions-with-a-mask
- array-maths/true-and-false-as-numbers
- exploring/value-counts
