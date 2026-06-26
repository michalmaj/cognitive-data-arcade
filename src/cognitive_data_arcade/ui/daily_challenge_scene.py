# src/cognitive_data_arcade/ui/daily_challenge_scene.py
"""DailyChallengeScene — daily 5-question tricky quiz with streak update."""

from __future__ import annotations

from datetime import date
from enum import Enum, auto

import pygame

from cognitive_data_arcade.data.act_content import ACT_INTROS
from cognitive_data_arcade.engine.challenge_loader import load_questions, pick_daily
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import ProfileManager

_W, _H = 1024, 640
_BG = (13, 15, 26)
_SURFACE = (22, 24, 40)
_SURFACE2 = (30, 32, 56)
_ACCENT = (99, 102, 241)
_TEXT = (240, 241, 255)
_DIM = (90, 96, 144)
_GREEN = (74, 222, 128)
_RED = (231, 76, 60)
_OPTION_KEYS = [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d]


class _State(Enum):
    TITLE = auto()
    QUESTION = auto()
    RESULT = auto()
    SUMMARY = auto()


class DailyChallengeScene(Scene):
    """Standalone daily challenge: 5 tricky questions, streak update on finish."""

    def __init__(
        self,
        pm: ProfileManager,
        strings: Strings,
        back_scene: Scene,
        today: date | None = None,
    ) -> None:
        self._pm = pm
        self._strings = strings
        self._back = back_scene
        self._today = today or date.today()
        self._done = False
        self._next: Scene | None = None

        questions = load_questions()
        self._questions = pick_daily(questions, self._today)
        self._q_idx = 0
        self._selected: int | None = None
        self._correct_count = 0
        self._state = _State.TITLE
        self._profile = pm.load()
        self._option_rects: list[pygame.Rect] = []

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_click(event.pos)
            return
        if event.type != pygame.KEYDOWN:
            return
        key = event.key
        if self._state == _State.TITLE:
            if key in (pygame.K_SPACE, pygame.K_RETURN):
                self._state = _State.QUESTION
        elif self._state == _State.QUESTION:
            if key in _OPTION_KEYS:
                self._selected = _OPTION_KEYS.index(key)
            elif key == pygame.K_RETURN and self._selected is not None:
                self._confirm()
        elif self._state == _State.RESULT:
            if key in (pygame.K_SPACE, pygame.K_RETURN):
                self._advance()
        elif self._state == _State.SUMMARY:
            if key in (pygame.K_SPACE, pygame.K_RETURN):
                self._exit()

    def _handle_click(self, pos: tuple[int, int]) -> None:
        if self._state == _State.TITLE:
            self._state = _State.QUESTION
        elif self._state == _State.QUESTION:
            for i, rect in enumerate(self._option_rects):
                if rect.collidepoint(pos):
                    self._selected = i
                    self._confirm()
                    return
            if self._selected is not None:
                self._confirm()
        elif self._state == _State.RESULT:
            self._advance()
        elif self._state == _State.SUMMARY:
            self._exit()

    def _confirm(self) -> None:
        if self._selected is None or self._state != _State.QUESTION:
            return
        q = self._questions[self._q_idx]
        if self._selected == q["correct_idx"]:
            self._correct_count += 1
        self._state = _State.RESULT

    def _advance(self) -> None:
        self._q_idx += 1
        self._selected = None
        if self._q_idx >= len(self._questions):
            self._finish()
        else:
            self._state = _State.QUESTION

    def _finish(self) -> None:
        self._profile = self._pm.touch_streak(self._today)
        self._state = _State.SUMMARY

    def _exit(self) -> None:
        self._next = self._back
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    # ── Drawing ───────────────────────────────────────────────────────────────

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        if self._state == _State.TITLE:
            self._draw_title(surface)
        elif self._state == _State.QUESTION:
            self._draw_question(surface)
        elif self._state == _State.RESULT:
            self._draw_result(surface)
        elif self._state == _State.SUMMARY:
            self._draw_summary(surface)

    def _draw_title(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        pygame.draw.rect(surface, _ACCENT, (0, 0, w, 4))
        title = get_font(42).render(self._strings.daily_title, True, _TEXT)
        surface.blit(title, (w // 2 - title.get_width() // 2, 120))
        streak = self._profile.streak_days
        if streak > 0:
            chip = get_font(28).render(f"🔥 {streak}", True, _ACCENT)
            surface.blit(chip, (w // 2 - chip.get_width() // 2, 185))
        sub = get_font(22).render(self._strings.daily_subtitle, True, _DIM)
        surface.blit(sub, (w // 2 - sub.get_width() // 2, 240))
        hint_text = "SPACJA - start" if self._strings.language == "pl" else "SPACE - start"
        hint = get_font(18).render(hint_text, True, _DIM)
        surface.blit(hint, (w // 2 - hint.get_width() // 2, h - 44))

    def _draw_question(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        is_pl = self._strings.language == "pl"
        q = self._questions[self._q_idx]
        n = len(self._questions)

        mod_idx = q["module_idx"]
        key = "short_title_pl" if is_pl else "short_title_en"
        prefix = "AKT" if is_pl else "ACT"
        act_label = f"{prefix} {mod_idx + 1} · {ACT_INTROS[mod_idx][key]}"
        chip = get_font(15).render(act_label, True, _ACCENT)
        surface.blit(chip, (32, 20))

        prog = get_font(15).render(f"{self._q_idx + 1} / {n}", True, _DIM)
        surface.blit(prog, (w - prog.get_width() - 32, 20))

        q_key = "q_pl" if is_pl else "q_en"
        q_text = q[q_key]
        q_font = get_font(26)
        q_y = 55
        words = q_text.split()
        line, q_lines = "", []
        for word in words:
            test = (line + " " + word).strip()
            if q_font.size(test)[0] < w - 120:
                line = test
            else:
                q_lines.append(line)
                line = word
        if line:
            q_lines.append(line)
        for ln in q_lines:
            ln_surf = q_font.render(ln, True, _TEXT)
            surface.blit(ln_surf, (w // 2 - ln_surf.get_width() // 2, q_y))
            q_y += q_font.get_height() + 4

        opts_key = "options_pl" if is_pl else "options_en"
        options = q[opts_key]
        labels = ["A", "B", "C", "D"]
        btn_w, btn_h = w - 120, 56
        btn_x = 60
        opt_y = max(150, q_y + 12)
        self._option_rects = []
        for i, opt in enumerate(options):
            rect = pygame.Rect(btn_x, opt_y, btn_w, btn_h)
            self._option_rects.append(rect)
            if self._selected == i:
                bg, border = (28, 32, 70), _ACCENT
            else:
                bg, border = _SURFACE, _SURFACE2
            pygame.draw.rect(surface, bg, rect, border_radius=8)
            pygame.draw.rect(surface, border, rect, 2, border_radius=8)
            lbl = get_font(20).render(f"[{labels[i]}]", True, _ACCENT)
            surface.blit(lbl, (btn_x + 14, opt_y + (btn_h - lbl.get_height()) // 2))
            opt_surf = get_font(20).render(opt, True, _TEXT)
            surface.blit(opt_surf, (btn_x + 56, opt_y + (btn_h - opt_surf.get_height()) // 2))
            opt_y += btn_h + 10

        if self._selected is not None:
            hint_text = "ENTER - potwierdź" if is_pl else "ENTER - confirm"
        else:
            hint_text = "[A/B/C/D] - wybierz" if is_pl else "[A/B/C/D] - choose"
        hint = get_font(16).render(hint_text, True, _DIM)
        surface.blit(hint, (w // 2 - hint.get_width() // 2, h - 36))

    def _draw_result(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        is_pl = self._strings.language == "pl"
        q = self._questions[self._q_idx]
        correct_idx = q["correct_idx"]
        labels = ["A", "B", "C", "D"]

        correct = self._selected == correct_idx
        verdict_text = self._strings.daily_correct if correct else self._strings.daily_wrong
        verdict_color = _GREEN if correct else _RED
        verdict = get_font(34).render(verdict_text, True, verdict_color)
        surface.blit(verdict, (w // 2 - verdict.get_width() // 2, 60))

        if not correct:
            was_lbl = get_font(20).render(
                f"{self._strings.daily_correct_was} [{labels[correct_idx]}]",
                True,
                _GREEN,
            )
            surface.blit(was_lbl, (w // 2 - was_lbl.get_width() // 2, 110))

        exp_key = "explanation_pl" if is_pl else "explanation_en"
        explanation = q[exp_key]
        exp_font = get_font(20)
        exp_y = 160
        words = explanation.split()
        line, lines = "", []
        for word in words:
            test = (line + " " + word).strip()
            if exp_font.size(test)[0] < w - 120:
                line = test
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        for ln in lines:
            ln_surf = exp_font.render(ln, True, _DIM)
            surface.blit(ln_surf, (w // 2 - ln_surf.get_width() // 2, exp_y))
            exp_y += exp_font.get_height() + 4

        hint_text = "SPACJA - dalej" if is_pl else "SPACE - next"
        hint = get_font(16).render(hint_text, True, _DIM)
        surface.blit(hint, (w // 2 - hint.get_width() // 2, h - 36))

    def _draw_summary(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        is_pl = self._strings.language == "pl"
        n = len(self._questions)

        score_text = f"{self._strings.daily_summary_score}  {self._correct_count} / {n}"
        score = get_font(40).render(score_text, True, _GREEN)
        surface.blit(score, (w // 2 - score.get_width() // 2, 120))

        streak = self._profile.streak_days
        if streak > 0:
            label = self._strings.daily_streak_label
            streak_text = f"🔥 {streak} {label}"
            streak_surf = get_font(26).render(streak_text, True, _ACCENT)
            surface.blit(streak_surf, (w // 2 - streak_surf.get_width() // 2, 195))

        hint_text = "SPACJA - wróć do menu" if is_pl else "SPACE - back to menu"
        hint = get_font(16).render(hint_text, True, _DIM)
        surface.blit(hint, (w // 2 - hint.get_width() // 2, h - 44))
