"""Font loading utility — loads bundled Inter-Regular.ttf for crisp, modern text."""
from __future__ import annotations

from pathlib import Path

import pygame

_BUNDLED = Path("assets") / "fonts" / "Inter-Regular.ttf"

_FALLBACK_CANDIDATES = [
    "dejavusans",
    "arialunicode",
    "arial",
    "helveticaneue",
    "liberationsans",
    "notosans",
    "freesans",
    "droidsans",
]

_cache: dict[int, pygame.font.Font] = {}
_bundled_ok: bool | None = None


def get_font(size: int) -> pygame.font.Font:
    """Return Inter at *size*, falling back to system fonts if the file is missing."""
    global _bundled_ok
    pygame.font.init()
    if size in _cache:
        try:
            _cache[size].size("a")
            return _cache[size]
        except Exception:
            _cache.clear()
            _bundled_ok = None

    if _bundled_ok is None:
        _bundled_ok = _BUNDLED.exists()

    if _bundled_ok:
        font = pygame.font.Font(str(_BUNDLED), size)
    else:
        font = _load_system_font(size)

    _cache[size] = font
    return font


def reset() -> None:
    """Clear the font cache. Call after pygame.quit() to avoid dangling C pointers."""
    global _bundled_ok
    _cache.clear()
    _bundled_ok = None


def _load_system_font(size: int) -> pygame.font.Font:
    pygame.font.init()
    avail = frozenset(pygame.font.get_fonts())
    for candidate in [c.replace(" ", "").lower() for c in _FALLBACK_CANDIDATES]:
        if candidate in avail:
            return pygame.font.SysFont(candidate, size)
    return pygame.font.SysFont(None, size)
