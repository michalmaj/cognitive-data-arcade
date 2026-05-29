from __future__ import annotations

import csv
from pathlib import Path

import pygame
import pytest

from cognitive_data_arcade.engine.i18n import EN
from cognitive_data_arcade.engine.scene import Scene

_COLS = [
    "task_name", "participant_id", "session_id", "trial_id", "block_id", "n_level",
    "position", "letter", "pos_match", "let_match", "key_a_pressed", "key_l_pressed",
    "pos_correct", "let_correct", "rt_a_ms", "rt_l_ms",
]


@pytest.fixture
def fixture_csv(tmp_path: Path) -> Path:
    path = tmp_path / "nback" / "test.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_COLS)
        writer.writeheader()
        for i in range(20):
            writer.writerow({
                "task_name": "nback", "participant_id": "p1", "session_id": "s1",
                "trial_id": i + 1, "block_id": 1, "n_level": 1,
                "position": 0, "letter": "B",
                "pos_match": False, "let_match": False,
                "key_a_pressed": False, "key_l_pressed": False,
                "pos_correct": True, "let_correct": True,
                "rt_a_ms": 0.0, "rt_l_ms": 0.0,
            })
    return path


class _DummyScene(Scene):
    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt_ms: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pass

    def is_done(self) -> bool:
        return False

    def next_scene(self) -> Scene | None:
        return None


def test_draws_without_crash(fixture_csv: Path) -> None:
    from cognitive_data_arcade.ui.nback_analysis_scene import NBackAnalysisScene

    pygame.init()
    surface = pygame.Surface((1024, 768))
    scene = NBackAnalysisScene(fixture_csv, EN, _DummyScene())
    scene.draw(surface)


def test_esc_sets_done(fixture_csv: Path) -> None:
    from cognitive_data_arcade.ui.nback_analysis_scene import NBackAnalysisScene

    pygame.init()
    scene = NBackAnalysisScene(fixture_csv, EN, _DummyScene())
    assert not scene.is_done()
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
    )
    assert scene.is_done()


def test_space_sets_done(fixture_csv: Path) -> None:
    from cognitive_data_arcade.ui.nback_analysis_scene import NBackAnalysisScene

    pygame.init()
    scene = NBackAnalysisScene(fixture_csv, EN, _DummyScene())
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=0, unicode=" ")
    )
    assert scene.is_done()


def test_next_scene_returns_back_scene(fixture_csv: Path) -> None:
    from cognitive_data_arcade.ui.nback_analysis_scene import NBackAnalysisScene

    pygame.init()
    back = _DummyScene()
    scene = NBackAnalysisScene(fixture_csv, EN, back)
    assert scene.next_scene() is None
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
    )
    assert scene.next_scene() is back
