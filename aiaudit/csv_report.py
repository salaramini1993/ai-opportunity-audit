"""Make a CSV file of the priority list.

Use the CSV file in a spreadsheet program. Each row is one opportunity.
The rows have the same order as the priority list in the report.
"""

import csv
import io

from .scoring import ScoredOpportunity

# The column names. Do not change them without a note in the README,
# because users can have spreadsheets that use these names.
COLUMNS = (
    "rank",
    "key",
    "title",
    "area",
    "quadrant",
    "impact",
    "effort",
    "weight",
    "priority",
    "fit",
    "hours_saved_low",
    "hours_saved_high",
    "cost_per_month",
)


def _row(rank: int, r: ScoredOpportunity) -> list[object]:
    """Return the CSV values for one result.

    An empty value means that the catalog has no estimate.
    """
    hours = r.hours_saved
    low, high = hours if hours is not None else ("", "")
    opp = r.opportunity
    return [
        rank,
        opp.key,
        opp.title,
        opp.area,
        r.quadrant,
        r.impact,
        r.effort,
        r.weight,
        r.priority,
        r.fit,
        low,
        high,
        opp.cost_per_month or "",
    ]


def render_csv(results: list[ScoredOpportunity]) -> str:
    """Return the priority list as CSV text with a header row.

    The text uses commas and "\\r\\n" line ends (the CSV standard, RFC 4180).
    If there are no results, the text has only the header row.
    """
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(COLUMNS)
    for rank, r in enumerate(results, start=1):
        writer.writerow(_row(rank, r))
    return buffer.getvalue()
