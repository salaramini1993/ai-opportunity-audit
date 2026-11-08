"""Tests for the manufacturer example business."""

import json
from pathlib import Path

from aiaudit.scoring import score

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "manufacturer.json"


def load_example() -> dict:
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def test_example_uses_a_known_industry():
    data = load_example()
    assert data["industry"] == "manufacturing"


def test_example_has_an_operations_opportunity():
    data = load_example()
    results = score(data["answers"], data["area_weights"], data["industry"])
    areas = {r.opportunity.area for r in results}
    assert "operations" in areas


def test_example_operations_weight_is_applied():
    data = load_example()
    results = score(data["answers"], data["area_weights"], data["industry"])
    ops = [r for r in results if r.opportunity.area == "operations"]
    assert ops
    assert all(r.weight == 1.3 for r in ops)
