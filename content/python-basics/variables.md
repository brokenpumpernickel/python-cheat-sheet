---
title: Variables
glyph: "x ="
summary: "Naming values, basic types, converting between them."
pl:
  title: Zmienne
  summary: "Zmienne (variables): nazywanie wartości, podstawowe typy i konwersja między nimi."
---

## Assigning values

PL: Przypisywanie wartości

`name = value` binds a name to a value. Python works out the type from the value, and `type()` tells you what it is.

PL: `name = value` wiąże nazwę z wartością, tworząc zmienną (variable). Python sam ustala typ (type) na podstawie wartości, a `type()` pokazuje, jaki to typ.

```python
n = 30
mean = 4.2
label = "trial A"
is_valid = True
print(n, mean, label, is_valid)
print(type(n), type(mean))
```

### Pitfall

`=` assigns a value and `==` compares two values, so `if x = 3:` is a `SyntaxError`.

PL: `=` przypisuje wartość, a `==` porównuje dwie wartości, więc `if x = 3:` to `SyntaxError`.

## Updating a variable

PL: Aktualizowanie zmiennej

`total += 5` is short for `total = total + 5`: it updates a variable from its current value. `-=`, `*=` and `/=` work the same way.

PL: `total += 5` to skrót od `total = total + 5`: zmienia zmienną (variable) na podstawie jej bieżącej wartości. Tak samo działają `-=`, `*=` i `/=`.

```python
total = 0
total += 5
print(total)
total *= 2
print(total)
```

## Converting types

PL: Konwersja typów

`int()`, `float()` and `str()` convert a value to another type; data read from a file arrives as text and needs converting. `int()` on a float drops the decimals instead of rounding.

PL: `int()`, `float()` i `str()` zamieniają wartość na inny typ (type); dane wczytane z pliku są tekstem i trzeba je przekonwertować. `int()` na liczbie zmiennoprzecinkowej (float) odcina część ułamkową zamiast zaokrąglać.

```python
print(int("42") + 1)
print(float("3.5") * 2)
print(str(42) + "1")
print(int(3.9))
```
