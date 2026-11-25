"""Tests for the warning when the filters hide every opportunity."""

import json
from pathlib import Path

from aiaudit.cli import main

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "bakery.json"
WARNING = "Warning: no opportunity is left after the filters"


def test_warning_when_min_priority_hides_everything(capsys):
    assert main(["--answers", str(EXAMPLE), "--min-priority", "99", "--out", "/dev/null"]) == 0
    assert WARNING in capsys.readouterr().err


def test_no_warning_when_some_opportunities_remain(capsys):
    assert main(["--answers", str(EXAMPLE), "--top", "1", "--out", "/dev/null"]) == 0
    assert WARNING not in capsys.readouterr().err


def test_quiet_hides_the_empty_filter_warning(capsys):
    args = ["--answers", str(EXAMPLE), "--min-priority", "99", "--out", "/dev/null", "--quiet"]
    assert main(args) == 0
    assert WARNING not in capsys.readouterr().err


def test_no_warning_when_the_answers_already_have_no_opportunities(tmp_path, capsys):
    data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    data["answers"] = {key: False for key in data["answers"]}
    src = tmp_path / "none.json"
    src.write_text(json.dumps(data), encoding="utf-8")
    assert main(["--answers", str(src), "--min-priority", "99", "--out", "/dev/null"]) == 0
    assert WARNING not in capsys.readouterr().err
