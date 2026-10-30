"""Tests for the HR opportunities."""

from datetime import date

from aiaudit.catalog import AREAS, by_key
from aiaudit.questions import keys
from aiaudit.report import render_markdown
from aiaudit.scoring import score


def test_hr_is_an_area():
    assert "hr" in AREAS


def test_hr_opportunities_exist():
    for key in ("hr_job_ads", "hr_cv_screening"):
        item = by_key(key)
        assert item.area == "hr"
        assert set(item.signals) <= keys()


def test_cv_screening_requires_human_review():
    item = by_key("hr_cv_screening")
    text = " ".join(item.risks).lower()
    assert "a person" in text
    assert "personal data" in text


def test_hiring_answers_find_hr_opportunities():
    answers = {"hires_often": True, "writes_job_ads": True, "many_applicants": True}
    results = score(answers)
    found = {r.opportunity.key for r in results}
    assert {"hr_job_ads", "hr_cv_screening"} <= found


def test_no_hiring_gives_no_hr_opportunities():
    results = score({"many_meetings": True})
    assert all(r.opportunity.area != "hr" for r in results)


def test_hr_weight_is_accepted():
    answers = {"hires_often": True, "many_applicants": True}
    results = score(answers, weights={"hr": 2})
    cv = next(r for r in results if r.opportunity.key == "hr_cv_screening")
    assert cv.weight == 2.0


def test_report_shows_hr_opportunity():
    results = score({"hires_often": True, "many_applicants": True})
    text = render_markdown("Agency", results, today=date(2026, 1, 1))
    assert "CV screening with human review" in text
