from datetime import date

import pytest

from aiaudit.action_plan import render_action_plan_html, render_action_plan_markdown
from aiaudit.catalog import CATALOG, CatalogError, by_key, parse_catalog
from aiaudit.i18n import LANGUAGES
from aiaudit.report import render_markdown
from aiaudit.scoring import score


def _catalog(translations):
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
                "translations": translations,
            }
        ],
    }


def test_each_opportunity_has_text_in_each_language():
    for item in CATALOG:
        for lang in LANGUAGES:
            if lang == "en":
                continue
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
