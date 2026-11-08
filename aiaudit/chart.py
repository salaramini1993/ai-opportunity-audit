"""Make an impact/effort chart as inline SVG.

The chart is a scatter plot. The x axis is the effort (1 to 5, low
effort on the left). The y axis is the impact (1 to 5, high impact at
the top). Each opportunity is a circle with its number from the
priority list. Lines divide the chart into the four types (quadrants)
from scoring.py.

The chart always has a left-to-right layout (direction="ltr"), also in
a right-to-left report. Then the axes and the text anchors of the labels
do not change. The browser still shows right-to-left text in the
labels in the correct order.

The SVG uses no script and no external files. It shows in all modern
web browsers and in print.
"""

from collections import defaultdict
from html import escape

from .i18n import DEFAULT_LANGUAGE, t
from .scoring import ScoredOpportunity

WIDTH = 480
HEIGHT = 360
LEFT = 50
RIGHT = 20
TOP = 20
BOTTOM = 50
RADIUS = 10
# Space between the centers of circles in the same cell.
STEP = 2 * RADIUS + 2
SCALE_MAX = 5

# The quadrant borders agree with ScoredOpportunity.quadrant:
# impact 3 or more is high, effort 2 or less is low.
EFFORT_BORDER = 2.5
IMPACT_BORDER = 2.5

# Text keys from i18n.py for the quadrant labels, with the text anchor.
QUADRANT_LABELS = (
    ("chart_quick_wins", "start"),
    ("chart_strategic", "end"),
    ("chart_small", "start"),
    ("chart_not_now", "end"),
)


def _x(effort: float) -> float:
    """Return the x position for an effort value."""
    width = WIDTH - LEFT - RIGHT
    return round(LEFT + (effort - 0.5) / SCALE_MAX * width, 1)


def _y(impact: float) -> float:
    """Return the y position for an impact value."""
    height = HEIGHT - TOP - BOTTOM
    return round(TOP + (SCALE_MAX + 0.5 - impact) / SCALE_MAX * height, 1)


def point_positions(results: list[ScoredOpportunity]) -> list[tuple[float, float]]:
    """Return the (x, y) center of each circle, in the order of results.

    Opportunities with the same impact and effort are in the same cell.
    Put them in one row, centered on the cell, so that they do not cover
    each other.
    """
    cells: dict[tuple[int, int], list[int]] = defaultdict(list)
    for i, r in enumerate(results):
        cells[(r.effort, r.impact)].append(i)
    positions: list[tuple[float, float]] = [(0.0, 0.0)] * len(results)
    for (effort, impact), indexes in cells.items():
        count = len(indexes)
        for slot, i in enumerate(indexes):
            offset = (slot - (count - 1) / 2) * STEP
            positions[i] = (round(_x(effort) + offset, 1), _y(impact))
    return positions


def render_svg(results: list[ScoredOpportunity], lang: str = DEFAULT_LANGUAGE) -> str:
    """Return an SVG element with the impact/effort chart.

    The lang code selects the language of the labels in the chart and
    of the opportunity names.

    The number in each circle is the position in the priority list
    (1 is the highest priority). The <title> of each circle gives the
    opportunity name. Browsers show it when you put the pointer on it.
    """
    left, right = LEFT, WIDTH - RIGHT
    top, bottom = TOP, HEIGHT - BOTTOM
    mid_x = _x(EFFORT_BORDER)
    mid_y = _y(IMPACT_BORDER)
    lines = [
        f'<svg class="chart" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" '
        'aria-labelledby="chart-title" direction="ltr" '
        'xmlns="http://www.w3.org/2000/svg">',
        '<title id="chart-title">' + escape(t(lang, "chart_svg_title")) + "</title>",
        f'<rect x="{left}" y="{top}" width="{right - left}" height="{bottom - top}" '
        'fill="#fff" stroke="#999"/>',
        f'<rect x="{left}" y="{top}" width="{mid_x - left}" height="{mid_y - top}" '
        'fill="#e8f5e9"/>',
        f'<line x1="{mid_x}" y1="{top}" x2="{mid_x}" y2="{bottom}" '
        'stroke="#999" stroke-dasharray="4 3"/>',
        f'<line x1="{left}" y1="{mid_y}" x2="{right}" y2="{mid_y}" '
        'stroke="#999" stroke-dasharray="4 3"/>',
    ]
    corners = (
        (left + 6, top + 14),
        (right - 6, top + 14),
        (left + 6, bottom - 6),
        (right - 6, bottom - 6),
    )
    for (key, anchor), (x, y) in zip(QUADRANT_LABELS, corners, strict=True):
        lines.append(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="11" '
            f'fill="#555">{escape(t(lang, key))}</text>'
        )
    for value in range(1, SCALE_MAX + 1):
        lines.append(
            f'<text x="{_x(value)}" y="{bottom + 16}" text-anchor="middle" '
            f'font-size="11">{value}</text>'
        )
        lines.append(
            f'<text x="{left - 8}" y="{_y(value) + 4}" text-anchor="end" '
            f'font-size="11">{value}</text>'
        )
    lines += [
        f'<text x="{(left + right) / 2}" y="{HEIGHT - 8}" text-anchor="middle" '
        'font-size="12">' + escape(t(lang, "chart_x_axis")) + "</text>",
        f'<text x="14" y="{(top + bottom) / 2}" text-anchor="middle" font-size="12" '
        f'transform="rotate(-90 14 {(top + bottom) / 2})">'
        + escape(t(lang, "chart_y_axis"))
        + "</text>",
    ]
    positions = point_positions(results)
    for number, (r, (px, py)) in enumerate(zip(results, positions, strict=True), start=1):
        label = t(
            lang,
            "chart_point",
            number=number,
            title=r.opportunity.text("title", lang),
            impact=r.impact,
            effort=r.effort,
        )
        lines += [
            "<g>",
            f"<title>{escape(label)}</title>",
            f'<circle cx="{px}" cy="{py}" r="{RADIUS}" fill="#1565c0"/>',
            f'<text x="{px}" y="{py + 4}" text-anchor="middle" font-size="11" '
            f'fill="#fff">{number}</text>',
            "</g>",
        ]
    lines.append("</svg>")
    return "\n".join(lines)
