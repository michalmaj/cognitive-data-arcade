# src/cognitive_data_arcade/games/architects_trial/phase_act.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
)
from cognitive_data_arcade.engine.colors import (
    DIM as _DIM,
)
from cognitive_data_arcade.engine.colors import (
    PURPLE as _PURPLE,
)
from cognitive_data_arcade.engine.colors import (
    WHITE as _WHITE,
)
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.architects_trial.domain_data import DOMAIN_DATA
from cognitive_data_arcade.games.architects_trial.game_state import DecisionCard, GameState

_W, _H = 1024, 768
_PANEL = (16, 20, 36)
_CARD_BG = (22, 30, 50)
_HOVER_BG = (45, 55, 90)
_NOTE_COLORS = {
    "green": (34, 197, 94),
    "orange": (249, 115, 22),
    "red": (239, 68, 68),
}
_ACT_TITLES = {1: "AKT 1 -- DANE", 2: "AKT 2 -- MODEL", 3: "AKT 3 -- SUKCES"}

_CARD_W, _CARD_H = 260, 210
_CARD_Y = 180
_GAP = 24
_SELECT_FLASH_MS = 300


class PhaseActScene(Scene):
    def __init__(self, state: GameState, act_num: int) -> None:
        assert act_num in (1, 2, 3)
        self._state = state
        self._act_num = act_num
        cards_key = f"act{act_num}_cards"
        self._cards: list[DecisionCard] = DOMAIN_DATA[state.domain][cards_key]
        self._question: str = DOMAIN_DATA[state.domain][f"act{act_num}_question"]
        n = len(self._cards)
        total = n * _CARD_W + (n - 1) * _GAP
        x0 = (_W - total) // 2
        self._rects = [
            pygame.Rect(x0 + i * (_CARD_W + _GAP), _CARD_Y, _CARD_W, _CARD_H) for i in range(n)
        ]
        self._selected = 0
        self._mouse_pos = (0, 0)
        self._flash_t = 0.0
        self._chosen: DecisionCard | None = None
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._chosen:
            return
        if event.type == pygame.MOUSEMOTION:
            self._mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self._rects):
                if rect.collidepoint(event.pos):
                    self._pick(i)
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self._selected = max(0, self._selected - 1)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self._selected = min(len(self._cards) - 1, self._selected + 1)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._pick(self._selected)

    def _pick(self, idx: int) -> None:
        card = self._cards[idx]
        self._chosen = card
        self._flash_t = 0.0
        self._state.decisions.append(card.key)
        self._state.fairness_score = min(
            100, max(0, self._state.fairness_score + card.fairness_delta)
        )
        self._state.compliance_score = min(
            100, max(0, self._state.compliance_score + card.compliance_delta)
        )
        self._state.effectiveness_score = min(
            100, max(0, self._state.effectiveness_score + card.effectiveness_delta)
        )

    def update(self, dt_ms: float = 0.0) -> None:
        if self._chosen:
            self._flash_t += dt_ms
            if self._flash_t >= _SELECT_FLASH_MS and not self._done:
                self._done = True
                if self._act_num < 3:
                    from cognitive_data_arcade.games.architects_trial.phase_act import PhaseActScene

                    self._next = PhaseActScene(self._state, self._act_num + 1)
                else:
                    from cognitive_data_arcade.games.architects_trial.phase_consequences import (
                        PhaseConsequencesScene,
                    )

                    self._next = PhaseConsequencesScene(self._state)

    def _draw_progress(self, surface: pygame.Surface) -> None:
        cx = _W // 2 - 60
        for i in range(1, 5):
            color = _PURPLE if i <= self._act_num else (50, 60, 90)
            pygame.draw.circle(
                surface, color, (cx + (i - 1) * 40, 70), 8, 0 if i <= self._act_num else 2
            )
            label = get_font(10).render(str(i), True, (8, 12, 20) if i <= self._act_num else _DIM)
            surface.blit(label, (cx + (i - 1) * 40 - label.get_width() // 2, 65))

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 56))
        title = get_font(20).render(_ACT_TITLES[self._act_num], True, _DIM)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))
        self._draw_progress(surface)

        q = get_font(18).render(self._question, True, _WHITE)
        surface.blit(q, (_W // 2 - q.get_width() // 2, 100))

        for i, (rect, card) in enumerate(zip(self._rects, self._cards)):
            is_chosen = self._chosen is not None and card.key == self._chosen.key
            hovered = rect.collidepoint(self._mouse_pos) and not self._chosen
            is_sel = (i == self._selected) and not self._chosen
            if is_chosen and self._flash_t < _SELECT_FLASH_MS:
                bg = (60, 50, 100)
                border = _PURPLE
            else:
                bg = _HOVER_BG if (hovered or is_sel) else _CARD_BG
                border = _PURPLE if (hovered or is_sel) else (50, 60, 90)
            pygame.draw.rect(surface, bg, rect, border_radius=10)
            pygame.draw.rect(surface, border, rect, 2, border_radius=10)

            label_s = get_font(16).render(card.label, True, _WHITE)
            surface.blit(label_s, (rect.x + rect.w // 2 - label_s.get_width() // 2, rect.y + 12))

            f11 = get_font(11)
            words = card.description.split()
            line, y = "", rect.y + 40
            for w in words:
                cand = (line + " " + w).strip()
                if f11.size(cand)[0] <= rect.w - 16:
                    line = cand
                else:
                    if line:
                        ls = f11.render(line, True, _DIM)
                        surface.blit(ls, (rect.x + 8, y))
                        y += 15
                    line = w
            if line:
                ls = f11.render(line, True, _DIM)
                surface.blit(ls, (rect.x + 8, y))

            note_color = _NOTE_COLORS.get(card.note_color, _DIM)
            note_s = get_font(10).render(card.note, True, note_color)
            note_bg = pygame.Rect(rect.x + 8, rect.bottom - 28, rect.w - 16, 20)
            pygame.draw.rect(surface, (20, 25, 40), note_bg, border_radius=4)
            surface.blit(
                note_s,
                (rect.x + 8 + (rect.w - 16) // 2 - note_s.get_width() // 2, rect.bottom - 26),
            )

        if not self._chosen:
            hint = get_font(12).render("Kliknij karte lub strzalki + ENTER", True, _DIM)
            surface.blit(hint, (_W // 2 - hint.get_width() // 2, _H - 40))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
