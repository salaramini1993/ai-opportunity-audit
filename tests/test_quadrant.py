"""Tests for the --quadrant option that shows one quadrant only."""

import csv
import io
from pathlib import Path

import pytest

from aiaudit.cli import main
from aiaudit.scoring import QUADRANTS

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "bakery.json"


def csv_rows(capsys, *args: str) -> list[dict[str, str]]:
    assert main(["--answers", str(EXAMPLE), "--format", "csv", *args]) == 0
    return list(csv.DictReader(io.StringIO(capsys.readouterr().out)))


def test_without_the_option_the_list_is_not_narrowed(capsys):
    rows = csv_rows(capsys)
    assert len(rows) > 1
    assert len({row["quadrant"] for row in rows}) > 1


@pytest.mark.parametrize("name", QUADRANTS)
def test_only_the_chosen_quadrant_is_shown(capsys, name):
    rows = csv_rows(capsys, "--quadrant", name)
    assert all(row["quadrant"] == name for row in rows)


def test_the_quadrants_add_up_to_all_rows(capsys):
    total = len(csv_rows(capsys))
    by_quadrant = sum(len(csv_rows(capsys, "--quadrant", name)) for name in QUADRANTS)
    assert by_quadrant == total


def test_an_unknown_quadrant_is_rejected(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--answers", str(EXAMPLE), "--quadrant", "nonsense"])
    assert exc.value.code == 2
    assert "invalid choice" in capsys.readouterr().err


def test_a_quadrant_with_no_opportunities_prints_the_warning(capsys):
    # A quadrant that no opportunity falls into, so the warning must appear.
    with_all = csv_rows(capsys)
    present = {row["quadrant"] for row in with_all}
    empty = [name for name in QUADRANTS if name not in present]
    if not empty:
        pytest.skip("every quadrant has an opportunity for this example")
    assert main(["--answers", str(EXAMPLE), "--format", "csv", "--quadrant", empty[0]]) == 0
    captured = capsys.readouterr()
    assert "no opportunity is left after the filters" in captured.err
