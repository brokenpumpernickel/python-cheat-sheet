"""The interface label table (site/src/labels.ts), read with Node as the site build reads it."""

# The `labels` fixture (the table, read with Node) is in conftest.py.


def test_every_label_exists_in_english_and_polish(labels):
    assert set(labels) == {"en", "pl"}
    assert labels["en"].keys() == labels["pl"].keys()
    for language in labels.values():
        assert all(text.strip() for text in language.values())


def test_agreed_polish_labels(labels):
    assert labels["pl"]["map"] == "Mapa"
    assert labels["pl"]["output"] == "Wynik"
    assert labels["pl"]["pitfall"] == "Pułapka"
