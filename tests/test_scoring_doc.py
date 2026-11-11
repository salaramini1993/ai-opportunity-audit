"""Tests that docs/scoring.md matches the values in aiaudit/scoring.py."""

from pathlib import Path

from aiaudit import scoring

ROOT = Path(__file__).resolve().parent.parent
DOC = (ROOT / "docs" / "scoring.md").read_text(encoding="utf-8")


def test_doc_states_the_fit_threshold():
    assert f"at least {scoring.MIN_FIT}" in DOC


def test_doc_states_the_weight_range():
    assert f"from {scoring.MIN_WEIGHT} to {scoring.MAX_WEIGHT}" in DOC


def test_doc_states_the_answer_scale():
    assert f"from 0 to {scoring.MAX_SCALE}" in DOC


def test_doc_quadrant_table_matches_code():
    assert "| 3 to 5 | 1 or 2 | quick win |" in DOC
    assert "| 3 to 5 | 3 to 5 | strategic project |" in DOC
    assert "| 1 or 2 | 1 or 2 | small improvement |" in DOC
    assert "| 1 or 2 | 3 to 5 | not now |" in DOC
