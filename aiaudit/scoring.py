"""Score opportunities from audit answers.

Score rules:
- Fit: the part of the opportunity signals that the business has (0.0 to 1.0).
- Impact: 1 to 5. More signals give more impact.
- Effort: the base effort from the catalog, 1 to 5.
- Priority: impact multiplied by the area weight, divided by effort.
  "Quick wins" have high impact and low effort.
- Area weight: optional. The default weight is 1.0. A weight of 2.0
  makes the priority of all opportunities in that area two times higher.
  The weight changes only the sort order. It does not change the type
  (quadrant) of an opportunity.
"""

from dataclasses import dataclass

from collections.abc import Mapping

from .catalog import AREAS, CATALOG, Opportunity
from .questions import keys as question_keys

MIN_FIT = 0.5
MIN_WEIGHT = 0.1
MAX_WEIGHT = 5.0


@dataclass(frozen=True)
class ScoredOpportunity:
    opportunity: Opportunity
    fit: float
    impact: int
    effort: int
    weight: float = 1.0

    @property
    def priority(self) -> float:
        return round(self.impact * self.weight / self.effort, 2)

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


def validate_weights(weights: Mapping[str, object]) -> dict[str, float]:
    """Check area weights and return them as floats.

    Each key must be a known area. Each value must be a number from
    MIN_WEIGHT to MAX_WEIGHT. Raise ValueError if a weight is not correct.
    """
    checked: dict[str, float] = {}
    for area, value in weights.items():
        if area not in AREAS:
            raise ValueError(f"Unknown area: {area}. Known areas: {', '.join(AREAS)}")
        # bool is a subclass of int. Do not accept true/false as a number.
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"Weight for {area} must be a number")
        if not MIN_WEIGHT <= value <= MAX_WEIGHT:
            raise ValueError(
                f"Weight for {area} must be from {MIN_WEIGHT} to {MAX_WEIGHT}"
            )
        checked[area] = float(value)
    return checked


def score(
    answers: dict[str, bool],
    weights: Mapping[str, object] | None = None,
) -> list[ScoredOpportunity]:
    """Return the opportunities that fit, sorted by priority (highest first).

    Use "weights" to make some areas more important (see validate_weights).
    """
    validate_answers(answers)
    area_weights = validate_weights(weights or {})
    results: list[ScoredOpportunity] = []
    for opp in CATALOG:
        matched = sum(1 for s in opp.signals if answers.get(s, False))
        fit = matched / len(opp.signals)
        if fit < MIN_FIT:
            continue
        impact = min(5, 2 + matched)
        results.append(
            ScoredOpportunity(
                opportunity=opp,
                fit=round(fit, 2),
                impact=impact,
                effort=opp.base_effort,
                weight=area_weights.get(opp.area, 1.0),
            )
        )
    results.sort(key=lambda r: (-r.priority, -r.impact, r.opportunity.key))
    return results
