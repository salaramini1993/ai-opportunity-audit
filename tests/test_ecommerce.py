"""Tests for the e-commerce opportunities."""

from datetime import date

from aiaudit.catalog import AREAS, by_key
from aiaudit.questions import keys
from aiaudit.report import render_markdown
from aiaudit.scoring import score

KEYS = ("ecommerce_review_replies", "ecommerce_return_reasons")


def test_ecommerce_is_an_area():
    assert "ecommerce" in AREAS


def test_ecommerce_opportunities_exist():
    for key in KEYS:
        item = by_key(key)
        assert item.area == "ecommerce"
        assert set(item.signals) <= keys()
        assert item.risks


def test_review_replies_require_a_check():
    text = " ".join(by_key("ecommerce_review_replies").risks).lower()
    assert "check" in text
    assert "personal data" in text


def test_shop_answers_find_ecommerce_opportunities():
    answers = {"sells_online": True, "gets_reviews": True, "many_returns": True}
    found = {r.opportunity.key for r in score(answers)}
    assert set(KEYS) <= found


def test_no_web_shop_gives_no_ecommerce_opportunities():
    results = score({"many_meetings": True})
    assert all(r.opportunity.area != "ecommerce" for r in results)


def test_ecommerce_weight_is_accepted():
    answers = {"sells_online": True, "many_returns": True}
    results = score(answers, weights={"ecommerce": 3})
    item = next(r for r in results if r.opportunity.key == "ecommerce_return_reasons")
    assert item.weight == 3.0


def test_report_shows_ecommerce_opportunity():
    results = score({"sells_online": True, "gets_reviews": True})
    text = render_markdown("Shop", results, today=date(2026, 1, 1))
    assert "Replies to product reviews" in text
