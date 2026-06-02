from __future__ import annotations

import pygame
import pytest

from cognitive_data_arcade.engine import audio
from cognitive_data_arcade.profile.manager import Profile


@pytest.fixture(autouse=True)
def mixer():
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    yield
    audio._sfx.clear()
    audio._current_track = ""
    audio._music_enabled = True
    audio._sfx_enabled = True
    audio._music_volume = 0.7
    audio._sfx_volume = 0.8
    pygame.mixer.quit()


def test_init_applies_profile_settings():
    profile = Profile(music_volume=0.3, sfx_volume=0.5,
                      music_enabled=False, sfx_enabled=True)
    audio.init(profile)
    s = audio.get_settings()
    assert s["music_volume"] == pytest.approx(0.3)
    assert s["music_enabled"] is False
    assert s["sfx_enabled"] is True


def test_init_generates_all_sfx():
    audio.init(Profile())
    for name in ("navigate", "select", "correct", "wrong", "pause"):
        assert name in audio._sfx


def test_play_sfx_skips_when_disabled():
    audio.init(Profile())
    audio.set_sfx_enabled(False)
    audio.play_sfx("navigate")   # must not raise


def test_play_music_skips_missing_file():
    audio.init(Profile())
    audio.play_music("menu")     # no OGG present; must not raise
    assert audio._current_track == "menu"


def test_set_music_volume_clamps():
    audio.init(Profile())
    audio.set_music_volume(1.5)
    assert audio.get_settings()["music_volume"] == pytest.approx(1.0)
    audio.set_music_volume(-0.1)
    assert audio.get_settings()["music_volume"] == pytest.approx(0.0)


def test_set_sfx_volume_clamps():
    audio.init(Profile())
    audio.set_sfx_volume(2.0)
    assert audio.get_settings()["sfx_volume"] == pytest.approx(1.0)


def test_set_music_enabled_false():
    audio.init(Profile())
    audio.set_music_enabled(False)
    assert audio.get_settings()["music_enabled"] is False


def test_get_settings_returns_all_keys():
    audio.init(Profile())
    s = audio.get_settings()
    assert set(s) == {"music_enabled", "sfx_enabled", "music_volume", "sfx_volume"}
