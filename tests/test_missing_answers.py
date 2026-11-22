"""Tests for the warning about questions that an answers file leaves out."""

import json
from pathlib import Path

from aiaudit.cli import main, missing_question_keys
from aiaudit.questions import QUESTIONS

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "bakery.json"


def test_no_keys_are_missing_when_every_question_is_answered():
    answers = {q.key: False for q in QUESTIONS}
    assert missing_question_keys(answers) == []


def test_missing_keys_are_listed_in_question_order():
    answers = {q.key: True for q in QUESTIONS[1:]}
    assert missing_question_keys(answers) == [QUESTIONS[0].key]


def test_all_keys_are_missing_from_an_empty_answer_set():
    assert missing_question_keys({}) == [q.key for q in QUESTIONS]


def test_warning_is_printed_for_a_short_answers_file(tmp_path, capsys):
    data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    dropped = QUESTIONS[0].key
    del data["answers"][dropped]
    src = tmp_path / "short.json"
    src.write_text(json.dumps(data), encoding="utf-8")

    assert main(["--answers", str(src)]) == 0
    captured = capsys.readouterr()
    assert "Warning: no answer for 1 question(s)" in captured.err
    assert dropped in captured.err
    assert captured.out.startswith("# AI Opportunity Audit")


def test_no_warning_for_a_complete_answers_file(capsys):
    assert main(["--answers", str(EXAMPLE)]) == 0
    assert "Warning" not in capsys.readouterr().err
