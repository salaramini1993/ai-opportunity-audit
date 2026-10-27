import pytest

from aiaudit.catalog import CATALOG
from aiaudit.questions import keys
from aiaudit.scoring import score, validate_answers


def test_every_signal_is_a_question():
    known = keys()
    for opp in CATALOG:
        for signal in opp.signals:
            assert signal in known, f"{opp.key} uses unknown signal {signal}"


def test_catalog_keys_are_unique():
    all_keys = [o.key for o in CATALOG]
    assert len(all_keys) == len(set(all_keys))


def test_no_answers_gives_no_results():
    assert score({}) == []


def test_support_answers_find_support_opportunities():
    results = score({"support_volume": True, "repeat_questions": True, "email_heavy": True})
    found = {r.opportunity.key for r in results}
    assert "support_faq_assistant" in found
    assert "support_reply_drafts" in found


def test_results_sorted_by_priority():
    answers = {k: True for k in keys()}
    results = score(answers)
    priorities = [r.priority for r in results]
    assert priorities == sorted(priorities, reverse=True)


def test_unknown_key_is_rejected():
    with pytest.raises(ValueError):
        validate_answers({"not_a_question": True})


def test_non_bool_is_rejected():
    with pytest.raises(ValueError):
        validate_answers({"sells_products": "yes"})
