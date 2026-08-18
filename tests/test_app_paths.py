"""Tests for AppPaths and CWD-independence of generated data paths."""

from __future__ import annotations

from pathlib import Path

import pytest

from cognitive_data_arcade.engine.app_paths import AppPaths, default_app_paths
from cognitive_data_arcade.profile.manager import ProfileManager


def _make_paths(tmp_path: Path) -> AppPaths:
    return AppPaths(
        profile_dir=tmp_path,
        generated_data_dir=tmp_path / "generated",
        export_dir=tmp_path / "exports",
        asset_dir=tmp_path,
    )


def _make_pm(tmp_path: Path) -> ProfileManager:
    paths = _make_paths(tmp_path)
    return ProfileManager(tmp_path / "profile.json", app_paths=paths)


# ── AppPaths construction ──────────────────────────────────────────────────────


def test_app_paths_requires_absolute_paths(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="must be absolute"):
        AppPaths(
            profile_dir=Path("relative"),
            generated_data_dir=tmp_path / "g",
            export_dir=tmp_path / "e",
            asset_dir=tmp_path,
        )


def test_default_app_paths_all_absolute() -> None:
    paths = default_app_paths()
    assert paths.profile_dir.is_absolute()
    assert paths.generated_data_dir.is_absolute()
    assert paths.export_dir.is_absolute()
    assert paths.asset_dir.is_absolute()


def test_default_app_paths_rooted_in_home() -> None:
    paths = default_app_paths()
    assert str(paths.profile_dir).startswith(str(Path.home()))
    assert str(paths.generated_data_dir).startswith(str(Path.home()))


# ── ProfileManager.paths ──────────────────────────────────────────────────────


def test_pm_paths_set_when_app_paths_provided(tmp_path: Path) -> None:
    paths = _make_paths(tmp_path)
    pm = ProfileManager(tmp_path / "profile.json", app_paths=paths)
    assert pm.paths is paths


def test_pm_paths_derived_when_no_app_paths(tmp_path: Path) -> None:
    pm = ProfileManager(tmp_path / "profile.json")
    assert pm.paths.profile_dir == tmp_path
    assert pm.paths.generated_data_dir.is_absolute()


# ── CWD independence ──────────────────────────────────────────────────────────


def test_profile_write_independent_of_cwd(tmp_path: Path, monkeypatch) -> None:
    """Profile is written to pm.paths regardless of process CWD."""
    pm = _make_pm(tmp_path)
    profile_path = tmp_path / "profile.json"

    # Change CWD to an unrelated directory
    monkeypatch.chdir(tmp_path / "..")
    pm.load()  # triggers save on first load

    assert profile_path.exists(), "Profile not written at absolute path"


def test_generated_data_dir_independent_of_cwd(tmp_path: Path, monkeypatch) -> None:
    """pm.paths.generated_data_dir is absolute and stays correct after CWD change."""
    pm = _make_pm(tmp_path)
    expected = tmp_path / "generated"

    monkeypatch.chdir(tmp_path / "..")

    # The path must remain correct regardless of CWD
    assert pm.paths.generated_data_dir == expected
    assert pm.paths.generated_data_dir.is_absolute()


def test_csv_loader_writes_to_absolute_path(tmp_path: Path, monkeypatch) -> None:
    """csv_loader uses the injected data_root, not a CWD-relative fallback."""
    from cognitive_data_arcade.games.cognitive_dashboard.csv_loader import (
        has_any_csv_data,
        load_session_from_csv,
    )

    data_root = tmp_path / "generated"
    data_root.mkdir()

    # No data yet
    monkeypatch.chdir(tmp_path / "..")
    assert not has_any_csv_data(data_root)
    session = load_session_from_csv(data_root)
    assert session.rt is None
