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

_ESC = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
_RETURN = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="\r")
_SPACE = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=0, unicode=" ")
_UP = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP, mod=0, unicode="")
_DOWN = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN, mod=0, unicode="")


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


def _pause(pg) -> None:
    """Put pg into paused state via ESC."""
    pg.handle_event(_ESC)


def _select(pg, item: int) -> None:
    """Navigate to pause menu item N (0-indexed) using DOWN events."""
    for _ in range(item):
        pg.handle_event(_DOWN)


def test_not_paused_initially(tmp_path: Path) -> None:
    pg, _, _ = _make(tmp_path)
    assert not pg.is_paused()
    assert not pg.is_done()


def test_esc_pauses(tmp_path: Path) -> None:
    pg, _, _ = _make(tmp_path)
    pg.handle_event(_ESC)
    assert pg.is_paused()


def test_esc_paused_resumes(tmp_path: Path) -> None:
    pg, _, _ = _make(tmp_path)
    pg.handle_event(_ESC)
    pg.handle_event(_ESC)
    assert not pg.is_paused()
    assert not pg.is_done()


def test_up_clamps_at_zero(tmp_path: Path) -> None:
    pg, _, _ = _make(tmp_path)
    _pause(pg)
    pg.handle_event(_UP)
    # Still paused and not done — navigation did not escape the menu
    assert pg.is_paused()
    assert not pg.is_done()


def test_down_navigates_and_clamps(tmp_path: Path) -> None:
    pg, _, _ = _make(tmp_path)
    _pause(pg)
    for _ in range(10):
        pg.handle_event(_DOWN)
    # Still paused — over-navigating does not break the menu
    assert pg.is_paused()
    assert not pg.is_done()


def test_restart_creates_new_scene(tmp_path: Path) -> None:
    """restart_factory must produce a scene that is not the already-played inner."""
    pg, original_inner, _ = _make(tmp_path)
    _pause(pg)
    _select(pg, 0)  # item 0 = Restart
    pg.handle_event(_RETURN)
    assert pg.is_done()
    restarted = pg.next_scene()
    assert restarted is not None
    assert restarted is not original_inner, (
        "restart_factory returned the same scene object that was already played; "
        "mutable gameplay state would persist across restarts"
    )


def test_how_to_play_opens_and_game_stays_alive(tmp_path: Path) -> None:
    from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

    pg, _, _ = _make(tmp_path)
    _pause(pg)
    _select(pg, 1)  # item 1 = How to Play
    pg.handle_event(_RETURN)
    assert not pg.is_done()
    # next_scene is None while still running; the sub-scene is active
    assert pg.next_scene() is None


def test_how_to_play_sub_scene_closes_on_space(tmp_path: Path) -> None:
    pg, _, _ = _make(tmp_path)
    _pause(pg)
    _select(pg, 1)
    pg.handle_event(_RETURN)
    pg.handle_event(_SPACE)
    # After closing HowToPlay, still paused and still alive
    assert pg.is_paused()
    assert not pg.is_done()


def test_keyref_opens_and_esc_closes(tmp_path: Path) -> None:
    pg, _, _ = _make(tmp_path)
    _pause(pg)
    _select(pg, 2)  # item 2 = Key Reference
    pg.handle_event(_RETURN)
    # After opening keyref, still paused
    assert pg.is_paused()
    assert not pg.is_done()
    # ESC closes keyref but keeps pause menu open
    pg.handle_event(_ESC)
    assert pg.is_paused()
    assert not pg.is_done()


def test_quit_returns_lesson_menu(tmp_path: Path) -> None:
    from cognitive_data_arcade.ui.menu import LessonMenuScene

    pg, _, _ = _make(tmp_path)
    _pause(pg)
    _select(pg, 4)  # item 4 = Quit
    pg.handle_event(_RETURN)
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
    _pause(pg)
    pg.update(9999)
    assert not pg.is_done()  # inner not done because update not forwarded


def test_draw_without_crash_unpaused(tmp_path: Path) -> None:
    pg, _, _ = _make(tmp_path)
    surface = pygame.Surface((1024, 768))
    pg.draw(surface)


def test_draw_without_crash_paused(tmp_path: Path) -> None:
    pg, _, _ = _make(tmp_path)
    _pause(pg)
    surface = pygame.Surface((1024, 768))
    pg.draw(surface)


def test_draw_without_crash_keyref(tmp_path: Path) -> None:
    pg, _, _ = _make(tmp_path)
    _pause(pg)
    _select(pg, 2)
    pg.handle_event(_RETURN)
    surface = pygame.Surface((1024, 768))
    pg.draw(surface)
