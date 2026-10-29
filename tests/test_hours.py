"""Tests for the hours saved per week estimate."""

from datetime import date

import pytest

from aiaudit.catalog import CATALOG, CatalogError, parse_catalog
from aiaudit.report import format_hours, render_markdown
from aiaudit.scoring import ScoredOpportunity, score, total_hours_saved


def catalog_with_hours(hours):
    item = {
        "key": "test_item",
        "area": "sales",
        "title": "Test",
        "description": "A test opportunity.",
        "signals": ["has_leads"],
        "base_effort": 2,
        "hours_saved_per_week": hours,
    }
    return {"areas": ["sales"], "opportunities": [item]}


def test_every_default_opportunity_has_hours():
    for item in CATALOG:
        assert item.hours_saved_per_week is not None, item.key
        low, high = item.hours_saved_per_week
        assert 0 < low <= high


def test_hours_are_parsed_as_float_tuple():
    _, items = parse_catalog(catalog_with_hours([1, 2.5]))
    assert items[0].hours_saved_per_week == (1.0, 2.5)


def test_hours_field_is_optional():
    data = catalog_with_hours([1, 2])
    del data["opportunities"][0]["hours_saved_per_week"]
    _, items = parse_catalog(data)
    assert items[0].hours_saved_per_week is None


@pytest.mark.parametrize(
    "hours",
    [3, [1], [1, 2, 3], [3, 1], [-1, 2], [1, 41], [True, 2], ["1", "2"]],
)
def test_bad_hours_are_rejected(hours):
    with pytest.raises(CatalogError, match="hours_saved_per_week"):
        parse_catalog(catalog_with_hours(hours))


def test_hours_scale_with_fit():
    _, items = parse_catalog(catalog_with_hours([2, 6]))
    full = ScoredOpportunity(items[0], fit=1.0, impact=3, effort=2)
    half = ScoredOpportunity(items[0], fit=0.5, impact=3, effort=2)
    assert full.hours_saved == (2.0, 6.0)
    assert half.hours_saved == (1.0, 3.0)


def test_no_estimate_gives_none_and_adds_zero():
    data = catalog_with_hours([1, 2])
    del data["opportunities"][0]["hours_saved_per_week"]
    _, items = parse_catalog(data)
    result = ScoredOpportunity(items[0], fit=1.0, impact=3, effort=2)
    assert result.hours_saved is None
    assert total_hours_saved([result]) == (0.0, 0.0)


def test_total_hours_is_the_sum():
    results = score({"support_volume": True, "repeat_questions": True, "email_heavy": True})
    expected_low = sum(r.hours_saved[0] for r in results)
    expected_high = sum(r.hours_saved[1] for r in results)
    assert total_hours_saved(results) == (round(expected_low, 1), round(expected_high, 1))


@pytest.mark.parametrize(
    "hours, text",
    [(None, "-"), ((2.0, 4.0), "2-4"), ((1.5, 1.5), "1.5"), ((0.5, 3.0), "0.5-3")],
)
def test_format_hours(hours, text):
    assert format_hours(hours) == text


def test_report_shows_hours():
    results = score({"many_meetings": True})
    text = render_markdown("Office", results, today=date(2026, 1, 1))
    assert "Hours/week" in text
    assert "Estimated time saved: 1-3 hours per week" in text
    assert "| 1-3 |" in text
