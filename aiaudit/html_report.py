"""Make an HTML report from scored opportunities.

The HTML report has the same content as the Markdown report. It uses
the same text keys from i18n.py, so it supports the same languages. It is one
file with no external files, so you can send it by e-mail or open it
in a web browser.
"""

from datetime import date
from html import escape

from .action_plan import render_action_plan_html
from .catalog import COST_LEVELS
from .chart import render_svg
from .i18n import DEFAULT_LANGUAGE, lines, t, text_direction, validate_language
from .report import format_cost, format_hours
from .scoring import ScoredOpportunity, total_hours_saved

# Keep the style small. The report must look good when you print it.
# Use "start" and "end", not "left" and "right". Then the table is also
# correct in a right-to-left report.
_STYLE = """
body { font-family: system-ui, sans-serif; max-width: 960px; margin: 2em auto;
       padding: 0 1em; color: #222; line-height: 1.5; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #ccc; padding: 0.3em 0.5em; text-align: start; }
th { background: #f2f2f2; }
td.num { text-align: end; }
.note { color: #555; }
svg.chart { width: 100%; max-width: 480px; height: auto; display: block; }
"""


def _list(items: list[str]) -> list[str]:
    """Return the HTML lines for a bullet list. Escape each item."""
    return ["<ul>", *[f"  <li>{escape(item)}</li>" for item in items], "</ul>"]


def render_html(
    business_name: str,
    results: list[ScoredOpportunity],
    today: date | None = None,
    industry: str | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> str:
    """Return a full HTML document for the audit results.

    All text from the input is escaped, so a business name such as
    "<b>Shop</b>" shows as text and does not change the page.

    The lang code selects the language of the report text. The
    opportunity text uses the catalog translation, as in the Markdown
    report. The labels inside the chart use the same language.

    For a right-to-left language (for example Persian), the <html>
    element gets dir="rtl". The chart keeps a left-to-right layout,
    because low effort is always on the left.
    """
    validate_language(lang)
    today = today or date.today()

    def p(key: str, **values: object) -> str:
        # Text with more than one line is one paragraph in HTML.
        return f"<p>{escape(' '.join(lines(lang, key, **values)))}</p>"

    def quadrant(r: ScoredOpportunity) -> str:
        return t(lang, f"quadrant.{r.quadrant}")

    def cost(level: str | None) -> str:
        return t(lang, f"cost.{level}") if level in COST_LEVELS else format_cost(level)

    title = t(lang, "title", name=business_name)
    out = [
        "<!doctype html>",
        f'<html lang="{lang}" dir="{text_direction(lang)}">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{escape(title)}</title>",
        f"<style>{_STYLE}</style>",
        "</head>",
        "<body>",
        f"<h1>{escape(title)}</h1>",
        p("date", date=today.isoformat()),
    ]
    if industry:
        out.append(p("industry", industry=industry))
    if not results:
        out += [
            f"<p>{escape(t(lang, 'empty_1'))}",
            f"{escape(t(lang, 'empty_2'))}</p>",
            "</body>",
            "</html>",
            "",
        ]
        return "\n".join(out)

    quick = [r for r in results if r.quadrant == "quick win"]
    columns = ["#"] + [
        t(lang, f"col_{c}")
        for c in ("opportunity", "area", "impact", "effort", "priority", "type", "hours", "cost")
    ]
    out += [
        f"<h2>{escape(t(lang, 'summary'))}</h2>",
        *_list(
            [
                t(lang, "found", count=len(results)),
                t(lang, "quick_wins", count=len(quick)),
                t(lang, "time_saved", hours=format_hours(total_hours_saved(results))),
            ]
        ),
        f"<h2>{escape(t(lang, 'priority_list'))}</h2>",
        "<table>",
        "<thead><tr>" + "".join(f"<th>{escape(c)}</th>" for c in columns) + "</tr></thead>",
        "<tbody>",
    ]
    for i, r in enumerate(results, start=1):
        o = r.opportunity
        cells = [
            f'<td class="num">{i}</td>',
            f"<td>{escape(o.text('title', lang))}</td>",
            f"<td>{escape(o.area)}</td>",
            f'<td class="num">{r.impact}</td>',
            f'<td class="num">{r.effort}</td>',
            f'<td class="num">{r.priority}</td>',
            f"<td>{escape(quadrant(r))}</td>",
            f'<td class="num">{format_hours(r.hours_saved)}</td>',
            f"<td>{escape(cost(o.cost_per_month))}</td>",
        ]
        out.append("<tr>" + "".join(cells) + "</tr>")
    out += ["</tbody>", "</table>"]
    out += [
        f"<h2>{escape(t(lang, 'chart_heading'))}</h2>",
        p("chart_intro"),
        render_svg(results, lang),
    ]
    weighted = sorted({(r.opportunity.area, r.weight) for r in results if r.weight != 1.0})
    if weighted:
        out.append(p("weights_used"))
        out += _list([f"{area}: {weight:g}" for area, weight in weighted])

    out.append(f"<h2>{escape(t(lang, 'details'))}</h2>")
    for r in results:
        o = r.opportunity
        out += [
            f"<h3>{escape(o.text('title', lang))}</h3>",
            f"<p>{escape(o.text('description', lang))}</p>",
        ]
        if o.example_tools:
            out.append(p("example_tools", tools=", ".join(o.example_tools)))
        if o.risks:
            out.append(p("risks"))
            out += _list(list(o.sentences("risks", lang)))
        if o.gdpr_notes:
            out.append(p("gdpr_notes"))
            out += _list(list(o.sentences("gdpr_notes", lang)))

    personal = sum(1 for r in results if r.opportunity.uses_personal_data)
    note = '<p class="note">'
    out.append(p("time_note").replace("<p>", note, 1))
    if personal:
        out.append(p("gdpr_footer", count=personal, total=len(results)).replace("<p>", note, 1))
    out.append(p("cost_levels").replace("<p>", note, 1))
    out += _list([f"{cost(level)}: {t(lang, f'cost_text.{level}')}" for level in COST_LEVELS])
    out += render_action_plan_html(results, lang)
    out += [
        f"<h2>{escape(t(lang, 'next_step'))}</h2>",
        p("next_step_text"),
        "</body>",
        "</html>",
        "",
    ]
    return "\n".join(out)
