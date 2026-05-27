from __future__ import annotations

from pathlib import Path

import pygame

from cognitive_data_arcade.engine.i18n import EN
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.ui.flanker_analysis_scene import FlankerAnalysisScene

_CSV = """\
participant_id,session_id,trial_id,task_name,condition,target_direction,correct,reaction_time_ms,timestamp
p1,s1,0,flanker,congruent,left,True,320.5,2026-01-01T10:00:00+00:00
p1,s1,1,flanker,congruent,right,False,2000.0,2026-01-01T10:00:01+00:00
p1,s1,2,flanker,incongruent,left,True,480.3,2026-01-01T10:00:02+00:00
p1,s1,3,flanker,incongruent,right,True,510.1,2026-01-01T10:00:03+00:00
"""


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


def test_flanker_analysis_scene_draws_without_crash(tmp_path: Path) -> None:
    csv_path = tmp_path / "flanker_session.csv"
    csv_path.write_text(_CSV)

    pygame.init()
    surface = pygame.Surface((1024, 768))
    back_scene = _DummyScene()

    scene = FlankerAnalysisScene(csv_path, EN, back_scene=back_scene)
    scene.draw(surface)


def test_flanker_analysis_scene_space_returns_to_back(tmp_path: Path) -> None:
    csv_path = tmp_path / "flanker_session.csv"
    csv_path.write_text(_CSV)

    pygame.init()
    back_scene = _DummyScene()

    scene = FlankerAnalysisScene(csv_path, EN, back_scene=back_scene)
    assert not scene.is_done()

    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=0, unicode=" ")
    )
    assert scene.is_done()
    assert scene.next_scene() is back_scene
