"""Tests for SyllabusScene."""

from pathlib import Path

import pygame
import pytest

from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.syllabus_scene import SyllabusScene


@pytest.fixture(autouse=True)
def _display():
    pygame.init()
    pygame.display.set_mode((1024, 640))
    yield
    pygame.quit()


def _pm(tmp_path: Path) -> ProfileManager:
    pm = ProfileManager(tmp_path / "p.json")
    pm.load()
    return pm


def test_syllabus_initial_not_done(tmp_path: Path) -> None:
    from unittest.mock import MagicMock

    from cognitive_data_arcade.engine.scene import Scene

    back = MagicMock(spec=Scene)
    scene = SyllabusScene(_pm(tmp_path), PL, back)
    assert not scene.is_done()


def test_syllabus_esc_exits(tmp_path: Path) -> None:
    from unittest.mock import MagicMock

    from cognitive_data_arcade.engine.scene import Scene

    back = MagicMock(spec=Scene)
    scene = SyllabusScene(_pm(tmp_path), PL, back)
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode=""))
    assert scene.is_done()
    assert scene.next_scene() is back


def test_syllabus_draw_does_not_crash(tmp_path: Path) -> None:
    from unittest.mock import MagicMock

    from cognitive_data_arcade.engine.scene import Scene

    back = MagicMock(spec=Scene)
    scene = SyllabusScene(_pm(tmp_path), PL, back)
    surface = pygame.display.get_surface()
    scene.draw(surface)


def test_syllabus_shows_completed_acts(tmp_path: Path) -> None:
    from unittest.mock import MagicMock

    from cognitive_data_arcade.engine.scene import Scene

    pm = _pm(tmp_path)
    # Complete all lessons in module 0 (lessons 1,2,3,4,6)
    for num in [1, 2, 3, 4, 6]:
        pm.complete_lesson(num)
    back = MagicMock(spec=Scene)
    scene = SyllabusScene(pm, PL, back)
    assert scene._completed_acts == {0}
