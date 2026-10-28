"""Tests for the package settings in pyproject.toml."""

from pathlib import Path

import pytest

import aiaudit

ROOT = Path(__file__).resolve().parent.parent


def load_pyproject() -> dict:
    # tomllib is in Python 3.11 and later. Skip on Python 3.10.
    tomllib = pytest.importorskip("tomllib")
    with (ROOT / "pyproject.toml").open("rb") as f:
        return tomllib.load(f)


def test_project_name_and_python_version():
    data = load_pyproject()
    assert data["project"]["name"] == "ai-opportunity-audit"
    assert data["project"]["requires-python"] == ">=3.10"


def test_version_comes_from_package():
    data = load_pyproject()
    assert "version" in data["project"]["dynamic"]
    assert data["tool"]["setuptools"]["dynamic"]["version"]["attr"] == "aiaudit.__version__"
    assert aiaudit.__version__


def test_package_list_includes_aiaudit():
    data = load_pyproject()
    packages = data["tool"]["setuptools"]["packages"]
    assert "aiaudit" in packages
    for name in packages:
        assert (ROOT / name / "__init__.py").is_file()
