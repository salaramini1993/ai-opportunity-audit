import json
from datetime import date

from aiaudit.cli import main
from aiaudit.html_report import render_html
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
