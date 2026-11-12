"""Tests for the dental clinic example business."""

import json
from pathlib import Path

from aiaudit.scoring import score

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "dental_clinic.json"


def load_example() -> dict:
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def test_example_uses_a_known_industry():
    assert load_example()["industry"] == "services"


def test_example_has_a_customer_support_opportunity():
    data = load_example()
    results = score(data["answers"], data["area_weights"], data["industry"])
    areas = {r.opportunity.area for r in results}
    assert "customer_support" in areas


def test_example_customer_support_weight_is_applied():
    data = load_example()
    results = score(data["answers"], data["area_weights"], data["industry"])
    weights = {r.opportunity.area: r.weight for r in results}
    assert weights["customer_support"] == 1.5
    assert weights["finance"] == 1.0


def test_example_answers_cover_every_question():
    from aiaudit.questions import QUESTIONS

    assert set(load_example()["answers"]) == {q.key for q in QUESTIONS}
