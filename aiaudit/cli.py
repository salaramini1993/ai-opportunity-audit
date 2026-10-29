"""Command-line interface.

Usage:
    python -m aiaudit --answers examples/online_shop.json
    python -m aiaudit --interactive --name "My Shop"
    python -m aiaudit --answers shop.json --weight customer_support=2
"""

import argparse
import json
import sys
from pathlib import Path

from .questions import QUESTIONS
from .report import render_markdown
from .scoring import score


def ask_interactive() -> dict[str, bool]:
    answers: dict[str, bool] = {}
    for q in QUESTIONS:
        while True:
            raw = input(f"{q.text} [y/n] ").strip().lower()
            if raw in ("y", "yes"):
                answers[q.key] = True
                break
            if raw in ("n", "no"):
                answers[q.key] = False
                break
            print("Type y or n.")
    return answers


def load_answers(path: Path) -> tuple[str, dict[str, bool], dict[str, object]]:
    """Read (business name, answers, area weights) from a JSON file.

    The "area_weights" object is optional.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    weights = data.get("area_weights", {})
    if not isinstance(weights, dict):
        raise ValueError("'area_weights' must be an object")
    return data.get("business_name", "Unnamed business"), data["answers"], weights


def parse_weight(text: str) -> tuple[str, float]:
    """Parse one "--weight AREA=NUMBER" value."""
    area, sep, number = text.partition("=")
    if not sep or not area.strip():
        raise argparse.ArgumentTypeError(f"'{text}' must have the form AREA=NUMBER")
    try:
        value = float(number)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{number}' is not a number") from None
    return area.strip(), value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aiaudit", description="Run an AI opportunity audit.")
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--answers", type=Path, help="JSON file with answers")
    src.add_argument("--interactive", action="store_true", help="Ask the questions in the terminal")
    parser.add_argument("--name", default=None, help="Business name for the report")
    parser.add_argument("--out", type=Path, default=None, help="Write the report to this file")
    parser.add_argument(
        "--weight",
        action="append",
        type=parse_weight,
        default=[],
        metavar="AREA=NUMBER",
        help="Make an area more (or less) important, for example customer_support=2. "
        "You can use this option more than one time.",
    )
    args = parser.parse_args(argv)

    weights: dict[str, object] = {}
    try:
        if args.answers:
            name, answers, weights = load_answers(args.answers)
        else:
            name, answers = "Unnamed business", ask_interactive()
    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 2
    if args.name:
        name = args.name
    # A weight on the command line replaces the same weight in the file.
    weights = {**weights, **dict(args.weight)}

    try:
        results = score(answers, weights)
    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 2

    report = render_markdown(name, results)
    if args.out:
        args.out.write_text(report, encoding="utf-8")
        print(f"Report written to {args.out}")
    else:
        print(report)
    return 0
