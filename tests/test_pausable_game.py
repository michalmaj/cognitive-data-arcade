from __future__ import annotations

from pathlib import Path

import pygame

from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.engine.pause import GameInfo
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import ProfileManager

_GAME_INFO = GameInfo(
    title="Test",
    description_lines=["desc"],
    key_bindings=[("SPACE", "act"), ("ESC", "pause")],
)


class _Inner(Scene):
    """Controllable inner scene for testing."""

    def __init__(self) -> None:
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt_ms: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((10, 10, 10))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    def finish(self, next_scene: Scene | None = None) -> None:
        self._next = next_scene
        self._done = True


def _make(tmp_path: Path) -> tuple:
    pygame.init()
    from cognitive_data_arcade.engine.pause import PausableGame

    pm = ProfileManager(tmp_path / "profile.json")
    inner = _Inner()
    pg = PausableGame(inner, _GAME_INFO, lambda: _Inner(), PL, pm)
    return pg, inner, pm


def test_not_paused_initially(tmp_path: Path) -> None:
    pg, _, _ = _make(tmp_path)
    assert not pg._paused
    assert not pg.is_done()


def test_esc_pauses(tmp_path: Path) -> None:
    pg, _, _ = _make(tmp_path)
    pg.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
    )
    assert pg._paused


def test_esc_paused_resumes(tmp_path: Path) -> None:
    pg, _, _ = _make(tmp_path)
    pg.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
    )
    pg.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
    )
    assert not pg._paused
    assert not pg.is_done()


def test_up_clamps_at_zero(tmp_path: Path) -> None:
    pg, _, _ = _make(tmp_path)
    pg._paused = True
    pg.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP, mod=0, unicode="")
    )
    assert pg._selected == 0


def test_down_navigates_and_clamps(tmp_path: Path) -> None:
    pg, _, _ = _make(tmp_path)
    pg._paused = True
    for _ in range(10):
        pg.handle_event(
            pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN, mod=0, unicode="")
        )
    assert pg._selected == 4  # clamped at max index (_MENU_ITEMS - 1)


def test_restart_creates_new_scene(tmp_path: Path) -> None:
    pg, _, _ = _make(tmp_path)
    pg._paused = True
    pg._selected = 0
    pg.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="\r")
    )
    assert pg.is_done()
    assert pg.next_scene() is not None


def test_how_to_play_opens_sub_scene(tmp_path: Path) -> None:
    from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

    pg, _, _ = _make(tmp_path)
    pg._paused = True
    pg._selected = 1
    pg.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="\r")
    )
    assert not pg.is_done()
    assert isinstance(pg._sub_scene, HowToPlayScene)


def test_how_to_play_sub_scene_closes_on_space(tmp_path: Path) -> None:
    pg, _, _ = _make(tmp_path)
    pg._paused = True
    pg._selected = 1
    pg.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="\r")
    )
    pg.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=0, unicode=" ")
    )
    assert pg._sub_scene is None
    assert not pg._paused  # resumed after how-to-play


def test_keyref_opens(tmp_path: Path) -> None:
    pg, _, _ = _make(tmp_path)
    pg._paused = True
    pg._selected = 2
    pg.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="\r")
    )
    assert pg._show_keyref


def test_keyref_esc_closes(tmp_path: Path) -> None:
    pg, _, _ = _make(tmp_path)
    pg._paused = True
    pg._show_keyref = True
    pg.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
    )
    assert not pg._show_keyref
    assert pg._paused  # still paused, just closed keyref


def test_quit_returns_lesson_menu(tmp_path: Path) -> None:
    from cognitive_data_arcade.ui.menu import LessonMenuScene

    pg, _, _ = _make(tmp_path)
    pg._paused = True
    pg._selected = 4
    pg.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="\r")
    )
    assert pg.is_done()
    assert isinstance(pg.next_scene(), LessonMenuScene)


def test_inner_done_propagates(tmp_path: Path) -> None:
    pg, inner, _ = _make(tmp_path)
    sentinel = _Inner()
    inner.finish(next_scene=sentinel)
    pg.update(0)
    assert pg.is_done()
    assert pg.next_scene() is sentinel


def test_update_frozen_when_paused(tmp_path: Path) -> None:
    pg, inner, _ = _make(tmp_path)
    pg._paused = True
    pg.update(9999)
    assert not pg.is_done()  # inner not done because update not forwarded


def test_draw_without_crash_unpaused(tmp_path: Path) -> None:
    pg, _, _ = _make(tmp_path)
    surface = pygame.Surface((1024, 768))
    pg.draw(surface)


def test_draw_without_crash_paused(tmp_path: Path) -> None:
    pg, _, _ = _make(tmp_path)
    pg._paused = True
    surface = pygame.Surface((1024, 768))
    pg.draw(surface)


def test_draw_without_crash_keyref(tmp_path: Path) -> None:
    pg, _, _ = _make(tmp_path)
    pg._paused = True
    pg._show_keyref = True
    surface = pygame.Surface((1024, 768))
    pg.draw(surface)
