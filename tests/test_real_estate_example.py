"""Tests for the real estate agency example business."""

import json
from pathlib import Path

from aiaudit.scoring import score

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "real_estate_agency.json"


def load_example() -> dict:
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def test_example_uses_a_known_industry():
    data = load_example()
    assert data["industry"] == "services"


def test_example_has_a_sales_opportunity():
    data = load_example()
    results = score(data["answers"], data["area_weights"], data["industry"])
    areas = {r.opportunity.area for r in results}
    assert "sales" in areas


def test_example_weights_are_applied():
    data = load_example()
    results = score(data["answers"], data["area_weights"], data["industry"])
    sales = [r for r in results if r.opportunity.area == "sales"]
    admin = [r for r in results if r.opportunity.area == "admin"]
    assert sales and admin
    assert all(r.weight == 1.3 for r in sales)
    assert all(r.weight == 1.2 for r in admin)
