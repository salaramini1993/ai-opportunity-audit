import json
from datetime import date

import pytest

from aiaudit.catalog import CATALOG, INDUSTRIES, CatalogError, Opportunity, parse_catalog
from aiaudit.cli import main
from aiaudit.questions import keys
from aiaudit.report import render_markdown
from aiaudit.scoring import score, validate_industry

ALL_YES = {k: True for k in keys()}


def item(**extra):
    base = {
        "key": "x",
        "area": "sales",
        "title": "X",
        "description": "Do X.",
        "signals": ["has_leads"],
        "base_effort": 1,
    }
    base.update(extra)
    return base


def test_catalog_has_four_industries():
    assert set(INDUSTRIES) == {"retail", "services", "manufacturing", "restaurant"}


def test_each_industry_has_opportunities():
    for industry in INDUSTRIES:
        assert any(o.industries and o.fits_industry(industry) for o in CATALOG)


def test_empty_industry_list_fits_all():
    opp = Opportunity("k", "sales", "T", "D", ("a",), 1)
    assert opp.fits_industry("retail")
    assert opp.fits_industry(None)


def test_tagged_opportunity_fits_only_its_industries():
    opp = Opportunity("k", "sales", "T", "D", ("a",), 1, industries=("retail",))
    assert opp.fits_industry("retail")
    assert not opp.fits_industry("restaurant")
    assert opp.fits_industry(None)


def test_parse_industries_field():
    data = {"areas": ["sales"], "industries": ["retail"], "opportunities": [item(industries=["retail"])]}
    _, items = parse_catalog(data)
    assert items[0].industries == ("retail",)


@pytest.mark.parametrize(
    "data, message",
    [
        ({"areas": ["sales"], "industries": ["retail"], "opportunities": [item(industries=["bank"])]}, "unknown industry"),
        ({"areas": ["sales"], "opportunities": [item(industries=["retail"])]}, "unknown industry"),
        ({"areas": ["sales"], "industries": ["retail"], "opportunities": [item(industries="retail")]}, "list of industry names"),
        ({"areas": ["sales"], "industries": ["retail", "retail"], "opportunities": [item()]}, "duplicate names"),
        ({"areas": ["sales"], "industries": [], "opportunities": [item()]}, "'industries' must be"),
    ],
)
def test_bad_industries_are_rejected(data, message):
    with pytest.raises(CatalogError, match=message):
        parse_catalog(data)


def test_score_without_industry_shows_all():
    assert len(score(ALL_YES)) == len(CATALOG)


def test_score_filters_by_industry():
    results = score(ALL_YES, industry="services")
    found = {r.opportunity.key for r in results}
    assert "lead_qualification" in found
    assert "ecommerce_return_reasons" not in found
    # Opportunities with no industry list apply to all industries.
    assert "meeting_notes" in found
    assert all(r.opportunity.fits_industry("services") for r in results)


@pytest.mark.parametrize("bad", ["bank", "", 3, True])
def test_bad_industry_is_rejected(bad):
    with pytest.raises(ValueError, match="industry"):
        validate_industry(bad)
    with pytest.raises(ValueError):
        score(ALL_YES, industry=bad)


def test_report_shows_industry():
    text = render_markdown("Cafe", score(ALL_YES, industry="restaurant"), today=date(2026, 1, 1), industry="restaurant")
    assert "Industry: restaurant" in text
    plain = render_markdown("Cafe", score(ALL_YES), today=date(2026, 1, 1))
    assert "Industry:" not in plain


def write_answers(tmp_path, **extra):
    path = tmp_path / "answers.json"
    path.write_text(json.dumps({"business_name": "Shop", "answers": ALL_YES, **extra}), encoding="utf-8")
    return path


def test_cli_industry_in_file(tmp_path, capsys):
    path = write_answers(tmp_path, industry="services")
    assert main(["--answers", str(path)]) == 0
    out = capsys.readouterr().out
    assert "Industry: services" in out
    # This opportunity is only for retail.
    assert "Return reasons analysis" not in out


def test_cli_option_replaces_file_industry(tmp_path, capsys):
    path = write_answers(tmp_path, industry="services")
    assert main(["--answers", str(path), "--industry", "retail"]) == 0
    assert "Industry: retail" in capsys.readouterr().out


def test_cli_bad_industry_in_file(tmp_path, capsys):
    path = write_answers(tmp_path, industry="bank")
    assert main(["--answers", str(path)]) == 2
    assert "Unknown industry" in capsys.readouterr().err


def test_cli_bad_industry_option(tmp_path):
    path = write_answers(tmp_path)
    with pytest.raises(SystemExit):
        main(["--answers", str(path), "--industry", "bank"])
