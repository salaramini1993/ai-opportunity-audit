"""Tests for the veterinary clinic example business."""

import json
from pathlib import Path

from aiaudit.scoring import score

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "veterinary_clinic.json"


def load_example() -> dict:
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def test_example_uses_a_known_industry():
    data = load_example()
    assert data["industry"] == "services"


def test_example_has_a_customer_support_opportunity():
    data = load_example()
    results = score(data["answers"], data["area_weights"], data["industry"])
    areas = {r.opportunity.area for r in results}
    assert "customer_support" in areas


def test_example_weights_are_applied():
    data = load_example()
    results = score(data["answers"], data["area_weights"], data["industry"])
    support = [r for r in results if r.opportunity.area == "customer_support"]
    hr = [r for r in results if r.opportunity.area == "hr"]
    assert support and hr
    assert all(r.weight == 1.3 for r in support)
    assert all(r.weight == 1.2 for r in hr)
