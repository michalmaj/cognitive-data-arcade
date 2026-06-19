"""Font loading utility.

pygame.font.SysFont(None, ...) uses the default system font which often lacks
Unicode coverage for Polish diacritics. This module tries a priority list of
fonts known to support full Latin Extended-A (Polish characters).
"""

from __future__ import annotations

import pygame

_CANDIDATES = [
    "dejavusans",
    "arialunicode",
    "arial",
    "helveticaneue",
    "liberationsans",
    "noto sans",
    "freesans",
    "droidsans",
]


def _available() -> frozenset[str]:
    pygame.font.init()
    return frozenset(pygame.font.get_fonts())


_cache: dict[int, pygame.font.Font] = {}
_found_name: str | None = None
_pygame_initialized: bool = False


def get_font(size: int) -> pygame.font.Font:
    """Return a font at *size* that can render Polish diacritics."""
    global _found_name, _pygame_initialized

    # Clear cache if pygame was quit and reinitialized
    try:
        if pygame.display.get_surface() is None and _pygame_initialized:
            _cache.clear()
    except:
        pass

    if size in _cache:
        try:
            # Verify the font is still valid by checking its size
            _cache[size].size(size)
            return _cache[size]
        except:
            # Font is stale, clear the cache
            _cache.clear()

    pygame.font.init()
    _pygame_initialized = True

    if _found_name is None:
        avail = _available()
        for candidate in _candidates_normalised():
            if candidate in avail:
                _found_name = candidate
                break

    if _found_name is not None:
        font = pygame.font.SysFont(_found_name, size)
    else:
        font = pygame.font.SysFont(None, size)

    _cache[size] = font
    return font


def _candidates_normalised() -> list[str]:
    return [c.replace(" ", "").lower() for c in _CANDIDATES]
