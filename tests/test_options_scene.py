from __future__ import annotations

import pygame
import pytest

from cognitive_data_arcade.engine import audio
from cognitive_data_arcade.engine.i18n import EN
from cognitive_data_arcade.profile.manager import Profile, ProfileManager
from cognitive_data_arcade.ui.options_scene import OptionsScene


@pytest.fixture
def pm(tmp_path):
    return ProfileManager(tmp_path / "profile.json")


@pytest.fixture(autouse=True)
def audio_ready(pm):
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    audio.init(pm.load())
    yield
    pygame.mixer.quit()


def _key(k: int) -> pygame.event.Event:
    return pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode="")


def test_esc_returns_back_scene(pm):
    sentinel = object()
    scene = OptionsScene(pm, EN, sentinel)
    scene.handle_event(_key(pygame.K_ESCAPE))
    assert scene.is_done()
    assert scene.next_scene() is sentinel


def test_right_increases_music_volume(pm):
    scene = OptionsScene(pm, EN, None)
    before = scene._music_vol
    scene.handle_event(_key(pygame.K_RIGHT))
    assert scene._music_vol == pytest.approx(before + 0.05)


def test_left_decreases_music_volume(pm):
    scene = OptionsScene(pm, EN, None)
    before = scene._music_vol
    scene.handle_event(_key(pygame.K_LEFT))
    assert scene._music_vol == pytest.approx(max(0.0, before - 0.05))


def test_down_switches_focus_to_sfx(pm):
    scene = OptionsScene(pm, EN, None)
    scene.handle_event(_key(pygame.K_DOWN))
    assert scene._focused == 1


def test_left_on_sfx_row_decreases_sfx_volume(pm):
    scene = OptionsScene(pm, EN, None)
    scene.handle_event(_key(pygame.K_DOWN))  # focus sfx
    before = scene._sfx_vol
    scene.handle_event(_key(pygame.K_LEFT))
    assert scene._sfx_vol == pytest.approx(max(0.0, before - 0.05))


def test_enter_toggles_music(pm):
    scene = OptionsScene(pm, EN, None)
    initial = scene._music_enabled
    scene.handle_event(_key(pygame.K_RETURN))
    assert scene._music_enabled is not initial


def test_enter_on_sfx_row_toggles_sfx(pm):
    scene = OptionsScene(pm, EN, None)
    scene.handle_event(_key(pygame.K_DOWN))
    initial = scene._sfx_enabled
    scene.handle_event(_key(pygame.K_RETURN))
    assert scene._sfx_enabled is not initial


def test_esc_persists_to_profile(pm):
    scene = OptionsScene(pm, EN, None)
    scene._music_vol = 0.42
    scene._sfx_enabled = False
    scene.handle_event(_key(pygame.K_ESCAPE))
    p = pm.load()
    assert p.music_volume == pytest.approx(0.42)
    assert p.sfx_enabled is False


def test_volume_clamps_at_zero(pm):
    scene = OptionsScene(pm, EN, None)
    for _ in range(20):
        scene.handle_event(_key(pygame.K_LEFT))
    assert scene._music_vol == pytest.approx(0.0)


def test_volume_clamps_at_one(pm):
    scene = OptionsScene(pm, EN, None)
    for _ in range(20):
        scene.handle_event(_key(pygame.K_RIGHT))
    assert scene._music_vol == pytest.approx(1.0)
