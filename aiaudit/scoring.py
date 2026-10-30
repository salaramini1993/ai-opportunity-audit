"""Score opportunities from audit answers.

Score rules:
- Answer: true/false or a number on a scale from 0 to 3.
  0 means "no", 1 "a little", 2 "some", 3 "a lot". true is the same as 3
  and false is the same as 0. The strength of a signal is the answer
  divided by 3 (0.0 to 1.0).
- Fit: the mean signal strength of the opportunity signals (0.0 to 1.0).
- Impact: 1 to 5. Stronger signals give more impact.
- Effort: the base effort from the catalog, 1 to 5.
- Priority: impact multiplied by the area weight, divided by effort.
  "Quick wins" have high impact and low effort.
- Area weight: optional. The default weight is 1.0. A weight of 2.0
  makes the priority of all opportunities in that area two times higher.
  The weight changes only the sort order. It does not change the type
  (quadrant) of an opportunity.
- Hours saved: the catalog range (low, high) multiplied by the fit.
  A business that has half of the signals gets half of the hours.
  This is a rough estimate. Use it to compare opportunities, not as a promise.
"""

from dataclasses import dataclass

from collections.abc import Mapping

from .catalog import AREAS, CATALOG, Opportunity
from .questions import keys as question_keys

MIN_FIT = 0.5
MAX_SCALE = 3
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
    def hours_saved(self) -> tuple[float, float] | None:
        """Return the estimated hours saved per week as (low, high).

        Return None if the catalog has no estimate for this opportunity.
        """
        hours = self.opportunity.hours_saved_per_week
        if hours is None:
            return None
        low, high = hours
        return (round(low * self.fit, 1), round(high * self.fit, 1))

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


def total_hours_saved(results: list[ScoredOpportunity]) -> tuple[float, float]:
    """Return the sum of the hours saved per week for all results.

    Results that have no estimate add zero.
    """
    low = high = 0.0
    for r in results:
        hours = r.hours_saved
        if hours is not None:
            low += hours[0]
            high += hours[1]
    return (round(low, 1), round(high, 1))


Answer = bool | int


def validate_answers(answers: Mapping[str, object]) -> None:
    """Raise ValueError if an answer key or value is not correct.

    A value must be true, false or a whole number from 0 to MAX_SCALE.
    """
    known = question_keys()
    for key, value in answers.items():
        if key not in known:
            raise ValueError(f"Unknown question key: {key}")
        if isinstance(value, bool):
            continue
        if not isinstance(value, int) or not 0 <= value <= MAX_SCALE:
            raise ValueError(
                f"Answer for {key} must be true, false or a number from 0 to {MAX_SCALE}"
            )


def signal_strength(value: object) -> float:
    """Return the strength of one answer, from 0.0 to 1.0.

    true gives 1.0. false and a missing answer give 0.0.
    A number on the scale gives the number divided by MAX_SCALE.
    """
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, int):
        return value / MAX_SCALE
    return 0.0


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
    answers: Mapping[str, Answer],
    weights: Mapping[str, object] | None = None,
) -> list[ScoredOpportunity]:
    """Return the opportunities that fit, sorted by priority (highest first).

    Use "weights" to make some areas more important (see validate_weights).
    """
    validate_answers(answers)
    area_weights = validate_weights(weights or {})
    results: list[ScoredOpportunity] = []
    for opp in CATALOG:
        matched = sum(signal_strength(answers.get(s, False)) for s in opp.signals)
        fit = matched / len(opp.signals)
        if fit < MIN_FIT:
            continue
        # Round to a whole number. With only yes/no answers, "matched" is
        # already a whole number, so the result does not change.
        impact = min(5, 2 + round(matched))
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
