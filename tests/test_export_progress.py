"""Tests for progress export."""

import json
from pathlib import Path

from cognitive_data_arcade.profile.manager import ProfileManager


def test_export_creates_file(tmp_path: Path) -> None:
    pm = ProfileManager(tmp_path / "p.json")
    p = pm.load()
    p.arcade_points = 200
    p.completed_lessons = [1, 2, 3]
    pm.save(p)

    out = tmp_path / "export.json"
    pm.export_progress(out)

    assert out.exists()
    data = json.loads(out.read_text())
    assert data["arcade_points"] == 200
    assert data["completed_lessons"] == [1, 2, 3]
    assert "exported_at" in data


def test_export_includes_quiz_results(tmp_path: Path) -> None:
    pm = ProfileManager(tmp_path / "p.json")
    pm.record_quiz_result(2, correct=True)
    pm.record_quiz_result(7, correct=False)

    out = tmp_path / "export.json"
    pm.export_progress(out)

    data = json.loads(out.read_text())
    assert data["quiz_results"]["L2"] is True
    assert data["quiz_results"]["L7"] is False
