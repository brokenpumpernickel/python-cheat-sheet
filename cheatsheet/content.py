"""Reads the content folder (Area descriptions and Topic files) into plain data.

This is the only parser of the Markdown content; the format is described in
docs/content-format.md. Code examples are returned unexecuted; see build.py.
"""

import re
from dataclasses import dataclass
from pathlib import Path

import yaml
from markdown_it import MarkdownIt

AREA_FILE = "_area.md"
AREA_ORDER_FILE = "areas.yaml"
POLISH = "PL:"

_MD = MarkdownIt("commonmark", {"html": False})
_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---[ \t]*(?:\n|\Z)(.*)\Z", re.DOTALL)
_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_SEE_ALSO = re.compile(r"^[a-z0-9-]+/[a-z0-9-]+$")
_RAISES = re.compile(r"^raises=([A-Za-z_][A-Za-z0-9_]*)$")


class ContentError(Exception):
    """The content folder is malformed. The message names the place to fix."""


@dataclass
class _Block:
    kind: str  # "heading", "paragraph", "fence", "list" or the markdown-it token type
    text: str = ""
    level: int = 0
    info: str = ""
    items: tuple[str, ...] = ()
    line: int = 0


def parse_content(content_dir: Path) -> list[dict]:
    """Return the Areas in Area order, each with its Topics in Topic order."""
    order_file = content_dir / AREA_ORDER_FILE
    area_ids = _load_yaml(order_file, order_file.name)
    if not isinstance(area_ids, list) or not all(isinstance(a, str) for a in area_ids):
        raise ContentError(f"{AREA_ORDER_FILE}: expected a list of Area ids")
    for area_id in _duplicates(area_ids):
        raise ContentError(f"{AREA_ORDER_FILE}: Area '{area_id}' is listed twice")
    for folder in sorted(p.name for p in content_dir.iterdir() if p.is_dir()):
        if folder not in area_ids:
            raise ContentError(f"{folder}/: Area folder is not listed in {AREA_ORDER_FILE}")
    references: list[tuple[str, str]] = []
    areas = [_parse_area(content_dir, area_id, references) for area_id in area_ids]

    seen: dict[str, str] = {}
    for area in areas:
        for topic in area["topics"]:
            if topic["id"] in seen:
                raise ContentError(
                    f"{area['id']}/{topic['id']}.md: Topic id '{topic['id']}' is also used in Area '{seen[topic['id']]}'"
                )
            seen[topic["id"]] = area["id"]

    topics = {topic["id"]: topic for area in areas for topic in area["topics"]}
    for here, reference in references:
        _check_reference(reference, topics, here)
    return areas


def _check_reference(reference: str, topics: dict[str, dict], here: str) -> None:
    topic_id, entry_id = reference.split("/")
    topic = topics.get(topic_id)
    if topic is None:
        raise ContentError(f"{here} See also: '{reference}' names Topic '{topic_id}', which does not exist")
    entry_ids = [entry["id"] for entry in topic["entries"]]
    if entry_id not in entry_ids:
        if topic["planned"]:
            raise ContentError(f"{here} See also: '{reference}' points into planned Topic '{topic_id}', which has no Entries yet")
        raise ContentError(
            f"{here} See also: '{reference}' names no Entry of Topic '{topic_id}'; its Entries are: {', '.join(entry_ids)}"
        )


def _parse_area(content_dir: Path, area_id: str, references: list[tuple[str, str]]) -> dict:
    where = f"{area_id}/{AREA_FILE}"
    path = content_dir / area_id / AREA_FILE
    if not path.is_file():
        raise ContentError(f"{AREA_ORDER_FILE}: Area '{area_id}' has no {where}")
    meta, body, _ = _split_frontmatter(path, where)
    if body.strip():
        raise ContentError(f"{where}: an Area description has frontmatter only, no body")

    topic_ids = meta.get("topics")
    if not isinstance(topic_ids, list) or not all(isinstance(t, str) for t in topic_ids):
        raise ContentError(f"{where}: 'topics' must be a list of Topic ids (the Topic order)")
    for topic_id in _duplicates(topic_ids):
        raise ContentError(f"{where}: Topic order lists '{topic_id}' twice")
    on_disk = {p.stem for p in path.parent.glob("*.md") if p.name != AREA_FILE}
    for topic_id in topic_ids:
        if topic_id not in on_disk:
            raise ContentError(f"{where}: Topic order names '{topic_id}', but there is no {area_id}/{topic_id}.md")
    for topic_id in sorted(on_disk - set(topic_ids)):
        raise ContentError(f"{area_id}/{topic_id}.md: Topic is not listed in the Topic order of {where}")

    pl = _mapping(meta, "pl", where)
    hue = meta.get("hue")
    if not isinstance(hue, int) or isinstance(hue, bool) or not 0 <= hue <= 360:
        raise ContentError(f"{where}: 'hue' must be a whole number from 0 to 360")
    area = {
        "id": _checked_id(area_id, where),
        "title": _text(meta, "title", where),
        "blurb": _text(meta, "blurb", where),
        "hue": hue,
        "planned": _flag(meta, "planned", where),
        "pl": {"title": _text(pl, "title", f"{where} pl"), "blurb": _text(pl, "blurb", f"{where} pl")},
        "topics": [_parse_topic(path.parent / f"{t}.md", f"{area_id}/{t}.md", references) for t in topic_ids],
    }
    for topic in area["topics"]:
        if area["planned"] and not topic["planned"]:
            raise ContentError(f"{area_id}/{topic['id']}.md: a planned Area lists only planned Topics; add 'planned: true'")
    return area


