# src/cognitive_data_arcade/games/data_cleaning/scene.py
from __future__ import annotations

import enum
from typing import TYPE_CHECKING

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.data_cleaning.difficulty import (
    ALL_DIFFICULTIES, EASY, DifficultyConfig,
)
from cognitive_data_arcade.games.data_cleaning.generator import (
    FALSE_FLAG_HINT_EN, FALSE_FLAG_HINT_PL,
    GENERIC_HINT_EN, GENERIC_HINT_PL,
    IDENTIFY_HINTS_EN, IDENTIFY_HINTS_PL,
    CleaningSession, apply_fixes, compute_score, compute_stats,
    generate_dataset, get_fix_feedback, get_fix_feedback_text,
)
from cognitive_data_arcade.games.data_cleaning.ui_legend import draw_legend_overlay
from cognitive_data_arcade.games.data_cleaning.ui_popup import DecisionPopup
from cognitive_data_arcade.games.data_cleaning.ui_table import ROW_H, TableWidget

if TYPE_CHECKING:
    from cognitive_data_arcade.profile.manager import ProfileManager

_BG = (26, 26, 46)
_WHITE = (240, 240, 240)
_DIM = (120, 120, 160)
_ORANGE = (243, 156, 18)
_GREEN = (39, 174, 96)
_RED = (231, 76, 60)

# Difficulty button colours: Easy=green, Medium=orange, Hard=red
_DIFF_COLORS = [(39, 174, 96), (230, 126, 34), (231, 76, 60)]

_HINT_MS = 2000.0
_WRONG_HINT_MS = 2500.0
_CORRECT_HINT_MS = 1500.0
_TABLE_Y0: int = 100  # y pixel offset where table rows start in IDENTIFY


class Phase(enum.Enum):
    INTRO = "intro"
    IDENTIFY = "identify"
    FIX = "fix"
    REPORT = "report"


