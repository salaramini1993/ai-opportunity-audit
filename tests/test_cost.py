"""Tests for the cost per month estimate."""

from datetime import date

import pytest

from aiaudit.catalog import CATALOG, COST_LEVELS, CatalogError, parse_catalog
from aiaudit.report import format_cost, render_markdown
from aiaudit.scoring import score


def catalog_with_cost(cost):
    item = {
        "key": "test_item",
        "area": "sales",
        "title": "Test",
        "description": "A test opportunity.",
        "signals": ["has_leads"],
        "base_effort": 2,
        "cost_per_month": cost,
    }
    return {"areas": ["sales"], "opportunities": [item]}


def test_every_default_opportunity_has_a_cost():
    for item in CATALOG:
        assert item.cost_per_month in COST_LEVELS, item.key


@pytest.mark.parametrize("cost", ["low", "medium", "high"])
def test_good_cost_is_parsed(cost):
    _, items = parse_catalog(catalog_with_cost(cost))
    assert items[0].cost_per_month == cost


def test_cost_field_is_optional():
    data = catalog_with_cost("low")
    del data["opportunities"][0]["cost_per_month"]
    _, items = parse_catalog(data)
    assert items[0].cost_per_month is None


@pytest.mark.parametrize("cost", ["cheap", "LOW", "", 1, True, ["low"]])
def test_bad_cost_is_rejected(cost):
    with pytest.raises(CatalogError, match="cost_per_month"):
        parse_catalog(catalog_with_cost(cost))


@pytest.mark.parametrize("cost, text", [(None, "-"), ("low", "low"), ("high", "high")])
def test_format_cost(cost, text):
    assert format_cost(cost) == text


def test_report_shows_cost():
    results = score({"many_meetings": True})
    text = render_markdown("Office", results, today=date(2026, 1, 1))
    assert "Cost/month" in text
    assert "| 1-3 | low |" in text
    assert "- medium: 50-300 EUR" in text
