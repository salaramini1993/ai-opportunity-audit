"""Tests that every example file uses only known keys and values."""

import json
from pathlib import Path

from aiaudit import questions
from aiaudit.catalog import AREAS, INDUSTRIES

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = sorted((ROOT / "examples").glob("*.json"))


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_every_example_industry_is_known():
    for path in EXAMPLES:
        industry = load(path).get("industry")
        if industry is not None:
            assert industry in INDUSTRIES, f"{path.name} has unknown industry {industry}"


def test_every_example_area_weight_is_a_known_area():
    for path in EXAMPLES:
        for area in load(path).get("area_weights", {}):
            assert area in AREAS, f"{path.name} has unknown area {area}"


def test_every_example_answer_is_a_known_question():
    known = questions.keys()
    for path in EXAMPLES:
        for key in load(path)["answers"]:
            assert key in known, f"{path.name} has unknown question {key}"


def test_every_example_answer_has_a_valid_value():
    for path in EXAMPLES:
        for key, value in load(path)["answers"].items():
            if isinstance(value, bool):
                continue
            assert isinstance(value, int) and 0 <= value <= 3, (
                f"{path.name}: {key} must be a bool or a whole number from 0 to 3"
            )
