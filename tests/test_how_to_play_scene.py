from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.engine.pause import GameInfo
from cognitive_data_arcade.engine.scene import Scene

_GAME_INFO = GameInfo(
    title="Test Game",
    description_lines=["Line one.", "Line two."],
    key_bindings=[("SPACE", "do something"), ("ESC", "pause")],
)


class _Dummy(Scene):
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


def test_how_to_play_draws_without_crash() -> None:
    pygame.init()
    from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

    surface = pygame.Surface((1024, 768))
    scene = HowToPlayScene(_GAME_INFO, PL, back_scene=_Dummy())
    scene.draw(surface)


def test_how_to_play_space_returns_back() -> None:
    from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

    back = _Dummy()
    scene = HowToPlayScene(_GAME_INFO, PL, back_scene=back)
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, mod=0, unicode=" ")
    )
    assert scene.is_done()
    assert scene.next_scene() is back


def test_how_to_play_enter_returns_back() -> None:
    from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

    back = _Dummy()
    scene = HowToPlayScene(_GAME_INFO, PL, back_scene=back)
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="\r")
    )
    assert scene.is_done()
    assert scene.next_scene() is back


def test_how_to_play_esc_returns_back() -> None:
    from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

    back = _Dummy()
    scene = HowToPlayScene(_GAME_INFO, PL, back_scene=back)
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
    )
    assert scene.is_done()
    assert scene.next_scene() is back
