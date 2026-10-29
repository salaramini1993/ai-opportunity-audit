import json
from datetime import date

import pytest

from aiaudit.cli import main, parse_weight
from aiaudit.questions import keys
from aiaudit.report import render_markdown
from aiaudit.scoring import score, validate_weights

ALL_YES = {k: True for k in keys()}


def test_default_weight_is_one():
    for r in score(ALL_YES):
        assert r.weight == 1.0
        assert r.priority == round(r.impact / r.effort, 2)


def test_weight_multiplies_priority():
    plain = {r.opportunity.key: r for r in score(ALL_YES)}
    weighted = score(ALL_YES, {"finance": 2})
    for r in weighted:
        base = plain[r.opportunity.key]
        if r.opportunity.area == "finance":
            assert r.priority == round(base.impact * 2 / base.effort, 2)
        else:
            assert r.priority == base.priority
        # The weight does not change the type.
        assert r.quadrant == base.quadrant


def test_high_weight_moves_area_to_top():
    results = score(ALL_YES, {"admin": 5})
    assert results[0].opportunity.area == "admin"


def test_results_stay_sorted_with_weights():
    results = score(ALL_YES, {"sales": 3, "marketing": 0.5})
    priorities = [r.priority for r in results]
    assert priorities == sorted(priorities, reverse=True)


@pytest.mark.parametrize(
    "weights",
    [{"not_an_area": 2}, {"sales": True}, {"sales": "2"}, {"sales": 0}, {"sales": 6}],
)
def test_bad_weights_are_rejected(weights):
    with pytest.raises(ValueError):
        validate_weights(weights)


def test_parse_weight():
    assert parse_weight("sales=2") == ("sales", 2.0)
    assert parse_weight(" sales =1.5") == ("sales", 1.5)


def test_report_lists_weights():
    results = score(ALL_YES, {"finance": 2})
    text = render_markdown("Shop", results, today=date(2026, 1, 1))
    assert "Area weights used for the priority:" in text
    assert "- finance: 2" in text


def test_report_without_weights_has_no_weight_list():
    text = render_markdown("Shop", score(ALL_YES), today=date(2026, 1, 1))
    assert "Area weights" not in text


def test_cli_reads_weights_from_file_and_flag(tmp_path, capsys):
    path = tmp_path / "answers.json"
    path.write_text(
        json.dumps({"answers": ALL_YES, "area_weights": {"finance": 2, "sales": 3}}),
        encoding="utf-8",
    )
    assert main(["--answers", str(path), "--weight", "sales=1.5"]) == 0
    out = capsys.readouterr().out
    assert "- finance: 2" in out
    # The command line value replaces the value in the file.
    assert "- sales: 1.5" in out


def test_cli_rejects_bad_weight(tmp_path, capsys):
    path = tmp_path / "answers.json"
    path.write_text(json.dumps({"answers": ALL_YES}), encoding="utf-8")
    assert main(["--answers", str(path), "--weight", "nowhere=2"]) == 2
    assert "Unknown area" in capsys.readouterr().err


def test_cli_rejects_bad_weight_object(tmp_path, capsys):
    path = tmp_path / "answers.json"
    path.write_text(json.dumps({"answers": {}, "area_weights": [1]}), encoding="utf-8")
    assert main(["--answers", str(path)]) == 2
    assert "area_weights" in capsys.readouterr().err