def _parse_topic(path: Path, where: str, references: list[tuple[str, str]]) -> dict:
    topic_id = _checked_id(path.stem, where)
    meta, body, body_line = _split_frontmatter(path, where)
    planned = _flag(meta, "planned", where)
    pl = _mapping(meta, "pl", where)
    blocks = _blocks(body, body_line)

    if planned:
        if blocks:
            raise ContentError(f"{where}:{blocks[0].line}: a planned Topic has no Entries")
        entries = []
    else:
        entries = _parse_entries(blocks, topic_id, where, references)
        if not entries:
            raise ContentError(f"{where}: a Topic needs at least one Entry (a '## ' section) unless it is planned")

    return {
        "id": topic_id,
        "title": _text(meta, "title", where),
        "summary": _text(meta, "summary", where, optional=planned),
        "glyph": _text(meta, "glyph", where),
        "planned": planned,
        "pl": {
            "title": _text(pl, "title", f"{where} pl"),
            "summary": _text(pl, "summary", f"{where} pl", optional=planned),
        },
        "entries": entries,
    }


def _parse_entries(blocks: list[_Block], topic_id: str, where: str, references: list[tuple[str, str]]) -> list[dict]:
    sections: list[tuple[_Block, list[_Block]]] = []
    for block in blocks:
        if block.kind == "heading" and block.level == 2:
            sections.append((block, []))
        elif not sections:
            raise ContentError(f"{where}:{block.line}: expected an Entry ('## Title') before any other content")
        else:
            sections[-1][1].append(block)

    entries: list[dict] = []
    for heading, body in sections:
        entry = _parse_entry(heading, body, topic_id, where, references)
        if any(e["id"] == entry["id"] for e in entries):
            raise ContentError(f"{where}:{heading.line}: two Entries have the id '{entry['id']}'; ids come from the titles, so change one title")
        entries.append(entry)
    return entries


def _parse_entry(
    heading: _Block, body: list[_Block], topic_id: str, where: str, references: list[tuple[str, str]]
) -> dict:
    entry_id = _slug(heading.text)
    if not entry_id:
        raise ContentError(f"{where}:{heading.line}: an Entry title needs letters or digits, since the Entry id is made from it")
    here = f"{where}:{heading.line} ({topic_id}/{entry_id})"

    parts: dict[str, list[_Block]] = {"": []}
    current = ""
    for block in body:
        if block.kind == "heading":
            if block.level != 3 or block.text not in ("Pitfall", "See also"):
                raise ContentError(f"{where}:{block.line}: unexpected heading '{block.text}'; inside an Entry only '### Pitfall' and '### See also' are allowed")
            if block.text in parts:
                raise ContentError(f"{where}:{block.line}: '### {block.text}' appears twice")
            current = block.text
            parts[current] = []
        else:
            parts[current].append(block)

    main = parts[""]
    if not main or not _is_polish(main[0]):
        raise ContentError(f"{here}: the heading must be followed by a '{POLISH} <Polish title>' paragraph")
    pl_title = _strip_polish(main[0].text)
    if not pl_title:
        raise ContentError(f"{here}: the '{POLISH}' paragraph after the heading is empty; write the Polish title")
    explain, pl_explain, fences = _prose_and_code(main[1:], here)
    if len(fences) != 1:
        raise ContentError(f"{here}: an Entry needs exactly one ```python code block, found {len(fences)}")
    code, raises = _example(fences[0], here)

    pitfall = pl_pitfall = None
    if "Pitfall" in parts:
        text, pl_pitfall, pitfall_fences = _prose_and_code(parts["Pitfall"], f"{here} Pitfall")
        if len(pitfall_fences) > 1:
            raise ContentError(f"{here} Pitfall: at most one ```python code block, found {len(pitfall_fences)}")
        pitfall_code, pitfall_raises = _example(pitfall_fences[0], f"{here} Pitfall") if pitfall_fences else (None, None)
        pitfall = {"text": text, "code": pitfall_code, "raises": pitfall_raises}

    see = _see_also(parts["See also"], here) if "See also" in parts else []
    references.extend((here, reference) for reference in see)

    return {
        "id": entry_id,
        "title": heading.text,
        "explain": explain,
        "code": code,
        "raises": raises,
        "see": see,
        "pitfall": pitfall,
        "pl": {"title": pl_title, "explain": pl_explain, "pitfall": pl_pitfall},
    }


