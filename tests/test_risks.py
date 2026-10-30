"""Tests for the "risks and checks" field."""

from datetime import date

import pytest

from aiaudit.catalog import CATALOG, CatalogError, parse_catalog
from aiaudit.report import render_markdown
from aiaudit.scoring import score


def catalog_with_risks(risks):
    item = {
        "key": "test_item",
        "area": "sales",
        "title": "Test",
        "description": "A test opportunity.",
        "signals": ["has_leads"],
        "base_effort": 2,
        "risks": risks,
    }
    return {"areas": ["sales"], "opportunities": [item]}


def test_every_default_opportunity_has_risks():
    for item in CATALOG:
        assert item.risks, item.key
        assert all(risk.endswith(".") for risk in item.risks), item.key


def test_good_risks_are_parsed():
    _, items = parse_catalog(catalog_with_risks(["Check each draft."]))
    assert items[0].risks == ("Check each draft.",)


def test_risks_field_is_optional():
    data = catalog_with_risks([])
    del data["opportunities"][0]["risks"]
    _, items = parse_catalog(data)
    assert items[0].risks == ()


@pytest.mark.parametrize("risks", ["Check it.", [1], [""], ["  "], None, [["x"]]])
def test_bad_risks_are_rejected(risks):
    with pytest.raises(CatalogError, match="'risks'"):
        parse_catalog(catalog_with_risks(risks))


def test_report_shows_risks():
    results = score({"many_meetings": True})
    text = render_markdown("Office", results, today=date(2026, 1, 1))
    assert "Risks and checks:" in text
    assert "- Tell all persons in the meeting before you record it." in text
