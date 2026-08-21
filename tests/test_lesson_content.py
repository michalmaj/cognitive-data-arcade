"""Regression tests for lesson content correctness.

These tests catch bugs that are invisible to the Python test suite because
they live inside string literals displayed to students, not executable code.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

_LESSONS_SRC = Path(__file__).resolve().parents[1] / "src" / "cognitive_data_arcade" / "lessons"
_LESSONS_MD = Path(__file__).resolve().parents[1] / "lessons"

# Matches "data/generated/" NOT immediately preceded by "cognitive_data_arcade/".
# The correct path is "~/.cognitive_data_arcade/data/generated/"; the stale path
# was the project-relative "data/generated/" used before v1.0.0b1.
_STALE_PATH_RE = re.compile(r"(?<!cognitive_data_arcade/)data/generated/")


def _lesson_py_files() -> list[Path]:
    return sorted(_LESSONS_SRC.glob("lesson_*.py"))


def _lesson_md_files() -> list[Path]:
    return sorted(_LESSONS_MD.rglob("*.md"))


@pytest.mark.parametrize("path", _lesson_py_files(), ids=lambda p: p.name)
def test_no_stale_data_path_in_lesson_py(path: Path) -> None:
    """In-game lesson text must not instruct students to look in data/generated/.

    Reproduces the regression where lesson_03.py and lesson_04.py
    referenced the pre-v1.0.0b1 project-relative path instead of
    ~/.cognitive_data_arcade/data/generated/.
    """
    content = path.read_text(encoding="utf-8")
    match = _STALE_PATH_RE.search(content)
    assert match is None, (
        f"{path.name}: stale path 'data/generated/' at offset {match.start() if match else -1} — "
        f"use '~/.cognitive_data_arcade/data/generated/' instead"
    )


@pytest.mark.parametrize("path", _lesson_md_files(), ids=lambda p: p.relative_to(_LESSONS_MD))
def test_no_stale_data_path_in_lesson_md(path: Path) -> None:
    """Lesson markdown files must not reference the stale data/generated/ path.

    Reproduces the regression where lessons/03-06 markdown files referenced
    the pre-v1.0.0b1 project-relative path.
    """
    content = path.read_text(encoding="utf-8")
    match = _STALE_PATH_RE.search(content)
    assert match is None, (
        f"{path.relative_to(_LESSONS_MD)}: stale path 'data/generated/' at offset "
        f"{match.start() if match else -1} — "
        f"use '~/.cognitive_data_arcade/data/generated/' instead"
    )
