from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.human_vs_model.challenge_data import DetectChallenge

_W, _H    = 1024, 720
_TOP_H    = 44
_MID      = 512
_BG       = (15, 15, 35)
_TOP_BG   = (10, 10, 28)
_LEFT_BG  = (12, 18, 32)
_RIGHT_BG = (12, 8, 28)
_WHITE    = (240, 240, 240)
_DIM      = (100, 100, 140)
_BLUE     = (52, 152, 219)
_PURPLE   = (155, 89, 182)
_AMBER    = (240, 165, 0)
_GREEN    = (39, 174, 96)
_RED      = (231, 76, 60)
_GREY     = (60, 60, 80)

_BASE_SCORE  = 20
_BEAT_BONUS  = 10
_AI_THINK_MS = 1500.0

_BTN_LEWY  = pygame.Rect(16, 384, 234, 44)   # center = (133, 406)
_BTN_PRAWY = pygame.Rect(262, 384, 234, 44)  # center = (379, 406)


def _wrap_text(
    surface: pygame.Surface,
    text: str,
    font_size: int,
    x: int,
    y: int,
    max_width: int,
    color: tuple[int, int, int],
) -> int:
    """Render word-wrapped text and return the y position after the last line."""
    font = get_font(font_size)
    words = text.split()
    line_buf = ""
    for word in words:
        candidate = f"{line_buf} {word}".strip()
        if font.size(candidate)[0] <= max_width:
            line_buf = candidate
        else:
            surface.blit(font.render(line_buf, True, color), (x, y))
            y += font.get_height() + 2
            line_buf = word
    if line_buf:
        surface.blit(font.render(line_buf, True, color), (x, y))
        y += font.get_height() + 2
    return y


