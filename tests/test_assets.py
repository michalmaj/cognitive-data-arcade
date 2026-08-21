from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

from cognitive_data_arcade.engine.assets import assets_dir


def test_assets_dir_returns_path():
    result = assets_dir()
    assert isinstance(result, Path)


def test_assets_dir_ends_with_assets():
    result = assets_dir()
    assert result.name == "assets"


def test_assets_dir_resolves_to_project_root_in_dev():
    result = assets_dir()
    # In dev mode the parent directory is the project root containing pyproject.toml
    assert (result.parent / "pyproject.toml").exists()


def test_assets_dir_frozen_mode_resolves_next_to_executable(tmp_path: Path) -> None:
    """In frozen (Nuitka/PyInstaller) mode assets/ must be next to the executable.

    The distribution model is: ship the exe + assets/ in the same directory.
    Students run the exe from that directory; assets/ is at Path(exe).parent / "assets".
    """
    fake_exe = tmp_path / "CognitiveDataArcade"
    fake_exe.touch()

    with (
        patch.object(sys, "frozen", True, create=True),
        patch.object(sys, "executable", str(fake_exe)),
    ):
        result = assets_dir()

    assert result == tmp_path / "assets"


def test_assets_dir_not_frozen_ignores_executable(tmp_path: Path) -> None:
    """Without sys.frozen the executable path must not influence the result."""
    fake_exe = tmp_path / "some_other_exe"
    fake_exe.touch()

    with patch.object(sys, "executable", str(fake_exe)):
        result = assets_dir()

    assert result != tmp_path / "assets"
    assert result.name == "assets"
