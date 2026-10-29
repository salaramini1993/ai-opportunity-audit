"""Make a Markdown report from scored opportunities."""

from datetime import date

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


def render_markdown(
    business_name: str,
    results: list[ScoredOpportunity],
    today: date | None = None,
) -> str:
    today = today or date.today()
    lines = [
        f"# AI Opportunity Audit: {business_name}",
        "",
        f"Date: {today.isoformat()}",
        "",
    ]
    if not results:
        lines += [
            "The audit found no clear AI opportunities from the answers.",
            "Do the audit again when the business changes.",
            "",
        ]
        return "\n".join(lines)

    quick = [r for r in results if r.quadrant == "quick win"]
    lines += [
        "## Summary",
        "",
        f"- Opportunities found: {len(results)}",
        f"- Quick wins: {len(quick)}",
        f"- Estimated time saved: {format_hours(total_hours_saved(results))} hours per week",
        "",
        "## Priority list",
        "",
        "| # | Opportunity | Area | Impact | Effort | Priority | Type | Hours/week |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(results, start=1):
        o = r.opportunity
        lines.append(
            f"| {i} | {o.title} | {o.area} | {r.impact} | {r.effort} "
            f"| {r.priority} | {r.quadrant} | {format_hours(r.hours_saved)} |"
        )
    weighted = sorted({(r.opportunity.area, r.weight) for r in results if r.weight != 1.0})
    if weighted:
        lines += ["", "Area weights used for the priority:", ""]
        lines += [f"- {area}: {weight:g}" for area, weight in weighted]
    lines += ["", "## Details", ""]
    for r in results:
        o = r.opportunity
        lines += [f"### {o.title}", "", o.description, ""]
        if o.example_tools:
            lines.append("Example tools: " + ", ".join(o.example_tools))
            lines.append("")
    lines += [
        "Time estimates are rough. They are for a small business and they",
        "change with the fit. Measure the real time before and after.",
        "",
        "## Next step",
        "",
        "Start with the first quick win. Measure the time it saves for 4 weeks.",
        "",
    ]
    return "\n".join(lines)
