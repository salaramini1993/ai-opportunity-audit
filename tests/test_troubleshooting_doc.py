"""Tests that docs/troubleshooting.md lists the messages that the code can print."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = (ROOT / "docs" / "troubleshooting.md").read_text(encoding="utf-8")
PACKAGE_SOURCE = "\n".join(
    path.read_text(encoding="utf-8") for path in (ROOT / "aiaudit").glob("*.py")
)

# Each text below is part of a message that the code prints or raises.
MESSAGE_PARTS = [
    "Unknown question key:",
    "must be true, false or a number from 0 to",
    "Unknown area:",
    "must be a number",
    "must be from",
    "Unknown industry:",
    "'area_weights' must be an object",
    "unknown language '",
    "Warning: no answer for",
]


def test_every_message_part_is_in_the_code():
    for part in MESSAGE_PARTS:
        assert part in PACKAGE_SOURCE, f"{part!r} is not in the code"


def test_every_message_part_is_in_the_doc():
    for part in MESSAGE_PARTS:
        assert part in DOC, f"{part!r} is not in docs/troubleshooting.md"


def test_doc_has_errors_and_warnings_sections():
    assert "## Errors" in DOC
    assert "## Warnings" in DOC
