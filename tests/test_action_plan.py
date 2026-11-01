from datetime import date

from aiaudit.action_plan import MAX_SECOND_PHASE, build_action_plan, render_action_plan_markdown
from aiaudit.report import render_markdown
from aiaudit.scoring import score
from aiaudit.questions import keys

ALL = {key: True for key in keys()}


def test_empty_results_give_no_plan():
    assert build_action_plan([]) == []
    assert render_action_plan_markdown([]) == []


def test_plan_has_three_phases_in_order():
    phases = build_action_plan(score(ALL))
    assert [p.title for p in phases] == ["Days 1-30", "Days 31-60", "Days 61-90"]


def test_first_phase_is_first_quick_win():
    results = score(ALL)
    quick = [r for r in results if r.quadrant == "quick win"]
    assert quick, "test data must have a quick win"
    phases = build_action_plan(results)
    assert phases[0].items == (quick[0],)


def test_each_opportunity_is_in_one_phase_only():
    phases = build_action_plan(score(ALL))
    keys_in_plan = [r.opportunity.key for p in phases for r in p.items]
    assert len(keys_in_plan) == len(set(keys_in_plan))
    assert len(phases[1].items) <= MAX_SECOND_PHASE
    assert all(r.quadrant in ("quick win", "small improvement") for r in phases[1].items)
    assert all(r.quadrant == "strategic project" for r in phases[2].items)


def test_fallback_when_no_quick_win():
    results = [r for r in score(ALL) if r.quadrant not in ("quick win", "small improvement")]
    assert results
    phases = build_action_plan(results)
    assert phases[0].items == (results[0],)
    assert phases[1].items == ()


def test_markdown_report_has_plan_section():
    text = render_markdown("Shop", score(ALL), today=date(2026, 1, 1))
    assert "## 30/60/90-day action plan" in text
    assert text.index("## 30/60/90-day action plan") < text.index("## Next step")
    assert "### Days 61-90" in text


def test_empty_phase_has_message():
    results = [r for r in score(ALL) if r.quadrant == "quick win"][:1]
    text = "\n".join(render_action_plan_markdown(results))
    assert "No new opportunity" in text


def test_empty_report_has_no_plan():
    text = render_markdown("Test AB", [], today=date(2026, 1, 1))
    assert "action plan" not in text


def test_html_plan_is_empty_for_no_results():
    from aiaudit.action_plan import render_action_plan_html

    assert render_action_plan_html([]) == []


def test_html_report_has_plan_section():
    from aiaudit.html_report import render_html

    results = score(ALL)
    text = render_html("Shop", results, today=date(2026, 1, 1))
    assert "<h2>30/60/90-day action plan</h2>" in text
    assert text.index("<h2>30/60/90-day action plan</h2>") < text.index("<h2>Next step</h2>")
    for title in ("Days 1-30", "Days 31-60", "Days 61-90"):
        assert f"<h3>{title}</h3>" in text
    first = build_action_plan(results)[0].items[0]
    assert first.opportunity.title in text


def test_html_plan_has_message_for_empty_phase():
    from aiaudit.action_plan import render_action_plan_html

    results = [r for r in score(ALL) if r.quadrant == "quick win"][:1]
    text = "\n".join(render_action_plan_html(results))
    assert "<li>No new opportunity. Continue the work from before.</li>" in text
    assert text.count("<ol>") == 3


def test_empty_html_report_has_no_plan():
    from aiaudit.html_report import render_html

    text = render_html("Test AB", [], today=date(2026, 1, 1))
    assert "action plan" not in text
