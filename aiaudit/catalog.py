"""Catalog of AI opportunities.

Each opportunity is one task in a business that AI can make faster,
cheaper or better. The audit asks questions to find which
opportunities apply to a business, then scores them.

The catalog data is in the file "data/catalog.json". To add or change
an opportunity, edit that file. You do not need to change Python code.
"""

import json
from dataclasses import dataclass, field
from importlib import resources
from pathlib import Path
from typing import Any, Optional, Union


@dataclass(frozen=True)
class Opportunity:
    """One AI opportunity that the audit can recommend."""

    key: str
    area: str
    title: str
    description: str
    # Question keys that show this task exists in the business.
    signals: tuple[str, ...]
    # 1 (low) to 5 (high): how difficult it is to put in place.
    base_effort: int
    # Example tools. These are examples only, not endorsements.
    example_tools: tuple[str, ...] = field(default_factory=tuple)
    # Hours saved per week when the task fits fully: (low, high).
    # This is a rough estimate for a small business. None means no estimate.
    hours_saved_per_week: Optional[tuple[float, float]] = None
    # Tool cost per month: "low", "medium" or "high". See COST_LEVELS.
    # None means no estimate.
    cost_per_month: Optional[str] = None


class CatalogError(ValueError):
    """The catalog data is not correct."""


_REQUIRED_FIELDS = ("key", "area", "title", "description", "signals", "base_effort")
_KNOWN_FIELDS = set(_REQUIRED_FIELDS) | {
    "example_tools",
    "hours_saved_per_week",
    "cost_per_month",
}
MAX_HOURS_PER_WEEK = 40

# Cost levels for the tool cost per month, from low to high.
# The value is a rough range in euro for a small business.
COST_LEVELS = {
    "low": "under 50 EUR",
    "medium": "50-300 EUR",
    "high": "more than 300 EUR",
}


def _parse_opportunity(raw: Any, areas: tuple[str, ...], index: int) -> Opportunity:
    """Make one Opportunity from raw JSON data. Check each field."""
    where = f"opportunity #{index}"
    if not isinstance(raw, dict):
        raise CatalogError(f"{where}: must be an object")
    missing = [name for name in _REQUIRED_FIELDS if name not in raw]
    if missing:
        raise CatalogError(f"{where}: missing field(s): {', '.join(missing)}")
    unknown = sorted(set(raw) - _KNOWN_FIELDS)
    if unknown:
        raise CatalogError(f"{where}: unknown field(s): {', '.join(unknown)}")

    where = f"opportunity '{raw['key']}'"
    for name in ("key", "area", "title", "description"):
        if not isinstance(raw[name], str) or not raw[name].strip():
            raise CatalogError(f"{where}: '{name}' must be a text that is not empty")
    if raw["area"] not in areas:
        raise CatalogError(f"{where}: unknown area '{raw['area']}'")

    signals = raw["signals"]
    if (
        not isinstance(signals, list)
        or not signals
        or not all(isinstance(s, str) and s for s in signals)
    ):
        raise CatalogError(f"{where}: 'signals' must be a list of question keys")

    effort = raw["base_effort"]
    # bool is a subclass of int. Do not accept true/false as a number.
    if isinstance(effort, bool) or not isinstance(effort, int) or not 1 <= effort <= 5:
        raise CatalogError(f"{where}: 'base_effort' must be an integer from 1 to 5")

    tools = raw.get("example_tools", [])
    if not isinstance(tools, list) or not all(isinstance(t, str) for t in tools):
        raise CatalogError(f"{where}: 'example_tools' must be a list of text")

    hours = _parse_hours(raw.get("hours_saved_per_week"), where)

    cost = raw.get("cost_per_month")
    if cost is not None and (not isinstance(cost, str) or cost not in COST_LEVELS):
        raise CatalogError(
            f"{where}: 'cost_per_month' must be one of: {', '.join(COST_LEVELS)}"
        )

    return Opportunity(
        key=raw["key"],
        area=raw["area"],
        title=raw["title"],
        description=raw["description"],
        signals=tuple(signals),
        base_effort=effort,
        example_tools=tuple(tools),
        hours_saved_per_week=hours,
        cost_per_month=cost,
    )


def _parse_hours(raw: Any, where: str) -> Optional[tuple[float, float]]:
    """Check the "hours_saved_per_week" field and return (low, high).

    The field is optional. It must be a list of two numbers [low, high].
    Each number must be from 0 to MAX_HOURS_PER_WEEK, and low must not
    be more than high.
    """
    if raw is None:
        return None
    message = (
        f"{where}: 'hours_saved_per_week' must be [low, high] with numbers "
        f"from 0 to {MAX_HOURS_PER_WEEK} and low <= high"
    )
    if not isinstance(raw, list) or len(raw) != 2:
        raise CatalogError(message)
    for value in raw:
        # bool is a subclass of int. Do not accept true/false as a number.
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise CatalogError(message)
    low, high = float(raw[0]), float(raw[1])
    if not 0 <= low <= high <= MAX_HOURS_PER_WEEK:
        raise CatalogError(message)
    return (low, high)


def parse_catalog(data: Any) -> tuple[tuple[str, ...], tuple[Opportunity, ...]]:
    """Check catalog data and return (areas, opportunities).

    The data must be an object with two lists: "areas" and "opportunities".
    Raise CatalogError if the data is not correct.
    """
    if not isinstance(data, dict):
        raise CatalogError("catalog must be an object")
    areas = data.get("areas")
    if (
        not isinstance(areas, list)
        or not areas
        or not all(isinstance(a, str) and a for a in areas)
    ):
        raise CatalogError("'areas' must be a list of area names")
    if len(set(areas)) != len(areas):
        raise CatalogError("'areas' has duplicate names")
    raw_items = data.get("opportunities")
    if not isinstance(raw_items, list) or not raw_items:
        raise CatalogError("'opportunities' must be a list that is not empty")

    area_tuple = tuple(areas)
    items = tuple(
        _parse_opportunity(raw, area_tuple, i) for i, raw in enumerate(raw_items, 1)
    )
    keys = [item.key for item in items]
    duplicates = sorted({k for k in keys if keys.count(k) > 1})
    if duplicates:
        raise CatalogError(f"duplicate opportunity key(s): {', '.join(duplicates)}")
    return area_tuple, items


def load_catalog(
    path: Union[str, Path, None] = None,
) -> tuple[tuple[str, ...], tuple[Opportunity, ...]]:
    """Load the catalog from a JSON file.

    If you do not give a path, load the default catalog in the package.
    """
    if path is None:
        text = (
            resources.files("aiaudit")
            .joinpath("data/catalog.json")
            .read_text(encoding="utf-8")
        )
        source = "built-in catalog"
    else:
        text = Path(path).read_text(encoding="utf-8")
        source = str(path)
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise CatalogError(f"{source}: not valid JSON: {exc}") from exc
    return parse_catalog(data)


AREAS, CATALOG = load_catalog()


def by_key(key: str) -> Opportunity:
    """Return the opportunity with this key."""
    for item in CATALOG:
        if item.key == key:
            return item
    raise KeyError(f"Unknown opportunity: {key}")
