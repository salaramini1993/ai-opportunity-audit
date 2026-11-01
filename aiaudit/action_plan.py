"""Make a 30/60/90-day action plan from scored opportunities.

Plan rules:
- Days 1-30: start one opportunity. Use the first quick win. If there is
  no quick win, use the first small improvement. If there is no small
  improvement, use the first opportunity in the priority list.
- Days 31-60: add up to MAX_SECOND_PHASE more quick wins or small
  improvements, in priority order.
- Days 61-90: plan the first strategic project. If there is no strategic
  project, do nothing new and keep the work from the first two phases.
- Opportunities of the type "not now" are not in the plan, except as the
  last fallback for the first phase.
- One opportunity is in one phase only.
"""

from dataclasses import dataclass
from html import escape

from .scoring import ScoredOpportunity

MAX_SECOND_PHASE = 2


@dataclass(frozen=True)
class Phase:
    title: str
    goal: str
    steps: tuple[str, ...]
    items: tuple[ScoredOpportunity, ...]


def _first(results: list[ScoredOpportunity], quadrant: str) -> ScoredOpportunity | None:
    return next((r for r in results if r.quadrant == quadrant), None)


def build_action_plan(results: list[ScoredOpportunity]) -> list[Phase]:
    """Return the three phases of the plan, in time order.

    The results must be in priority order (as score() returns them).
    Return an empty list if there are no results.
    """
    if not results:
        return []
    start = _first(results, "quick win") or _first(results, "small improvement") or results[0]
    used = {start.opportunity.key}

    second = [
        r
        for r in results
        if r.opportunity.key not in used
        and r.quadrant in ("quick win", "small improvement")
    ][:MAX_SECOND_PHASE]
    used.update(r.opportunity.key for r in second)

    third = [
        r
        for r in results
        if r.opportunity.key not in used and r.quadrant == "strategic project"
    ][:1]

    return [
        Phase(
            title="Days 1-30",
            goal="Start one opportunity and measure the result.",
            steps=(
                "Measure the time the task takes now, for 1 week.",
                "Select a tool and test it on real work.",
                "Write down the checks a person must do on the AI output.",
            ),
            items=(start,),
        ),
        Phase(
            title="Days 31-60",
            goal="Keep what works and add small changes.",
            steps=(
                "Compare the time before and after the first change.",
                "Stop the change if it does not save time or quality drops.",
                "Start the next opportunities in the list.",
            ),
            items=tuple(second),
        ),
        Phase(
            title="Days 61-90",
            goal="Plan a larger project.",
            steps=(
                "Write a short plan with the goal, the cost and the owner.",
                "Do a small pilot before you change the full process.",
                "Do the audit again to find new opportunities.",
            ),
            items=tuple(third),
        ),
    ]


def render_action_plan_markdown(results: list[ScoredOpportunity]) -> list[str]:
    """Return the Markdown lines of the action plan section.

    Return an empty list if there are no results.
    """
    phases = build_action_plan(results)
    if not phases:
        return []
    lines = ["## 30/60/90-day action plan", ""]
    for phase in phases:
        lines += [f"### {phase.title}", "", f"Goal: {phase.goal}", ""]
        if phase.items:
            lines += [
                f"- {r.opportunity.title} ({r.quadrant})" for r in phase.items
            ]
        else:
            lines.append("- No new opportunity. Continue the work from before.")
        lines += ["", "Steps:", ""]
        lines += [f"{i}. {step}" for i, step in enumerate(phase.steps, start=1)]
        lines.append("")
    return lines


def render_action_plan_html(results: list[ScoredOpportunity]) -> list[str]:
    """Return the HTML lines of the action plan section.

    The content is the same as in the Markdown section. All text is
    escaped. Return an empty list if there are no results.
    """
    phases = build_action_plan(results)
    if not phases:
        return []
    lines = ["<h2>30/60/90-day action plan</h2>"]
    for phase in phases:
        lines += [
            f"<h3>{escape(phase.title)}</h3>",
            f"<p>Goal: {escape(phase.goal)}</p>",
            "<ul>",
        ]
        if phase.items:
            lines += [
                f"  <li>{escape(r.opportunity.title)} ({escape(r.quadrant)})</li>"
                for r in phase.items
            ]
        else:
            lines.append("  <li>No new opportunity. Continue the work from before.</li>")
        lines += ["</ul>", "<p>Steps:</p>", "<ol>"]
        lines += [f"  <li>{escape(step)}</li>" for step in phase.steps]
        lines.append("</ol>")
    return lines
