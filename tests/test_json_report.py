"""Tests for the JSON report (--format json)."""

import json

from aiaudit.cli import FORMATS, main
from aiaudit.csv_report import COLUMNS
from aiaudit.json_report import render_json
from aiaudit.scoring import score

SHOP = {"sells_products": True, "many_products": True, "multi_language": True}


def test_json_is_in_the_format_choices():
    assert "json" in FORMATS


def test_empty_list_has_no_opportunities():
    data = json.loads(render_json("Shop", []))
    assert data == {"business": "Shop", "industry": None, "opportunities": []}


def test_items_are_in_priority_order_with_csv_fields():
    results = score(SHOP)
    data = json.loads(render_json("Shop", results))
    items = data["opportunities"]
    assert len(items) == len(results)
    for item in items:
        assert list(item) == list(COLUMNS)
    assert [item["rank"] for item in items] == list(range(1, len(items) + 1))
    priorities = [item["priority"] for item in items]
    assert priorities == sorted(priorities, reverse=True)


def test_empty_estimate_is_null():
    results = score(SHOP)
    items = json.loads(render_json("Shop", results))["opportunities"]
    for r, item in zip(results, items, strict=True):
        if r.hours_saved is None:
            assert item["hours_saved_low"] is None
        else:
            assert item["hours_saved_low"] == r.hours_saved[0]
        if not r.opportunity.cost_per_month:
            assert item["cost_per_month"] is None


def test_industry_is_kept():
    data = json.loads(render_json("Shop", [], industry="retail"))
    assert data["industry"] == "retail"


def test_cli_writes_json_file(tmp_path):
    answers = tmp_path / "answers.json"
    answers.write_text(json.dumps({"business_name": "Shop", "answers": SHOP}))
    out = tmp_path / "out" / "priorities.json"
    assert main(["--answers", str(answers), "--format", "json", "--out", str(out)]) == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["business"] == "Shop"
    assert len(data["opportunities"]) == len(score(SHOP))
