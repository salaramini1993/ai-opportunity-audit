from datetime import date
from html import escape
from xml.etree import ElementTree

from aiaudit.catalog import CATALOG
from aiaudit.chart import _x, _y, point_positions, render_svg
from aiaudit.html_report import render_html
from aiaudit.scoring import ScoredOpportunity, score

SHOP = {"sells_products": True, "many_products": True, "multi_language": True}


def _scored(index: int, impact: int, effort: int) -> ScoredOpportunity:
    return ScoredOpportunity(
        opportunity=CATALOG[index], fit=1.0, impact=impact, effort=effort
    )


def test_svg_is_valid_xml_with_one_circle_per_result():
    results = score(SHOP)
    root = ElementTree.fromstring(render_svg(results))
    ns = "{http://www.w3.org/2000/svg}"
    assert root.tag == ns + "svg"
    assert len(root.findall(f".//{ns}circle")) == len(results)


def test_high_impact_low_effort_is_top_left():
    x_low, x_high = _x(1), _x(5)
    y_high, y_low = _y(5), _y(1)
    assert x_low < x_high
    assert y_high < y_low


def test_points_in_same_cell_do_not_overlap():
    results = [_scored(0, 4, 2), _scored(1, 4, 2), _scored(2, 4, 2)]
    positions = point_positions(results)
    xs = sorted(x for x, _ in positions)
    assert len({y for _, y in positions}) == 1
    assert all(b - a >= 20 for a, b in zip(xs, xs[1:], strict=False))
    # The row is centered on the cell.
    assert xs[1] == _x(2)


def test_points_have_priority_numbers():
    results = [_scored(0, 5, 1), _scored(1, 2, 4)]
    svg = render_svg(results)
    assert f"1. {CATALOG[0].title}" in svg
    assert f"2. {CATALOG[1].title}" in svg


def test_svg_escapes_titles():
    opp = CATALOG[0].__class__(**{**CATALOG[0].__dict__, "title": "<b>X & Y</b>"})
    svg = render_svg([ScoredOpportunity(opportunity=opp, fit=1.0, impact=3, effort=2)])
    assert "<b>" not in svg
    assert "&lt;b&gt;X &amp; Y&lt;/b&gt;" in svg
    ElementTree.fromstring(svg)


def test_html_report_includes_chart():
    text = render_html("Shop", score(SHOP), today=date(2026, 1, 1))
    assert "<h2>Impact and effort</h2>" in text
    assert '<svg class="chart"' in text


def test_empty_html_report_has_no_chart():
    text = render_html("Shop", [], today=date(2026, 1, 1))
    assert "<svg" not in text


def test_chart_labels_are_in_english_by_default():
    svg = render_svg(score(SHOP))
    for label in ("Quick wins", "Not now", "Effort (1 = low)", "Impact (5 = high)"):
        assert label in svg


def test_chart_labels_in_swedish():
    results = score(SHOP)
    svg = render_svg(results, "sv")
    ElementTree.fromstring(svg)
    for label in (
        "Effekt och insats för varje möjlighet",
        "Snabba vinster",
        "Strategiska projekt",
        "Små förbättringar",
        "Inte nu",
        "Insats (1 = låg)",
        "Effekt (5 = hög)",
    ):
        assert label in svg
    for label in ("Quick wins", "Effort (1 = low)", "Impact (5 = high)"):
        assert label not in svg
    first = results[0]
    expected = (
        f"1. {first.opportunity.text('title', 'sv')} "
        f"(effekt {first.impact}, insats {first.effort})"
    )
    assert escape(expected) in svg


def test_swedish_html_report_has_swedish_chart():
    text = render_html("Shop", score(SHOP), today=date(2026, 1, 1), lang="sv")
    assert "Snabba vinster" in text
    assert "Quick wins" not in text
