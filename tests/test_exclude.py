"""Tests for the --exclude option that hides opportunities by key."""

import argparse
import csv
import io
import json
from pathlib import Path

import pytest

from aiaudit.catalog import CATALOG
from aiaudit.cli import main, parse_exclude
from aiaudit.scoring import score

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "bakery.json"


def shown_keys(capsys, extra: list[str]) -> list[str]:
    assert main(["--answers", str(EXAMPLE), "--format", "csv", *extra]) == 0
    rows = list(csv.DictReader(io.StringIO(capsys.readouterr().out)))
    return [row["key"] for row in rows]


def all_keys_for_example() -> list[str]:
    data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    results = score(data["answers"], data["area_weights"], data["industry"])
    return [r.opportunity.key for r in results]


def test_parse_exclude_accepts_a_known_key():
    key = CATALOG[0].key
    assert parse_exclude(key) == key


def test_parse_exclude_rejects_an_unknown_key():
    with pytest.raises(argparse.ArgumentTypeError, match="is not an opportunity key"):
        parse_exclude("no_such_opportunity")


def test_bad_exclude_key_is_a_usage_error(capsys):
    with pytest.raises(SystemExit) as info:
        main(["--answers", str(EXAMPLE), "--exclude", "no_such_opportunity"])
    assert info.value.code == 2
    assert "is not an opportunity key" in capsys.readouterr().err


def test_exclude_hides_one_opportunity(capsys):
    before = all_keys_for_example()
    hidden = before[0]
    after = shown_keys(capsys, ["--exclude", hidden])
    assert hidden not in after
    assert after == [key for key in before if key != hidden]


def test_exclude_can_be_repeated(capsys):
    before = all_keys_for_example()
    hidden = before[:2]
    after = shown_keys(capsys, ["--exclude", hidden[0], "--exclude", hidden[1]])
    assert after == before[2:]


def test_exclude_runs_before_top(capsys):
    before = all_keys_for_example()
    after = shown_keys(capsys, ["--exclude", before[0], "--top", "1"])
    assert after == [before[1]]


def test_exclude_is_empty_by_default(capsys):
    assert shown_keys(capsys, []) == all_keys_for_example()


def test_excluding_every_opportunity_prints_the_filter_warning(capsys):
    before = all_keys_for_example()
    args = ["--answers", str(EXAMPLE), "--format", "csv"]
    for key in before:
        args += ["--exclude", key]
    assert main(args) == 0
    assert "no opportunity is left after the filters" in capsys.readouterr().err
