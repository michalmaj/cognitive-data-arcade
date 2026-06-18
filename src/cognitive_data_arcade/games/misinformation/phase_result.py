# src/cognitive_data_arcade/games/misinformation/phase_result.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.misinformation.networks import ROUNDS

_W, _H = 1024, 720
_BG    = (12, 12, 20)
_PANEL = (18, 18, 32)
_WHITE = (240, 240, 240)
_DIM   = (140, 140, 160)
_GOLD  = (243, 156, 18)
_GREY  = (60, 60, 80)
_RED   = (231, 76, 60)
_GREEN = (39, 174, 96)
_BLUE  = (52, 152, 219)

_BTN_REPLAY = pygame.Rect(_W // 2 - 210, _H - 76, 190, 44)
_BTN_MENU   = pygame.Rect(_W // 2 + 20,  _H - 76, 190, 44)

_AHA_LOW  = (
    "Siec bezskalowa z super-hubem jest prawie nie do obronienia. "
    "Hub zarazil wszystkich zanim zdazyles zareagowac."
)
_AHA_MID  = (
    "Widzisz rosnaca asymetrie? W rundzie 3 spreader mial przewage "
    "-- hub jako patient-zero to przewaga nie do nadrobienia."
)
_AHA_HIGH = (
    "Swietna robota jako fact-checker! Ale zauwazyles, ze w rundzie 3 "
    "bylo trudniej niz w rundzie 1? To efekt huba."
)


def _wrap(text: str, font: pygame.font.Font, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        cand = (cur + " " + w).strip()
        if font.size(cand)[0] <= max_w:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


class PhaseResultScene(Scene):
    def __init__(self, scores: list[int]) -> None:
        # scores: [r1_spread, r1_fact, r2_spread, r2_fact, r3_spread, r3_fact]
        self._scores = list(scores)
        self._total  = sum(scores)
        self._stars  = 3 if self._total >= 480 else (2 if self._total >= 300 else 1)

        fact3 = scores[5] if len(scores) >= 6 else 0
        if fact3 < 40:
            self._aha = _AHA_LOW
        elif fact3 <= 70:
            self._aha = _AHA_MID
        else:
            self._aha = _AHA_HIGH

        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if _BTN_REPLAY.collidepoint(event.pos):
                from cognitive_data_arcade.games.misinformation.game import MisinformationScene
                self._next = MisinformationScene()
                self._done = True
            elif _BTN_MENU.collidepoint(event.pos):
                self._next = None
                self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)

        # Title bar
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 54))
        title = get_font(24).render("Misinformation Spread -- Wyniki sesji", True, _WHITE)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))

        # Total score
        total_surf = get_font(22).render(f"WYNIK: {self._total} / 660", True, _GOLD)
        surface.blit(total_surf, (_W // 2 - total_surf.get_width() // 2, 66))

        # Stars as filled / empty circles
        for i in range(3):
            filled = i < self._stars
            color = _GOLD if filled else _GREY
            cx = _W // 2 - 30 + i * 30
            pygame.draw.circle(surface, color, (cx, 102), 10, 0 if filled else 2)

        # Column headers
        col_xs = [60, 280, 500, 720]
        y = 134
        for col, hdr in zip(col_xs, ["Runda", "Spreader", "Fact-Checker", "Roznica"]):
            surf = get_font(14).render(hdr, True, (100, 100, 120))
            surface.blit(surf, (col, y))
        y += 22
        pygame.draw.line(surface, (40, 40, 60), (50, y), (_W - 50, y), 1)
        y += 6

        # Per-round rows
        for i, cfg in enumerate(ROUNDS):
            r_spread = self._scores[i * 2]     if len(self._scores) > i * 2     else 0
            r_fact   = self._scores[i * 2 + 1] if len(self._scores) > i * 2 + 1 else 0
            diff     = r_spread - r_fact
            diff_color = _RED if diff > 20 else _GREEN

            row = [
                (f"{i + 1}. {cfg.label} ({cfg.n} wezlow)", (200, 160, 80)),
                (f"{r_spread}%", _RED),
                (f"{r_fact}%", _GREEN),
                ((f"+{diff}%" if diff >= 0 else f"{diff}%"), diff_color),
            ]
            for col, (text, color) in zip(col_xs, row):
                surf = get_font(15).render(text, True, color)
                surface.blit(surf, (col, y))
            y += 28
            pygame.draw.line(surface, (26, 26, 46), (50, y), (_W - 50, y), 1)
            y += 6

        # AHA insight box
        aha_y = y + 14
        box_h = 70
        pygame.draw.rect(surface, (10, 28, 10), (50, aha_y, _W - 100, box_h), border_radius=6)
        pygame.draw.rect(surface, _GREEN,        (50, aha_y, _W - 100, box_h), 1, border_radius=6)
        lbl = get_font(11).render("SPOSTRZEZENIE", True, _GREEN)
        surface.blit(lbl, (64, aha_y + 6))
        aha_font = get_font(12)
        wrapped = _wrap(self._aha, aha_font, _W - 140)
        for li, line in enumerate(wrapped):
            ls = aha_font.render(line, True, _DIM)
            surface.blit(ls, (64, aha_y + 22 + li * 16))

        # Replay / Menu buttons
        pygame.draw.rect(surface, _PANEL, _BTN_REPLAY, border_radius=6)
        pygame.draw.rect(surface, _GREY,  _BTN_REPLAY, 1, border_radius=6)
        r_lbl = get_font(16).render("Zagraj ponownie", True, (180, 180, 200))
        surface.blit(r_lbl, (
            _BTN_REPLAY.x + (_BTN_REPLAY.w - r_lbl.get_width()) // 2,
            _BTN_REPLAY.y + (_BTN_REPLAY.h - r_lbl.get_height()) // 2,
        ))

        pygame.draw.rect(surface, _PANEL, _BTN_MENU, border_radius=6)
        pygame.draw.rect(surface, _BLUE,  _BTN_MENU, 1, border_radius=6)
        m_lbl = get_font(16).render("Menu", True, _BLUE)
        surface.blit(m_lbl, (
            _BTN_MENU.x + (_BTN_MENU.w - m_lbl.get_width()) // 2,
            _BTN_MENU.y + (_BTN_MENU.h - m_lbl.get_height()) // 2,
        ))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
