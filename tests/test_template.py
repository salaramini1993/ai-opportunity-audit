"""Tests for the --template option, which prints a blank answers file."""

import json

from aiaudit.cli import answers_template, main
from aiaudit.questions import QUESTIONS
from aiaudit.scoring import validate_answers


def test_template_is_valid_json():
    data = json.loads(answers_template())
    assert data["business_name"]
    assert isinstance(data["answers"], dict)


def test_template_has_every_question_key_set_to_false():
    answers = json.loads(answers_template())["answers"]
    assert set(answers) == {q.key for q in QUESTIONS}
    assert all(value is False for value in answers.values())


def test_template_passes_answer_validation():
    answers = json.loads(answers_template())["answers"]
    validate_answers(answers)


def test_template_option_prints_the_template_and_stops(capsys):
    assert main(["--template"]) == 0
    out = capsys.readouterr().out
    assert json.loads(out) == json.loads(answers_template())


def test_template_file_can_be_used_as_answers(tmp_path, capsys):
    src = tmp_path / "blank.json"
    src.write_text(answers_template(), encoding="utf-8")
    assert main(["--answers", str(src)]) == 0
    assert capsys.readouterr().out.startswith("# AI Opportunity Audit")
