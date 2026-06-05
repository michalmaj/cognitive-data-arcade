from __future__ import annotations

import json
import tempfile
from pathlib import Path

from cognitive_data_arcade.profile.manager import Profile, ProfileManager


def _make_pm() -> tuple[ProfileManager, Path]:
    tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
    tmp.close()
    path = Path(tmp.name)
    path.unlink()  # let manager create it fresh
    return ProfileManager(path), path


def test_seen_intro_default_is_false():
    profile = Profile()
    assert profile.seen_intro is False


def test_set_seen_intro_persists():
    pm, _ = _make_pm()
    pm.set_seen_intro(True)
    assert pm.load().seen_intro is True


def test_old_json_without_seen_intro_defaults_to_false():
    pm, path = _make_pm()
    # Write a profile JSON that has no seen_intro key
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"alias": "tester", "language": "pl"}), encoding="utf-8")
    assert pm.load().seen_intro is False
