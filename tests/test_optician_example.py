"""Tests for the optician example business."""

import json
from pathlib import Path

from aiaudit.questions import QUESTIONS
from aiaudit.scoring import score

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "optician.json"


def load_example() -> dict:
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def test_example_uses_a_known_industry():
    assert load_example()["industry"] == "retail"


def test_example_answers_cover_every_question():
    keys = {question.key for question in QUESTIONS}
    assert set(load_example()["answers"]) == keys


def test_example_has_an_ecommerce_opportunity():
    data = load_example()
    results = score(data["answers"], data["area_weights"], data["industry"])
    assert any(r.opportunity.area == "ecommerce" for r in results)


def test_example_admin_weight_is_applied():
    data = load_example()
    results = score(data["answers"], data["area_weights"], data["industry"])
    admin = [r for r in results if r.opportunity.area == "admin"]
    assert admin
    assert all(r.weight == 1.2 for r in admin)
