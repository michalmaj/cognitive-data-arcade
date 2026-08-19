# src/cognitive_data_arcade/games/architects_trial/phase_tribunal.py
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
from cognitive_data_arcade.games.architects_trial.game_state import GameState, compute_verdict

_W, _H = 1024, 768
_PANEL = (16, 20, 36)
_CARD_BG = (22, 30, 50)
_HOVER_BG = (45, 55, 90)

_JUDGES = [
    ("fairness", "Rzecznik Rownosci", (239, 68, 68)),
    ("compliance", "Prawnik EU AI Act", (96, 165, 250)),
    ("effectiveness", "Dyrektor ds. Skutecznosci", (34, 197, 94)),
]

_CHARGES = {
    "fairness": [
        "Twoje decyzje projektowe stworzyly nieproporcjonalny wplyw na grupy chronione.",
        "System gromadzil dane w sposob naruszajacy prywatnosc osob.",
        "Wyniki systemu sa sprawiedliwe i uwzgledniaja roznorodnosc grup.",
    ],
    "compliance": [
        "Projekt nie spelnia wymagan EU AI Act dla systemow wysokiego ryzyka.",
        "Brak dokumentacji procesu decyzyjnego i audytu algorytmu.",
        "System jest zgodny z regulacjami i posiada odpowiednia dokumentacje.",
    ],
    "effectiveness": [
        "System osiagnal skutecznosc ponizej oczekiwan instytucji.",
        "Wybrane metryki sukcesu nie odzwierciedlaja rzeczywistych wynikow.",
        "System dziala skutecznie i spelnia postawione cele operacyjne.",
    ],
}

_RESPONSES = {
    "defensive": "Decyzje byly uzasadnione dostepnymi danymi i zasobami.",
    "reflective": "Nie przewidzialem tych konsekwencji. To byl blad projektowy.",
}

_VERDICT_COLORS = {
    "ZATWIERDZONY": (34, 197, 94),
    "ZATWIERDZONY Z ZALECENIAMI": (167, 139, 250),
    "ZAWIESZONY": (249, 115, 22),
    "ODRZUCONY": (239, 68, 68),
}

_VERDICT_COMMENTS = {
    "ZATWIERDZONY": "System moze byc wdrozony. Monitoruj wyniki co 6 miesiecy.",
    "ZATWIERDZONY Z ZALECENIAMI": "Wdrozenie warunkowe. Wymagane poprawki w ciagu 90 dni.",
    "ZAWIESZONY": "Wdrozenie wstrzymane. Wymagany ponowny audyt i korekta projektu.",
    "ODRZUCONY": "Projekt odrzucony. Naruszenie podstawowych wymagan prawnych i etycznych.",
}

_AHA = "Nie ma neutralnych decyzji projektowych. Kazdy parametr to wybor polityczny."
_AHA_DELAY = 1500


