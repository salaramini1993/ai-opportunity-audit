"""Tests that docs/examples.md lists every example file and each file is valid."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = sorted((ROOT / "examples").glob("*.json"))
DOC = (ROOT / "docs" / "examples.md").read_text(encoding="utf-8")


def test_there_are_example_files():
    assert EXAMPLES


def test_doc_lists_every_example_file():
    for path in EXAMPLES:
        assert f"`examples/{path.name}`" in DOC, f"{path.name} is not in docs/examples.md"


def test_doc_lists_no_missing_example_file():
    names = {p.name for p in EXAMPLES}
    for line in DOC.splitlines():
        if line.startswith("- `examples/"):
            name = line.split("`")[1].removeprefix("examples/")
            assert name in names, f"{name} is in the doc but not in examples/"


def test_every_example_has_a_business_name_and_answers():
    for path in EXAMPLES:
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data.get("business_name"), f"{path.name} has no business_name"
        assert isinstance(data.get("answers"), dict), f"{path.name} has no answers"
