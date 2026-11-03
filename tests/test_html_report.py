import json
from datetime import date

import pytest

from aiaudit.cli import main
from aiaudit.html_report import render_html
from aiaudit.i18n import text_direction
from aiaudit.scoring import score

SHOP = {"sells_products": True, "many_products": True, "multi_language": True}


def test_empty_html_report_has_message():
    text = render_html("Test AB", [], today=date(2026, 1, 1))
    assert text.startswith("<!doctype html>")
    assert "<h1>AI Opportunity Audit: Test AB</h1>" in text
    assert "no clear AI opportunities" in text
    assert text.rstrip().endswith("</html>")


def test_html_report_lists_opportunities():
    results = score(SHOP)
    text = render_html("Shop", results, today=date(2026, 1, 1))
    assert "Product descriptions and listings" in text
    assert "<table>" in text
    # One header row and one row for each result.
    assert text.count("<tr>") == len(results) + 1
    assert "Date: 2026-01-01" in text
    assert "<h2>Next step</h2>" in text


def test_html_report_escapes_text():
    text = render_html("<b>Bad & Co</b>", [], today=date(2026, 1, 1))
    assert "<b>Bad" not in text
    assert "&lt;b&gt;Bad &amp; Co&lt;/b&gt;" in text


def test_html_report_shows_industry():
    text = render_html("Shop", score(SHOP), industry="retail")
    assert "<p>Industry: retail</p>" in text


def test_cli_writes_html_file(tmp_path):
    answers = tmp_path / "shop.json"
    answers.write_text(json.dumps({"business_name": "Shop", "answers": SHOP}))
    out = tmp_path / "report.html"
    code = main(["--answers", str(answers), "--format", "html", "--out", str(out)])
    assert code == 0
    text = out.read_text(encoding="utf-8")
    assert text.startswith("<!doctype html>")
    assert "AI Opportunity Audit: Shop" in text


def test_cli_default_format_is_markdown(tmp_path, capsys):
    answers = tmp_path / "shop.json"
    answers.write_text(json.dumps({"business_name": "Shop", "answers": SHOP}))
    assert main(["--answers", str(answers)]) == 0
    assert capsys.readouterr().out.startswith("# AI Opportunity Audit: Shop")


def test_swedish_html_report_labels():
    results = score(SHOP)
    text = render_html("Butik", results, today=date(2026, 1, 1), lang="sv")
    assert '<html lang="sv" dir="ltr">' in text
    assert "<h1>AI-möjlighetsanalys: Butik</h1>" in text
    assert "<p>Datum: 2026-01-01</p>" in text
    assert "<h2>Sammanfattning</h2>" in text
    assert "<th>Möjlighet</th>" in text
    assert "<h2>Effekt och insats</h2>" in text
    assert "<h2>Handlingsplan för 30/60/90 dagar</h2>" in text
    assert "<h2>Nästa steg</h2>" in text
    # The English headings are not in the Swedish report.
    assert "<h2>Summary</h2>" not in text
    assert "<h2>Next step</h2>" not in text


def test_swedish_html_report_uses_catalog_translation():
    results = score(SHOP)
    first = results[0].opportunity
    text = render_html("Butik", results, lang="sv")
    assert f"<h3>{first.text('title', 'sv')}</h3>" in text
    assert first.text("title", "sv") != first.title


def test_swedish_empty_html_report():
    text = render_html("Butik", [], today=date(2026, 1, 1), lang="sv")
    assert "inga tydliga AI-möjligheter" in text


def test_html_report_rejects_unknown_language():
    import pytest

    with pytest.raises(ValueError):
        render_html("Shop", [], lang="xx")


def test_cli_swedish_html(tmp_path, capsys):
    answers = tmp_path / "shop.json"
    answers.write_text(json.dumps({"business_name": "Butik", "answers": SHOP}))
    assert main(["--answers", str(answers), "--format", "html", "--lang", "sv"]) == 0
    assert "<h2>Sammanfattning</h2>" in capsys.readouterr().out


def test_text_direction():
    assert text_direction("en") == "ltr"
    assert text_direction("sv") == "ltr"
    assert text_direction("fa") == "rtl"
    with pytest.raises(ValueError):
        text_direction("xx")


def test_persian_html_report_is_right_to_left():
    results = score(SHOP)
    text = render_html("Shop", results, today=date(2026, 1, 1), lang="fa")
    assert '<html lang="fa" dir="rtl">' in text
    # The table alignment follows the text direction.
    assert "text-align: start" in text
    assert "text-align: left" not in text
    assert "text-align: right" not in text


def test_chart_keeps_left_to_right_layout_in_persian_report():
    text = render_html("Shop", score(SHOP), today=date(2026, 1, 1), lang="fa")
    assert '<svg class="chart"' in text
    assert 'direction="ltr"' in text


def test_english_html_report_is_left_to_right():
    text = render_html("Shop", score(SHOP), today=date(2026, 1, 1))
    assert '<html lang="en" dir="ltr">' in text
