"""Tests that docs/report_formats.md covers every report format and CSV column."""

import re
from pathlib import Path

from aiaudit.cli import main
from aiaudit.csv_report import COLUMNS

ROOT = Path(__file__).resolve().parent.parent
DOC = (ROOT / "docs" / "report_formats.md").read_text(encoding="utf-8")


def format_choices(capsys) -> list[str]:
    """Return the values that --format accepts, from the help text."""
    try:
        main(["--help"])
    except SystemExit:
        pass
    text = capsys.readouterr().out
    match = re.search(r"--format \{([^}]+)\}", text)
    assert match, "--format choices not found in help text"
    return match.group(1).split(",")


def test_doc_covers_every_format(capsys):
    formats = format_choices(capsys)
    assert set(formats) == {"markdown", "html", "csv", "json"}
    headings = {"markdown": "Markdown", "html": "HTML", "csv": "CSV", "json": "JSON"}
    for name in formats:
        assert f"## {headings[name]}" in DOC, f"{name} has no section"


def test_doc_lists_every_csv_column():
    for column in COLUMNS:
        assert f"`{column}`" in DOC, f"{column} is not in docs/report_formats.md"


def test_doc_lists_no_unknown_csv_column():
    listed = re.findall(r"^- `([a-z_]+)`:", DOC, flags=re.MULTILINE)
    assert listed == list(COLUMNS)
