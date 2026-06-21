# src/cognitive_data_arcade/games/architects_trial/phase_domain_picker.py
from __future__ import annotations
import pygame
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.architects_trial.game_state import GameState

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    WHITE as _WHITE,
    DIM as _DIM,
    PURPLE as _PURPLE,
)

_W, _H = 1024, 720
_PANEL = (16, 20, 36)
_HOVER = (45, 55, 90)
_CARD_BG = (22, 30, 50)

_DOMAINS = [
    (
        "social",
        "[S]",
        "Opieka spoleczna",
        "Oceniasz ryzyko dla dzieci na podstawie danych miejskich.",
    ),
    ("hiring", "[H]", "Rekrutacja AI", "Selekcjonujesz CV na stanowiska w magistracie."),
    ("triage", "[T]", "Triage SOR", "Priorytyzujesz pacjentow na szpitalnym oddziale ratunkowym."),
]

_CARD_W, _CARD_H = 270, 220
_CARD_Y = 200
_GAP = 30


def _card_rects() -> list[pygame.Rect]:
    total = len(_DOMAINS) * _CARD_W + (len(_DOMAINS) - 1) * _GAP
    x0 = (_W - total) // 2
    return [
        pygame.Rect(x0 + i * (_CARD_W + _GAP), _CARD_Y, _CARD_W, _CARD_H)
        for i in range(len(_DOMAINS))
    ]


class PhaseDomainPickerScene(Scene):
    def __init__(self, state: GameState) -> None:
        self._state = state
        self._selected = 0
        self._rects = _card_rects()
        self._done = False
        self._next: Scene | None = None
        self._mouse_pos = (0, 0)

    def handle_event(self, event: pygame.event.Event) -> None:
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
                self._selected = min(len(_DOMAINS) - 1, self._selected + 1)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._pick(self._selected)

    def _pick(self, idx: int) -> None:
        if self._done:
            return
        domain_key = _DOMAINS[idx][0]
        self._state.domain = domain_key
        from cognitive_data_arcade.games.architects_trial.phase_act import PhaseActScene

        self._next = PhaseActScene(self._state, act_num=1)
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 56))
        title = get_font(22).render("Wybierz projekt ktory budujesz", True, _WHITE)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))

        for i, (rect, (_, badge, name, desc)) in enumerate(zip(self._rects, _DOMAINS)):
            hovered = rect.collidepoint(self._mouse_pos)
            is_sel = i == self._selected
            bg = _HOVER if (hovered or is_sel) else _CARD_BG
            border = _PURPLE if (hovered or is_sel) else (50, 60, 90)
            pygame.draw.rect(surface, bg, rect, border_radius=10)
            pygame.draw.rect(surface, border, rect, 2, border_radius=10)

            badge_s = get_font(28).render(badge, True, _PURPLE)
            surface.blit(badge_s, (rect.x + rect.w // 2 - badge_s.get_width() // 2, rect.y + 20))
            name_s = get_font(16).render(name, True, _WHITE)
            surface.blit(name_s, (rect.x + rect.w // 2 - name_s.get_width() // 2, rect.y + 70))

            f12 = get_font(12)
            words = desc.split()
            line, y = "", rect.y + 100
            for w in words:
                cand = (line + " " + w).strip()
                if f12.size(cand)[0] <= rect.w - 16:
                    line = cand
                else:
                    if line:
                        ls = f12.render(line, True, _DIM)
                        surface.blit(ls, (rect.x + 8, y))
                        y += 16
                    line = w
            if line:
                ls = f12.render(line, True, _DIM)
                surface.blit(ls, (rect.x + 8, y))

        hint = get_font(13).render(
            "Replay: sprobuj innych domen po zakonczeniu", True, (70, 80, 110)
        )
        surface.blit(hint, (_W // 2 - hint.get_width() // 2, _H - 40))

        nav = get_font(13).render("Kliknij lub strzalki + ENTER", True, _DIM)
        surface.blit(nav, (_W // 2 - nav.get_width() // 2, _H - 60))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
