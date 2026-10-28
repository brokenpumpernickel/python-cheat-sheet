---
title: Missing values
glyph: "NaN"
summary: "Gaps in a table: finding and counting NaN, statistics that skip it, dropping rows and filling gaps."
pl:
  title: Brakujące wartości
  summary: "Brakujące wartości (missing values) w ramce danych: znajdowanie i zliczanie NaN, statystyki, które je pomijają, usuwanie wierszy i uzupełnianie braków."
---

## Finding missing values

PL: Znajdowanie brakujących wartości

pandas shows a missing value as `NaN`: write it as `np.nan` or `None` when you build a table, and `pd.read_csv` reads an empty field as `NaN` too. `df.isna()` marks each cell `True` or `False`, and `df.isna().sum()` counts the gaps in each column, since `True` counts as 1.

PL: pandas pokazuje brakującą wartość (missing value) jako `NaN`: przy tworzeniu tabeli zapisz ją jako `np.nan` lub `None`, a `pd.read_csv` też wczytuje puste pole jako `NaN`. `df.isna()` oznacza każdą komórkę jako `True` albo `False`, a `df.isna().sum()` zlicza braki w każdej kolumnie, bo `True` liczy się jako 1.

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", None, "Olek"],
    "score": [72, np.nan, 90, np.nan],
})
print(df)
print(df.isna())
print(df.isna().sum())
```

### See also

- exploring/info
- array-files/missing-values-with-genfromtxt
- array-maths/true-and-false-as-numbers

## Statistics skip NaN

PL: Statystyki pomijają NaN

`.mean()`, `.sum()`, `.std()` and the other column statistics skip `NaN`, so here the mean is over the 3 known scores; NumPy's `a.mean()` would give `nan`. `.count()` counts the values that aren't missing, while `len(df)` counts every row.

PL: `.mean()`, `.sum()`, `.std()` i inne statystyki kolumn pomijają `NaN`, czyli brakujące wartości (missing values), więc tutaj średnia liczy się z 3 znanych wyników; w NumPy `a.mean()` dałoby `nan`. `.count()` zlicza wartości, których nie brakuje, a `len(df)` wszystkie wiersze.

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "score": [72, np.nan, 90, 66],
})
score = df["score"]
print(score.mean(), score.sum())
print(score.count(), len(df))
```

### See also

- exploring/column-statistics
- array-files/missing-values-with-genfromtxt

## Dropping rows with missing values

PL: Usuwanie wierszy z brakami

`df.dropna()` returns the table without the rows that miss a value in any column. `df.dropna(subset=["score"])` looks only at the listed columns, so a gap elsewhere doesn't cost you a row; assign the result back to keep it.

PL: `df.dropna()` zwraca tabelę bez wierszy, w których brakuje wartości (missing value) w dowolnej kolumnie. `df.dropna(subset=["score"])` patrzy tylko na wymienione kolumny, więc brak w innej kolumnie nie usuwa wiersza; przypisz wynik z powrotem, aby go zachować.

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa", "Olek"],
    "height": [165, np.nan, 172, 178],
    "score": [72, 85, np.nan, 64],
})
print(df.dropna())
print(df.dropna(subset=["score"]))
```

## Filling missing values

PL: Uzupełnianie brakujących wartości

`fillna(0)` replaces every `NaN` with 0, and `fillna(df["score"].mean())` with the column's mean. Filling with the mean keeps the mean but makes the data look less spread out than it is, so the standard deviation comes out too small and tests look more certain than they are.

PL: `fillna(0)` zastępuje każdą brakującą wartość (missing value) `NaN` zerem, a `fillna(df["score"].mean())` średnią kolumny. Uzupełnianie średnią zachowuje średnią, ale dane wyglądają na mniej rozproszone, niż są, więc odchylenie standardowe (standard deviation) wychodzi za małe, a testy wydają się pewniejsze, niż są.

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "score": [72, np.nan, 90, 66],
})
score = df["score"]
print(score.fillna(0))
filled = score.fillna(score.mean())
print(filled)
print(f"{score.std():.2f}")
print(f"{filled.std():.2f}")
```

### Pitfall

`df["score"] == np.nan` is `False` in every row, even the missing ones, because `NaN` equals nothing, not even itself; a filter or fill built on it changes nothing. Use `df["score"].isna()`.

PL: `df["score"] == np.nan` daje `False` w każdym wierszu, nawet przy brakach, bo `NaN` nie jest równe niczemu, nawet sobie; filtr albo uzupełnianie oparte na tym porównaniu niczego nie zmienia. Użyj `df["score"].isna()`.

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "score": [72, np.nan, 90],
})
print(df["score"] == np.nan)
print(np.nan == np.nan)
```

### See also

- exploring/column-statistics
- aggregates/standard-deviation-and-variance
