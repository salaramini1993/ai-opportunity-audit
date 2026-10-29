"""Tests for loading the catalog from the JSON data file."""

import json

import pytest

from aiaudit.catalog import (
    AREAS,
    CATALOG,
    CatalogError,
    Opportunity,
    load_catalog,
    parse_catalog,
)
from aiaudit.questions import QUESTIONS


def valid_item(**changes):
    item = {
        "key": "test_item",
        "area": "sales",
        "title": "Test",
        "description": "A test opportunity.",
        "signals": ["has_leads"],
        "base_effort": 2,
        "example_tools": ["LLM"],
    }
    item.update(changes)
    return item


def catalog_data(*items):
    return {"areas": ["sales"], "opportunities": list(items) or [valid_item()]}


def test_default_catalog_loads():
    areas, items = load_catalog()
    assert areas == AREAS
    assert items == CATALOG
    assert len(CATALOG) >= 12
    assert all(isinstance(item, Opportunity) for item in CATALOG)


def test_all_signals_are_known_questions():
    question_keys = {q.key for q in QUESTIONS}
    for item in CATALOG:
        for signal in item.signals:
            assert signal in question_keys, f"{item.key}: {signal}"


def test_lists_become_tuples():
    _, items = parse_catalog(catalog_data())
    assert items[0].signals == ("has_leads",)
    assert items[0].example_tools == ("LLM",)


def test_example_tools_is_optional():
    item = valid_item()
    del item["example_tools"]
    _, items = parse_catalog(catalog_data(item))
    assert items[0].example_tools == ()


def test_load_from_custom_file(tmp_path):
    path = tmp_path / "catalog.json"
    path.write_text(json.dumps(catalog_data()), encoding="utf-8")
    areas, items = load_catalog(path)
    assert areas == ("sales",)
    assert items[0].key == "test_item"


def test_bad_json_file(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(CatalogError, match="not valid JSON"):
        load_catalog(path)


@pytest.mark.parametrize(
    "data, message",
    [
        ([], "must be an object"),
        ({"areas": [], "opportunities": [valid_item()]}, "'areas'"),
        ({"areas": ["sales", "sales"], "opportunities": [valid_item()]}, "duplicate names"),
        ({"areas": ["sales"], "opportunities": []}, "'opportunities'"),
        (catalog_data("text"), "must be an object"),
        (catalog_data({"key": "x"}), "missing field"),
        (catalog_data(valid_item(extra=1)), "unknown field"),
        (catalog_data(valid_item(title=" ")), "'title'"),
        (catalog_data(valid_item(area="legal")), "unknown area"),
        (catalog_data(valid_item(signals=[])), "'signals'"),
        (catalog_data(valid_item(signals="has_leads")), "'signals'"),
        (catalog_data(valid_item(base_effort=0)), "'base_effort'"),
        (catalog_data(valid_item(base_effort=6)), "'base_effort'"),
        (catalog_data(valid_item(base_effort=True)), "'base_effort'"),
        (catalog_data(valid_item(base_effort="2")), "'base_effort'"),
        (catalog_data(valid_item(example_tools=[1])), "'example_tools'"),
        (catalog_data(valid_item(), valid_item()), "duplicate opportunity key"),
    ],
)
def test_bad_catalog_data(data, message):
    with pytest.raises(CatalogError, match=message):
        parse_catalog(data)
