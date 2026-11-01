from datetime import date

import pytest

from aiaudit.cli import main
from aiaudit.i18n import LANGUAGES, TEXT, t, validate_language
from aiaudit.report import render_markdown
from aiaudit.scoring import score

ANSWERS = {"sells_products": True, "many_products": True, "multi_language": True}


def test_all_languages_have_the_same_keys():
    keys = set(TEXT["en"])
    for lang in LANGUAGES:
        assert set(TEXT[lang]) == keys, lang


def test_placeholders_match_english():
    import string

    def fields(text):
        return {f for _, f, _, _ in string.Formatter().parse(text) if f}

    for lang in LANGUAGES:
        for key, text in TEXT[lang].items():
            assert fields(text) == fields(TEXT["en"][key]), (lang, key)


def test_unknown_language_raises():
    with pytest.raises(ValueError, match="unknown language"):
        validate_language("xx")
    with pytest.raises(ValueError):
        render_markdown("Shop", [], lang="xx")


def test_t_fills_values():
    assert t("sv", "found", count=3) == "Hittade möjligheter: 3"


def test_swedish_empty_report():
    text = render_markdown("Test AB", [], today=date(2026, 1, 1), lang="sv")
    assert "# AI-möjlighetsanalys: Test AB" in text
    assert "Datum: 2026-01-01" in text
    assert "inga tydliga AI-möjligheter" in text


def test_swedish_report_labels():
    results = score(ANSWERS)
    text = render_markdown("Shop", results, today=date(2026, 1, 1), lang="sv")
    assert "## Sammanfattning" in text
    assert "## Prioriteringslista" in text
    assert "| # | Möjlighet | Område |" in text
    assert "## Nästa steg" in text
    assert "- låg: under 50 EUR" in text
    # The catalog text stays in English in this version.
    assert "Product descriptions and listings" in text
    # The types in the table are in Swedish.
    swedish_types = {t("sv", f"quadrant.{r.quadrant}") for r in results}
    for name in swedish_types:
        assert f"| {name} |" in text


def test_english_is_default():
    results = score(ANSWERS)
    day = date(2026, 1, 1)
    assert render_markdown("Shop", results, today=day) == render_markdown(
        "Shop", results, today=day, lang="en"
    )


def test_cli_lang_option(tmp_path, capsys):
    answers = tmp_path / "a.json"
    answers.write_text('{"business_name": "Bageri", "answers": {"sells_products": true}}')
    out = tmp_path / "rapport.md"
    assert main(["--answers", str(answers), "--lang", "sv", "--out", str(out)]) == 0
    assert "# AI-möjlighetsanalys: Bageri" in out.read_text(encoding="utf-8")


def test_cli_rejects_unknown_lang(tmp_path):
    answers = tmp_path / "a.json"
    answers.write_text('{"answers": {}}')
    with pytest.raises(SystemExit):
        main(["--answers", str(answers), "--lang", "xx"])
