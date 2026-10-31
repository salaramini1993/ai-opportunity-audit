"""Tests for the logistics opportunities."""

from datetime import date

from aiaudit.catalog import AREAS, by_key
from aiaudit.questions import keys
from aiaudit.report import render_markdown
from aiaudit.scoring import score

KEYS = ("logistics_shipment_status_replies", "logistics_customs_document_check")


def test_logistics_is_an_area():
    assert "logistics" in AREAS


def test_logistics_opportunities_exist():
    for key in KEYS:
        item = by_key(key)
        assert item.area == "logistics"
        assert set(item.signals) <= keys()
        assert item.risks
        assert item.cost_per_month == "medium"


def test_customs_check_requires_a_person():
    text = " ".join(by_key("logistics_customs_document_check").risks).lower()
    assert "person" in text
    assert "approve" in text


def test_shipping_answers_find_logistics_opportunities():
    answers = {
        "ships_parcels": True,
        "where_is_my_order": True,
        "ships_abroad": True,
        "customs_documents": True,
    }
    found = {r.opportunity.key for r in score(answers)}
    assert set(KEYS) <= found


def test_no_shipping_gives_no_logistics_opportunities():
    results = score({"many_meetings": True})
    assert all(r.opportunity.area != "logistics" for r in results)


def test_logistics_weight_is_accepted():
    answers = {"ships_abroad": True, "customs_documents": True}
    results = score(answers, weights={"logistics": 2})
    item = next(r for r in results if r.opportunity.key == "logistics_customs_document_check")
    assert item.weight == 2.0


def test_report_shows_logistics_opportunity():
    results = score({"ships_parcels": True, "where_is_my_order": True})
    text = render_markdown("Shop", results, today=date(2026, 1, 1))
    assert "Replies to shipment status questions" in text
