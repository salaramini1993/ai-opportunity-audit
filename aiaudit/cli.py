"""Command-line interface.

Usage:
    python -m aiaudit --answers examples/online_shop.json
    python -m aiaudit --interactive --name "My Shop"
    python -m aiaudit --answers shop.json --weight customer_support=2
    python -m aiaudit --answers shop.json --industry retail
    python -m aiaudit --answers shop.json --format html --out report.html
    python -m aiaudit --answers shop.json --format csv --out priorities.csv
    python -m aiaudit --answers shop.json --lang sv
    python -m aiaudit --answers shop.json --top 3
    python -m aiaudit --list-questions
    python -m aiaudit --list-opportunities
    python -m aiaudit --list-industries
    python -m aiaudit --list-areas
    python -m aiaudit --list-languages
    python -m aiaudit --list-formats
    python -m aiaudit --template > my_business.json
"""

import argparse
import json
import sys
from collections.abc import Mapping
from pathlib import Path

from . import __version__
from .catalog import AREAS, CATALOG, INDUSTRIES
from .csv_report import render_csv
from .html_report import render_html
from .i18n import DEFAULT_LANGUAGE, LANGUAGES
from .json_report import render_json
from .questions import QUESTIONS
from .report import render_markdown
from .scoring import MAX_SCALE, score


def parse_interactive_answer(raw: str) -> bool | int | None:
    """Parse one typed answer.

    Accept y/yes, n/no or a number from 0 to MAX_SCALE.
    Return None if the text is not a correct answer.
    """
    raw = raw.strip().lower()
    if raw in ("y", "yes"):
        return True
    if raw in ("n", "no"):
        return False
    if raw.isdigit() and 0 <= int(raw) <= MAX_SCALE:
        return int(raw)
    return None


def ask_interactive() -> dict[str, bool | int]:
    answers: dict[str, bool | int] = {}
    for q in QUESTIONS:
        while True:
            value = parse_interactive_answer(input(f"{q.text} [y/n or 0-{MAX_SCALE}] "))
            if value is not None:
                answers[q.key] = value
                break
            print(f"Type y, n or a number from 0 to {MAX_SCALE}.")
    return answers


