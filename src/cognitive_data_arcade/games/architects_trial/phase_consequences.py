# src/cognitive_data_arcade/games/architects_trial/phase_consequences.py
from __future__ import annotations
import pygame
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.architects_trial.game_state import GameState
from cognitive_data_arcade.games.architects_trial.domain_data import DOMAIN_DATA

_W, _H = 1024, 720
_BG = (8, 12, 20)
_PANEL = (16, 20, 36)
_WHITE = (240, 240, 240)
_DIM = (148, 163, 184)
_PURPLE = (167, 139, 250)
_RED = (239, 68, 68)
_BLUE = (96, 165, 250)
_GREEN = (34, 197, 94)
_ADVANCE_AFTER = 1000


class PhaseConsequencesScene(Scene):
    def __init__(self, state: GameState) -> None:
        self._state = state
        self._t = 0.0
        self._done = False
        self._next: Scene | None = None
        all_consequences = DOMAIN_DATA[state.domain]["act4_consequences"]
        self._texts = [all_consequences[k] for k in state.decisions if k in all_consequences][:4]

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._t >= _ADVANCE_AFTER and event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self._advance()

    def _advance(self) -> None:
        if self._done:
            return
        from cognitive_data_arcade.games.architects_trial.phase_tribunal import PhaseTribunalScene

        self._next = PhaseTribunalScene(self._state)
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        self._t += dt_ms

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 56))
        title = get_font(20).render("AKT 4 -- KONSEKWENCJE", True, _DIM)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))

        sub = get_font(16).render("System dziala od 6 miesiecy. Oto co sie stalo.", True, _WHITE)
        surface.blit(sub, (_W // 2 - sub.get_width() // 2, 80))

        border_colors = [_RED, _BLUE, _GREEN, _RED]
        y = 130
        f13 = get_font(13)
        for i, text in enumerate(self._texts):
            block_h = 70
            block = pygame.Rect(80, y, _W - 160, block_h)
            pygame.draw.rect(surface, (18, 22, 38), block, border_radius=6)
            pygame.draw.rect(
                surface, border_colors[i % len(border_colors)], block, 2, border_radius=6
            )
            pygame.draw.rect(
                surface,
                border_colors[i % len(border_colors)],
                pygame.Rect(80, y, 4, block_h),
                border_radius=6,
            )
            words = text.split()
            line, ty = "", y + 12
            for w in words:
                cand = (line + " " + w).strip()
                if f13.size(cand)[0] <= _W - 200:
                    line = cand
                else:
                    if line:
                        ls = f13.render(line, True, _WHITE)
                        surface.blit(ls, (96, ty))
                        ty += 18
                    line = w
            if line:
                ls = f13.render(line, True, _WHITE)
                surface.blit(ls, (96, ty))
            y += block_h + 12

        if self._t >= _ADVANCE_AFTER:
            hint = get_font(13).render("[SPACJA] -- staje przed komisja", True, _PURPLE)
            surface.blit(hint, (_W // 2 - hint.get_width() // 2, _H - 50))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
