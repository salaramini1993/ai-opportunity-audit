"""Make a JSON file of the priority list.

The file has the business name, the industry and the priority list.
Each item in the list has the same fields as a row of the CSV report.
An empty value in the CSV report is null in the JSON report.
"""

import json

from .csv_report import COLUMNS, result_values
from .scoring import ScoredOpportunity


def render_json(
    business_name: str,
    results: list[ScoredOpportunity],
    industry: str | None = None,
) -> str:
    """Return the priority list as JSON text, with a line end at the end.

    The items are in priority order. If there are no results, the list is empty.
    """
    items = []
    for rank, r in enumerate(results, start=1):
        values = result_values(rank, r)
        items.append({c: (None if v == "" else v) for c, v in zip(COLUMNS, values, strict=True)})
    data = {"business": business_name, "industry": industry, "opportunities": items}
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"
