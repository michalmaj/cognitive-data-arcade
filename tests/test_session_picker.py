import csv
import time
from pathlib import Path

import pygame

from cognitive_data_arcade.engine.i18n import EN
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.analysis_scene import AnalysisScene
from cognitive_data_arcade.ui.session_picker import SessionPickerScene

_ROWS = [
    {
        "participant_id": "p1",
        "session_id": "s1",
        "trial_id": 1,
        "task_name": "reaction_time",
        "condition": "simple",
        "stimulus": "circle",
        "expected_response": "space",
        "actual_response": "space",
        "correct": "True",
        "reaction_time_ms": "200.0",
        "timestamp": "2026-05-26T10:00:00+00:00",
        "distractor_count": "3",
    },
    {
        "participant_id": "p1",
        "session_id": "s1",
        "trial_id": 2,
        "task_name": "reaction_time",
        "condition": "simple",
        "stimulus": "circle",
        "expected_response": "space",
        "actual_response": "space",
        "correct": "True",
        "reaction_time_ms": "300.0",
        "timestamp": "2026-05-26T10:00:01+00:00",
        "distractor_count": "3",
    },
]


def _write_session_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(_ROWS[0].keys()))
        writer.writeheader()
        writer.writerows(_ROWS)


def _make_picker(sessions_dir: Path, tmp_path: Path) -> SessionPickerScene:
    pm = ProfileManager(tmp_path / "profile.json")
    pm.load()
    return SessionPickerScene(
        sessions_dir=sessions_dir,
        strings=EN,
        profile_manager=pm,
    )


def test_picker_lists_sessions(tmp_path: Path) -> None:
    sessions_dir = tmp_path / "rt"
    for name in ("s1.csv", "s2.csv", "s3.csv"):
        _write_session_csv(sessions_dir / name)
        time.sleep(0.01)  # ensure distinct mtimes
    picker = _make_picker(sessions_dir, tmp_path)
    assert len(picker._sessions) == 3


def test_picker_empty_dir(tmp_path: Path) -> None:
    sessions_dir = tmp_path / "rt"
    sessions_dir.mkdir()
    picker = _make_picker(sessions_dir, tmp_path)
    assert picker._sessions == []
    assert not picker.is_done()


def test_enter_on_session_sets_done(tmp_path: Path) -> None:
    sessions_dir = tmp_path / "rt"
    _write_session_csv(sessions_dir / "s1.csv")
    picker = _make_picker(sessions_dir, tmp_path)
    enter = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="\r")
    picker.handle_event(enter)
    assert picker.is_done()
    assert isinstance(picker.next_scene(), AnalysisScene)
