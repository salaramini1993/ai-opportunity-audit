"""Make a Markdown report from scored opportunities."""

from datetime import date

from .scoring import ScoredOpportunity


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
        "",
        "## Priority list",
        "",
        "| # | Opportunity | Area | Impact | Effort | Priority | Type |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(results, start=1):
        o = r.opportunity
        lines.append(
            f"| {i} | {o.title} | {o.area} | {r.impact} | {r.effort} "
            f"| {r.priority} | {r.quadrant} |"
        )
    lines += ["", "## Details", ""]
    for r in results:
        o = r.opportunity
        lines += [f"### {o.title}", "", o.description, ""]
        if o.example_tools:
            lines.append("Example tools: " + ", ".join(o.example_tools))
            lines.append("")
    lines += [
        "## Next step",
        "",
        "Start with the first quick win. Measure the time it saves for 4 weeks.",
        "",
    ]
    return "\n".join(lines)
