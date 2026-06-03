from __future__ import annotations

from pathlib import Path

import pygame

from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.ui.gono_analysis_scene import GoNoGoAnalysisScene

_CSV = """\
participant_id,session_id,trial_id,task_name,trial_type,response,correct,reaction_time_ms,timestamp
p1,s1,1,gono,go,hit,True,280.0,2026-01-01T10:00:00+00:00
p1,s1,2,gono,go,hit,True,310.0,2026-01-01T10:00:01+00:00
p1,s1,3,gono,go,miss,False,0.0,2026-01-01T10:00:02+00:00
p1,s1,4,gono,nogo,false_alarm,False,150.0,2026-01-01T10:00:03+00:00
p1,s1,5,gono,nogo,correct_rejection,True,0.0,2026-01-01T10:00:04+00:00
p1,s1,6,gono,nogo,correct_rejection,True,0.0,2026-01-01T10:00:05+00:00
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


def test_gono_analysis_scene_draws_without_crash(tmp_path: Path) -> None:
    csv_path = tmp_path / "gono_session.csv"
    csv_path.write_text(_CSV)

    pygame.init()
    surface = pygame.Surface((1024, 768))

    scene = GoNoGoAnalysisScene(csv_path, PL, back_scene=None)
    scene.draw(surface)


def test_gono_analysis_scene_space_returns_to_back(tmp_path: Path) -> None:
    csv_path = tmp_path / "gono_session.csv"
    csv_path.write_text(_CSV)

    pygame.init()
    back_scene = _DummyScene()

    scene = GoNoGoAnalysisScene(csv_path, PL, back_scene=back_scene)
    assert not scene.is_done()

    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=0, unicode=" ")
    )
    assert scene.is_done()
    assert scene.next_scene() is back_scene


def test_gono_analysis_scene_mouse_click_sets_done(tmp_path: Path) -> None:
    csv_path = tmp_path / "gono_session.csv"
    csv_path.write_text(_CSV)

    pygame.init()
    scene = GoNoGoAnalysisScene(csv_path, PL, back_scene=_DummyScene())
    scene.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(400, 300)))
    assert scene.is_done()
