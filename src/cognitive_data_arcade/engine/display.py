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
    surface = pygame.display.get_surface()
    if surface is None:
        return
    currently = bool(surface.get_flags() & pygame.FULLSCREEN)
    if _fullscreen != currently:
        pygame.display.toggle_fullscreen()
