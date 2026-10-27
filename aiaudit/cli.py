"""Command-line interface.

Usage:
    python -m aiaudit --answers examples/online_shop.json
    python -m aiaudit --interactive --name "My Shop"
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


def load_answers(path: Path) -> tuple[str, dict[str, bool]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("business_name", "Unnamed business"), data["answers"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aiaudit", description="Run an AI opportunity audit.")
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--answers", type=Path, help="JSON file with answers")
    src.add_argument("--interactive", action="store_true", help="Ask the questions in the terminal")
    parser.add_argument("--name", default=None, help="Business name for the report")
    parser.add_argument("--out", type=Path, default=None, help="Write the report to this file")
    args = parser.parse_args(argv)

    if args.answers:
        name, answers = load_answers(args.answers)
    else:
        name, answers = "Unnamed business", ask_interactive()
    if args.name:
        name = args.name

    try:
        results = score(answers)
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
