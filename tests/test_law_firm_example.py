"""Tests for the law firm example business."""

import json
from pathlib import Path

from aiaudit.scoring import score

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "law_firm.json"


def load_example() -> dict:
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def test_example_uses_a_known_industry():
    data = load_example()
    assert data["industry"] == "services"


def test_example_has_an_admin_opportunity():
    data = load_example()
    results = score(data["answers"], data["area_weights"], data["industry"])
    areas = {r.opportunity.area for r in results}
    assert "admin" in areas


def test_example_admin_weight_is_applied():
    data = load_example()
    results = score(data["answers"], data["area_weights"], data["industry"])
    admin = [r for r in results if r.opportunity.area == "admin"]
    assert admin
    assert all(r.weight == 1.3 for r in admin)


def test_example_sales_weight_is_applied():
    data = load_example()
    results = score(data["answers"], data["area_weights"], data["industry"])
    sales = [r for r in results if r.opportunity.area == "sales"]
    assert sales
    assert all(r.weight == 1.1 for r in sales)
