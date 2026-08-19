from __future__ import annotations

import random

import pygame

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
)
from cognitive_data_arcade.engine.colors import (
    BLUE as _BLUE,
)
from cognitive_data_arcade.engine.colors import (
    DIM as _DIM,
)
from cognitive_data_arcade.engine.colors import (
    GREEN as _GREEN,
)
from cognitive_data_arcade.engine.colors import (
    WHITE as _WHITE,
)
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene

_W, _H = 1024, 768
_TOP_BG = (10, 10, 28)
_PANEL = (18, 18, 42)
_GOLD = (240, 165, 0)
_GREY = (60, 60, 80)

_BTN_PLAY = pygame.Rect(_W // 2 - 120, 460, 240, 50)
_BTN_MENU = pygame.Rect(_W // 2 - 120, 530, 240, 50)

_AHA_INSIGHTS = [
    "AI najczesciej myli się na negacji -- 'nie byl zly' to dla modelu chaos.",
    "Detekcja tekstu AI jest trudna nawet dla modeli -- formalizm to nie dowod.",
    "Uzupelnianie zdan ujawnia ze AI wybiera 'bezpieczne' zakonczenia, nie naturalne.",
]


def _wrap_text(text: str, font: pygame.font.Font, max_width: int) -> list[str]:
    """Wrap text into lines that fit within max_width pixels."""
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = (current + " " + word).strip()
        if font.size(candidate)[0] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


class PhaseResultScene(Scene):
    def __init__(self, session_score: int, beat_ai_count: int, pm=None, strings=None) -> None:
        self._session_score = session_score
        self._beat_ai_count = beat_ai_count
        self._pm = pm
        self._strings = strings
        self._done = False
        self._next: Scene | None = None
        self._aha = random.choice(_AHA_INSIGHTS)

        if session_score >= 200:
            self._stars = 3
        elif session_score >= 120:
            self._stars = 2
        else:
            self._stars = 1

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not self._done and self._pm is not None:
                    self._next = self._build_next_scene()
                self._done = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if _BTN_PLAY.collidepoint(event.pos):
                from cognitive_data_arcade.games.human_vs_model.phase_intro import PhaseIntroScene

                self._next = PhaseIntroScene()
                self._done = True
            elif _BTN_MENU.collidepoint(event.pos):
                if not self._done and self._pm is not None:
                    self._next = self._build_next_scene()
                else:
                    self._next = None
                self._done = True

    def _build_next_scene(self) -> Scene:
        from cognitive_data_arcade.engine.badges import BadgeEngine, SessionResult
        from cognitive_data_arcade.ui.session_summary import SessionSummaryScene

        ap = min(100, self._session_score // 3)
        session = SessionResult(
            task_name="human_vs_model",
            participant_id=self._pm.load().device_uuid,
            session_id="hvm_session",
            total_trials=8,
            correct_trials=min(8, self._beat_ai_count),
            avg_reaction_time_ms=0.0,
            min_reaction_time_ms=0.0,
            max_reaction_time_ms=0.0,
            arcade_points_earned=ap,
            science_points_earned=0,
        )
        profile_before = self._pm.load()
        badge_engine = BadgeEngine()
        new_badge_ids = badge_engine.evaluate(session, profile_before)
        self._pm.add_ap(ap)
        for bid in new_badge_ids:
            self._pm.award_badge(bid)
        profile_after = self._pm.load()
        return SessionSummaryScene(
            session=session,
            new_badge_ids=new_badge_ids,
            profile_before=profile_before,
            profile_after=profile_after,
            strings=self._strings,
            profile_manager=self._pm,
        )

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        self._draw_top_bar(surface)
        self._draw_content(surface)
        self._draw_buttons(surface)

    def _draw_top_bar(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _TOP_BG, (0, 0, _W, 44))
        label = get_font(22).render("WYNIKI", True, _WHITE)
        surface.blit(label, (_W // 2 - label.get_width() // 2, 10))

    def _draw_content(self, surface: pygame.Surface) -> None:
        # Title
        title = get_font(30).render("KONIEC GRY", True, _GOLD)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 100))

        # Score line
        score_text = f"Wynik: {self._session_score} / 270 pkt"
        score_surf = get_font(20).render(score_text, True, _WHITE)
        surface.blit(score_surf, (_W // 2 - score_surf.get_width() // 2, 160))

        # Beat AI line
        beat_text = f"Razy pobil AI: {self._beat_ai_count}/8"
        beat_surf = get_font(18).render(beat_text, True, _WHITE)
        surface.blit(beat_surf, (_W // 2 - beat_surf.get_width() // 2, 200))

        # Stars as circles
        star_y = 250
        for i in range(3):
            filled = i < self._stars
            color = _GOLD if filled else _GREY
            cx = _W // 2 - 40 + i * 40
            pygame.draw.circle(surface, color, (cx, star_y), 14, 0 if filled else 2)

        # AHA insight text (word-wrapped, centered)
        aha_font = get_font(14)
        wrapped = _wrap_text(self._aha, aha_font, 700)
        y = 320
        for line in wrapped:
            line_surf = aha_font.render(line, True, _DIM)
            surface.blit(line_surf, (_W // 2 - line_surf.get_width() // 2, y))
            y += 22

    def _draw_buttons(self, surface: pygame.Surface) -> None:
        # "Zagraj ponownie" button
        pygame.draw.rect(surface, _PANEL, _BTN_PLAY, border_radius=8)
        pygame.draw.rect(surface, _GREEN, _BTN_PLAY, 2, border_radius=8)
        lbl_play = get_font(20).render("Zagraj ponownie", True, _GREEN)
        surface.blit(
            lbl_play,
            (
                _W // 2 - lbl_play.get_width() // 2,
                _BTN_PLAY.y + (_BTN_PLAY.height - lbl_play.get_height()) // 2,
            ),
        )

        # "Menu" button
        pygame.draw.rect(surface, _PANEL, _BTN_MENU, border_radius=8)
        pygame.draw.rect(surface, _BLUE, _BTN_MENU, 2, border_radius=8)
        lbl_menu = get_font(20).render("Menu", True, _BLUE)
        surface.blit(
            lbl_menu,
            (
                _W // 2 - lbl_menu.get_width() // 2,
                _BTN_MENU.y + (_BTN_MENU.height - lbl_menu.get_height()) // 2,
            ),
        )

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
