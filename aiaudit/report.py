"""Make a Markdown report from scored opportunities."""

from datetime import date

from .action_plan import render_action_plan_markdown
from .catalog import COST_LEVELS
from .i18n import DEFAULT_LANGUAGE, lines, t, validate_language
from .scoring import ScoredOpportunity, total_hours_saved


def format_hours(hours: tuple[float, float] | None) -> str:
    """Return a range of hours as text, for example "2-4".

    Return "-" if there is no estimate.
    """
    if hours is None:
        return "-"
    low, high = hours
    if low == high:
        return f"{low:g}"
    return f"{low:g}-{high:g}"


def format_cost(cost: str | None) -> str:
    """Return the cost level as text, for example "low".

    Return "-" if there is no estimate.
    """
    return cost if cost is not None else "-"


def _gdpr_footer(results: list[ScoredOpportunity], lang: str = DEFAULT_LANGUAGE) -> list[str]:
    """Return the report lines about GDPR notes.

    Return an empty list if no opportunity in the results uses
    personal data.
    """
    count = sum(1 for r in results if r.opportunity.uses_personal_data)
    if not count:
        return []
    return [*lines(lang, "gdpr_footer", count=count, total=len(results)), ""]


def render_markdown(
    business_name: str,
    results: list[ScoredOpportunity],
    today: date | None = None,
    industry: str | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> str:
    """Return the Markdown report.

    The lang code selects the language of the fixed report text. The
    opportunity text from the catalog and the action plan stay in English.
    """
    validate_language(lang)
    today = today or date.today()

    def quadrant(r: ScoredOpportunity) -> str:
        return t(lang, f"quadrant.{r.quadrant}")

    def cost(level: str | None) -> str:
        return t(lang, f"cost.{level}") if level in COST_LEVELS else format_cost(level)

    lines_ = [
        "# " + t(lang, "title", name=business_name),
        "",
        t(lang, "date", date=today.isoformat()),
        "",
    ]
    if industry:
        # Tell the reader that the list shows only one industry.
        lines_ += [t(lang, "industry", industry=industry), ""]
    if not results:
        lines_ += [t(lang, "empty_1"), t(lang, "empty_2"), ""]
        return "\n".join(lines_)

    quick = [r for r in results if r.quadrant == "quick win"]
    columns = ["#"] + [
        t(lang, f"col_{c}")
        for c in ("opportunity", "area", "impact", "effort", "priority", "type", "hours", "cost")
    ]
    lines_ += [
        "## " + t(lang, "summary"),
        "",
        "- " + t(lang, "found", count=len(results)),
        "- " + t(lang, "quick_wins", count=len(quick)),
        "- " + t(lang, "time_saved", hours=format_hours(total_hours_saved(results))),
        "",
        "## " + t(lang, "priority_list"),
        "",
        "| " + " | ".join(columns) + " |",
        "|" + "---|" * len(columns),
    ]
    for i, r in enumerate(results, start=1):
        o = r.opportunity
        lines_.append(
            f"| {i} | {o.title} | {o.area} | {r.impact} | {r.effort} "
            f"| {r.priority} | {quadrant(r)} | {format_hours(r.hours_saved)} "
            f"| {cost(o.cost_per_month)} |"
        )
    weighted = sorted({(r.opportunity.area, r.weight) for r in results if r.weight != 1.0})
    if weighted:
        lines_ += ["", t(lang, "weights_used"), ""]
        lines_ += [f"- {area}: {weight:g}" for area, weight in weighted]
    lines_ += ["", "## " + t(lang, "details"), ""]
    for r in results:
        o = r.opportunity
        lines_ += [f"### {o.title}", "", o.description, ""]
        if o.example_tools:
            lines_.append(t(lang, "example_tools", tools=", ".join(o.example_tools)))
            lines_.append("")
        if o.risks:
            lines_ += [t(lang, "risks"), ""]
            lines_ += [f"- {risk}" for risk in o.risks]
            lines_.append("")
        if o.gdpr_notes:
            lines_ += [t(lang, "gdpr_notes"), ""]
            lines_ += [f"- {note}" for note in o.gdpr_notes]
            lines_.append("")
    lines_ += [
        *lines(lang, "time_note"),
        "",
        *_gdpr_footer(results, lang),
        t(lang, "cost_levels"),
        "",
        *[f"- {cost(level)}: {t(lang, f'cost_text.{level}')}" for level in COST_LEVELS],
        "",
        *render_action_plan_markdown(results, lang),
        "## " + t(lang, "next_step"),
        "",
        t(lang, "next_step_text"),
        "",
    ]
    return "\n".join(lines_)
