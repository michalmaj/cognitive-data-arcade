from pathlib import Path

import pygame

from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.profile_screen import ProfileScene


class _StubScene(Scene):
    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt_ms: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pass

    def is_done(self) -> bool:
        return False


def _make_scene(tmp_path: Path) -> ProfileScene:
    pm = ProfileManager(tmp_path / "profile.json")
    pm.load()  # create default profile
    return ProfileScene(pm, PL, _StubScene())


def test_profile_scene_is_not_done_initially(tmp_path: Path) -> None:
    scene = _make_scene(tmp_path)
    assert not scene.is_done()


def test_profile_scene_esc_triggers_done(tmp_path: Path) -> None:
    scene = _make_scene(tmp_path)
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
    )
    assert scene.is_done()


def test_profile_scene_esc_returns_back_scene(tmp_path: Path) -> None:
    pm = ProfileManager(tmp_path / "profile.json")
    back = _StubScene()
    scene = ProfileScene(pm, PL, back)
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
    )
    assert scene.next_scene() is back


def test_profile_scene_draw_does_not_crash(tmp_path: Path) -> None:
    pygame.init()
    surface = pygame.Surface((1024, 768))
    scene = _make_scene(tmp_path)
    scene.draw(surface)


def test_profile_scene_alias_edit_saves(tmp_path: Path) -> None:
    pm = ProfileManager(tmp_path / "profile.json")
    pm.load()  # create default profile with alias="anonymous"
    scene = ProfileScene(pm, PL, _StubScene())

    # Press E to start editing (clears buffer)
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e, mod=0, unicode="e")
    )

    # Type "neo"
    for char in "neo":
        scene.handle_event(
            pygame.event.Event(pygame.KEYDOWN, key=0, mod=0, unicode=char)
        )

    # Confirm with Enter
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode="\r")
    )

    assert pm.load().alias == "neo"


def test_profile_scene_alias_edit_cancel_restores(tmp_path: Path) -> None:
    pm = ProfileManager(tmp_path / "profile.json")
    pm.load()
    scene = ProfileScene(pm, PL, _StubScene())

    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e, mod=0, unicode="e")
    )
    for char in "neo":
        scene.handle_event(
            pygame.event.Event(pygame.KEYDOWN, key=0, mod=0, unicode=char)
        )

    # Cancel with Escape — cancels edit AND triggers scene done (returns to back)
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
    )

    # Alias not saved
    assert pm.load().alias == "anonymous"
