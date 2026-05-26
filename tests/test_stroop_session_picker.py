import csv
from pathlib import Path

import pygame

from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.stroop_session_picker import StroopSessionPickerScene

_STROOP_FIELDNAMES = [
    "participant_id",
    "session_id",
    "trial_id",
    "task_name",
    "condition",
    "stimulus",
    "ink_color",
    "word_color",
    "expected_response",
    "actual_response",
    "correct",
    "reaction_time_ms",
    "timestamp",
]

_CONDS = ["congruent"] * 4 + ["neutral"] * 4 + ["incongruent"] * 4
_RTS = [260, 270, 250, 280, 310, 320, 300, 330, 420, 440, 400, 410]


def _make_stroop_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        {
            "participant_id": "p1",
            "session_id": "s1",
            "trial_id": str(i + 1),
            "task_name": "stroop",
            "condition": _CONDS[i],
            "stimulus": "CZERWONY",
            "ink_color": "red",
            "word_color": "red",
            "expected_response": "r",
            "actual_response": "r",
            "correct": "True",
            "reaction_time_ms": str(_RTS[i]),
            "timestamp": "2026-01-01T00:00:00+00:00",
        }
        for i in range(12)
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_STROOP_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def _make_picker(tmp_path: Path, sessions_dir: Path) -> StroopSessionPickerScene:
    pm = ProfileManager(tmp_path / "profile.json")
    return StroopSessionPickerScene(sessions_dir, PL, pm)


def test_picker_lists_sessions(tmp_path: Path) -> None:
    sd = tmp_path / "stroop"
    sd.mkdir()
    for i in range(3):
        _make_stroop_csv(sd / f"s{i}.csv")
    picker = _make_picker(tmp_path, sd)
    assert len(picker._sessions) == 3


def test_picker_empty_dir(tmp_path: Path) -> None:
    sd = tmp_path / "stroop"
    sd.mkdir()
    picker = _make_picker(tmp_path, sd)
    assert picker._sessions == []
    assert not picker.is_done()


def test_picker_nonexistent_dir(tmp_path: Path) -> None:
    sd = tmp_path / "stroop"
    picker = _make_picker(tmp_path, sd)
    assert picker._sessions == []


def test_enter_on_session_sets_done(tmp_path: Path) -> None:
    from cognitive_data_arcade.ui.stroop_analysis_scene import StroopAnalysisScene

    pygame.init()
    sd = tmp_path / "stroop"
    sd.mkdir()
    _make_stroop_csv(sd / "s1.csv")
    picker = _make_picker(tmp_path, sd)
    assert len(picker._sessions) == 1
    picker.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="\r")
    )
    assert picker.is_done()
    assert isinstance(picker.next_scene(), StroopAnalysisScene)
