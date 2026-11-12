"""Tests that docs/answers.md matches the questions, areas and CLI."""

import json
import re
from pathlib import Path

from aiaudit.catalog import AREAS, INDUSTRIES
from aiaudit.questions import QUESTIONS
from aiaudit.scoring import score

ROOT = Path(__file__).resolve().parent.parent
DOC = (ROOT / "docs" / "answers.md").read_text(encoding="utf-8")


def test_doc_lists_every_question_key():
    for q in QUESTIONS:
        assert f"| `{q.key}` |" in DOC, q.key


def test_doc_lists_every_area():
    for area in AREAS:
        assert f"- `{area}`" in DOC, area


def test_doc_mentions_every_industry():
    for name in INDUSTRIES:
        assert name in DOC, name


def test_doc_example_runs_through_scoring():
    block = re.search(r"```json\n(.*?)\n```", DOC, re.DOTALL)
    assert block is not None
    data = json.loads(block.group(1))
    results = score(data["answers"], data["area_weights"], data["industry"])
    assert results
