import json
from pathlib import Path

from cognitive_data_arcade.profile.manager import Profile, ProfileManager


def _make_pm(tmp_path: Path, **profile_kwargs) -> tuple[ProfileManager, Path]:
    profile_path = tmp_path / "profile.json"
    pm = ProfileManager(profile_path)
    profile = Profile(**profile_kwargs)
    pm.save(profile)
    export_path = tmp_path / "export.json"
    return pm, export_path


def test_export_has_required_keys(tmp_path):
    pm, export_path = _make_pm(tmp_path)
    pm.export_progress(export_path)
    data = json.loads(export_path.read_text())
    required = {
        "alias",
        "exported_at",
        "app_version",
        "completed_lessons",
        "completed_count",
        "arcade_points",
        "sp_points",
        "streak_days",
        "last_active_date",
        "quiz_results",
        "quiz_accuracy_pct",
        "badges",
        "module_completion",
    }
    assert required.issubset(data.keys())


def test_export_module_completion(tmp_path):
    pm, export_path = _make_pm(tmp_path, completed_lessons=[1, 2, 3, 4, 6])
    pm.export_progress(export_path)
    data = json.loads(export_path.read_text())
    assert data["module_completion"]["1"] == {"done": 5, "total": 5}
    assert data["module_completion"]["2"] == {"done": 0, "total": 6}


def test_export_quiz_accuracy(tmp_path):
    pm, export_path = _make_pm(tmp_path, quiz_results={"1": True, "2": True, "3": False})
    pm.export_progress(export_path)
    data = json.loads(export_path.read_text())
    assert data["quiz_accuracy_pct"] == 67


def test_export_quiz_accuracy_null_when_no_quizzes(tmp_path):
    pm, export_path = _make_pm(tmp_path)
    pm.export_progress(export_path)
    data = json.loads(export_path.read_text())
    assert data["quiz_accuracy_pct"] is None


def test_export_app_version_present(tmp_path):
    pm, export_path = _make_pm(tmp_path)
    pm.export_progress(export_path)
    data = json.loads(export_path.read_text())
    assert isinstance(data["app_version"], str)
    assert len(data["app_version"]) > 0
