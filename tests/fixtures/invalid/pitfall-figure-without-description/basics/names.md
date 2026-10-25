---
title: Names
glyph: "x ="
summary: Binding names.
pl:
  title: Nazwy
  summary: Wiązanie nazw.
---

## Binding

PL: Wiązanie

`=` binds a name to a value.

PL: `=` wiąże nazwę z wartością.

```python
x = 1
print(x)
```

### Pitfall

`x == 1` compares; it does not bind.

PL: `x == 1` porównuje, a nie wiąże.

```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3], [1, 4, 9])
plt.show()
```
