"""The interface label table (site/src/labels.ts), read with Node as the site build reads it."""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

LABELS = Path(__file__).parent.parent / "site" / "src" / "labels.ts"


@pytest.fixture(scope="module")
def labels() -> dict:
    node = shutil.which("node")
    assert node, "node not found; install Node.js to build the site"
    script = f"const m = await import({json.dumps(LABELS.as_uri())}); console.log(JSON.stringify(m.labels));"
    run = subprocess.run(
        [node, "--input-type=module", "--no-warnings", "-e", script],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return json.loads(run.stdout)


def test_every_label_exists_in_english_and_polish(labels):
    assert set(labels) == {"en", "pl"}
    assert labels["en"].keys() == labels["pl"].keys()
    for language in labels.values():
        assert all(text.strip() for text in language.values())


def test_agreed_polish_labels(labels):
    assert labels["pl"]["map"] == "Mapa"
    assert labels["pl"]["output"] == "Wynik"
