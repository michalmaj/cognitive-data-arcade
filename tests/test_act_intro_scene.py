"""Tests for ActIntroScene and make_act_intro factory."""

from pathlib import Path

import pygame
import pytest

from cognitive_data_arcade.engine.i18n import PL, EN
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.act_intro_scene import ActIntroScene, make_act_intro


@pytest.fixture(autouse=True)
def _display():
    pygame.init()
    pygame.display.set_mode((1024, 768))
    yield
    pygame.quit()


def _pm(tmp_path: Path) -> ProfileManager:
    pm = ProfileManager(tmp_path / "p.json")
    pm.load()
    return pm


def test_act_intro_initial_not_done(tmp_path: Path) -> None:
    from unittest.mock import MagicMock
    from cognitive_data_arcade.engine.scene import Scene

    back = MagicMock(spec=Scene)
    scene = ActIntroScene(module_idx=0, pm=_pm(tmp_path), strings=PL, back_scene=back)
    assert not scene.is_done()


def test_act_intro_space_marks_done_and_seen(tmp_path: Path) -> None:
    from unittest.mock import MagicMock
    from cognitive_data_arcade.engine.scene import Scene

    pm = _pm(tmp_path)
    back = MagicMock(spec=Scene)
    scene = ActIntroScene(module_idx=2, pm=pm, strings=PL, back_scene=back)
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=0, unicode=" "))
    assert scene.is_done()
    assert 2 in pm.load().seen_act_intros


def test_act_intro_escape_exits_without_marking_seen(tmp_path: Path) -> None:
    from unittest.mock import MagicMock
    from cognitive_data_arcade.engine.scene import Scene

    pm = _pm(tmp_path)
    back = MagicMock(spec=Scene)
    scene = ActIntroScene(module_idx=1, pm=pm, strings=PL, back_scene=back)
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode=""))
    assert scene.is_done()
    assert 1 not in pm.load().seen_act_intros


def test_make_act_intro_returns_intro_scene_when_not_seen(tmp_path: Path) -> None:
    from unittest.mock import MagicMock
    from cognitive_data_arcade.engine.scene import Scene

    pm = _pm(tmp_path)
    back = MagicMock(spec=Scene)
    result = make_act_intro(pm, module_idx=0, strings=PL, back_scene=back)
    assert isinstance(result, ActIntroScene)


def test_make_act_intro_returns_back_when_already_seen(tmp_path: Path) -> None:
    from unittest.mock import MagicMock
    from cognitive_data_arcade.engine.scene import Scene

    pm = _pm(tmp_path)
    pm.set_seen_act_intro(0)
    back = MagicMock(spec=Scene)
    result = make_act_intro(pm, module_idx=0, strings=PL, back_scene=back)
    assert result is back


def test_draw_does_not_crash(tmp_path: Path) -> None:
    from unittest.mock import MagicMock
    from cognitive_data_arcade.engine.scene import Scene

    back = MagicMock(spec=Scene)
    scene = ActIntroScene(module_idx=3, pm=_pm(tmp_path), strings=EN, back_scene=back)
    surface = pygame.display.get_surface()
    scene.draw(surface)
