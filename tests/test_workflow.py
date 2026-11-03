"""Tests for the GitHub Actions workflow file."""

from pathlib import Path

WORKFLOW = Path(__file__).resolve().parent.parent / ".github" / "workflows" / "tests.yml"


def _text():
    return WORKFLOW.read_text(encoding="utf-8")


def test_workflow_file_exists():
    assert WORKFLOW.is_file()


def test_workflow_runs_on_push_and_pull_request():
    text = _text()
    assert "push:" in text
    assert "pull_request:" in text


def test_workflow_installs_package_and_runs_pytest():
    text = _text()
    assert 'pip install ".[test]"' in text
    assert "python -m pytest" in text


def test_workflow_tests_lowest_supported_python():
    # pyproject.toml says requires-python = ">=3.10".
    assert '"3.10"' in _text()
