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

The lang code selects the language of the plan text. The opportunity
titles come from the catalog and are not translated.
"""

from dataclasses import dataclass
from html import escape

from .i18n import DEFAULT_LANGUAGE, lines, t, validate_language
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


def _phase(lang: str, number: int, items: list[ScoredOpportunity]) -> Phase:
    return Phase(
        title=t(lang, f"plan.{number}.title"),
        goal=t(lang, f"plan.{number}.goal"),
        steps=tuple(lines(lang, f"plan.{number}.steps")),
        items=tuple(items),
    )


def build_action_plan(
    results: list[ScoredOpportunity], lang: str = DEFAULT_LANGUAGE
) -> list[Phase]:
    """Return the three phases of the plan, in time order.

    The results must be in priority order (as score() returns them).
    Return an empty list if there are no results.
    """
    validate_language(lang)
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
        _phase(lang, 1, [start]),
        _phase(lang, 2, second),
        _phase(lang, 3, third),
    ]


def render_action_plan_markdown(
    results: list[ScoredOpportunity], lang: str = DEFAULT_LANGUAGE
) -> list[str]:
    """Return the Markdown lines of the action plan section.

    Return an empty list if there are no results.
    """
    phases = build_action_plan(results, lang)
    if not phases:
        return []
    out = ["## " + t(lang, "plan.heading"), ""]
    for phase in phases:
        out += [f"### {phase.title}", "", t(lang, "plan.goal", goal=phase.goal), ""]
        if phase.items:
            out += [
                f"- {r.opportunity.title} ({t(lang, f'quadrant.{r.quadrant}')})"
                for r in phase.items
            ]
        else:
            out.append("- " + t(lang, "plan.none"))
        out += ["", t(lang, "plan.steps"), ""]
        out += [f"{i}. {step}" for i, step in enumerate(phase.steps, start=1)]
        out.append("")
    return out


def render_action_plan_html(
    results: list[ScoredOpportunity], lang: str = DEFAULT_LANGUAGE
) -> list[str]:
    """Return the HTML lines of the action plan section.

    The content is the same as in the Markdown section. All text is
    escaped. Return an empty list if there are no results.
    """
    phases = build_action_plan(results, lang)
    if not phases:
        return []
    out = [f"<h2>{escape(t(lang, 'plan.heading'))}</h2>"]
    for phase in phases:
        out += [
            f"<h3>{escape(phase.title)}</h3>",
            f"<p>{escape(t(lang, 'plan.goal', goal=phase.goal))}</p>",
            "<ul>",
        ]
        if phase.items:
            out += [
                f"  <li>{escape(r.opportunity.title)} "
                f"({escape(t(lang, f'quadrant.{r.quadrant}'))})</li>"
                for r in phase.items
            ]
        else:
            out.append(f"  <li>{escape(t(lang, 'plan.none'))}</li>")
        out += ["</ul>", f"<p>{escape(t(lang, 'plan.steps'))}</p>", "<ol>"]
        out += [f"  <li>{escape(step)}</li>" for step in phase.steps]
        out.append("</ol>")
    return out
