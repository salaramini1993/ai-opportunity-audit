"""Tests for the --quiet option."""

import json
from pathlib import Path

from aiaudit.cli import main
from aiaudit.questions import QUESTIONS

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "bakery.json"


def write_short_answers(tmp_path) -> Path:
    data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    del data["answers"][QUESTIONS[0].key]
    src = tmp_path / "short.json"
    src.write_text(json.dumps(data), encoding="utf-8")
    return src


def test_quiet_hides_the_missing_answers_warning(tmp_path, capsys):
    src = write_short_answers(tmp_path)
    assert main(["--answers", str(src), "--quiet"]) == 0
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out.startswith("# AI Opportunity Audit")


def test_warning_is_still_printed_without_quiet(tmp_path, capsys):
    src = write_short_answers(tmp_path)
    assert main(["--answers", str(src)]) == 0
    assert "Warning: no answer" in capsys.readouterr().err


def test_quiet_does_not_hide_errors(tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    assert main(["--answers", str(bad), "--quiet"]) == 2
    assert "Error:" in capsys.readouterr().err