class PhaseTribunalScene(Scene):
    def __init__(self, state: GameState) -> None:
        self._state = state
        self._done = False
        self._next: Scene | None = None
        scores = {
            "fairness": state.fairness_score,
            "compliance": state.compliance_score,
            "effectiveness": state.effectiveness_score,
        }
        self._judges = sorted(_JUDGES, key=lambda j: scores[j[0]])
        self._phase = "questioning"  # "questioning" | "verdict"
        self._judge_idx = 0
        self._response_rects = [
            pygame.Rect(_W // 2 + 20, 300, 360, 60),
            pygame.Rect(_W // 2 + 20, 380, 360, 60),
        ]
        self._mouse_pos = (0, 0)
        self._verdict = compute_verdict(
            state.fairness_score, state.compliance_score, state.effectiveness_score
        )
        self._aha_t = 0.0
        self._verdict_entered = False

    def _current_judge(self):
        return self._judges[self._judge_idx]

    def _charge_text(self) -> str:
        criterion, _, _ = self._current_judge()
        score = getattr(self._state, f"{criterion}_score")
        if score <= 30:
            return _CHARGES[criterion][0]
        elif score <= 55:
            return _CHARGES[criterion][1]
        return _CHARGES[criterion][2]

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._phase == "verdict":
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN) and self._aha_t >= _AHA_DELAY:
                self._advance()
            return
        if event.type == pygame.MOUSEMOTION:
            self._mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self._response_rects):
                if rect.collidepoint(event.pos):
                    self._respond(i)
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_1,):
                self._respond(0)
            elif event.key in (pygame.K_2,):
                self._respond(1)

    def _respond(self, idx: int) -> None:
        keys = list(_RESPONSES.keys())
        self._state.tribunal_response = keys[idx]
        self._judge_idx += 1
        if self._judge_idx >= len(self._judges):
            self._phase = "verdict"
            self._verdict_entered = True

    def _advance(self) -> None:
        if self._done:
            return
        from cognitive_data_arcade.games.architects_trial.phase_result import PhaseResultScene

        self._next = PhaseResultScene(self._state)
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        if self._phase == "verdict":
            self._aha_t += dt_ms

    def _draw_questioning(self, surface: pygame.Surface) -> None:
        criterion, judge_name, color = self._current_judge()
        score = getattr(self._state, f"{criterion}_score")
        step_s = get_font(13).render(
            f"Sedzia {self._judge_idx + 1} / {len(self._judges)}", True, _DIM
        )
        surface.blit(step_s, (_W // 2 - step_s.get_width() // 2, 65))

        left = pygame.Rect(40, 100, int(_W * 0.38), 320)
        pygame.draw.rect(surface, _PANEL, left, border_radius=10)
        pygame.draw.rect(surface, color, left, 2, border_radius=10)
        name_s = get_font(16).render(judge_name, True, color)
        surface.blit(name_s, (left.x + left.w // 2 - name_s.get_width() // 2, left.y + 20))
        score_s = get_font(22).render(f"{score}/100", True, _WHITE)
        surface.blit(score_s, (left.x + left.w // 2 - score_s.get_width() // 2, left.y + 60))
        crit_s = get_font(11).render(criterion.upper(), True, color)
        surface.blit(crit_s, (left.x + left.w // 2 - crit_s.get_width() // 2, left.y + 100))

        charge = self._charge_text()
        f12 = get_font(12)
        words = charge.split()
        line, cy = "", left.y + 140
        for w in words:
            cand = (line + " " + w).strip()
            if f12.size(cand)[0] <= left.w - 24:
                line = cand
            else:
                if line:
                    ls = f12.render(line, True, _DIM)
                    surface.blit(ls, (left.x + 12, cy))
                    cy += 17
                line = w
        if line:
            ls = f12.render(line, True, _DIM)
            surface.blit(ls, (left.x + 12, cy))

        right_label = get_font(14).render("Twoja odpowiedz:", True, _WHITE)
        surface.blit(right_label, (_W // 2 + 20, 270))
        response_texts = list(_RESPONSES.values())
        for _i, (rect, text) in enumerate(zip(self._response_rects, response_texts)):
            hovered = rect.collidepoint(self._mouse_pos)
            bg = _HOVER_BG if hovered else _CARD_BG
            border = _PURPLE if hovered else (50, 60, 90)
            pygame.draw.rect(surface, bg, rect, border_radius=8)
            pygame.draw.rect(surface, border, rect, 2, border_radius=8)
            f12 = get_font(12)
            words = text.split()
            line, ty = "", rect.y + 8
            for w in words:
                cand = (line + " " + w).strip()
                if f12.size(cand)[0] <= rect.w - 16:
                    line = cand
                else:
                    if line:
                        ls = f12.render(line, True, _WHITE)
                        surface.blit(ls, (rect.x + 8, ty))
                        ty += 15
                    line = w
            if line:
                ls = f12.render(line, True, _WHITE)
                surface.blit(ls, (rect.x + 8, ty))

        hint = get_font(11).render("Kliknij odpowiedz lub 1 / 2", True, _DIM)
        surface.blit(hint, (_W // 2 + 20, _H - 50))

    def _draw_verdict(self, surface: pygame.Surface) -> None:
        label_s = get_font(14).render("WERDYKT KOMISJI ETYCZNEJ", True, _DIM)
        surface.blit(label_s, (_W // 2 - label_s.get_width() // 2, 75))

        criteria = [
            ("Fairness", self._state.fairness_score, (239, 68, 68)),
            ("Compliance", self._state.compliance_score, (96, 165, 250)),
            ("Skutecznosc", self._state.effectiveness_score, (34, 197, 94)),
        ]
        bar_w, bar_h = 200, 18
        bx = _W // 2 - (3 * bar_w + 2 * 30) // 2
        by = 120
        for i, (name, score, color) in enumerate(criteria):
            x = bx + i * (bar_w + 30)
            name_s = get_font(12).render(name, True, _DIM)
            surface.blit(name_s, (x + bar_w // 2 - name_s.get_width() // 2, by))
            bg_rect = pygame.Rect(x, by + 20, bar_w, bar_h)
            pygame.draw.rect(surface, (30, 35, 55), bg_rect, border_radius=4)
            fill_w = int(bar_w * score / 100)
            if fill_w > 0:
                pygame.draw.rect(
                    surface, color, pygame.Rect(x, by + 20, fill_w, bar_h), border_radius=4
                )
            score_s = get_font(11).render(str(score), True, _WHITE)
            surface.blit(score_s, (x + bar_w // 2 - score_s.get_width() // 2, by + 44))

        verdict_color = _VERDICT_COLORS.get(self._verdict, _WHITE)
        v_s = get_font(30).render(self._verdict, True, verdict_color)
        surface.blit(v_s, (_W // 2 - v_s.get_width() // 2, 200))

        comment = _VERDICT_COMMENTS.get(self._verdict, "")
        c_s = get_font(14).render(comment, True, _DIM)
        surface.blit(c_s, (_W // 2 - c_s.get_width() // 2, 250))

        if self._aha_t >= _AHA_DELAY:
            aha_box = pygame.Rect(100, 310, _W - 200, 60)
            pygame.draw.rect(surface, (15, 18, 35), aha_box, border_radius=8)
            pygame.draw.rect(surface, _PURPLE, aha_box, 1, border_radius=8)
            aha_s = get_font(14).render(_AHA, True, _PURPLE)
            surface.blit(aha_s, (_W // 2 - aha_s.get_width() // 2, 330))
            hint = get_font(12).render("[SPACJA] -- wyniki", True, _DIM)
            surface.blit(hint, (_W // 2 - hint.get_width() // 2, _H - 50))

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 56))
        title_s = get_font(20).render("AKT 5 -- TRYBUNAL ETYCZNY", True, _DIM)
        surface.blit(title_s, (_W // 2 - title_s.get_width() // 2, 14))
        if self._phase == "questioning":
            self._draw_questioning(surface)
        else:
            self._draw_verdict(surface)

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
