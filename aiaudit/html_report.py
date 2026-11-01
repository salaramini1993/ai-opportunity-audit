"""Make an HTML report from scored opportunities.

The HTML report has the same content as the Markdown report. It is one
file with no external files, so you can send it by e-mail or open it
in a web browser.
"""

from datetime import date
from html import escape

from .catalog import COST_LEVELS
from .chart import render_svg
from .report import format_cost, format_hours
from .scoring import ScoredOpportunity, total_hours_saved

# Keep the style small. The report must look good when you print it.
_STYLE = """
body { font-family: system-ui, sans-serif; max-width: 960px; margin: 2em auto;
       padding: 0 1em; color: #222; line-height: 1.5; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #ccc; padding: 0.3em 0.5em; text-align: left; }
th { background: #f2f2f2; }
td.num { text-align: right; }
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
) -> str:
    """Return a full HTML document for the audit results.

    All text from the input is escaped, so a business name such as
    "<b>Shop</b>" shows as text and does not change the page.
    """
    today = today or date.today()
    title = f"AI Opportunity Audit: {business_name}"
    lines = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{escape(title)}</title>",
        f"<style>{_STYLE}</style>",
        "</head>",
        "<body>",
        f"<h1>{escape(title)}</h1>",
        f"<p>Date: {today.isoformat()}</p>",
    ]
    if industry:
        lines.append(f"<p>Industry: {escape(industry)}</p>")
    if not results:
        lines += [
            "<p>The audit found no clear AI opportunities from the answers.",
            "Do the audit again when the business changes.</p>",
            "</body>",
            "</html>",
            "",
        ]
        return "\n".join(lines)

    quick = [r for r in results if r.quadrant == "quick win"]
    lines += [
        "<h2>Summary</h2>",
        *_list(
            [
                f"Opportunities found: {len(results)}",
                f"Quick wins: {len(quick)}",
                "Estimated time saved: "
                f"{format_hours(total_hours_saved(results))} hours per week",
            ]
        ),
        "<h2>Priority list</h2>",
        "<table>",
        "<thead><tr><th>#</th><th>Opportunity</th><th>Area</th><th>Impact</th>"
        "<th>Effort</th><th>Priority</th><th>Type</th><th>Hours/week</th>"
        "<th>Cost/month</th></tr></thead>",
        "<tbody>",
    ]
    for i, r in enumerate(results, start=1):
        o = r.opportunity
        cells = [
            f'<td class="num">{i}</td>',
            f"<td>{escape(o.title)}</td>",
            f"<td>{escape(o.area)}</td>",
            f'<td class="num">{r.impact}</td>',
            f'<td class="num">{r.effort}</td>',
            f'<td class="num">{r.priority}</td>',
            f"<td>{escape(r.quadrant)}</td>",
            f'<td class="num">{format_hours(r.hours_saved)}</td>',
            f"<td>{escape(format_cost(o.cost_per_month))}</td>",
        ]
        lines.append("<tr>" + "".join(cells) + "</tr>")
    lines += ["</tbody>", "</table>"]
    lines += [
        "<h2>Impact and effort</h2>",
        "<p>Each circle is one opportunity. The number is the position in the "
        "priority list. Start with the circles in the top-left area.</p>",
        render_svg(results),
    ]
    weighted = sorted({(r.opportunity.area, r.weight) for r in results if r.weight != 1.0})
    if weighted:
        lines.append("<p>Area weights used for the priority:</p>")
        lines += _list([f"{area}: {weight:g}" for area, weight in weighted])

    lines.append("<h2>Details</h2>")
    for r in results:
        o = r.opportunity
        lines += [f"<h3>{escape(o.title)}</h3>", f"<p>{escape(o.description)}</p>"]
        if o.example_tools:
            lines.append(f"<p>Example tools: {escape(', '.join(o.example_tools))}</p>")
        if o.risks:
            lines.append("<p>Risks and checks:</p>")
            lines += _list(list(o.risks))
        if o.gdpr_notes:
            lines.append("<p>GDPR notes (this opportunity uses personal data):</p>")
            lines += _list(list(o.gdpr_notes))

    personal = sum(1 for r in results if r.opportunity.uses_personal_data)
    lines.append(
        '<p class="note">Time estimates are rough. They are for a small business '
        "and they change with the fit. Measure the real time before and after.</p>"
    )
    if personal:
        lines.append(
            f'<p class="note">{personal} of {len(results)} opportunities use '
            "personal data. Read the GDPR notes for these opportunities before you "
            "start. The notes are a checklist. They are not legal advice.</p>"
        )
    lines.append('<p class="note">Cost levels are for the tool cost per month:</p>')
    lines += _list([f"{level}: {text}" for level, text in COST_LEVELS.items()])
    lines += [
        "<h2>Next step</h2>",
        "<p>Start with the first quick win. Measure the time it saves for 4 weeks.</p>",
        "</body>",
        "</html>",
        "",
    ]
    return "\n".join(lines)
