from __future__ import annotations

import pygame

_W, _H = 1024, 768
_fullscreen: bool = False


def init(fullscreen: bool) -> None:
    global _fullscreen
    _fullscreen = fullscreen
    _apply()


def toggle() -> None:
    global _fullscreen
    _fullscreen = not _fullscreen
    _apply()


def is_fullscreen() -> bool:
    return _fullscreen


def _apply() -> None:
    if pygame.display.get_surface() is None:
        return
    flags = (pygame.FULLSCREEN | pygame.SCALED) if _fullscreen else 0
    pygame.display.set_mode((_W, _H), flags)