class PhaseDetectScene(Scene):
    def __init__(
        self,
        challenges: list[DetectChallenge],
        round_idx: int,
        session_score: int,
        beat_ai_count: int,
    ) -> None:
        self._challenges    = challenges
        self._challenge     = challenges[round_idx]
        self._round_idx     = round_idx
        self._session_score = session_score
        self._beat_ai_count = beat_ai_count
        self._selected: str | None = None   # "Lewy" | "Prawy"
        self._state         = "task"         # "task" | "ai_thinking" | "reveal"
        self._ai_timer      = 0.0
        self._anim_tick     = 0.0
        self._dots          = ""
        self._correct       = False
        self._beat_ai       = False
        self._round_score   = 0
        self._done          = False
        self._next: Scene | None = None

    # --- events ---------------------------------------------------------------

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._done:
            return
        if self._state == "reveal":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._advance()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._advance()
            return
        if self._state != "task":
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if _BTN_LEWY.collidepoint(event.pos):
                self._submit("Lewy")
            elif _BTN_PRAWY.collidepoint(event.pos):
                self._submit("Prawy")

    # --- state transitions ----------------------------------------------------

    def _submit(self, chosen: str) -> None:
        self._selected  = chosen
        self._state     = "ai_thinking"
        self._ai_timer  = _AI_THINK_MS
        self._anim_tick = 0.0

    def _calc_score(self) -> None:
        # Correct answer is always "Lewy" (human_text always shown on the left)
        self._correct     = self._selected == "Lewy"
        self._beat_ai     = self._correct   # AI always fails detect
        base              = _BASE_SCORE if self._correct else 0
        bonus             = _BEAT_BONUS if self._beat_ai else 0
        self._round_score = base + bonus

    def _advance(self) -> None:
        new_score = self._session_score + self._round_score
        new_beat  = self._beat_ai_count + (1 if self._beat_ai else 0)
        if self._round_idx < len(self._challenges) - 1:
            self._next = PhaseDetectScene(
                self._challenges, self._round_idx + 1, new_score, new_beat
            )
        else:
            from cognitive_data_arcade.games.human_vs_model.challenge_data import COMPLETE_CHALLENGES
            from cognitive_data_arcade.games.human_vs_model.phase_complete import PhaseCompleteScene
            self._next = PhaseCompleteScene(COMPLETE_CHALLENGES, 0, new_score, new_beat)
        self._done = True

    # --- update ---------------------------------------------------------------

    def update(self, dt_ms: float = 0.0) -> None:
        if self._state == "ai_thinking":
            self._ai_timer  -= dt_ms
            self._anim_tick += dt_ms
            self._dots       = "." * (int(self._anim_tick / 400) % 4)
            if self._ai_timer <= 0:
                self._calc_score()
                self._state = "reveal"

    # --- draw -----------------------------------------------------------------

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        self._draw_top_bar(surface)
        self._draw_left_panel(surface)
        self._draw_right_panel(surface)

    def _draw_top_bar(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _TOP_BG, (0, 0, _W, _TOP_H))
        pygame.draw.line(surface, _GREY, (0, _TOP_H), (_W, _TOP_H))

        phase_lbl = get_font(13).render("MEDIUM (B)", True, _AMBER)
        surface.blit(phase_lbl, (16, (_TOP_H - phase_lbl.get_height()) // 2))

        rnd = get_font(13).render(
            f"Runda {self._round_idx + 1}/{len(self._challenges)}", True, _DIM
        )
        surface.blit(rnd, (_W // 2 - rnd.get_width() // 2, (_TOP_H - rnd.get_height()) // 2))

        score_lbl = get_font(13).render(f"{self._session_score} pkt", True, _AMBER)
        surface.blit(
            score_lbl,
            (_W - score_lbl.get_width() - 16, (_TOP_H - score_lbl.get_height()) // 2),
        )

    def _draw_left_panel(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _LEFT_BG, (0, _TOP_H, _MID, _H - _TOP_H))
        pygame.draw.line(surface, _GREY, (_MID, _TOP_H), (_MID, _H))

        hdr = get_font(12).render("TY", True, _BLUE)
        surface.blit(hdr, (16, _TOP_H + 10))
        pygame.draw.line(surface, _BLUE, (0, _TOP_H + 26), (_MID, _TOP_H + 26), 1)

        task_lbl = get_font(11).render("WYKRYJ TEKST CZLOWIEKA", True, _DIM)
        surface.blit(task_lbl, (16, _TOP_H + 34))

        # Text boxes
        box1_rect = pygame.Rect(16, 74, 480, 120)
        box2_rect = pygame.Rect(16, 204, 480, 120)

        # Labels above boxes
        lbl1 = get_font(11).render("Tekst 1:", True, _DIM)
        surface.blit(lbl1, (16, 58))
        lbl2 = get_font(11).render("Tekst 2:", True, _DIM)
        surface.blit(lbl2, (16, 188))

        # Draw box borders
        pygame.draw.rect(surface, _GREY, box1_rect, 1)
        pygame.draw.rect(surface, _GREY, box2_rect, 1)

        # Render text inside boxes (with 8px padding)
        pad = 8
        _wrap_text(
            surface,
            self._challenge.human_text,
            12,
            box1_rect.x + pad,
            box1_rect.y + pad,
            box1_rect.width - 2 * pad,
            _WHITE,
        )
        _wrap_text(
            surface,
            self._challenge.ai_text,
            12,
            box2_rect.x + pad,
            box2_rect.y + pad,
            box2_rect.width - 2 * pad,
            _WHITE,
        )

        # Answer buttons
        for rect, label in [(_BTN_LEWY, "Lewy"), (_BTN_PRAWY, "Prawy")]:
            is_sel = label == self._selected
            if self._state == "task":
                bg       = (20, 35, 55)
                color    = _BLUE
                text_col = _WHITE
            elif self._state == "ai_thinking":
                bg       = (25, 40, 60) if is_sel else (15, 15, 25)
                color    = _BLUE if is_sel else _GREY
                text_col = _WHITE if is_sel else _DIM
            else:  # reveal
                if is_sel and self._correct:
                    bg, color = (20, 40, 20), _GREEN
                elif is_sel and not self._correct:
                    bg, color = (40, 15, 15), _RED
                else:
                    bg, color = (15, 15, 25), _GREY
                text_col = _WHITE if is_sel else _DIM
            pygame.draw.rect(surface, bg, rect, border_radius=6)
            pygame.draw.rect(surface, color, rect, 2 if is_sel else 1, border_radius=6)
            btn_lbl = get_font(14).render(label, True, text_col)
            surface.blit(
                btn_lbl,
                (rect.centerx - btn_lbl.get_width() // 2, rect.centery - btn_lbl.get_height() // 2),
            )

        if self._state == "reveal":
            if self._round_score > 0:
                delta = get_font(20).render(f"+{self._round_score} pkt", True, _GREEN)
                surface.blit(delta, (16, _TOP_H + 380))
            hint = get_font(11).render("SPACJA = nastepna runda", True, _GREY)
            surface.blit(hint, (16, _H - 28))

    def _draw_right_panel(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _RIGHT_BG, (_MID, _TOP_H, _MID, _H - _TOP_H))

        hdr = get_font(12).render("AI", True, _PURPLE)
        surface.blit(hdr, (_MID + 16, _TOP_H + 10))
        pygame.draw.line(surface, _PURPLE, (_MID, _TOP_H + 26), (_W, _TOP_H + 26), 1)

        cx = _MID + _MID // 2

        if self._state == "task":
            lock = get_font(24).render("?", True, (60, 40, 80))
            surface.blit(lock, (cx - lock.get_width() // 2, _H // 2 - 30))
            wait = get_font(13).render("AI czeka...", True, (60, 40, 80))
            surface.blit(wait, (cx - wait.get_width() // 2, _H // 2 + 10))

        elif self._state == "ai_thinking":
            lbl = get_font(16).render(f"AI analizuje{self._dots}", True, _PURPLE)
            surface.blit(lbl, (cx - lbl.get_width() // 2, _H // 2 - 16))

        elif self._state == "reveal":
            # AI always fails detect
            ai_lbl = get_font(16).render("AI: Prawy", True, _RED)
            surface.blit(ai_lbl, (cx - ai_lbl.get_width() // 2, _TOP_H + 60))
            verdict = get_font(13).render("(AI sie pomylila)", True, _RED)
            surface.blit(verdict, (cx - verdict.get_width() // 2, _TOP_H + 86))

            if self._beat_ai:
                beat = get_font(14).render("POBILES AI!  +10 bonus", True, _AMBER)
                surface.blit(beat, (cx - beat.get_width() // 2, _TOP_H + 116))

            # Explanation (word-wrapped)
            _wrap_text(
                surface,
                self._challenge.explanation,
                12,
                _MID + 16,
                _TOP_H + 160,
                _MID - 32,
                _DIM,
            )

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
