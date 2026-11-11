"""Tests for the command-line interface (JSON input, bad input, output files)."""

import json
from pathlib import Path

import pytest

from aiaudit.cli import main
from aiaudit.questions import QUESTIONS

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = sorted((ROOT / "examples").glob("*.json"))


def write_json(path: Path, data: object) -> Path:
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


@pytest.mark.parametrize("example", EXAMPLES, ids=lambda p: p.name)
def test_every_example_runs(example, capsys):
    assert main(["--answers", str(example)]) == 0
    out = capsys.readouterr().out
    assert out.startswith("# AI Opportunity Audit")


def test_output_file_is_written(tmp_path, capsys):
    out_file = tmp_path / "report.md"
    code = main(["--answers", str(ROOT / "examples" / "online_shop.json"), "--out", str(out_file)])
    assert code == 0
    assert out_file.read_text(encoding="utf-8").startswith("# AI Opportunity Audit")
    assert "Report written to" in capsys.readouterr().out


def test_name_option_replaces_file_name(tmp_path):
    src = write_json(tmp_path / "a.json", {"business_name": "Old", "answers": {}})
    out_file = tmp_path / "r.md"
    main(["--answers", str(src), "--name", "New Name", "--out", str(out_file)])
    assert "New Name" in out_file.read_text(encoding="utf-8")


def test_invalid_json_returns_error(tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    assert main(["--answers", str(bad)]) == 2
    assert "Error:" in capsys.readouterr().err


def test_missing_answers_key_is_an_error(tmp_path):
    src = write_json(tmp_path / "no_answers.json", {"business_name": "X"})
    with pytest.raises(KeyError):
        main(["--answers", str(src)])


def test_unknown_question_key_returns_error(tmp_path, capsys):
    src = write_json(tmp_path / "unknown.json", {"answers": {"not_a_question": True}})
    assert main(["--answers", str(src)]) == 2
    assert "Unknown" in capsys.readouterr().err


def test_bad_weight_format_is_rejected(tmp_path):
    src = write_json(tmp_path / "a.json", {"answers": {}})
    with pytest.raises(SystemExit):
        main(["--answers", str(src), "--weight", "customer_support"])


def test_weight_must_be_a_number(tmp_path):
    src = write_json(tmp_path / "a.json", {"answers": {}})
    with pytest.raises(SystemExit):
        main(["--answers", str(src), "--weight", "admin=lots"])


def test_bad_industry_is_rejected(tmp_path):
    src = write_json(tmp_path / "a.json", {"answers": {}})
    with pytest.raises(SystemExit):
        main(["--answers", str(src), "--industry", "space"])


def test_answers_and_interactive_are_exclusive(tmp_path):
    src = write_json(tmp_path / "a.json", {"answers": {}})
    with pytest.raises(SystemExit):
        main(["--answers", str(src), "--interactive"])


def test_csv_output_has_header(tmp_path):
    out_file = tmp_path / "p.csv"
    answers = str(ROOT / "examples" / "online_shop.json")
    main(["--answers", answers, "--format", "csv", "--out", str(out_file)])
    first_line = out_file.read_text(encoding="utf-8").splitlines()[0]
    assert first_line.startswith("rank,key,title")


def test_command_line_weight_beats_file_weight(tmp_path):
    answers = {"support_volume": True, "repeat_questions": True}
    file_low = write_json(
        tmp_path / "low.json", {"answers": answers, "area_weights": {"customer_support": 0.5}}
    )
    file_high = write_json(
        tmp_path / "high.json", {"answers": answers, "area_weights": {"customer_support": 4}}
    )
    # The file says 0.5, but the command line says 4. The output must match a file that says 4.
    override = tmp_path / "override.csv"
    expected = tmp_path / "expected.csv"
    main(["--answers", str(file_low), "--weight", "customer_support=4",
          "--format", "csv", "--out", str(override)])
    main(["--answers", str(file_high), "--format", "csv", "--out", str(expected)])
    assert override.read_bytes() == expected.read_bytes()


def test_version_option_prints_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert capsys.readouterr().out.startswith("aiaudit ")


def test_list_questions_prints_every_key(capsys):
    assert main(["--list-questions"]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert len(lines) == len(QUESTIONS)
    assert lines[0] == f"{QUESTIONS[0].key}: {QUESTIONS[0].text}"


def test_list_questions_needs_no_answers_file(capsys):
    assert main(["--list-questions"]) == 0
    assert "sells_products:" in capsys.readouterr().out


def test_missing_source_is_an_error(capsys):
    with pytest.raises(SystemExit) as exc:
        main([])
    assert exc.value.code == 2
    assert "--answers" in capsys.readouterr().err
