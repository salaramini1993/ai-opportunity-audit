"""Tests for the GDPR notes field."""

from datetime import date

import pytest

from aiaudit.catalog import CATALOG, CatalogError, by_key, parse_catalog
from aiaudit.report import render_markdown
from aiaudit.scoring import score


def catalog_with_notes(notes):
    item = {
        "key": "test_item",
        "area": "sales",
        "title": "Test",
        "description": "A test opportunity.",
        "signals": ["has_leads"],
        "base_effort": 2,
        "gdpr_notes": notes,
    }
    return {"areas": ["sales"], "opportunities": [item]}


# These opportunities read data about persons. They must have GDPR notes.
PERSONAL_DATA_KEYS = [
    "support_faq_assistant",
    "support_reply_drafts",
    "lead_qualification",
    "invoice_extraction",
    "meeting_notes",
    "hr_cv_screening",
    "logistics_shipment_status_replies",
]


@pytest.mark.parametrize("key", PERSONAL_DATA_KEYS)
def test_personal_data_opportunities_have_gdpr_notes(key):
    item = by_key(key)
    assert item.uses_personal_data
    assert all(note.endswith(".") for note in item.gdpr_notes)


def test_cv_screening_notes_mention_human_decision():
    notes = " ".join(by_key("hr_cv_screening").gdpr_notes)
    assert "Article 22" in notes
    assert "DPIA" in notes


def test_some_opportunities_have_no_personal_data():
    assert not by_key("cashflow_summary").uses_personal_data
    assert not by_key("inventory_forecast").uses_personal_data
    assert any(not item.uses_personal_data for item in CATALOG)


def test_good_notes_are_parsed():
    _, items = parse_catalog(catalog_with_notes(["Make a DPA."]))
    assert items[0].gdpr_notes == ("Make a DPA.",)
    assert items[0].uses_personal_data


def test_gdpr_notes_field_is_optional():
    data = catalog_with_notes([])
    del data["opportunities"][0]["gdpr_notes"]
    _, items = parse_catalog(data)
    assert items[0].gdpr_notes == ()
    assert not items[0].uses_personal_data


@pytest.mark.parametrize("notes", ["Make a DPA.", [1], [""], ["  "], None, [["x"]]])
def test_bad_notes_are_rejected(notes):
    with pytest.raises(CatalogError, match="'gdpr_notes'"):
        parse_catalog(catalog_with_notes(notes))


def test_report_shows_gdpr_notes():
    results = score({"many_meetings": True})
    text = render_markdown("Office", results, today=date(2026, 1, 1))
    assert "GDPR notes (this opportunity uses personal data):" in text
    assert "- Get consent or have a different legal basis" in text
    assert "use personal data. Read the" in text
    assert "They are not legal advice." in text


def test_report_has_no_gdpr_footer_without_personal_data():
    results = [r for r in score({}) if not r.opportunity.uses_personal_data]
    text = render_markdown("Office", results, today=date(2026, 1, 1))
    assert "GDPR notes" not in text
    assert "use personal data" not in text
