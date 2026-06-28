# tests/test_logout.py
from __future__ import annotations

from pathlib import Path

import pytest

from cognitive_data_arcade.profile.manager import Profile, ProfileManager


def _make_pm(tmp_path: Path) -> ProfileManager:
    return ProfileManager(tmp_path / "profile.json")


def test_onboarding_done_defaults_false(tmp_path: Path) -> None:
    pm = _make_pm(tmp_path)
    profile = pm.load()
    assert profile.onboarding_done is False


def test_set_onboarding_done(tmp_path: Path) -> None:
    pm = _make_pm(tmp_path)
    pm.load()
    returned = pm.set_onboarding_done()
    assert returned.onboarding_done is True
    # persisted
    assert pm.load().onboarding_done is True


def test_delete_profile_removes_json(tmp_path: Path) -> None:
    pm = _make_pm(tmp_path)
    pm.load()  # creates the file
    assert (tmp_path / "profile.json").exists()
    pm.delete_profile(generated_dir=tmp_path / "generated")
    assert not (tmp_path / "profile.json").exists()


def test_delete_profile_removes_csv_files(tmp_path: Path) -> None:
    generated = tmp_path / "generated" / "reaction_time"
    generated.mkdir(parents=True)
    csv_file = generated / "20260101_120000.csv"
    csv_file.write_text("a,b\n1,2\n")

    pm = _make_pm(tmp_path)
    pm.load()
    pm.delete_profile(generated_dir=tmp_path / "generated")

    assert not csv_file.exists()


def test_delete_profile_idempotent_when_missing(tmp_path: Path) -> None:
    pm = _make_pm(tmp_path)
    # no profile created — should not raise
    pm.delete_profile(generated_dir=tmp_path / "generated")
