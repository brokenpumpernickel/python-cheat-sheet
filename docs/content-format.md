# Content format

How Areas, Topics and Entries are written in `content/`. This is the short reference; the full authoring guide (tone, length, Topic order, Polish terminology) comes later. The content build (`cheatsheet/content.py`) is the only reader of these files.

## Folder layout

```
content/
  areas.yaml              # Area order: a YAML list of Area ids
  python-basics/          # one folder per Area; the folder name is the Area id
    _area.md              # the Area description
    lists.md              # one file per Topic; the file name is the Topic id
```

Ids are lowercase words joined by `-`. Topic ids are unique across all Areas, because links are `#topic` and `#topic/entry`.

## Area description (`_area.md`)

Frontmatter only, no body:

```yaml
---
title: Python Basics
blurb: "The core language: names, control flow, functions and built-in collections."
hue: 160                  # 0–360, the Area's colour
planned: false            # optional, default false
topics:                   # Topic order, including planned Topics
  - lists
  - tuples
pl:
  title: Podstawy Pythona
  blurb: "Rdzeń języka: nazwy, sterowanie przepływem, funkcje i wbudowane kolekcje."
---
```

Quote a value when it contains `: ` or starts with `[`, `{` or `"`.

## Topic file (`<topic-id>.md`)

Frontmatter, then the Entries in reading order:

```yaml
---
title: Lists
glyph: "[ ]"              # short symbol on the Topic's bubble
summary: "Ordered, changeable sequences: indexing, slicing, sorting."
planned: false            # optional; a planned Topic has no Entries and may leave out summary
pl:
  title: Listy
  summary: "Listy (lists): uporządkowane, modyfikowalne sekwencje."
---
```

## Entry

Every Entry is a `##` section. **Pair rule:** every piece of English prose (the `##` title, the explanation, the Pitfall text) is immediately followed by its Polish counterpart, a paragraph that starts with `PL:`.

````markdown
## Sorting

PL: Sortowanie

`sorted(x)` returns a new sorted list; `x.sort()` sorts the list in place and returns `None`.

PL: `sorted(x)` zwraca nową posortowaną listę; `x.sort()` sortuje listę w miejscu i zwraca `None`.

```python
data = [3, 1, 2]
print(sorted(data))
```

### Pitfall

`data = data.sort()` replaces your list with `None`.

PL: `data = data.sort()` zastępuje Twoją listę wartością `None`.

```python
data = [3, 1, 2]
data = data.sort()
print(data)
```

### See also

- functions/lambda
````

- **Title**: the `##` heading in English, then a `PL:` paragraph with the Polish title. The Entry id is the English title slugified (`List comprehensions` → `list-comprehensions`).
- **Explanation**: one English paragraph and one `PL:` paragraph. Inline Markdown (`` `code` ``, `*emphasis*`, `**bold**`) is allowed.
- **Code example**: exactly one ` ```python ` block. It must be self-contained and print what it shows with `print(...)`. The Output is captured by the build, never written by hand.
- **Expected error**: add `raises=<ExceptionType>` to the code block's info string, e.g. ` ```python raises=KeyError `. The Output then ends with the error's final line (`KeyError: 'sd'`). Any other error fails the build.
- **Pitfall** (optional): a `### Pitfall` section with one English paragraph, one `PL:` paragraph and optionally one ` ```python ` block (which may also carry `raises=`).
- **See also** (optional): a `### See also` section with a bullet list of `topic-id/entry-id` references.

No other headings or blocks are allowed inside a Topic file.
