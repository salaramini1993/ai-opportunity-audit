"""Score opportunities from audit answers.

Score rules:
- Fit: the part of the opportunity signals that the business has (0.0 to 1.0).
- Impact: 1 to 5. More signals give more impact.
- Effort: the base effort from the catalog, 1 to 5.
- Priority: impact divided by effort. "Quick wins" have high impact
  and low effort.
"""

from dataclasses import dataclass

from .catalog import CATALOG, Opportunity
from .questions import keys as question_keys

MIN_FIT = 0.5


@dataclass(frozen=True)
class ScoredOpportunity:
    opportunity: Opportunity
    fit: float
    impact: int
    effort: int

    @property
    def priority(self) -> float:
        return round(self.impact / self.effort, 2)

    @property
    def quadrant(self) -> str:
        high_impact = self.impact >= 3
        low_effort = self.effort <= 2
        if high_impact and low_effort:
            return "quick win"
        if high_impact:
            return "strategic project"
        if low_effort:
            return "small improvement"
        return "not now"


def validate_answers(answers: dict[str, bool]) -> None:
    """Raise ValueError if an answer key is unknown or a value is not bool."""
    known = question_keys()
    for key, value in answers.items():
        if key not in known:
            raise ValueError(f"Unknown question key: {key}")
        if not isinstance(value, bool):
            raise ValueError(f"Answer for {key} must be true or false")


def score(answers: dict[str, bool]) -> list[ScoredOpportunity]:
    """Return the opportunities that fit, sorted by priority (highest first)."""
    validate_answers(answers)
    results: list[ScoredOpportunity] = []
    for opp in CATALOG:
        matched = sum(1 for s in opp.signals if answers.get(s, False))
        fit = matched / len(opp.signals)
        if fit < MIN_FIT:
            continue
        impact = min(5, 2 + matched)
        results.append(
            ScoredOpportunity(
                opportunity=opp, fit=round(fit, 2), impact=impact, effort=opp.base_effort
            )
        )
    results.sort(key=lambda r: (-r.priority, -r.impact, r.opportunity.key))
    return results
