"""Tests that docs/cli.md lists every option of the aiaudit command."""

from pathlib import Path

from aiaudit.cli import main

ROOT = Path(__file__).resolve().parent.parent
DOC = (ROOT / "docs" / "cli.md").read_text(encoding="utf-8")


def help_option_names(capsys) -> list[str]:
    """Return the long option names that the help text shows."""
    try:
        main(["--help"])
    except SystemExit:
        pass
    text = capsys.readouterr().out
    names = []
    for word in text.replace(",", " ").replace("[", " ").replace("]", " ").split():
        word = word.split("=")[0].strip("()|")
        if word.startswith("--") and word != "--":
            names.append(word)
    return sorted(set(names))


def test_doc_mentions_every_help_option(capsys):
    names = help_option_names(capsys)
    assert "--answers" in names
    for name in names:
        assert f"`{name}" in DOC, f"{name} is not in docs/cli.md"


def test_doc_mentions_the_list_options():
    for name in (
        "--list-questions",
        "--list-opportunities",
        "--list-industries",
        "--list-areas",
        "--list-languages",
        "--list-formats",
    ):
        assert f"`{name}`" in DOC
