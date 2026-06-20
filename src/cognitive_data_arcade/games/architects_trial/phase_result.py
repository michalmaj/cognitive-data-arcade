# src/cognitive_data_arcade/games/architects_trial/phase_result.py
from __future__ import annotations
import pygame
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.architects_trial.game_state import GameState, compute_verdict

_W, _H = 1024, 720
_BG = (8, 12, 20)
_PANEL = (16, 20, 36)
_WHITE = (240, 240, 240)
_DIM = (148, 163, 184)
_PURPLE = (167, 139, 250)
_GOLD = (243, 156, 18)
_GREY = (60, 60, 80)

_VERDICT_COLORS = {
    "ZATWIERDZONY": (34, 197, 94),
    "ZATWIERDZONY Z ZALECENIAMI": (167, 139, 250),
    "ZAWIESZONY": (249, 115, 22),
    "ODRZUCONY": (239, 68, 68),
}

_DOMAIN_TAGS = {
    "social": "[Opieka spoleczna]",
    "hiring": "[Rekrutacja AI]",
    "triage": "[Triage SOR]",
}

_WORST_COMMENTS = {
    "fairness": "System wykazal nieproporcjonalny wplyw na grupy chronione.",
    "compliance": "Projekt nie spelnia pelnych wymagan regulacyjnych.",
    "effectiveness": "Skutecznosc systemu pozostawia pole do poprawy.",
}


class PhaseResultScene(Scene):
    def __init__(self, state: GameState) -> None:
        self._state = state
        self._verdict = compute_verdict(
            state.fairness_score, state.compliance_score, state.effectiveness_score
        )
        worst = min(
            [("fairness", state.fairness_score),
             ("compliance", state.compliance_score),
             ("effectiveness", state.effectiveness_score)],
            key=lambda x: x[1],
        )
        self._comment = _WORST_COMMENTS[worst[0]]
        self._btn_replay = pygame.Rect(_W // 2 - 220, _H - 70, 200, 44)
        self._btn_menu = pygame.Rect(_W // 2 + 20, _H - 70, 200, 44)
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._btn_replay.collidepoint(event.pos):
                from cognitive_data_arcade.games.architects_trial.game import ArchitectsTrialScene
                self._next = ArchitectsTrialScene()
                self._done = True
            elif self._btn_menu.collidepoint(event.pos):
                self._next = None
                self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 56))
        title = get_font(20).render("The Architect's Trial -- Wyniki", True, _WHITE)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))

        tag = _DOMAIN_TAGS.get(self._state.domain, "")
        tag_s = get_font(13).render(tag, True, _DIM)
        surface.blit(tag_s, (_W // 2 - tag_s.get_width() // 2, 60))

        verdict_color = _VERDICT_COLORS.get(self._verdict, _WHITE)
        v_s = get_font(26).render(self._verdict, True, verdict_color)
        surface.blit(v_s, (_W // 2 - v_s.get_width() // 2, 90))

        for i in range(3):
            pygame.draw.circle(surface, _GOLD, (_W // 2 - 30 + i * 30, 148), 10)

        criteria = [
            ("Fairness", self._state.fairness_score, (239, 68, 68)),
            ("Compliance", self._state.compliance_score, (96, 165, 250)),
            ("Skutecznosc", self._state.effectiveness_score, (34, 197, 94)),
        ]
        bar_w, bar_h = 220, 20
        bx = _W // 2 - (3 * bar_w + 2 * 24) // 2
        by = 175
        for i, (name, score, color) in enumerate(criteria):
            x = bx + i * (bar_w + 24)
            name_s = get_font(12).render(name, True, _DIM)
            surface.blit(name_s, (x + bar_w // 2 - name_s.get_width() // 2, by))
            pygame.draw.rect(surface, (30, 35, 55), pygame.Rect(x, by + 18, bar_w, bar_h), border_radius=4)
            fill_w = int(bar_w * score / 100)
            if fill_w > 0:
                pygame.draw.rect(surface, color, pygame.Rect(x, by + 18, fill_w, bar_h), border_radius=4)
            sc_s = get_font(11).render(str(score), True, _WHITE)
            surface.blit(sc_s, (x + bar_w // 2 - sc_s.get_width() // 2, by + 42))

        comment_s = get_font(13).render(self._comment, True, _DIM)
        surface.blit(comment_s, (_W // 2 - comment_s.get_width() // 2, 270))

        pygame.draw.rect(surface, _PANEL, self._btn_replay, border_radius=6)
        pygame.draw.rect(surface, _GREY, self._btn_replay, 1, border_radius=6)
        rl = get_font(14).render("Zagraj -- inna domena", True, (180, 180, 200))
        surface.blit(rl, (self._btn_replay.x + (self._btn_replay.w - rl.get_width()) // 2,
                          self._btn_replay.y + (self._btn_replay.h - rl.get_height()) // 2))

        pygame.draw.rect(surface, _PANEL, self._btn_menu, border_radius=6)
        pygame.draw.rect(surface, _PURPLE, self._btn_menu, 1, border_radius=6)
        ml = get_font(14).render("Menu", True, _PURPLE)
        surface.blit(ml, (self._btn_menu.x + (self._btn_menu.w - ml.get_width()) // 2,
                          self._btn_menu.y + (self._btn_menu.h - ml.get_height()) // 2))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