def _prose_and_code(blocks: list[_Block], here: str) -> tuple[str, str, list[_Block]]:
    """One English paragraph, its PL: counterpart, and any code blocks. Prose is returned as inline HTML."""
    english, polish, fences = [], [], []
    for block in blocks:
        if block.kind == "fence":
            fences.append(block)
        elif block.kind == "paragraph":
            (polish if _is_polish(block) else english).append(block)
        else:
            raise ContentError(f"{here}: unexpected {block.kind} at line {block.line}; use paragraphs and ```python blocks only")
    if len(english) != 1:
        raise ContentError(f"{here}: expected one English paragraph, found {len(english)}")
    if len(polish) != 1:
        raise ContentError(f"{here}: expected one '{POLISH}' paragraph with the Polish text, found {len(polish)}")
    if not _strip_polish(polish[0].text):
        raise ContentError(f"{here}: the '{POLISH}' paragraph at line {polish[0].line} is empty; write the Polish text")
    return _MD.renderInline(english[0].text), _MD.renderInline(_strip_polish(polish[0].text)), fences


def _example(fence: _Block, here: str) -> tuple[str, str | None]:
    language, *attributes = fence.info.split()
    if language != "python":
        raise ContentError(f"{here}: code blocks must be ```python, not ```{language} (line {fence.line})")
    raises = None
    for attribute in attributes:
        match = _RAISES.match(attribute)
        if not match:
            raise ContentError(f"{here}: unknown code block option '{attribute}'; the only option is raises=<ExceptionType>")
        raises = match.group(1)
    if not fence.text.strip():
        raise ContentError(f"{here}: the code block at line {fence.line} is empty")
    return fence.text.rstrip("\n"), raises


def _see_also(blocks: list[_Block], here: str) -> list[str]:
    if len(blocks) != 1 or blocks[0].kind != "list":
        raise ContentError(f"{here} See also: expected one bullet list of topic-id/entry-id references")
    for item in blocks[0].items:
        if not _SEE_ALSO.match(item):
            raise ContentError(f"{here} See also: '{item}' is not a topic-id/entry-id reference")
    return list(blocks[0].items)


def _blocks(body: str, first_line: int) -> list[_Block]:
    """Flatten the Markdown body into top-level blocks, with 1-based file line numbers."""
    tokens = _MD.parse(body)
    blocks, i = [], 0
    while i < len(tokens):
        token = tokens[i]
        line = first_line + (token.map[0] if token.map else 0)
        end = i
        if token.nesting == 1:
            depth = 0
            while True:
                depth += tokens[end].nesting
                if depth == 0:
                    break
                end += 1
        inner = tokens[i + 1 : end]
        if token.type == "heading_open":
            blocks.append(_Block("heading", inner[0].content.strip(), level=int(token.tag[1:]), line=line))
        elif token.type == "paragraph_open":
            blocks.append(_Block("paragraph", inner[0].content.strip(), line=line))
        elif token.type == "fence":
            blocks.append(_Block("fence", token.content, info=token.info, line=line))
        elif token.type == "bullet_list_open":
            items = tuple(t.content.strip() for t in inner if t.type == "inline")
            blocks.append(_Block("list", items=items, line=line))
        else:
            blocks.append(_Block(token.type.removesuffix("_open").replace("_", " "), line=line))
        i = end + 1
    return blocks


def _split_frontmatter(path: Path, where: str) -> tuple[dict, str, int]:
    text = path.read_text(encoding="utf-8")
    match = _FRONTMATTER.match(text)
    if not match:
        raise ContentError(f"{where}: the file must start with YAML frontmatter between '---' lines")
    meta = _load_yaml_text(match.group(1), where)
    if not isinstance(meta, dict):
        raise ContentError(f"{where}: the frontmatter must be a set of 'key: value' lines")
    body_line = text[: match.start(2)].count("\n") + 1
    return meta, match.group(2), body_line


def _load_yaml(path: Path, where: str):
    if not path.is_file():
        raise ContentError(f"{where}: file not found in {path.parent}")
    return _load_yaml_text(path.read_text(encoding="utf-8"), where)


def _load_yaml_text(text: str, where: str):
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError as error:
        raise ContentError(f"{where}: invalid YAML ({error}); quote values that contain ': '") from None


def _text(meta: dict, key: str, where: str, optional: bool = False) -> str | None:
    value = meta.get(key)
    if value is None and optional:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ContentError(f"{where}: '{key}' is required and must be text")
    return value.strip()


def _flag(meta: dict, key: str, where: str) -> bool:
    value = meta.get(key, False)
    if not isinstance(value, bool):
        raise ContentError(f"{where}: '{key}' must be true or false")
    return value


def _mapping(meta: dict, key: str, where: str) -> dict:
    value = meta.get(key)
    if not isinstance(value, dict):
        raise ContentError(f"{where}: '{key}' is required and must hold the Polish fields")
    return value


def _checked_id(value: str, where: str) -> str:
    if not _ID.match(value):
        raise ContentError(f"{where}: '{value}' is not a valid id (lowercase letters, digits and '-')")
    return value


def _duplicates(ids: list[str]) -> list[str]:
    return sorted({i for i in ids if ids.count(i) > 1})


def _is_polish(block: _Block) -> bool:
    return block.kind == "paragraph" and block.text.startswith(POLISH)


def _strip_polish(text: str) -> str:
    return text.removeprefix(POLISH).strip()


def _slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
