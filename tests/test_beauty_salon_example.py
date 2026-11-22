"""Tests for the beauty salon example business."""

import json
from pathlib import Path

from aiaudit.questions import QUESTIONS
from aiaudit.scoring import score

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "beauty_salon.json"


def load_example() -> dict:
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def test_example_uses_a_known_industry():
    assert load_example()["industry"] == "services"


def test_example_answers_cover_every_question():
    keys = {question.key for question in QUESTIONS}
    assert set(load_example()["answers"]) == keys


def test_example_has_a_marketing_opportunity():
    data = load_example()
    results = score(data["answers"], data["area_weights"], data["industry"])
    assert any(r.opportunity.area == "marketing" for r in results)


def test_example_weights_are_applied():
    data = load_example()
    results = score(data["answers"], data["area_weights"], data["industry"])
    support = [r for r in results if r.opportunity.area == "customer_support"]
    assert support
    assert all(r.weight == 1.2 for r in support)
