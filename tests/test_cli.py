"""Tests for the command-line interface (JSON input, bad input, output files)."""

import json
from pathlib import Path

import pytest

from aiaudit.catalog import AREAS, CATALOG, INDUSTRIES
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


def test_list_opportunities_prints_every_key(capsys):
    assert main(["--list-opportunities"]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert len(lines) == len(CATALOG)
    first = CATALOG[0]
    assert lines[0] == f"{first.key}: {first.area}: {first.title}"


def test_list_opportunities_needs_no_answers_file(capsys):
    assert main(["--list-opportunities"]) == 0
    out = capsys.readouterr().out
    assert out.endswith("\n")
    assert all(item.key + ":" in out for item in CATALOG)


def test_list_areas_prints_every_area(capsys):
    assert main(["--list-areas"]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert lines == list(AREAS)


def test_list_areas_output_works_with_weight_option(capsys):
    assert main(["--list-areas"]) == 0
    for name in capsys.readouterr().out.splitlines():
        assert main(["--answers", str(EXAMPLES[0]), "--weight", f"{name}=1"]) == 0
        capsys.readouterr()


def test_list_industries_prints_every_industry(capsys):
    assert main(["--list-industries"]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert lines == list(INDUSTRIES)


def test_list_industries_output_works_with_industry_option(capsys):
    assert main(["--list-industries"]) == 0
    for name in capsys.readouterr().out.splitlines():
        assert main(["--answers", str(EXAMPLES[0]), "--industry", name]) == 0
        capsys.readouterr()


def test_top_option_limits_the_priority_list(capsys):
    example = str(ROOT / "examples" / "online_shop.json")
    assert main(["--answers", example, "--format", "csv"]) == 0
    full = [line for line in capsys.readouterr().out.splitlines() if line]
    assert main(["--answers", example, "--format", "csv", "--top", "2"]) == 0
    top = [line for line in capsys.readouterr().out.splitlines() if line]
    assert len(full) > 3
    assert len(top) == 3  # header row and two opportunities
    assert top == full[:3]


def test_top_option_must_be_one_or_more(capsys):
    example = str(ROOT / "examples" / "online_shop.json")
    with pytest.raises(SystemExit) as excinfo:
        main(["--answers", example, "--top", "0"])
    assert excinfo.value.code == 2
    assert "must be 1 or more" in capsys.readouterr().err


def test_top_option_must_be_a_whole_number(capsys):
    example = str(ROOT / "examples" / "online_shop.json")
    with pytest.raises(SystemExit) as excinfo:
        main(["--answers", example, "--top", "two"])
    assert excinfo.value.code == 2
    assert "is not a whole number" in capsys.readouterr().err


def test_list_languages_prints_every_language(capsys):
    from aiaudit.i18n import LANGUAGES

    assert main(["--list-languages"]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert [line.split(":")[0] for line in lines] == list(LANGUAGES)
    assert "sv: Swedish" in lines


def test_list_languages_output_works_with_lang_option(capsys):
    from aiaudit.cli import list_languages
    from aiaudit.i18n import LANGUAGES

    for line in list_languages().splitlines():
        code = line.split(":")[0]
        assert code in LANGUAGES
        assert main(["--answers", str(ROOT / "examples" / "online_shop.json"), "--lang", code]) == 0
        capsys.readouterr()


def test_list_formats_prints_every_format(capsys):
    from aiaudit.cli import FORMATS

    assert main(["--list-formats"]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert lines == list(FORMATS)
    assert "csv" in lines


def test_list_formats_output_works_with_format_option(capsys):
    from aiaudit.cli import list_formats

    for name in list_formats().splitlines():
        shop = str(ROOT / "examples" / "online_shop.json")
        assert main(["--answers", shop, "--format", name]) == 0
        capsys.readouterr()
