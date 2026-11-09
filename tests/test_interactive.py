"""Tests for the interactive question mode in the command-line interface."""

import pytest

from aiaudit.cli import ask_interactive, main, parse_interactive_answer
from aiaudit.questions import QUESTIONS
from aiaudit.scoring import MAX_SCALE


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("y", True),
        ("YES", True),
        (" n ", False),
        ("No", False),
        ("0", 0),
        (str(MAX_SCALE), MAX_SCALE),
    ],
)
def test_valid_answers_are_parsed(raw, expected):
    assert parse_interactive_answer(raw) == expected


@pytest.mark.parametrize("raw", ["", "maybe", "-1", str(MAX_SCALE + 1), "1.5"])
def test_invalid_answers_return_none(raw):
    assert parse_interactive_answer(raw) is None


def test_ask_interactive_repeats_until_answer_is_valid(monkeypatch, capsys):
    replies = iter(["maybe", "", "y"] + ["n"] * (len(QUESTIONS) - 1))
    monkeypatch.setattr("builtins.input", lambda prompt: next(replies))

    answers = ask_interactive()

    assert len(answers) == len(QUESTIONS)
    assert answers[QUESTIONS[0].key] is True
    assert capsys.readouterr().out.count("Type y, n or a number") == 2


def test_interactive_main_writes_report(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt: "2")
    out_file = tmp_path / "interactive.md"

    code = main(["--interactive", "--name", "Test Shop", "--out", str(out_file)])

    assert code == 0
    text = out_file.read_text(encoding="utf-8")
    assert "Test Shop" in text
    assert "Report written to" in capsys.readouterr().out
