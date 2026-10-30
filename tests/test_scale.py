import pytest

from aiaudit.cli import parse_interactive_answer
from aiaudit.scoring import score, signal_strength, validate_answers

SUPPORT = ("support_volume", "repeat_questions", "email_heavy")


def by_key(results):
    return {r.opportunity.key: r for r in results}


def test_signal_strength_values():
    assert signal_strength(True) == 1.0
    assert signal_strength(False) == 0.0
    assert signal_strength(0) == 0.0
    assert signal_strength(3) == 1.0
    assert signal_strength(1) == pytest.approx(1 / 3)


def test_scale_3_gives_same_result_as_true():
    yes = score({k: True for k in SUPPORT})
    full = score({k: 3 for k in SUPPORT})
    assert yes == full


def test_scale_0_gives_same_result_as_false():
    assert score({k: 0 for k in SUPPORT}) == score({k: False for k in SUPPORT})


def test_lower_scale_gives_lower_fit():
    full = by_key(score({k: 3 for k in SUPPORT}))
    part = by_key(score({k: 2 for k in SUPPORT}))
    key = "support_faq_assistant"
    assert key in full and key in part
    assert part[key].fit < full[key].fit


def test_low_scale_can_drop_an_opportunity():
    results = by_key(score({k: 1 for k in SUPPORT}))
    assert "support_faq_assistant" not in results


def test_mixed_bool_and_scale_answers():
    results = score({"support_volume": True, "repeat_questions": 2, "email_heavy": False})
    assert all(0.0 <= r.fit <= 1.0 for r in results)


@pytest.mark.parametrize("value", [4, -1, 1.5, "2", None])
def test_bad_scale_value_is_rejected(value):
    with pytest.raises(ValueError):
        validate_answers({"sells_products": value})


@pytest.mark.parametrize(
    "raw, expected",
    [("y", True), ("Yes", True), ("n", False), ("no", False), ("0", 0), (" 3 ", 3), ("2", 2)],
)
def test_parse_interactive_answer(raw, expected):
    assert parse_interactive_answer(raw) == expected


@pytest.mark.parametrize("raw", ["4", "-1", "maybe", "", "1.5"])
def test_parse_interactive_answer_rejects_bad_text(raw):
    assert parse_interactive_answer(raw) is None
