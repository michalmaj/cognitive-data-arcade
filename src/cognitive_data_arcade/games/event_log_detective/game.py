"""EventLogDetectiveGame — main game scene for the Event Log Detective mini-game.

State machine: INTRO -> CONFIG_MAP <-> DECISION -> REPORT
"""

from __future__ import annotations

import enum
from collections.abc import Callable

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.event_log_detective.scenarios import Scenario
from cognitive_data_arcade.profile.manager import ProfileManager

# ---------------------------------------------------------------------------
# Colours
# ---------------------------------------------------------------------------

_BG = (26, 26, 46)
_WHITE = (240, 240, 240)
_DIM = (120, 120, 160)
_ACCENT = (243, 156, 18)
_GREEN = (39, 174, 96)
_RED = (231, 76, 60)
_PANEL_BG = (18, 18, 40)


# ---------------------------------------------------------------------------
# State enum
# ---------------------------------------------------------------------------


class _State(enum.Enum):
    INTRO = "intro"
    CONFIG_MAP = "config_map"
    DECISION = "decision"
    REPORT = "report"


# ---------------------------------------------------------------------------
# Game scene
# ---------------------------------------------------------------------------


class EventLogDetectiveGame(Scene):
    """Main scene for the Event Log Detective mini-game."""

    def __init__(
        self,
        scenario: Scenario,
        difficulty: str,
        strings: Strings,
        pm: ProfileManager,
        back_factory: Callable[[], Scene] | None = None,
    ) -> None:
        self._scenario = scenario
        self._difficulty = difficulty
        self._strings = strings
        self._pm = pm
        self._back_factory = back_factory

        self._state = _State.INTRO
        self._node_idx = 0
        self._option_idx = 0
        self._choices: list[int | None] = [None] * len(scenario.decisions)
        self._popup_visible = False
        self._hint_visible = False
        self._done = False
        self._next: Scene | None = None
        # Populated during draw so mouse handlers can use them
        self._node_rects: list[pygame.Rect] = []
        self._option_rects: list[pygame.Rect] = []

        self._font_title = get_font(48)
        self._font_body = get_font(30)
        self._font_option = get_font(32)
        self._font_hint = get_font(26)

    # ------------------------------------------------------------------
    # Scene interface
    # ------------------------------------------------------------------

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event.pos)
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_mouse_click(event.pos)
            return
        if event.type != pygame.KEYDOWN:
            return

        # If popup is visible it takes priority
        if self._popup_visible:
            self._handle_popup(event)
            return

        if self._state == _State.INTRO:
            self._handle_intro(event)
        elif self._state == _State.CONFIG_MAP:
            self._handle_config_map(event)
        elif self._state == _State.DECISION:
            self._handle_decision(event)
        elif self._state == _State.REPORT:
            self._handle_report(event)

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next if self._done else None

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        if self._state == _State.INTRO:
            self._draw_intro(surface)
        elif self._state == _State.CONFIG_MAP:
            self._draw_config_map(surface)
        elif self._state == _State.DECISION:
            self._draw_decision(surface)
        elif self._state == _State.REPORT:
            self._draw_report(surface)

        if self._popup_visible:
            self._draw_popup(surface)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _handle_intro(self, event: pygame.event.Event) -> None:
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self._state = _State.CONFIG_MAP

    def _handle_config_map(self, event: pygame.event.Event) -> None:
        n = len(self._scenario.decisions)
        if event.key == pygame.K_UP:
            self._node_idx = max(0, self._node_idx - 1)
        elif event.key == pygame.K_DOWN:
            self._node_idx = min(n - 1, self._node_idx + 1)
        elif event.key == pygame.K_RETURN:
            if self._all_decided():
                self._state = _State.REPORT
            else:
                prev = self._choices[self._node_idx]
                self._option_idx = prev if prev is not None else 0
                self._hint_visible = False
                self._state = _State.DECISION
        elif event.key == pygame.K_ESCAPE:
            self._go_back()

    def _handle_decision(self, event: pygame.event.Event) -> None:
        dec = self._scenario.decisions[self._node_idx]
        n_opts = len(dec.options)

        if event.key == pygame.K_UP:
            self._option_idx = max(0, self._option_idx - 1)
        elif event.key == pygame.K_DOWN:
            self._option_idx = min(n_opts - 1, self._option_idx + 1)
        elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
            idx = event.key - pygame.K_1
            if idx < n_opts:
                self._option_idx = idx
        elif event.key == pygame.K_h and self._difficulty == "medium":
            self._hint_visible = not self._hint_visible
        elif event.key == pygame.K_RETURN:
            opt = dec.options[self._option_idx]
            if (
                self._difficulty == "easy"
                and not opt.is_correct
                and opt.consequence_easy_en
            ):
                self._popup_visible = True
            else:
                self._confirm_decision()
        elif event.key == pygame.K_ESCAPE:
            self._state = _State.CONFIG_MAP

    def _handle_popup(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_RETURN:
            self._popup_visible = False
            self._confirm_decision()
        elif event.key == pygame.K_ESCAPE:
            self._popup_visible = False

    def _handle_report(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_RETURN and self._back_factory is not None:
            self._next = self._back_factory()
            self._done = True
        elif event.key == pygame.K_ESCAPE:
            from cognitive_data_arcade.ui.menu import LessonMenuScene  # lazy import

            self._next = LessonMenuScene(self._pm, self._strings)
            self._done = True

    def _handle_mouse_motion(self, pos: tuple[int, int]) -> None:
        if self._popup_visible:
            return
        if self._state == _State.CONFIG_MAP:
            for i, rect in enumerate(self._node_rects):
                if rect.collidepoint(pos):
                    self._node_idx = i
                    break
        elif self._state == _State.DECISION:
            for j, rect in enumerate(self._option_rects):
                if rect.collidepoint(pos):
                    self._option_idx = j
                    break

    def _handle_mouse_click(self, pos: tuple[int, int]) -> None:
        if self._popup_visible:
            return
        if self._state == _State.INTRO:
            self._state = _State.CONFIG_MAP
        elif self._state == _State.CONFIG_MAP:
            for i, rect in enumerate(self._node_rects):
                if rect.collidepoint(pos):
                    self._node_idx = i
                    if self._all_decided():
                        self._state = _State.REPORT
                    else:
                        prev = self._choices[self._node_idx]
                        self._option_idx = prev if prev is not None else 0
                        self._hint_visible = False
                        self._state = _State.DECISION
                    return
        elif self._state == _State.DECISION:
            for j, rect in enumerate(self._option_rects):
                if rect.collidepoint(pos):
                    self._option_idx = j
                    dec = self._scenario.decisions[self._node_idx]
                    opt = dec.options[self._option_idx]
                    if (
                        self._difficulty == "easy"
                        and not opt.is_correct
                        and opt.consequence_easy_en
                    ):
                        self._popup_visible = True
                    else:
                        self._confirm_decision()
                    return
        elif self._state == _State.REPORT:
            if self._back_factory is not None:
                self._next = self._back_factory()
                self._done = True

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _confirm_decision(self) -> None:
        self._choices[self._node_idx] = self._option_idx
        self._state = _State.CONFIG_MAP

    def _go_back(self) -> None:
        if self._back_factory is not None:
            self._next = self._back_factory()
        else:
            from cognitive_data_arcade.ui.menu import LessonMenuScene  # lazy import

            self._next = LessonMenuScene(self._pm, self._strings)
        self._done = True

    def _all_decided(self) -> bool:
        return all(c is not None for c in self._choices)

    def _score(self) -> tuple[int, int, int]:
        """Return (correct, total, weighted_score)."""
        multiplier = {"easy": 1, "medium": 2, "hard": 3}.get(self._difficulty, 1)
        total = len(self._scenario.decisions)
        correct = 0
        for i, dec in enumerate(self._scenario.decisions):
            choice = self._choices[i]
            if choice is not None and dec.options[choice].is_correct:
                correct += 1
        weighted_score = correct * multiplier
        return correct, total, weighted_score

    def _wrap(self, text: str, max_width: int) -> list[str]:
        """Word-wrap *text* to fit within *max_width* pixels using _font_body."""
        lines: list[str] = []
        for paragraph in text.split("\n"):
            words = paragraph.split()
            if not words:
                lines.append("")
                continue
            current = words[0]
            for word in words[1:]:
                test = current + " " + word
                if self._font_body.size(test)[0] < max_width:
                    current = test
                else:
                    lines.append(current)
                    current = word
            lines.append(current)
        return lines

    # ------------------------------------------------------------------
    # Draw helpers
    # ------------------------------------------------------------------

    def _draw_intro(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        sc = self._scenario
        lang = self._strings.language

        title = sc.title_pl if lang == "pl" else sc.title_en
        intro_text = sc.intro_pl if lang == "pl" else sc.intro_en

        title_surf = self._font_title.render(title, True, _ACCENT)
        surface.blit(title_surf, (w // 2 - title_surf.get_width() // 2, 80))

        wrapped = self._wrap(intro_text, w - 120)
        y = 180
        for line in wrapped:
            surf = self._font_body.render(line, True, _WHITE)
            surface.blit(surf, (60, y))
            y += 36

        if lang == "pl":
            hint = "ENTER / SPACJA — dalej"
        else:
            hint = "ENTER / SPACE — continue"
        hint_surf = self._font_hint.render(hint, True, _DIM)
        surface.blit(hint_surf, (w // 2 - hint_surf.get_width() // 2, h - 50))

    def _draw_config_map(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        sc = self._scenario
        lang = self._strings.language
        decisions = sc.decisions

        title = sc.title_pl if lang == "pl" else sc.title_en
        title_surf = self._font_title.render(title, True, _ACCENT)
        surface.blit(title_surf, (w // 2 - title_surf.get_width() // 2, 20))

        # Vertical divider
        divider_x = w // 2
        pygame.draw.line(surface, _DIM, (divider_x, 70), (divider_x, h - 60), 1)

        # Left panel — decision list
        left_w = divider_x - 20
        y = 80
        self._node_rects = []
        for i, dec in enumerate(decisions):
            label = dec.title_pl if lang == "pl" else dec.title_en
            if i == self._node_idx:
                marker = ">"
                color = _ACCENT
            elif self._choices[i] is not None:
                marker = "*"
                color = _WHITE
            else:
                marker = "o"
                color = _DIM
            row = f"{marker} {label}"
            surf = self._font_body.render(row, True, color)
            surface.blit(surf, (20, y))
            self._node_rects.append(pygame.Rect(20, y, left_w, 34))
            y += 34

        # Right panel — context of selected node
        dec = decisions[self._node_idx]
        ctx = dec.context_pl if lang == "pl" else dec.context_en
        ctx_lines = self._wrap(ctx, left_w - 20)
        y = 80
        for line in ctx_lines:
            surf = self._font_body.render(line, True, _WHITE)
            surface.blit(surf, (divider_x + 10, y))
            y += 34

        # Bottom hint
        if self._all_decided():
            if lang == "pl":
                hint = "ENTER — raport   ESC — menu"
            else:
                hint = "ENTER — report   ESC — menu"
        else:
            if lang == "pl":
                hint = "↑↓ — wybierz   ENTER — decyduj   ESC — menu"
            else:
                hint = "UP/DN — select   ENTER — decide   ESC — menu"
        hint_surf = self._font_hint.render(hint, True, _DIM)
        surface.blit(hint_surf, (w // 2 - hint_surf.get_width() // 2, h - 40))

    def _draw_decision(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        sc = self._scenario
        lang = self._strings.language
        dec = sc.decisions[self._node_idx]

        title = dec.title_pl if lang == "pl" else dec.title_en
        title_surf = self._font_title.render(title, True, _ACCENT)
        surface.blit(title_surf, (w // 2 - title_surf.get_width() // 2, 20))

        # Context
        ctx = dec.context_pl if lang == "pl" else dec.context_en
        ctx_lines = self._wrap(ctx, w - 80)
        y = 90
        for line in ctx_lines:
            surf = self._font_body.render(line, True, _DIM)
            surface.blit(surf, (40, y))
            y += 34

        y += 10
        # Options
        self._option_rects = []
        for j, opt in enumerate(dec.options):
            label = opt.label_pl if lang == "pl" else opt.label_en
            row = f"[{j + 1}] {label}"
            color = _ACCENT if j == self._option_idx else _WHITE
            surf = self._font_option.render(row, True, color)
            surface.blit(surf, (40, y))
            self._option_rects.append(pygame.Rect(40, y, w - 80, 40))
            y += 40

        # Medium hint toggle
        if self._difficulty == "medium":
            hint_key_surf = self._font_hint.render(
                self._strings.eld_hint_key, True, _DIM
            )
            surface.blit(
                hint_key_surf, (w // 2 - hint_key_surf.get_width() // 2, h - 80)
            )

            if self._hint_visible:
                hint_text = dec.hint_medium_pl if lang == "pl" else dec.hint_medium_en
                hint_lines = self._wrap(hint_text, w - 80)
                hy = h - 80 - len(hint_lines) * 28 - 10
                for line in hint_lines:
                    surf = self._font_hint.render(line, True, _WHITE)
                    surface.blit(surf, (40, hy))
                    hy += 28

        # ESC hint
        if lang == "pl":
            esc_hint = "ESC — wróć"
        else:
            esc_hint = "ESC — back"
        esc_surf = self._font_hint.render(esc_hint, True, _DIM)
        surface.blit(esc_surf, (w // 2 - esc_surf.get_width() // 2, h - 40))

    def _draw_popup(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        lang = self._strings.language
        dec = self._scenario.decisions[self._node_idx]
        opt = dec.options[self._option_idx]

        # Semi-transparent overlay
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

        # Popup box
        box_w, box_h = 500, 240
        box_x = w // 2 - box_w // 2
        box_y = h // 2 - box_h // 2
        pygame.draw.rect(
            surface, _PANEL_BG, (box_x, box_y, box_w, box_h), border_radius=8
        )
        pygame.draw.rect(
            surface, _ACCENT, (box_x, box_y, box_w, box_h), 2, border_radius=8
        )

        label = opt.label_pl if lang == "pl" else opt.label_en
        title_text = self._strings.eld_consequence_fmt.format(label=label)
        title_surf = self._font_body.render(title_text, True, _ACCENT)
        surface.blit(title_surf, (box_x + 20, box_y + 20))

        consequence = (
            opt.consequence_easy_pl if lang == "pl" else opt.consequence_easy_en
        )
        wrapped = self._wrap(consequence, box_w - 40)
        cy = box_y + 60
        for line in wrapped:
            surf = self._font_body.render(line, True, _WHITE)
            surface.blit(surf, (box_x + 20, cy))
            cy += 30

        confirm_surf = self._font_hint.render(
            self._strings.eld_confirm_hint, True, _DIM
        )
        surface.blit(
            confirm_surf,
            (box_x + box_w // 2 - confirm_surf.get_width() // 2, box_y + box_h - 36),
        )

    def _draw_report(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        lang = self._strings.language
        sc = self._scenario

        title_surf = self._font_title.render(
            self._strings.eld_report_title, True, _ACCENT
        )
        surface.blit(title_surf, (w // 2 - title_surf.get_width() // 2, 20))

        correct, total, pts = self._score()
        mult = {"easy": 1, "medium": 2, "hard": 3}.get(self._difficulty, 1)
        diff_label = self._difficulty
        score_text = self._strings.eld_score_fmt.format(
            correct=correct, total=total, diff=diff_label, mult=mult, pts=pts
        )
        score_surf = self._font_body.render(score_text, True, _WHITE)
        surface.blit(score_surf, (w // 2 - score_surf.get_width() // 2, 80))

        # Horizontal divider
        pygame.draw.line(surface, _DIM, (40, 120), (w - 40, 120), 1)

        y = 134
        for i, dec in enumerate(sc.decisions):
            choice = self._choices[i]
            if choice is None:
                continue
            opt = dec.options[choice]
            is_ok = opt.is_correct

            marker = "OK" if is_ok else "X!"
            marker_color = _GREEN if is_ok else _RED
            marker_surf = self._font_option.render(marker, True, marker_color)
            surface.blit(marker_surf, (20, y))

            dec_title = dec.title_pl if lang == "pl" else dec.title_en
            opt_label = opt.label_pl if lang == "pl" else opt.label_en
            row_text = f"{dec_title}: {opt_label}"
            row_surf = self._font_body.render(row_text, True, _WHITE)
            surface.blit(row_surf, (70, y + 4))

            # Correct choices: explain WHY it was right (dec.report).
            # Wrong choices: show the consequence of this specific bad choice.
            if is_ok:
                explanation = dec.report_pl if lang == "pl" else dec.report_en
            else:
                explanation = (
                    opt.consequence_easy_pl if lang == "pl" else opt.consequence_easy_en
                )
                if not explanation:
                    explanation = dec.report_pl if lang == "pl" else dec.report_en
            exp_lines = self._wrap(explanation, w - 90)
            ry = y + 32
            for line in exp_lines:
                surf = self._font_hint.render(line, True, _DIM)
                surface.blit(surf, (70, ry))
                ry += 22
            y = ry + 6

            if y > h - 80:
                break

        # Bottom hint
        hint_surf = self._font_hint.render(self._strings.eld_play_again, True, _DIM)
        surface.blit(hint_surf, (w // 2 - hint_surf.get_width() // 2, h - 40))
