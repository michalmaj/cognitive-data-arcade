"""Tests for ResetConfirmScene — progress reset dialog."""

from pathlib import Path

import pygame
import pytest

from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.reset_confirm_scene import ResetConfirmScene


@pytest.fixture(autouse=True)
def _display():
    pygame.init()
    pygame.display.set_mode((1024, 768))
    yield
    pygame.quit()


def _make(tmp_path: Path) -> tuple[ResetConfirmScene, ProfileManager]:
    from cognitive_data_arcade.engine.scene import Scene
    from unittest.mock import MagicMock

    pm = ProfileManager(tmp_path / "profile.json")
    p = pm.load()
    p.arcade_points = 500
    p.badges = ["first_game"]
    p.current_module_idx = 1
    p.seen_intro = True
    pm.save(p)

    back = MagicMock(spec=Scene)
    scene = ResetConfirmScene(pm, PL, back)
    return scene, pm


def _key(k: int) -> pygame.event.Event:
    return pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode="")


def test_initial_state_is_choosing(tmp_path: Path) -> None:
    scene, _ = _make(tmp_path)
    assert scene._state == "choosing"
    assert not scene.is_done()


def test_esc_in_choosing_exits(tmp_path: Path) -> None:
    scene, _ = _make(tmp_path)
    scene.handle_event(_key(pygame.K_ESCAPE))
    assert scene.is_done()


def test_key_1_enters_confirming(tmp_path: Path) -> None:
    scene, _ = _make(tmp_path)
    scene.handle_event(_key(pygame.K_1))
    assert scene._state == "confirming"
    assert scene._selected == 0


def test_key_2_enters_confirming(tmp_path: Path) -> None:
    scene, _ = _make(tmp_path)
    scene.handle_event(_key(pygame.K_2))
    assert scene._state == "confirming"
    assert scene._selected == 1


def test_key_3_enters_confirming(tmp_path: Path) -> None:
    scene, _ = _make(tmp_path)
    scene.handle_event(_key(pygame.K_3))
    assert scene._state == "confirming"
    assert scene._selected == 2


def test_esc_in_confirming_returns_to_choosing(tmp_path: Path) -> None:
    scene, _ = _make(tmp_path)
    scene.handle_event(_key(pygame.K_1))
    assert scene._state == "confirming"
    scene.handle_event(_key(pygame.K_ESCAPE))
    assert scene._state == "choosing"
    assert not scene.is_done()


def test_confirm_option0_resets_progress(tmp_path: Path) -> None:
    scene, pm = _make(tmp_path)
    scene.handle_event(_key(pygame.K_1))  # select option 0
    scene.handle_event(_key(pygame.K_RETURN))  # confirm YES
    assert scene.is_done()
    after = pm.load()
    assert after.arcade_points == 0
    assert after.badges == []
    assert after.current_module_idx == 1  # preserved


def test_confirm_option1_resets_module_progress(tmp_path: Path) -> None:
    scene, pm = _make(tmp_path)
    scene.handle_event(_key(pygame.K_2))
    scene.handle_event(_key(pygame.K_RETURN))
    assert scene.is_done()
    after = pm.load()
    assert after.current_module_idx is None
    assert after.seen_intro is False
    assert after.arcade_points == 500  # preserved


def test_confirm_option2_full_reset(tmp_path: Path) -> None:
    scene, pm = _make(tmp_path)
    scene.handle_event(_key(pygame.K_3))
    scene.handle_event(_key(pygame.K_RETURN))
    assert scene.is_done()
    after = pm.load()
    assert after.arcade_points == 0
    assert after.badges == []
    assert after.current_module_idx is None


def test_draw_does_not_crash(tmp_path: Path) -> None:
    scene, _ = _make(tmp_path)
    surface = pygame.display.get_surface()
    scene.draw(surface)  # CHOOSING state
    scene.handle_event(_key(pygame.K_2))
    scene.draw(surface)  # CONFIRMING state
