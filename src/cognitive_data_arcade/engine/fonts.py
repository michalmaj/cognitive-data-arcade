"""Font loading utility — loads bundled Space Grotesk TTF for crisp, modern text."""

from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.assets import assets_dir

_BUNDLED = assets_dir() / "fonts" / "SpaceGrotesk-Regular.ttf"
_BUNDLED_MEDIUM = assets_dir() / "fonts" / "SpaceGrotesk-Medium.ttf"

# Space Grotesk renders ~1.87x taller than pygame's bitmap SysFont(None,...) at
# the same nominal size.  All size constants in the codebase were calibrated for
# the bitmap font, so we scale down uniformly so that SG fits the existing layout.
_SCALE = 0.72

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
_cache_medium: dict[int, pygame.font.Font] = {}
_bundled_ok: bool | None = None
_bundled_med_ok: bool | None = None


def get_font(size: int) -> pygame.font.Font:
    """Return Space Grotesk Regular at *size*, falling back to system fonts."""
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

    actual = max(10, round(size * _SCALE))
    font = pygame.font.Font(str(_BUNDLED), actual) if _bundled_ok else _load_system_font(actual)
    _cache[size] = font
    return font


def get_font_medium(size: int) -> pygame.font.Font:
    """Return Space Grotesk Medium at *size*, falling back to Regular if unavailable."""
    global _bundled_med_ok
    pygame.font.init()
    if size in _cache_medium:
        try:
            _cache_medium[size].size("a")
            return _cache_medium[size]
        except Exception:
            _cache_medium.clear()
            _bundled_med_ok = None

    if _bundled_med_ok is None:
        _bundled_med_ok = _BUNDLED_MEDIUM.exists()

    actual = max(10, round(size * _SCALE))
    font = pygame.font.Font(str(_BUNDLED_MEDIUM), actual) if _bundled_med_ok else get_font(size)
    _cache_medium[size] = font
    return font


def reset() -> None:
    """Clear font caches. Call after pygame.quit() to avoid dangling C pointers."""
    global _bundled_ok, _bundled_med_ok
    _cache.clear()
    _cache_medium.clear()
    _bundled_ok = None
    _bundled_med_ok = None


def _load_system_font(size: int) -> pygame.font.Font:
    pygame.font.init()
    avail = frozenset(pygame.font.get_fonts())
    for candidate in [c.replace(" ", "").lower() for c in _FALLBACK_CANDIDATES]:
        if candidate in avail:
            return pygame.font.SysFont(candidate, size)
    return pygame.font.SysFont(None, size)
