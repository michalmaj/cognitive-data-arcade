from __future__ import annotations

import pygame
import pytest

from cognitive_data_arcade.engine.i18n import EN
from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene, make_how_to_play


class _FakePM:
    class _Profile:
        device_uuid = "x"
        completed_lessons: list = []
        seen_intro: bool = False
        music_enabled = True
        sfx_enabled = True
        music_volume = 1.0
        sfx_volume = 1.0

    def __init__(self, seen_intro: bool = False):
        self._seen_intro = seen_intro

    def load(self):
        p = self._Profile()
        p.seen_intro = self._seen_intro
        return p

    def complete_lesson(self, n: int) -> None:
        pass


@pytest.fixture(autouse=True)
def _pygame():
    pygame.font.init()
    yield


def _fake_game_info():
    from cognitive_data_arcade.engine.pause import GameInfo

    return GameInfo(title="Test", description_lines=[], key_bindings=[])


def _fake_scene():
    from cognitive_data_arcade.engine.scene import Scene

    class _Dummy(Scene):
        def handle_event(self, e):
            pass

        def update(self, dt):
            pass

        def is_done(self):
            return False

        def next_scene(self):
            return None

        def draw(self, s):
            pass

    return _Dummy()


def test_make_how_to_play_returns_how_to_play_when_intro_not_seen():
    pm = _FakePM(seen_intro=False)
    back = _fake_scene()
    result = make_how_to_play(pm, _fake_game_info(), EN, back_scene=back)
    assert isinstance(result, HowToPlayScene)


def test_make_how_to_play_returns_back_scene_when_intro_seen():
    pm = _FakePM(seen_intro=True)
    back = _fake_scene()
    result = make_how_to_play(pm, _fake_game_info(), EN, back_scene=back)
    assert result is back


def test_enter_on_stroop_skips_intro_when_seen(tmp_path):
    from cognitive_data_arcade.profile.manager import ProfileManager
    from cognitive_data_arcade.ui.stroop_level_scene import StroopLevelScene

    pm = ProfileManager(tmp_path / "profile.json")
    pm.set_seen_intro(True)

    scene = StroopLevelScene(pm, EN)
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert scene.is_done()
    assert not isinstance(scene.next_scene(), HowToPlayScene)


def test_enter_on_stroop_shows_intro_when_not_seen(tmp_path):
    from cognitive_data_arcade.profile.manager import ProfileManager
    from cognitive_data_arcade.ui.stroop_level_scene import StroopLevelScene

    pm = ProfileManager(tmp_path / "profile.json")

    scene = StroopLevelScene(pm, EN)
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert scene.is_done()
    assert isinstance(scene.next_scene(), HowToPlayScene)


def test_enter_on_gono_skips_intro_when_seen(tmp_path):
    from cognitive_data_arcade.profile.manager import ProfileManager
    from cognitive_data_arcade.ui.gono_level_scene import GoNoGoLevelScene

    pm = ProfileManager(tmp_path / "profile.json")
    pm.set_seen_intro(True)

    scene = GoNoGoLevelScene(pm, EN)
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert scene.is_done()
    assert not isinstance(scene.next_scene(), HowToPlayScene)


def test_enter_on_flanker_skips_intro_when_seen(tmp_path):
    from cognitive_data_arcade.profile.manager import ProfileManager
    from cognitive_data_arcade.ui.flanker_level_scene import FlankerLevelScene

    pm = ProfileManager(tmp_path / "profile.json")
    pm.set_seen_intro(True)

    scene = FlankerLevelScene(pm, EN)
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=0, unicode=""))
    assert scene.is_done()
    assert not isinstance(scene.next_scene(), HowToPlayScene)
