# src/cognitive_data_arcade/games/you_were_the_dataset/phase_profile.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.you_were_the_dataset.game_state import GameState, ProfileData

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    WHITE as _WHITE,
    DIM as _DIM,
)

_W, _H = 1024, 720
_PANEL = (16, 24, 40)

# Card colors
_C_RT = (34, 197, 94)  # green
_C_STROOP = (167, 139, 250)  # purple
_C_FLANKER = (96, 165, 250)  # blue
_C_GONO = (249, 115, 22)  # orange
_C_NBACK = (52, 211, 153)  # teal

_CARD_W, _CARD_H = 600, 360
_CARD_X = (_W - _CARD_W) // 2
_CARD_Y = (_H - _CARD_H) // 2


def _bar(
    surface: pygame.Surface,
    x: int,
    y: int,
    w: int,
    h: int,
    value: float,
    lo: float,
    hi: float,
    color: tuple,
) -> None:
    """Draw a horizontal progress bar with a marker at 'value'."""
    pygame.draw.rect(surface, (30, 40, 60), (x, y, w, h), border_radius=h // 2)
    frac = max(0.0, min(1.0, (value - lo) / (hi - lo))) if hi > lo else 0.5
    pygame.draw.rect(surface, color, (x, y, int(w * frac), h), border_radius=h // 2)
    # Marker line
    mx = x + int(w * frac)
    pygame.draw.rect(surface, _WHITE, (mx - 2, y - 4, 4, h + 8))


def _draw_card_rt(surface: pygame.Surface, p: ProfileData) -> None:
    label = get_font(13).render("TWOJ CZAS REAKCJI BAZOWY", True, _DIM)
    surface.blit(label, (_W // 2 - label.get_width() // 2, _CARD_Y + 30))
    big = get_font(56).render(f"{p.rt_median_ms:.0f} ms", True, _C_RT)
    surface.blit(big, (_W // 2 - big.get_width() // 2, _CARD_Y + 70))
    _bar(
        surface, _CARD_X + 40, _CARD_Y + 160, _CARD_W - 80, 14, p.rt_median_ms, 150.0, 560.0, _C_RT
    )
    lo_lbl = get_font(12).render("150ms", True, _DIM)
    hi_lbl = get_font(12).render("560ms+", True, _DIM)
    surface.blit(lo_lbl, (_CARD_X + 40, _CARD_Y + 180))
    surface.blit(hi_lbl, (_CARD_X + _CARD_W - 80 - hi_lbl.get_width() + 40, _CARD_Y + 180))
    if p.rt_percentile >= 50:
        interp = f"Szybciej niz {p.rt_percentile}% uzytkownikow."
    else:
        interp = f"Wolniej niz {100 - p.rt_percentile}% uzytkownikow."
    txt = get_font(16).render(interp, True, _DIM)
    surface.blit(txt, (_W // 2 - txt.get_width() // 2, _CARD_Y + 210))


def _draw_card_stroop(surface: pygame.Surface, p: ProfileData) -> None:
    label = get_font(13).render("TWOJA INTERFERENCJA POZNAWCZA (STROOP)", True, _DIM)
    surface.blit(label, (_W // 2 - label.get_width() // 2, _CARD_Y + 30))
    big = get_font(56).render(f"+{p.stroop_effect_ms:.0f} ms", True, _C_STROOP)
    surface.blit(big, (_W // 2 - big.get_width() // 2, _CARD_Y + 70))
    txt = get_font(15).render(
        "Tyle czasu zajmuje Twojemu mozgowi ignorowanie mylacego bodzca.", True, _DIM
    )
    surface.blit(txt, (_W // 2 - txt.get_width() // 2, _CARD_Y + 160))


def _draw_card_flanker(surface: pygame.Surface, p: ProfileData) -> None:
    label = get_font(13).render("TWOJA KONTROLA UWAGI (FLANKER)", True, _DIM)
    surface.blit(label, (_W // 2 - label.get_width() // 2, _CARD_Y + 30))
    big = get_font(56).render(f"+{p.flanker_effect_ms:.0f} ms", True, _C_FLANKER)
    surface.blit(big, (_W // 2 - big.get_width() // 2, _CARD_Y + 70))
    txt = get_font(15).render("Jak bardzo rozpraszacze spowalniaja Twoje decyzje.", True, _DIM)
    surface.blit(txt, (_W // 2 - txt.get_width() // 2, _CARD_Y + 160))


def _draw_card_gono(surface: pygame.Surface, p: ProfileData) -> None:
    label = get_font(13).render("TWOJA INHIBICJA (GO/NO-GO)", True, _DIM)
    surface.blit(label, (_W // 2 - label.get_width() // 2, _CARD_Y + 30))
    pct = p.gono_false_alarm_rate * 100
    big = get_font(56).render(f"{pct:.1f}% FA", True, _C_GONO)
    surface.blit(big, (_W // 2 - big.get_width() // 2, _CARD_Y + 70))
    if pct < 10:
        interp = "Doskonala kontrola impulsow."
    elif pct < 25:
        interp = "Przecietna inhibicja."
    else:
        interp = "Hamowanie impulsu sprawialo Ci trudnosc."
    txt = get_font(15).render(interp, True, _DIM)
    surface.blit(txt, (_W // 2 - txt.get_width() // 2, _CARD_Y + 160))


def _draw_card_nback(surface: pygame.Surface, p: ProfileData) -> None:
    label = get_font(13).render("TWOJA PAMIEC ROBOCZA (N-BACK)", True, _DIM)
    surface.blit(label, (_W // 2 - label.get_width() // 2, _CARD_Y + 30))
    big = get_font(56).render(f"N = {p.nback_max_level}", True, _C_NBACK)
    surface.blit(big, (_W // 2 - big.get_width() // 2, _CARD_Y + 70))
    # Level indicators
    for n in range(1, 4):
        col = _C_NBACK if n <= p.nback_max_level else (40, 60, 80)
        nx = _W // 2 - 80 + (n - 1) * 80
        pygame.draw.circle(surface, col, (nx, _CARD_Y + 175), 24)
        lbl = get_font(18).render(str(n), True, _WHITE)
        surface.blit(lbl, (nx - lbl.get_width() // 2, _CARD_Y + 165))
    txt = get_font(15).render(
        f"Twoja pamiec robocza przechowuje jednoczesnie {p.nback_max_level} elem.",
        True,
        _DIM,
    )
    surface.blit(txt, (_W // 2 - txt.get_width() // 2, _CARD_Y + 220))


_DRAW_FUNCS = [
    _draw_card_rt,
    _draw_card_stroop,
    _draw_card_flanker,
    _draw_card_gono,
    _draw_card_nback,
]


class PhaseProfileScene(Scene):
    def __init__(self, state: GameState) -> None:
        self._state = state
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._done:
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self._advance()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._advance()

    def _advance(self) -> None:
        if self._state.current_card < len(_DRAW_FUNCS) - 1:
            self._state.current_card += 1
        else:
            from cognitive_data_arcade.games.you_were_the_dataset.phase_connection import (
                PhaseConnectionScene,
            )

            self._next = PhaseConnectionScene(self._state)
            self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        # Card background
        pygame.draw.rect(surface, _PANEL, (_CARD_X, _CARD_Y, _CARD_W, _CARD_H), border_radius=12)
        # Counter
        counter = get_font(13).render(
            f"{self._state.current_card + 1} / {len(_DRAW_FUNCS)}", True, _DIM
        )
        surface.blit(counter, (_W // 2 - counter.get_width() // 2, _CARD_Y - 30))
        # Draw current card
        assert self._state.profile is not None
        _DRAW_FUNCS[self._state.current_card](surface, self._state.profile)
        # Footer hint
        if self._state.current_card < len(_DRAW_FUNCS) - 1:
            hint_txt = "SPACJA -> nastepna karta"
        else:
            hint_txt = "SPACJA -> dalej"
        hint = get_font(13).render(hint_txt, True, _DIM)
        surface.blit(hint, (_W // 2 - hint.get_width() // 2, _CARD_Y + _CARD_H + 16))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