class DataCleaningScene(Scene):
    def __init__(
        self,
        strings: Strings,
        pm: "ProfileManager",
        seed: int | None = None,
        difficulty: DifficultyConfig = EASY,
    ) -> None:
        self._strings = strings
        self._pm = pm
        self._seed = seed
        self._difficulty = difficulty
        self._diff_idx = ALL_DIFFICULTIES.index(difficulty)

        # Generate initial dataset (allows tests to skip INTRO)
        self._session: CleaningSession = generate_dataset(difficulty, seed)

        self._phase = Phase.INTRO
        self._done = False
        self._next: Scene | None = None

        # Hints / legend overlay state
        self._hints_visible: bool = difficulty.hints_mode == "always"
        self._legend_visible: bool = False

        # IDENTIFY state
        self._table = TableWidget(self._session.rows)
        self._hint_text = ""
        self._hint_color = _GREEN
        self._hint_timer = 0.0
        self._h_hint_active = False  # H-key hint persists until H again or cursor move

        # FIX state
        self._fix_queue: list[int] = []
        self._fix_idx = 0
        self._popup: DecisionPopup | None = None
        self._fixes: dict[int, str] = {}
        self._fix_hint_text = ""
        self._fix_hint_color = _GREEN
        self._fix_hint_timer = 0.0

        self._diff_rects: list[pygame.Rect] = []

        # Fonts
        self._font_title = get_font(48)
        self._font_body = get_font(28)
        self._font_hint = get_font(22)

    # ── Scene interface ──────────────────────────────────────────────────────────

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_l:
                self._legend_visible = not self._legend_visible
                return
            if self._phase == Phase.INTRO:
                self._handle_intro(key)
            elif self._phase == Phase.IDENTIFY:
                self._handle_identify(key)
            elif self._phase == Phase.FIX:
                self._handle_fix(key)
            elif self._phase == Phase.REPORT:
                self._handle_report(key)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._phase == Phase.INTRO:
                self._handle_intro_click(event.pos)
            elif self._phase == Phase.IDENTIFY:
                self._handle_identify_click(event.pos)

    def update(self, dt_ms: float) -> None:
        if self._hint_timer > 0:
            self._hint_timer = max(0.0, self._hint_timer - dt_ms)
        if self._fix_hint_timer > 0:
            self._fix_hint_timer = max(0.0, self._fix_hint_timer - dt_ms)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        if self._phase == Phase.INTRO:
            self._draw_intro(surface)
        elif self._phase == Phase.IDENTIFY:
            self._draw_identify(surface)
        elif self._phase == Phase.FIX:
            self._draw_fix(surface)
        elif self._phase == Phase.REPORT:
            self._draw_report(surface)
        if self._legend_visible:
            draw_legend_overlay(surface, self._font_hint, self._strings)

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next if self._done else None

    # ── Event handlers ──────────────────────────────────────────────────────────

    def _handle_intro(self, key: int) -> None:
        if key == pygame.K_1:
            self._set_difficulty(0)
        elif key == pygame.K_2:
            self._set_difficulty(1)
        elif key == pygame.K_3:
            self._set_difficulty(2)
        elif key in (pygame.K_RIGHT, pygame.K_DOWN):
            self._set_difficulty((self._diff_idx + 1) % len(ALL_DIFFICULTIES))
        elif key in (pygame.K_LEFT, pygame.K_UP):
            self._set_difficulty((self._diff_idx - 1) % len(ALL_DIFFICULTIES))
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            self._start_game()

    def _handle_intro_click(self, pos: tuple[int, int]) -> None:
        for i, rect in enumerate(self._diff_rects):
            if rect.collidepoint(pos):
                self._set_difficulty(i)
                return

    def _handle_identify_click(self, pos: tuple[int, int]) -> None:
        row = (pos[1] - _TABLE_Y0) // ROW_H + self._table.scroll
        if not (0 <= row < len(self._session.rows)):
            return
        prev_cursor = self._table.cursor
        self._table.set_cursor(row)
        if row != prev_cursor:
            self._clear_h_hint()
        result = self._table.flag_toggle(row)
        if result == "flagged" and self._hints_visible:
            self._show_identify_hint(row)
        elif result == "unflagged":
            self._hint_text = ""
            self._hint_timer = 0.0
            self._h_hint_active = False

    def _set_difficulty(self, idx: int) -> None:
        self._diff_idx = idx
        self._difficulty = ALL_DIFFICULTIES[idx]

    def _start_game(self) -> None:
        self._session = generate_dataset(self._difficulty, self._seed)
        self._table = TableWidget(self._session.rows)
        self._hints_visible = self._difficulty.hints_mode == "always"
        self._phase = Phase.IDENTIFY

    def _handle_identify(self, key: int) -> None:
        if key == pygame.K_h:
            if self._difficulty.hints_mode == "toggle":
                self._toggle_h_hint()
        elif key == pygame.K_f:
            self._enter_fix_phase()
        else:
            prev_cursor = self._table.cursor
            result = self._table.handle_keydown(key)
            if self._table.cursor != prev_cursor:
                self._clear_h_hint()
            if result == "flagged":
                if self._hints_visible:
                    self._show_identify_hint(self._table.cursor)
            elif result == "unflagged":
                self._hint_text = ""
                self._hint_timer = 0.0
                self._h_hint_active = False

    def _handle_fix(self, key: int) -> None:
        if self._popup is None:
            return
        choice = self._popup.handle_keydown(key)
        if choice is not None:
            row_idx = self._fix_queue[self._fix_idx]
            self._fixes[row_idx] = choice
            error_type = self._session.ground_truth.get(row_idx)
            level = get_fix_feedback(error_type, choice)
            self._fix_hint_text = get_fix_feedback_text(
                error_type, choice, level, self._strings.language
            )
            if level == "correct":
                self._fix_hint_color = _GREEN
                self._fix_hint_timer = _CORRECT_HINT_MS
            elif level == "suboptimal":
                self._fix_hint_color = _ORANGE
                self._fix_hint_timer = _WRONG_HINT_MS
            else:
                self._fix_hint_color = _RED
                self._fix_hint_timer = _WRONG_HINT_MS
            self._advance_fix()

    def _handle_report(self, key: int) -> None:
        pass

    # ── Helpers ─────────────────────────────────────────────────────────────────

    def _show_identify_hint(self, idx: int) -> None:
        error_type = self._session.ground_truth.get(idx)
        lang = self._strings.language
        hints = IDENTIFY_HINTS_PL if lang == "pl" else IDENTIFY_HINTS_EN
        if error_type is not None:
            self._hint_text = hints[error_type]
            self._hint_color = _GREEN
        else:
            self._hint_text = FALSE_FLAG_HINT_PL if lang == "pl" else FALSE_FLAG_HINT_EN
            self._hint_color = _RED
        self._hint_timer = _HINT_MS

    def _toggle_h_hint(self) -> None:
        if self._h_hint_active:
            self._hint_text = ""
            self._h_hint_active = False
            return
        cursor = self._table.cursor
        lang = self._strings.language
        if cursor in self._table.flagged:
            error_type = self._session.ground_truth.get(cursor)
            hints = IDENTIFY_HINTS_PL if lang == "pl" else IDENTIFY_HINTS_EN
            if error_type is not None:
                self._hint_text = hints[error_type]
                self._hint_color = _GREEN
            else:
                self._hint_text = FALSE_FLAG_HINT_PL if lang == "pl" else FALSE_FLAG_HINT_EN
                self._hint_color = _RED
        else:
            self._hint_text = GENERIC_HINT_PL if lang == "pl" else GENERIC_HINT_EN
            self._hint_color = _DIM
        self._h_hint_active = True

    def _clear_h_hint(self) -> None:
        if self._h_hint_active:
            self._hint_text = ""
            self._h_hint_active = False

    def _enter_fix_phase(self) -> None:
        self._fix_queue = sorted(self._table.flagged)
        self._fix_idx = 0
        if not self._fix_queue:
            self._phase = Phase.REPORT
            return
        self._phase = Phase.FIX
        self._load_popup()

    def _load_popup(self) -> None:
        row_idx = self._fix_queue[self._fix_idx]
        row = self._session.rows[row_idx]
        has_format_fix = row.accuracy is not None and row.accuracy > 1.0
        self._popup = DecisionPopup(row, has_format_fix=has_format_fix)

    def _advance_fix(self) -> None:
        self._fix_idx += 1
        if self._fix_idx >= len(self._fix_queue):
            self._phase = Phase.REPORT
            self._popup = None
        else:
            self._load_popup()

    # ── Draw helpers ─────────────────────────────────────────────────────────────

    def _draw_intro(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        lang = self._strings.language

        title_surf = self._font_title.render(
            self._strings.data_cleaning_title, True, _ORANGE
        )
        surface.blit(title_surf, (w // 2 - title_surf.get_width() // 2, 60))

        intro_lines = self._wrap(self._strings.data_cleaning_intro, self._font_body, w - 120)
        y = 140
        for line in intro_lines:
            s = self._font_body.render(line, True, _WHITE)
            surface.blit(s, (60, y))
            y += 36

        # Difficulty label
        dl = self._font_hint.render(self._strings.difficulty_label, True, _DIM)
        surface.blit(dl, (60, y + 20))
        y += 56

        # Three difficulty buttons
        diff_labels = [
            self._strings.difficulty_easy,
            self._strings.difficulty_medium,
            self._strings.difficulty_hard,
        ]
        diff_descs = [
            self._strings.difficulty_easy_desc,
            self._strings.difficulty_medium_desc,
            self._strings.difficulty_hard_desc,
        ]
        btn_x = 60
        self._diff_rects = []
        for i, (label, desc, color) in enumerate(zip(diff_labels, diff_descs, _DIFF_COLORS)):
            is_active = i == self._diff_idx
            btn_color = color if is_active else _DIM
            btn_surf = self._font_body.render(f"[{i+1}] {label}", True, btn_color)
            surface.blit(btn_surf, (btn_x, y))
            desc_surf = self._font_hint.render(desc, True, btn_color)
            surface.blit(desc_surf, (btn_x + btn_surf.get_width() + 16, y + 4))
            self._diff_rects.append(pygame.Rect(btn_x, y, w - btn_x - 60, 36))
            y += 40

        # Hint bar
        if lang == "pl":
            hint = "[1/2/3] poziom  [strzalki] zmien  [L] legenda  [ENTER] start  [ESC] pauza"
        else:
            hint = "[1/2/3] difficulty  [arrows] change  [L] legend  [ENTER] start  [ESC] pause"
        hs = self._font_hint.render(hint, True, _DIM)
        surface.blit(hs, (w // 2 - hs.get_width() // 2, h - 48))

    def _draw_identify(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        title_surf = self._font_title.render(
            self._strings.data_cleaning_title, True, _ORANGE
        )
        surface.blit(title_surf, (40, 12))
        self._table.draw(surface, x0=40, y0=_TABLE_Y0, hints_visible=self._hints_visible)
        if (self._hint_timer > 0 or self._h_hint_active) and self._hint_text:
            hs = self._font_hint.render(self._hint_text, True, self._hint_color)
            surface.blit(hs, (40, h - 72))
        hint_parts = [self._strings.data_cleaning_done_btn]
        if self._difficulty.hints_mode == "toggle":
            hint_parts.append(self._strings.hint_key_hints)
        hint_parts.append(self._strings.hint_key_legend)
        ds = self._font_hint.render("   ".join(hint_parts), True, _DIM)
        surface.blit(ds, (40, h - 40))

    def _draw_fix(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        if self._popup is None:
            return
        progress = f"{self._fix_idx + 1} / {len(self._fix_queue)}"
        ps = self._font_body.render(progress, True, _DIM)
        surface.blit(ps, (w - ps.get_width() - 40, 20))
        self._popup.draw(surface)
        if self._fix_hint_timer > 0 and self._fix_hint_text:
            hs = self._font_hint.render(
                self._fix_hint_text, True, self._fix_hint_color
            )
            surface.blit(hs, (40, h - 48))

    def _draw_report(self, surface: pygame.Surface) -> None:
        from cognitive_data_arcade.games.data_cleaning.ui_report import draw_report
        draw_report(
            surface,
            self._session,
            self._table.flagged,
            self._fixes,
            self._strings,
            self._font_title,
            self._font_body,
            self._font_hint,
        )

    @staticmethod
    def _wrap(text: str, font: pygame.font.Font, max_w: int) -> list[str]:
        lines: list[str] = []
        for para in text.split("\n"):
            words = para.split()
            if not words:
                lines.append("")
                continue
            current = words[0]
            for word in words[1:]:
                candidate = f"{current} {word}"
                if font.size(candidate)[0] < max_w:
                    current = candidate
                else:
                    lines.append(current)
                    current = word
            lines.append(current)
        return lines
