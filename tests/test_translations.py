from datetime import date

import pytest

from aiaudit.action_plan import render_action_plan_html, render_action_plan_markdown
from aiaudit.catalog import CATALOG, CatalogError, by_key, parse_catalog
from aiaudit.i18n import LANGUAGES
from aiaudit.report import render_markdown
from aiaudit.scoring import score


def _catalog(translations, risks=None):
    return {
        "areas": ["sales"],
        "opportunities": [
            {
                "key": "x",
                "area": "sales",
                "title": "Title",
                "description": "Text.",
                "signals": ["q"],
                "base_effort": 1,
                "risks": risks or ["Check it."],
                "translations": translations,
            }
        ],
    }


# Languages that have a catalog title and description. English text is
# in the main fields.
CATALOG_LANGUAGES = tuple(lang for lang in LANGUAGES if lang != "en")


def test_each_opportunity_has_text_in_each_language():
    assert "sv" in CATALOG_LANGUAGES
    assert "fa" in CATALOG_LANGUAGES
    for item in CATALOG:
        for lang in CATALOG_LANGUAGES:
            assert item.translations[lang]["title"].strip(), (item.key, lang)
            assert item.translations[lang]["description"].strip(), (item.key, lang)


def test_text_returns_translation_or_english():
    item = by_key("support_faq_assistant")
    assert item.text("title", "sv") == "FAQ-assistent för kundfrågor"
    assert item.text("title") == item.title
    assert item.text("description", "xx") == item.description


def test_text_rejects_other_fields():
    with pytest.raises(ValueError):
        by_key("support_faq_assistant").text("risks", "sv")


def test_missing_field_uses_english():
    _, items = parse_catalog(_catalog({"sv": {"title": "Titel"}}))
    assert items[0].text("title", "sv") == "Titel"
    assert items[0].text("description", "sv") == "Text."


def test_opportunity_stays_hashable():
    hash(by_key("support_faq_assistant"))


@pytest.mark.parametrize(
    "bad",
    [
        [],
        {"en": {"title": "Title"}},
        {"": {"title": "Titel"}},
        {"sv": "Titel"},
        {"sv": {"risks": "x"}},
        {"sv": {"title": ""}},
        {"sv": {"title": 3}},
        {"sv": {"title": ["Titel"]}},
        {"sv": {"risks": [""]}},
        {"sv": {"risks": ["En.", "Två."]}},
        {"sv": {"gdpr_notes": ["En."]}},
    ],
)
def test_bad_translations_raise(bad):
    with pytest.raises(CatalogError, match="translations"):
        parse_catalog(_catalog(bad))


def test_swedish_report_and_plan_use_swedish_titles():
    results = score({"support_volume": True, "repeat_questions": True})
    text = render_markdown("Butik", results, today=date(2026, 1, 1), lang="sv")
    assert "### FAQ-assistent för kundfrågor" in text
    assert "Använd en AI-assistent" in text
    plan = "\n".join(render_action_plan_markdown(results, "sv"))
    assert "FAQ-assistent för kundfrågor" in plan
    html = "\n".join(render_action_plan_html(results, "sv"))
    assert "FAQ-assistent för kundfrågor" in html
    english = render_markdown("Shop", results, today=date(2026, 1, 1))
    assert "FAQ-assistent" not in english


def test_each_risk_and_gdpr_note_has_swedish_text():
    for item in CATALOG:
        sv = item.translations["sv"]
        assert len(sv.get("risks", ())) == len(item.risks), item.key
        assert len(sv.get("gdpr_notes", ())) == len(item.gdpr_notes), item.key


def test_sentences_returns_translation_or_english():
    item = by_key("support_faq_assistant")
    assert item.sentences("risks", "sv")[1] == (
        "Berätta för kunderna att de talar med en AI-assistent."
    )
    assert item.sentences("gdpr_notes") == item.gdpr_notes
    assert item.sentences("risks", "xx") == item.risks
    with pytest.raises(ValueError):
        item.sentences("title", "sv")


def test_missing_sentences_use_english():
    _, items = parse_catalog(_catalog({"sv": {"title": "Titel"}}))
    assert items[0].sentences("risks", "sv") == ("Check it.",)


def test_swedish_report_has_swedish_risks_and_gdpr_notes():
    results = score({"support_volume": True, "repeat_questions": True})
    text = render_markdown("Butik", results, today=date(2026, 1, 1), lang="sv")
    assert "- Berätta för kunderna att de talar med en AI-assistent." in text
    assert "personuppgiftsbiträdesavtal (DPA)" in text
    assert "Tell customers that they talk to an AI assistant." not in text
    english = render_markdown("Shop", results, today=date(2026, 1, 1))
    assert "- Tell customers that they talk to an AI assistant." in english
    assert "personuppgiftsbiträdesavtal" not in english


def test_persian_report_and_plan_use_persian_titles():
    results = score({"support_volume": True, "repeat_questions": True})
    title = "دستیار پرسش‌های متداول برای پرسش‌های مشتریان"
    text = render_markdown("فروشگاه", results, today=date(2026, 1, 1), lang="fa")
    assert f"### {title}" in text
    assert "از یک دستیار هوش مصنوعی" in text
    assert "FAQ assistant for customer questions" not in text
    plan = "\n".join(render_action_plan_markdown(results, "fa"))
    assert title in plan
    html = "\n".join(render_action_plan_html(results, "fa"))
    assert title in html


def test_each_risk_and_gdpr_note_has_persian_text():
    for item in CATALOG:
        fa = item.translations["fa"]
        assert len(fa.get("risks", ())) == len(item.risks), item.key
        assert len(fa.get("gdpr_notes", ())) == len(item.gdpr_notes), item.key


def test_persian_report_has_persian_risks_and_gdpr_notes():
    results = score({"support_volume": True, "repeat_questions": True})
    text = render_markdown("فروشگاه", results, today=date(2026, 1, 1), lang="fa")
    assert "- به مشتریان بگویید که با یک دستیار هوش مصنوعی صحبت می‌کنند." in text
    assert "قرارداد پردازش داده (DPA)" in text
    assert "Tell customers that they talk to an AI assistant." not in text
    assert "data processing agreement" not in text
