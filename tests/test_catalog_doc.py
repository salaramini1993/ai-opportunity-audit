"""Tests that docs/catalog.md matches the catalog code and its example is valid."""

import json
import re
from pathlib import Path

from aiaudit.catalog import _KNOWN_FIELDS, COST_LEVELS, MAX_HOURS_PER_WEEK, parse_catalog
from aiaudit.i18n import LANGUAGES

ROOT = Path(__file__).resolve().parent.parent
DOC = (ROOT / "docs" / "catalog.md").read_text(encoding="utf-8")


def test_doc_names_every_opportunity_field():
    for name in sorted(_KNOWN_FIELDS):
        assert f"`{name}`" in DOC, f"{name} is not in docs/catalog.md"


def test_doc_states_the_cost_levels():
    for level, meaning in COST_LEVELS.items():
        assert f"`{level}`" in DOC
        assert meaning.lower() in DOC.lower(), meaning


def test_doc_states_the_hours_range():
    assert f"from 0 to {MAX_HOURS_PER_WEEK}" in DOC


def test_doc_lists_the_translation_codes():
    for code in LANGUAGES:
        if code != "en":
            assert f"`{code}`" in DOC, f"{code} is not in docs/catalog.md"


def test_doc_example_is_a_valid_opportunity():
    match = re.search(r"```json\n(.*?)\n```", DOC, re.DOTALL)
    assert match, "docs/catalog.md has no json example"
    example = json.loads(match.group(1))
    data = {
        "areas": [example["area"]],
        "opportunities": [example],
    }
    areas, opportunities = parse_catalog(data)
    assert areas == (example["area"],)
    assert opportunities[0].key == example["key"]
