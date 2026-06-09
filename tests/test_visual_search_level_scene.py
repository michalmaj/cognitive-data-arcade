from __future__ import annotations

import pygame
import pytest

from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.visual_search_level_scene import VisualSearchLevelScene


@pytest.fixture(autouse=True)
def pg() -> None:
    pygame.init()
    yield
    pygame.quit()
    # Clear the font cache so stale Font objects don't cause segfaults
    # when pygame is re-initialised in subsequent tests.
    import cognitive_data_arcade.engine.fonts as _fonts
    _fonts._cache.clear()
    _fonts._found_name = None


def _make_scene(tmp_path) -> VisualSearchLevelScene:
    pm = ProfileManager(tmp_path / "profile.json")
    return VisualSearchLevelScene(pm, PL)


def test_initial_not_done(tmp_path) -> None:
    assert not _make_scene(tmp_path).is_done()


def test_draw_no_crash(tmp_path) -> None:
    scene = _make_scene(tmp_path)
    surf = pygame.Surface((1024, 768))
    scene.draw(surf)


def test_esc_goes_to_menu(tmp_path) -> None:
    scene = _make_scene(tmp_path)
    esc = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE, "mod": 0, "unicode": ""})
    scene.handle_event(esc)
    assert scene.is_done()
    assert scene.next_scene() is not None


def test_right_key_changes_mode_idx(tmp_path) -> None:
    scene = _make_scene(tmp_path)
    before = scene._mode_idx
    right = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT, "mod": 0, "unicode": ""})
    scene.handle_event(right)
    # active_row starts at 0 (mode row), so RIGHT increments mode
    assert scene._mode_idx == min(1, before + 1)


def test_down_key_switches_active_row(tmp_path) -> None:
    scene = _make_scene(tmp_path)
    assert scene._active_row == 0
    down = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN, "mod": 0, "unicode": ""})
    scene.handle_event(down)
    assert scene._active_row == 1


def test_enter_launches_game(tmp_path) -> None:
    scene = _make_scene(tmp_path)
    enter = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN, "mod": 0, "unicode": ""})
    scene.handle_event(enter)
    assert scene.is_done()
    next_s = scene.next_scene()
    assert next_s is not None


def test_mouse_click_mode_tile(tmp_path) -> None:
    scene = _make_scene(tmp_path)
    # Click on mode tile 1 (Shapes) — tile rect starts at _TILES_X + 1*(_TILE_W+_TILE_GAP)
    from cognitive_data_arcade.ui.visual_search_level_scene import _TILES_X, _TILE_W, _TILE_GAP, _ROW1_Y
    tile_x = _TILES_X + 1 * (_TILE_W + _TILE_GAP) + _TILE_W // 2
    tile_y = _ROW1_Y + 45
    click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (tile_x, tile_y)})
    scene.handle_event(click)
    assert scene._mode_idx == 1
