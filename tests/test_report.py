from datetime import date

from aiaudit.report import render_markdown
from aiaudit.scoring import score


def test_empty_report_has_message():
    text = render_markdown("Test AB", [], today=date(2026, 1, 1))
    assert "# AI Opportunity Audit: Test AB" in text
    assert "no clear AI opportunities" in text


def test_report_lists_opportunities():
    results = score({"sells_products": True, "many_products": True, "multi_language": True})
    text = render_markdown("Shop", results, today=date(2026, 1, 1))
    assert "Product descriptions and listings" in text
    assert "| 1 |" in text
