from __future__ import annotations

import numpy as np
import pygame

from cognitive_data_arcade.profile.manager import Profile

_music_enabled: bool = True
_sfx_enabled: bool = True
_music_volume: float = 0.7
_sfx_volume: float = 0.8
_current_track: str = ""
_sfx: dict[str, pygame.mixer.Sound] = {}


def init(profile: Profile) -> None:
    global _music_enabled, _sfx_enabled, _music_volume, _sfx_volume
    _music_enabled = profile.music_enabled
    _sfx_enabled = profile.sfx_enabled
    _music_volume = profile.music_volume
    _sfx_volume = profile.sfx_volume
    if not pygame.mixer.get_init():
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    _build_sfx()


def _build_sfx() -> None:
    global _sfx
    _sfx = {
        "navigate": _make_tone(440, 60),
        "select":   _make_tone(660, 80),
        "correct":  _make_tone(880, 120),
        "wrong":    _make_tone(220, 150),
        "pause":    _make_tone(550, 90),
    }
    _apply_sfx_volume()


def _make_tone(freq: float, duration_ms: int) -> pygame.mixer.Sound:
    sample_rate = 44100
    n = int(sample_rate * duration_ms / 1000)
    t = np.linspace(0, duration_ms / 1000, n, endpoint=False)
    fade = max(1, n // 5)
    env = np.ones(n, dtype=np.float32)
    env[-fade:] = np.linspace(1.0, 0.0, fade)
    wave = (0.4 * np.sin(2 * np.pi * freq * t) * env * 32767).astype(np.int16)
    stereo = np.column_stack([wave, wave])
    return pygame.sndarray.make_sound(stereo)


def play_music(track: str) -> None:
    global _current_track
    _current_track = track
    if not _music_enabled:
        return
    _start_music(track)


def _start_music(track: str) -> None:
    from pathlib import Path
    path = Path("assets") / "audio" / "music" / f"{track}.ogg"
    if not path.exists():
        return
    try:
        pygame.mixer.music.load(str(path))
        pygame.mixer.music.set_volume(_music_volume)
        pygame.mixer.music.play(-1)
    except pygame.error:
        pass


def stop_music() -> None:
    global _current_track
    _current_track = ""
    try:
        pygame.mixer.music.stop()
    except pygame.error:
        pass


def play_sfx(name: str) -> None:
    if not _sfx_enabled:
        return
    sound = _sfx.get(name)
    if sound is not None:
        sound.play()


def set_music_volume(v: float) -> None:
    global _music_volume
    _music_volume = max(0.0, min(1.0, v))
    try:
        pygame.mixer.music.set_volume(_music_volume)
    except pygame.error:
        pass


def set_sfx_volume(v: float) -> None:
    global _sfx_volume
    _sfx_volume = max(0.0, min(1.0, v))
    _apply_sfx_volume()


def set_music_enabled(b: bool) -> None:
    global _music_enabled
    _music_enabled = b
    if b and _current_track:
        _start_music(_current_track)
    elif not b:
        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass


def set_sfx_enabled(b: bool) -> None:
    global _sfx_enabled
    _sfx_enabled = b


def get_settings() -> dict:
    return {
        "music_enabled": _music_enabled,
        "sfx_enabled": _sfx_enabled,
        "music_volume": _music_volume,
        "sfx_volume": _sfx_volume,
    }


def _apply_sfx_volume() -> None:
    for sound in _sfx.values():
        sound.set_volume(_sfx_volume)