def load_answers(
    path: Path,
) -> tuple[str, dict[str, bool | int], dict[str, object], object]:
    """Read (business name, answers, area weights, industry) from a JSON file.

    The "area_weights" object and the "industry" name are optional.
    The industry is None if the file does not have it.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    weights = data.get("area_weights", {})
    if not isinstance(weights, dict):
        raise ValueError("'area_weights' must be an object")
    return (
        data.get("business_name", "Unnamed business"),
        data["answers"],
        weights,
        data.get("industry"),
    )


def missing_question_keys(answers: Mapping[str, object]) -> list[str]:
    """Return the question keys that have no answer, in question order.

    A missing answer counts as "no", so the report still runs.
    The caller can warn the user about these keys.
    """
    return [q.key for q in QUESTIONS if q.key not in answers]


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


def parse_top(text: str) -> int:
    """Parse one "--top NUMBER" value. The number must be 1 or more."""
    try:
        value = int(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{text}' is not a whole number") from None
    if value < 1:
        raise argparse.ArgumentTypeError(f"'{text}' must be 1 or more")
    return value


def parse_min_priority(text: str) -> float:
    """Parse one "--min-priority NUMBER" value. The number must be 0 or more."""
    try:
        value = float(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{text}' is not a number") from None
    if value < 0:
        raise argparse.ArgumentTypeError(f"'{text}' must be 0 or more")
    return value


def parse_exclude(text: str) -> str:
    """Parse one "--exclude KEY" value. The key must be an opportunity key."""
    known = {item.key for item in CATALOG}
    if text not in known:
        raise argparse.ArgumentTypeError(
            f"'{text}' is not an opportunity key. Use --list-opportunities to see the keys"
        )
    return text


# English names of the languages, in the same order as LANGUAGES.
LANGUAGE_NAMES = {"en": "English", "sv": "Swedish", "fa": "Persian"}


def list_languages() -> str:
    """Return one line for each language: its code, then its English name."""
    return "\n".join(f"{code}: {LANGUAGE_NAMES[code]}" for code in LANGUAGES)


# Report formats that you can use with --format, in the order of the help text.
FORMATS = ("markdown", "html", "csv", "json")


def list_formats() -> str:
    """Return one format name for each line, in the order of FORMATS."""
    return "\n".join(FORMATS)


def list_questions() -> str:
    """Return one line for each question: its key, then its text."""
    return "\n".join(f"{q.key}: {q.text}" for q in QUESTIONS)


def list_industries() -> str:
    """Return one industry name for each line, in sorted order."""
    return "\n".join(INDUSTRIES)


def list_areas() -> str:
    """Return one area name for each line, in the order of the catalog file."""
    return "\n".join(AREAS)


def list_opportunities() -> str:
    """Return one line for each opportunity: its key, area and English title."""
    return "\n".join(f"{item.key}: {item.area}: {item.title}" for item in CATALOG)


def answers_template() -> str:
    """Return a blank answers file as JSON text.

    Every question key is set to false. Change the answers you know,
    then run the file with --answers. The business name is a placeholder.
    """
    data = {
        "business_name": "Your business name",
        "answers": {q.key: False for q in QUESTIONS},
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aiaudit", description="Run an AI opportunity audit.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    src = parser.add_mutually_exclusive_group()
    src.add_argument("--answers", type=Path, help="JSON file with answers")
    src.add_argument("--interactive", action="store_true", help="Ask the questions in the terminal")
    parser.add_argument(
        "--list-questions",
        action="store_true",
        help="Print the yes/no questions with their keys and stop. "
        "Use the keys in an answers file.",
    )
    parser.add_argument(
        "--list-opportunities",
        action="store_true",
        help="Print the opportunities with their keys, areas and titles and stop.",
    )
    parser.add_argument(
        "--list-industries",
        action="store_true",
        help="Print the industry names that you can use with --industry and stop.",
    )
    parser.add_argument(
        "--list-areas",
        action="store_true",
        help="Print the area names that you can use with --weight and stop.",
    )
    parser.add_argument(
        "--list-languages",
        action="store_true",
        help="Print the language codes that you can use with --lang and stop.",
    )
    parser.add_argument(
        "--list-formats",
        action="store_true",
        help="Print the report format names that you can use with --format and stop.",
    )
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
    parser.add_argument(
        "--industry",
        choices=INDUSTRIES,
        default=None,
        help="Show only the opportunities for this industry. "
        "This replaces the industry in the answers file.",
    )
    parser.add_argument(
        "--format",
        choices=FORMATS,
        default="markdown",
        help="Report format. The default is markdown. "
        "csv gives only the priority list, for a spreadsheet.",
    )
    parser.add_argument(
        "--template",
        action="store_true",
        help="Print a blank answers file with every question key set to false and stop. "
        "Save it, change the answers, then run it with the --answers option.",
    )
    parser.add_argument(
        "--lang",
        choices=LANGUAGES,
        default=DEFAULT_LANGUAGE,
        help="Language of the report headings and labels. The default is en. "
        "The markdown and html formats use this option. The csv format does not.",
    )
    parser.add_argument(
        "--top",
        type=parse_top,
        default=None,
        metavar="NUMBER",
        help="Show only the N opportunities with the highest priority. "
        "The default is to show all opportunities that fit.",
    )
    parser.add_argument(
        "--min-priority",
        type=parse_min_priority,
        default=None,
        metavar="NUMBER",
        help="Hide the opportunities with a priority below this number. "
        "The default is to hide none.",
    )
    parser.add_argument(
        "--exclude",
        type=parse_exclude,
        action="append",
        default=[],
        metavar="KEY",
        help="Hide the opportunity with this key. Use this option more than one time "
        "for more opportunities. The default is to hide none.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Do not print warnings. Errors are still printed.",
    )
    args = parser.parse_args(argv)

    if args.list_questions:
        print(list_questions())
        return 0
    if args.list_opportunities:
        print(list_opportunities())
        return 0
    if args.list_industries:
        print(list_industries())
        return 0
    if args.list_areas:
        print(list_areas())
        return 0
    if args.list_languages:
        print(list_languages())
        return 0
    if args.list_formats:
        print(list_formats())
        return 0
    if args.template:
        print(answers_template())
        return 0
    if not args.answers and not args.interactive:
        parser.error("one of the arguments --answers --interactive is required")

    weights: dict[str, object] = {}
    industry: object = None
    try:
        if args.answers:
            name, answers, weights, industry = load_answers(args.answers)
            missing = missing_question_keys(answers)
            if missing and not args.quiet:
                # Tell the user, but still make the report. Missing answers count as "no".
                print(
                    f"Warning: no answer for {len(missing)} question(s), counted as no: "
                    + ", ".join(missing),
                    file=sys.stderr,
                )
        else:
            name, answers = "Unnamed business", ask_interactive()
    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 2
    if args.name:
        name = args.name
    # A weight on the command line replaces the same weight in the file.
    weights = {**weights, **dict(args.weight)}
    if args.industry:
        industry = args.industry

    try:
        results = score(answers, weights, industry)
    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 2

    shown_before_filters = len(results)
    if args.exclude:
        results = [r for r in results if r.opportunity.key not in args.exclude]
    if args.min_priority is not None:
        results = [r for r in results if r.priority >= args.min_priority]
    if args.top:
        results = results[: args.top]
    if shown_before_filters and not results and not args.quiet:
        print(
            "Warning: no opportunity is left after the filters. "
            "Try a lower --min-priority or a higher --top.",
            file=sys.stderr,
        )

    # score() checked the industry, so it is a known name or None here.
    if args.format == "csv":
        report = render_csv(results)
    elif args.format == "json":
        report = render_json(name, results, industry=str(industry) if industry else None)
    elif args.format == "html":
        report = render_html(
            name, results, industry=str(industry) if industry else None, lang=args.lang
        )
    else:
        report = render_markdown(
            name, results, industry=str(industry) if industry else None, lang=args.lang
        )
    if args.out:
        # Make the folders of the file first, so a new folder name works.
        try:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            # newline="" keeps the "\r\n" line ends of the CSV text as they are.
            args.out.write_text(report, encoding="utf-8", newline="")
        except OSError as err:
            print(f"Error: cannot write the report: {err}", file=sys.stderr)
            return 2
        print(f"Report written to {args.out}")
    else:
        print(report)
    return 0
