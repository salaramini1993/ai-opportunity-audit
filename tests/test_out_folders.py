"""Tests for --out: make the folders of the report file, and report write errors."""

import json

from aiaudit.cli import main

SHOP = {"sells_products": True, "many_products": True, "multi_language": True}


def _answers(tmp_path):
    answers = tmp_path / "answers.json"
    answers.write_text(json.dumps({"business_name": "Shop", "answers": SHOP}))
    return answers


def test_out_makes_missing_folders(tmp_path):
    answers = _answers(tmp_path)
    out = tmp_path / "reports" / "2026" / "shop.md"
    assert main(["--answers", str(answers), "--out", str(out)]) == 0
    assert out.read_text(encoding="utf-8").startswith("#")


def test_out_existing_folder_still_works(tmp_path):
    answers = _answers(tmp_path)
    out = tmp_path / "shop.html"
    assert main(["--answers", str(answers), "--format", "html", "--out", str(out)]) == 0
    assert out.exists()


def test_out_error_is_printed_and_returns_2(tmp_path, capsys):
    answers = _answers(tmp_path)
    blocker = tmp_path / "file.txt"
    blocker.write_text("not a folder")
    out = blocker / "report.md"
    assert main(["--answers", str(answers), "--out", str(out)]) == 2
    err = capsys.readouterr().err
    assert "Error: cannot write the report:" in err
