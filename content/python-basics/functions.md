---
title: Functions
glyph: "def"
summary: "Reusable code: defining, arguments, return values, lambda."
pl:
  title: Funkcje
  summary: "Funkcje (functions): kod wielokrotnego użytku — definiowanie, argumenty, zwracane wartości, lambda."
---

## Defining and calling

PL: Definiowanie i wywoływanie

`def name(params):` creates a function, and `return` sends a value back to the caller. Call the function by writing its name with the arguments in parentheses.

PL: `def name(params):` tworzy funkcję (function), a `return` odsyła wartość do miejsca wywołania. Funkcję wywołujesz, pisząc jej nazwę z argumentami (arguments) w nawiasach.

```python
def mean(values):
    return sum(values) / len(values)

print(mean([2, 4, 9]))
```

### Pitfall

A function without `return` gives back `None`: printing a value inside the function doesn't return it.

PL: Funkcja bez `return` zwraca `None`: wypisanie wartości wewnątrz funkcji nie jest jej zwróceniem.

```python
def mean(values):
    print(sum(values) / len(values))

m = mean([2, 4, 9])
print(m)
```

### See also

- array-maths/functions-that-work-on-whole-arrays

## Default arguments

PL: Argumenty domyślne

`def f(x, digits=2):` gives `digits` a default value, used when the call leaves it out. You can also pass an argument by name: `digits=4`.

PL: `def f(x, digits=2):` daje parametrowi (parameter) `digits` wartość domyślną (default value), używaną, gdy wywołanie go pominie. Argument (argument) możesz też przekazać po nazwie: `digits=4`.

```python
def describe(x, digits=2):
    return f"{x:.{digits}f}"

print(describe(3.14159))
print(describe(3.14159, digits=4))
```

### See also

- strings/f-strings

## Returning several values

PL: Zwracanie kilku wartości

`return a, b` returns several values separated by commas. They come back as a tuple, which you can unpack into separate names.

PL: `return a, b` zwraca kilka wartości oddzielonych przecinkami. Wracają jako krotka (tuple), którą możesz rozpakować (unpack) do osobnych nazw.

```python
def spread(values):
    return min(values), max(values)

low, high = spread([4, 8, 1, 6])
print(low, high)
```

### See also

- tuples/unpacking

## lambda

PL: lambda

`lambda p: p[1]` makes a small one-line function without a name. It is most often used as the `key` when sorting.

PL: `lambda p: p[1]` tworzy małą, jednolinijkową funkcję (function) bez nazwy. Najczęściej służy jako `key` przy sortowaniu.

```python
people = [("Ola", 23), ("Jan", 19),
          ("Ewa", 31)]
print(sorted(people, key=lambda p: p[1]))
```

### See also

- lists/sorting
