# src/cognitive_data_arcade/games/bias_blind_spot/phase_applicant.py
"""Act 1 -- Applicant: 6 loan cards in 2x3 grid, pattern question, redlining reveal."""
from __future__ import annotations
import pygame
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.bias_blind_spot.game_state import (
    GameState, APPLICANTS, ACT1_CORRECT,
)

_W, _H = 1024, 720
_BG    = (8, 12, 20)
_PANEL = (16, 20, 36)
_WHITE = (240, 240, 240)
_DIM   = (130, 130, 150)
_GREEN = (39, 174, 96)
_RED   = (231, 76, 60)
_GOLD  = (243, 156, 18)
_C_APP = (155, 89, 182)

_CARD_W, _CARD_H = 440, 145
_CARD_GAP_X, _CARD_GAP_Y = 24, 16
_GRID_TOP = 68
_GRID_LEFT = (_W - 2 * _CARD_W - _CARD_GAP_X) // 2

_CHOICES = [
    ("income",  "A) Wysokosc dochodu"),
    ("zipcode", "B) Kod pocztowy / dzielnica"),
    ("credit",  "C) Historia kredytowa"),
]
_BTN_H = 44
_BTN_W = 280
_BTN_Y = _H - 130


def _card_rect(idx: int) -> pygame.Rect:
    col = idx % 2
    row = idx // 2
    x = _GRID_LEFT + col * (_CARD_W + _CARD_GAP_X)
    y = _GRID_TOP + row * (_CARD_H + _CARD_GAP_Y)
    return pygame.Rect(x, y, _CARD_W, _CARD_H)


def _choice_btn_rect(idx: int) -> pygame.Rect:
    total_w = 3 * _BTN_W + 2 * 20
    x0 = (_W - total_w) // 2
    return pygame.Rect(x0 + idx * (_BTN_W + 20), _BTN_Y, _BTN_W, _BTN_H)


class PhaseApplicantScene(Scene):
    def __init__(self, state: GameState) -> None:
        self._state = state
        self._answered = False
        self._revealed = False
        self._done = False
        self._next: Scene | None = None
        self._choice_idx: int = -1

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._revealed:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._advance()
            return
        if not self._answered and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, (key, _) in enumerate(_CHOICES):
                if _choice_btn_rect(i).collidepoint(event.pos):
                    self._choice_idx = i
                    self._answered = True
                    self._state.act1_choice = key
                    self._state.act1_correct = (key == ACT1_CORRECT)
                    self._revealed = True
                    break

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def _advance(self) -> None:
        if self._done:
            return
        from cognitive_data_arcade.games.bias_blind_spot.phase_interlude import PhaseInterludeScene
        lines = [
            ("Czas zostac inzynierem modelu.", (39, 174, 96)),
            ("Bedziesz usuwac cechy -- i obserwowac bias.", (140, 140, 160)),
            ("", (0, 0, 0)),
            ("SPACJA aby kontynuowac", (60, 60, 80)),
        ]
        self._next = PhaseInterludeScene(self._state, lines, "engineer")
        self._done = True

    def _draw_card(self, surface: pygame.Surface, app: dict, rect: pygame.Rect) -> None:
        approved = app["approved"]
        border_col = _GREEN if approved else _RED
        pygame.draw.rect(surface, _PANEL, rect, border_radius=6)
        pygame.draw.rect(surface, border_col, rect, 2, border_radius=6)

        f11 = get_font(11)
        f13 = get_font(13)
        x, y = rect.x + 10, rect.y + 8

        name_surf = f13.render(app["name"], True, _WHITE)
        surface.blit(name_surf, (x, y))
        y += 20

        status = "ZATWIERDZONO" if approved else "ODRZUCONO"
        s_surf = f11.render(status, True, border_col)
        surface.blit(s_surf, (rect.right - s_surf.get_width() - 10, rect.y + 8))

        rows = [
            f"Dochod: {app['income']} zl/mies.",
            f"Zatrudnienie: {app['employment']}",
            f"Historia kredytu: {app['credit']}",
            f"Dzielnica: {app['zip']}",
            f"Wskaznik dlugu: {app['debt']}%",
        ]
        for row in rows:
            rs = f11.render(row, True, _DIM)
            surface.blit(rs, (x, y))
            y += 16

    def _draw_reveal(self, surface: pygame.Surface) -> None:
        overlay = pygame.Surface((_W, _H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        box_w, box_h = 680, 320
        bx = (_W - box_w) // 2
        by = (_H - box_h) // 2
        pygame.draw.rect(surface, _PANEL, (bx, by, box_w, box_h), border_radius=10)
        pygame.draw.rect(surface, _C_APP, (bx, by, box_w, box_h), 2, border_radius=10)

        f16 = get_font(16)
        f13 = get_font(13)
        f11 = get_font(11)

        if self._state.act1_correct:
            msg = "Dobrze! Kod pocztowy (dzielnica) jest kluczowy."
            msg_col = _GREEN
        else:
            msg = "Odpowiedz: B -- Kod pocztowy / dzielnica."
            msg_col = _GOLD

        ms = f16.render(msg, True, msg_col)
        surface.blit(ms, (bx + box_w // 2 - ms.get_width() // 2, by + 20))

        lines = [
            "Amina B. (4100 zl) ODRZUCONA -- Praga Pd.",
            "Fatima N. (4500 zl) ODRZUCONA -- Praga Pd.",
            "Ibrahim O. (3900 zl) ODRZUCONY -- Praga Pd.",
            "Marek W. (2900 zl) ZATWIERDZONY -- Wola",
            "Piotr M. (3200 zl) ZATWIERDZONY -- Zoliborz",
            "Jan K. (3800 zl) ZATWIERDZONY -- Mokotow",
        ]
        y = by + 60
        for i, ln in enumerate(lines):
            col = _RED if i < 3 else _GREEN
            ls = f11.render(ln, True, col)
            surface.blit(ls, (bx + 20, y))
            y += 20

        aha = "Algorytm nigdy nie widzial rasy. Ale widzial kod pocztowy."
        aha_s = f13.render(aha, True, _GOLD)
        surface.blit(aha_s, (bx + box_w // 2 - aha_s.get_width() // 2, by + 230))

        hint = f11.render("SPACJA aby kontynuowac", True, (80, 80, 100))
        surface.blit(hint, (bx + box_w // 2 - hint.get_width() // 2, by + box_h - 30))

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 56))
        title = get_font(20).render("Akt 1: Aplikant -- znajdz wzorzec", True, _WHITE)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 16))

        for i, app in enumerate(APPLICANTS):
            self._draw_card(surface, app, _card_rect(i))

        if not self._answered:
            q_s = get_font(14).render("Co wyjasnia te decyzje?", True, _DIM)
            surface.blit(q_s, (_W // 2 - q_s.get_width() // 2, _BTN_Y - 28))
            for i, (_, label) in enumerate(_CHOICES):
                btn_r = _choice_btn_rect(i)
                pygame.draw.rect(surface, _PANEL, btn_r, border_radius=6)
                pygame.draw.rect(surface, _DIM, btn_r, 1, border_radius=6)
                ls = get_font(13).render(label, True, _WHITE)
                surface.blit(ls, (btn_r.x + btn_r.w // 2 - ls.get_width() // 2,
                                  btn_r.y + btn_r.h // 2 - ls.get_height() // 2))

        if self._revealed:
            self._draw_reveal(surface)

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
