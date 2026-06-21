# src/cognitive_data_arcade/games/you_were_the_dataset/phase_result.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.you_were_the_dataset.game_state import GameState

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    WHITE as _WHITE,
    DIM as _DIM,
)

_W, _H = 1024, 768
_PANEL = (16, 20, 36)
_GOLD = (243, 156, 18)

_AHA = [
    "Byłeś jednocześnie naukowcem i uczestnikiem.",
    "Każde kliknięcie było danymi.",
    "Dane to ślad Twojego zachowania.",
]


class PhaseResultScene(Scene):
    def __init__(self, state: GameState) -> None:
        self._state = state
        self._done = False
        self._next: Scene | None = None
        self._btn_replay = pygame.Rect(_W // 2 - 210, _H - 70, 190, 44)
        self._btn_menu = pygame.Rect(_W // 2 + 20, _H - 70, 190, 44)

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._done:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._btn_replay.collidepoint(event.pos):
                from cognitive_data_arcade.games.you_were_the_dataset.game import (
                    YouWereTheDatasetScene,
                )

                # Replay: restart with same pm/strings stored in state
                pm = getattr(self._state, "_pm", None)
                strings = getattr(self._state, "_strings", None)
                self._next = YouWereTheDatasetScene(pm, strings)
                self._done = True
            elif self._btn_menu.collidepoint(event.pos):
                self._next = None
                self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 60))

        # Title
        title = get_font(26).render("Kognitywny Profil Ukończony", True, _WHITE)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))

        # 3 gold stars
        for i in range(3):
            cx = _W // 2 - 36 + i * 36
            pygame.draw.circle(surface, _GOLD, (cx, 95), 12)

        # Compact metric table
        p = self._state.profile
        if p is not None:
            rows = [
                ("Czas reakcji bazowy", f"{p.rt_median_ms:.0f} ms"),
                ("Efekt Stroopa", f"+{p.stroop_effect_ms:.0f} ms"),
                ("Efekt Flankera", f"+{p.flanker_effect_ms:.0f} ms"),
                ("Inhibicja (FA rate)", f"{p.gono_false_alarm_rate * 100:.1f}%"),
                ("Pamięć robocza", f"N = {p.nback_max_level}"),
            ]
            row_h = 36
            table_top = 130
            for i, (label, val) in enumerate(rows):
                y = table_top + i * row_h
                bg = (14, 18, 32) if i % 2 == 0 else (18, 24, 40)
                pygame.draw.rect(surface, bg, (_W // 2 - 300, y, 600, row_h - 2))
                lbl_surf = get_font(15).render(label, True, _DIM)
                val_surf = get_font(15).render(val, True, _WHITE)
                surface.blit(lbl_surf, (_W // 2 - 290, y + 9))
                surface.blit(val_surf, (_W // 2 + 290 - val_surf.get_width(), y + 9))

            if p.is_synthetic:
                tag = get_font(12).render("[dane syntetyczne]", True, (60, 60, 80))
                surface.blit(
                    tag, (_W // 2 - tag.get_width() // 2, table_top + len(rows) * row_h + 4)
                )

        # AHA lines
        aha_y = 330
        for line in _AHA:
            surf = get_font(15).render(line, True, _DIM)
            surface.blit(surf, (_W // 2 - surf.get_width() // 2, aha_y))
            aha_y += 26

        # Buttons
        pygame.draw.rect(surface, _PANEL, self._btn_replay, border_radius=8)
        pygame.draw.rect(surface, _WHITE, self._btn_replay, 1, border_radius=8)
        r_txt = get_font(17).render("Zagraj ponownie", True, _WHITE)
        surface.blit(
            r_txt,
            (
                self._btn_replay.x + (self._btn_replay.w - r_txt.get_width()) // 2,
                self._btn_replay.y + (self._btn_replay.h - r_txt.get_height()) // 2,
            ),
        )

        pygame.draw.rect(surface, _PANEL, self._btn_menu, border_radius=8)
        pygame.draw.rect(surface, _WHITE, self._btn_menu, 1, border_radius=8)
        m_txt = get_font(17).render("Menu", True, _WHITE)
        surface.blit(
            m_txt,
            (
                self._btn_menu.x + (self._btn_menu.w - m_txt.get_width()) // 2,
                self._btn_menu.y + (self._btn_menu.h - m_txt.get_height()) // 2,
            ),
        )

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
