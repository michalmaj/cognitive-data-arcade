# src/cognitive_data_arcade/games/data_cleaning/scene.py
from __future__ import annotations

import enum
from typing import TYPE_CHECKING

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.data_cleaning.generator import (
    IDENTIFY_HINTS_EN,
    IDENTIFY_HINTS_PL,
    FALSE_FLAG_HINT_EN,
    FALSE_FLAG_HINT_PL,
    CleaningSession,
    apply_fixes,
    compute_score,
    compute_stats,
    generate_dataset,
    get_fix_feedback,
    get_fix_feedback_text,
)
from cognitive_data_arcade.games.data_cleaning.ui_popup import DecisionPopup
from cognitive_data_arcade.games.data_cleaning.ui_table import TableWidget

if TYPE_CHECKING:
    from cognitive_data_arcade.profile.manager import ProfileManager

_BG = (26, 26, 46)
_WHITE = (240, 240, 240)
_DIM = (120, 120, 160)
_ORANGE = (243, 156, 18)
_GREEN = (39, 174, 96)
_RED = (231, 76, 60)

_HINT_MS = 2000.0
_WRONG_HINT_MS = 2500.0
_CORRECT_HINT_MS = 1500.0


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
    ) -> None:
        self._strings = strings
        self._pm = pm
        self._session: CleaningSession = generate_dataset(seed=seed)

        self._phase = Phase.INTRO
        self._done = False
        self._next: Scene | None = None

        # IDENTIFY state
        self._table = TableWidget(self._session.rows)
        self._hint_text = ""
        self._hint_color = _GREEN
        self._hint_timer = 0.0

        # FIX state
        self._fix_queue: list[int] = []
        self._fix_idx = 0
        self._popup: DecisionPopup | None = None
        self._fixes: dict[int, str] = {}
        self._fix_hint_text = ""
        self._fix_hint_color = _GREEN
        self._fix_hint_timer = 0.0

        # Fonts
        self._font_title = get_font(48)
        self._font_body = get_font(28)
        self._font_hint = get_font(22)

    # ── Scene interface ──────────────────────────────────────────────────────────

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        key = event.key
        if self._phase == Phase.INTRO:
            self._handle_intro(key)
        elif self._phase == Phase.IDENTIFY:
            self._handle_identify(key)
        elif self._phase == Phase.FIX:
            self._handle_fix(key)
        elif self._phase == Phase.REPORT:
            self._handle_report(key)

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

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next if self._done else None

    # ── Event handlers ──────────────────────────────────────────────────────────

    def _handle_intro(self, key: int) -> None:
        if key == pygame.K_ESCAPE:
            self._go_menu()
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            self._phase = Phase.IDENTIFY

    def _handle_identify(self, key: int) -> None:
        if key == pygame.K_ESCAPE:
            self._go_menu()
        elif key == pygame.K_f:
            self._enter_fix_phase()
        else:
            result = self._table.handle_keydown(key)
            if result == "flagged":
                self._show_identify_hint(self._table.cursor)
            elif result == "unflagged":
                self._hint_text = ""
                self._hint_timer = 0.0

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
        if key == pygame.K_ESCAPE:
            self._go_menu()
        elif key in (pygame.K_RETURN, pygame.K_r):
            self._next = DataCleaningScene(self._strings, self._pm)
            self._done = True

    # ── Helpers ─────────────────────────────────────────────────────────────────

    def _go_menu(self) -> None:
        from cognitive_data_arcade.ui.menu import LessonMenuScene
        self._next = LessonMenuScene(self._pm, self._strings)
        self._done = True

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
        surface.blit(title_surf, (w // 2 - title_surf.get_width() // 2, 80))
        lines = self._wrap(self._strings.data_cleaning_intro, self._font_body, w - 120)
        y = 180
        for line in lines:
            s = self._font_body.render(line, True, _WHITE)
            surface.blit(s, (60, y))
            y += 36
        hint = "ENTER / SPACJA — dalej" if lang == "pl" else "ENTER / SPACE — continue"
        hs = self._font_hint.render(hint, True, _DIM)
        surface.blit(hs, (w // 2 - hs.get_width() // 2, h - 48))

    def _draw_identify(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        title_surf = self._font_title.render(
            self._strings.data_cleaning_title, True, _ORANGE
        )
        surface.blit(title_surf, (40, 12))
        self._table.draw(surface, x0=40, y0=100)
        if self._hint_timer > 0 and self._hint_text:
            hs = self._font_hint.render(self._hint_text, True, self._hint_color)
            surface.blit(hs, (40, h - 72))
        ds = self._font_hint.render(
            self._strings.data_cleaning_done_btn, True, _DIM
        )
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
