from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.cognitive_dashboard.profile import cognitive_profile
from cognitive_data_arcade.games.cognitive_dashboard.session import DashboardSession, TaskResult
from cognitive_data_arcade.profile.manager import ProfileManager

_BG     = (26, 26, 46)
_PANEL  = (18, 18, 42)
_WHITE  = (240, 240, 240)
_DIM    = (100, 100, 150)
_ORANGE = (243, 156, 18)
_GREEN  = (39, 174, 96)
_RED    = (231, 76, 60)
_BLUE   = (52, 152, 219)
_W, _H  = 1024, 768

_TASK_COLORS = [
    (52, 152, 219),   # RT — blue
    (231, 76, 60),    # Stroop — red
    (230, 126, 34),   # Flanker — orange
    (39, 174, 96),    # GoNoGo — green
]
_TASK_NAMES = ["RT Lab", "Stroop", "Flanker", "Go/No-Go"]

_TILE_W, _TILE_H = 420, 190
_TILE_GAP = 40
_TILES_LEFT = (_W - 2 * _TILE_W - _TILE_GAP) // 2
_ROW1_Y = 130
_ROW2_Y = _ROW1_Y + _TILE_H + 24

# What-if slider constants (fixed literary ranges)
_WI_STROOP_MAX  = 150.0
_WI_FLANKER_MAX = 100.0


def _tile_rect(idx: int) -> pygame.Rect:
    col = idx % 2
    row = idx // 2
    x = _TILES_LEFT + col * (_TILE_W + _TILE_GAP)
    y = _ROW1_Y if row == 0 else _ROW2_Y
    return pygame.Rect(x, y, _TILE_W, _TILE_H)


def _avg_rt(rt_ms: list[float]) -> float:
    valid = [r for r in rt_ms if r > 0]
    return sum(valid) / len(valid) if valid else 0.0


def _accuracy(correct: list[bool]) -> float:
    return 100.0 * sum(correct) / len(correct) if correct else 0.0


def _effect(rt_ms: list[float], condition: list[str], a: str, b: str) -> float:
    a_rts = [r for r, c in zip(rt_ms, condition) if c == a and r > 0]
    b_rts = [r for r, c in zip(rt_ms, condition) if c == b and r > 0]
    if not a_rts or not b_rts:
        return 0.0
    return sum(b_rts) / len(b_rts) - sum(a_rts) / len(a_rts)


def _dim_overlay(surface: pygame.Surface) -> None:
    ov = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 180))
    surface.blit(ov, (0, 0))


class CognitiveDashboardScene(Scene):

    # ── Detail-panel geometry ──────────────────────────────────────
    _DP_W, _DP_H = 680, 400
    _DP_X = (_W - _DP_W) // 2
    _DP_Y = (_H - _DP_H) // 2

    # ── What-if-panel geometry ─────────────────────────────────────
    _WI_W, _WI_H  = 720, 500
    _WI_X = (_W - _WI_W) // 2
    _WI_Y = (_H - _WI_H) // 2
    _WI_TRACK_W   = 360
    _WI_TRACK_X   = _WI_X + 220      # slider track left edge
    _WI_STROOP_Y  = _WI_Y + 76
    _WI_FLANKER_Y = _WI_Y + 160
    _WI_FA_Y      = _WI_Y + 244      # label row
    _WI_FA_BTN_Y  = _WI_Y + 278      # buttons row (separate from label)

    def __init__(
        self,
        session: DashboardSession,
        strings: Strings,
        pm: ProfileManager,
    ) -> None:
        self._session = session
        self._strings = strings
        self._pm = pm
        self._selected = 0
        self._done = False
        self._next: Scene | None = None

        # A: detail panel
        self._detail_idx: int | None = None

        # C: what-if overlay
        self._show_what_if = False
        self._wi_stroop:  float = 60.0
        self._wi_flanker: float = 40.0
        self._wi_fa: int = 0
        self._dragging: str | None = None  # "stroop" | "flanker"

    # ── helpers ────────────────────────────────────────────────────

    def _show_synthetic_button(self) -> bool:
        s = self._session
        return s.rt is None and s.stroop is None and s.flanker is None and s.gonogo is None

    def _task_result(self, idx: int) -> TaskResult | None:
        return [self._session.rt, self._session.stroop,
                self._session.flanker, self._session.gonogo][idx]

    def _open_what_if(self) -> None:
        self._show_what_if = True
        s = self._session
        if s.stroop:
            self._wi_stroop = max(0.0, _effect(
                s.stroop.rt_ms, s.stroop.condition, "congruent", "incongruent"))
        if s.flanker:
            self._wi_flanker = max(0.0, _effect(
                s.flanker.rt_ms, s.flanker.condition, "congruent", "incongruent"))
        if s.gonogo:
            self._wi_fa = sum(
                1 for c, ok in zip(s.gonogo.condition, s.gonogo.correct)
                if c == "nogo" and not ok
            )

    def _wi_btn_rect(self) -> pygame.Rect:
        profile_y = _ROW2_Y + _TILE_H + 20
        btn_y = profile_y + 34 + 4 * 26 + 10   # just below the 4 profile lines
        return pygame.Rect(40, btn_y, 320, 28)

    def _fa_btn_rect(self, val: int) -> pygame.Rect:
        return pygame.Rect(self._WI_TRACK_X + val * 52, self._WI_FA_BTN_Y, 44, 32)

    # ── scene protocol ─────────────────────────────────────────────

    def _launch_task(self, idx: int) -> None:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.cognitive_dashboard.info import get_game_info
        from cognitive_data_arcade.games.cognitive_dashboard.mini_tasks import (
            MiniFlankerScene,
            MiniGoNoGoScene,
            MiniRTScene,
            MiniStroopScene,
        )

        s = self._session
        pm, strings = self._pm, self._strings

        def back() -> Scene:
            def make_dash() -> Scene:
                inner = CognitiveDashboardScene(s, strings, pm)
                return PausableGame(inner, get_game_info(strings), make_dash, strings, pm)
            return make_dash()

        scene_factories = [
            lambda: MiniRTScene(s, back),
            lambda: MiniStroopScene(s, back),
            lambda: MiniFlankerScene(s, back),
            lambda: MiniGoNoGoScene(s, back),
        ]

        def make_pausable() -> Scene:
            inner = scene_factories[idx]()
            return PausableGame(inner, get_game_info(strings), make_pausable, strings, pm)

        self._next = make_pausable()
        self._done = True

    def handle_event(self, event: pygame.event.Event) -> None:
        # ── Detail panel open — intercept all input ────────────────
        if self._detail_idx is not None:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._detail_idx = None
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                panel = pygame.Rect(self._DP_X, self._DP_Y, self._DP_W, self._DP_H)
                if not panel.collidepoint(event.pos):
                    self._detail_idx = None
            return

        # ── What-if overlay open ───────────────────────────────────
        if self._show_what_if:
            self._handle_what_if_event(event)
            return

        # ── Normal dashboard events ────────────────────────────────
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self._selected = max(0, self._selected - 1)
            elif event.key == pygame.K_RIGHT:
                self._selected = min(3, self._selected + 1)
            elif event.key == pygame.K_UP:
                self._selected = max(0, self._selected - 2)
            elif event.key == pygame.K_DOWN:
                self._selected = min(3, self._selected + 2)
            elif event.key == pygame.K_RETURN:
                result = self._task_result(self._selected)
                if result is not None:
                    self._detail_idx = self._selected
                else:
                    self._launch_task(self._selected)
            elif event.key == pygame.K_s and self._show_synthetic_button():
                from cognitive_data_arcade.games.cognitive_dashboard.config import generate_synthetic
                synth = generate_synthetic()
                self._session.rt = synth.rt
                self._session.stroop = synth.stroop
                self._session.flanker = synth.flanker
                self._session.gonogo = synth.gonogo
                self._session.synthetic = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._session.is_complete() and self._wi_btn_rect().collidepoint(event.pos):
                self._open_what_if()
                return
            for i in range(4):
                if _tile_rect(i).collidepoint(event.pos):
                    self._selected = i
                    result = self._task_result(i)
                    if result is not None:
                        self._detail_idx = i
                    else:
                        self._launch_task(i)
                    return

    def _handle_what_if_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._show_what_if = False
            self._dragging = None
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            # FA count buttons
            for val in range(3):
                if self._fa_btn_rect(val).collidepoint(pos):
                    self._wi_fa = val
                    return
            # Slider tracks
            for name, slider_y in [("stroop", self._WI_STROOP_Y), ("flanker", self._WI_FLANKER_Y)]:
                track = pygame.Rect(self._WI_TRACK_X, slider_y + 8, self._WI_TRACK_W, 12)
                if track.collidepoint(pos):
                    self._dragging = name
                    self._apply_slider(name, pos[0])
                    return
            # Click outside panel → close
            if not pygame.Rect(self._WI_X, self._WI_Y, self._WI_W, self._WI_H).collidepoint(pos):
                self._show_what_if = False
                self._dragging = None
        elif event.type == pygame.MOUSEMOTION and self._dragging:
            self._apply_slider(self._dragging, event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._dragging = None

    def _apply_slider(self, name: str, mouse_x: int) -> None:
        t = max(0.0, min(1.0, (mouse_x - self._WI_TRACK_X) / self._WI_TRACK_W))
        if name == "stroop":
            self._wi_stroop = t * _WI_STROOP_MAX
        else:
            self._wi_flanker = t * _WI_FLANKER_MAX

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    # ── draw ───────────────────────────────────────────────────────

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        w, h = surface.get_size()

        title = get_font(42).render("Cognitive Dashboard", True, _WHITE)
        surface.blit(title, (40, 46))

        esc_hint = get_font(24).render("ESC = pauza", True, _DIM)
        surface.blit(esc_hint, (w - esc_hint.get_width() - 20, 50))

        for i in range(4):
            self._draw_tile(surface, i)

        if self._session.is_complete():
            self._draw_profile(surface)
        elif self._show_synthetic_button():
            self._draw_synthetic_button(surface, w, h)

        hint = get_font(22).render("strzałki + ENTER = zagraj / szczegóły zadania", True, _DIM)
        surface.blit(hint, (w // 2 - hint.get_width() // 2, h - 34))

        # Overlays (drawn last, on top of everything)
        if self._detail_idx is not None:
            _dim_overlay(surface)
            self._draw_detail_panel(surface, self._detail_idx)
        elif self._show_what_if:
            _dim_overlay(surface)
            self._draw_what_if_panel(surface)

    # ── tile drawing ───────────────────────────────────────────────

    def _draw_tile(self, surface: pygame.Surface, idx: int) -> None:
        rect = _tile_rect(idx)
        color = _TASK_COLORS[idx]
        result = self._task_result(idx)
        selected = idx == self._selected

        if result is not None:
            pygame.draw.rect(surface, color, rect, border_radius=8)
            tc = _BG
            detail_hint = get_font(18).render("klik = szczegóły", True, _BG)
            surface.blit(detail_hint, (rect.right - detail_hint.get_width() - 8, rect.bottom - 22))
        else:
            border_color = color if selected else _DIM
            width = 3 if selected else 2
            pygame.draw.rect(surface, border_color, rect, width, border_radius=8)
            tc = _WHITE if selected else _DIM

        name = get_font(30).render(_TASK_NAMES[idx], True, tc)
        surface.blit(name, (rect.x + 16, rect.y + 14))

        if result is None:
            lbl = get_font(24).render("ENTER = zagraj", True, tc)
            surface.blit(lbl, (rect.x + 16, rect.y + 56))
        else:
            self._draw_tile_metrics(surface, rect, idx, result)

    def _draw_tile_metrics(self, surface: pygame.Surface, rect: pygame.Rect,
                           idx: int, result: TaskResult) -> None:
        font = get_font(24)
        tc = _BG
        y = rect.y + 48

        avg = _avg_rt(result.rt_ms)
        acc = _accuracy(result.correct)
        surface.blit(font.render(f"avg RT: {avg:.0f} ms", True, tc), (rect.x + 16, y))
        y += 28
        surface.blit(font.render(f"trafność: {acc:.0f}%", True, tc), (rect.x + 16, y))
        y += 28

        if idx == 1:
            eff = _effect(result.rt_ms, result.condition, "congruent", "incongruent")
            surface.blit(font.render(f"efekt Stroopa: {eff:+.0f} ms", True, tc), (rect.x + 16, y))
        elif idx == 2:
            eff = _effect(result.rt_ms, result.condition, "congruent", "incongruent")
            surface.blit(font.render(f"efekt Flankera: {eff:+.0f} ms", True, tc), (rect.x + 16, y))
        elif idx == 3:
            fa = sum(1 for c, ok in zip(result.condition, result.correct)
                     if c == "nogo" and not ok)
            surface.blit(font.render(f"false alarms: {fa}", True, tc), (rect.x + 16, y))

    def _draw_profile(self, surface: pygame.Surface) -> None:
        lines = cognitive_profile(self._session)
        profile_y = _ROW2_Y + _TILE_H + 20
        font = get_font(22)
        header = get_font(26).render("Profil poznawczy", True, _ORANGE)
        surface.blit(header, (40, profile_y))
        for i, line in enumerate(lines):
            txt = font.render(line, True, _WHITE)
            surface.blit(txt, (40, profile_y + 34 + i * 26))

        # What-if button below profile
        btn = self._wi_btn_rect()
        pygame.draw.rect(surface, _DIM, btn, 1, border_radius=4)
        lbl = get_font(20).render("Co by było gdyby? ->", True, _ORANGE)
        surface.blit(lbl, (btn.x + 8, btn.y + 5))

    def _draw_synthetic_button(self, surface: pygame.Surface, w: int, h: int) -> None:
        btn_rect = pygame.Rect(w // 2 - 200, h - 110, 400, 44)
        pygame.draw.rect(surface, _DIM, btn_rect, border_radius=6)
        lbl = get_font(24).render("S = wygeneruj dane losowe", True, _WHITE)
        surface.blit(lbl, (btn_rect.centerx - lbl.get_width() // 2,
                           btn_rect.centery - lbl.get_height() // 2))

    # ── Detail panel (A) ───────────────────────────────────────────

    def _draw_detail_panel(self, surface: pygame.Surface, idx: int) -> None:
        result = self._task_result(idx)
        if result is None:
            return

        px, py, pw, ph = self._DP_X, self._DP_Y, self._DP_W, self._DP_H
        pygame.draw.rect(surface, _PANEL, (px, py, pw, ph), border_radius=10)
        pygame.draw.rect(surface, _TASK_COLORS[idx], (px, py, pw, ph), 2, border_radius=10)

        title = get_font(26).render(f"{_TASK_NAMES[idx]} — próba po próbie", True, _WHITE)
        surface.blit(title, (px + 18, py + 14))
        close_hint = get_font(20).render("klik poza = zamknij", True, _DIM)
        surface.blit(close_hint, (px + pw - close_hint.get_width() - 12, py + 18))

        # Chart area
        chart_x = px + 44
        chart_y = py + 58
        chart_w = pw - 88
        chart_h = 240

        valid_rts = [r for r in result.rt_ms if r > 0]
        max_rt = max(valid_rts, default=800.0)
        max_rt = max(max_rt * 1.1, 200.0)   # 10% headroom above tallest bar

        n = len(result.rt_ms)
        slot_w = chart_w // n
        bar_w = max(8, slot_w - 6)

        # Axes
        pygame.draw.line(surface, _DIM,
                         (chart_x, chart_y + chart_h),
                         (chart_x + chart_w, chart_y + chart_h), 1)
        pygame.draw.line(surface, _DIM,
                         (chart_x, chart_y),
                         (chart_x, chart_y + chart_h), 1)

        # Average RT line
        if valid_rts:
            avg = sum(valid_rts) / len(valid_rts)
            avg_y = chart_y + chart_h - int(avg / max_rt * chart_h)
            pygame.draw.line(surface, _ORANGE,
                             (chart_x, avg_y), (chart_x + chart_w, avg_y), 1)
            avg_lbl = get_font(17).render(f"avg {avg:.0f}", True, _ORANGE)
            surface.blit(avg_lbl, (chart_x + chart_w + 4, avg_y - 9))

        color_fn = self._bar_color_fn(idx)

        for i, (rt, cond, ok) in enumerate(
            zip(result.rt_ms, result.condition, result.correct)
        ):
            bx = chart_x + i * slot_w + (slot_w - bar_w) // 2
            color = color_fn(cond, rt, ok)

            if rt <= 0:
                # Stub for miss / correct rejection
                stub_h = 10
                by = chart_y + chart_h - stub_h
                pygame.draw.rect(surface, color, (bx, by, bar_w, stub_h), border_radius=2)
                tag = "CR" if cond == "nogo" else "MISS"
                tag_surf = get_font(14).render(tag, True, color)
                surface.blit(tag_surf, (bx + bar_w // 2 - tag_surf.get_width() // 2, by - 16))
            else:
                bar_h = max(4, int(rt / max_rt * chart_h))
                by = chart_y + chart_h - bar_h
                pygame.draw.rect(surface, color, (bx, by, bar_w, bar_h), border_radius=2)
                if bar_h > 28:
                    val_surf = get_font(13).render(f"{rt:.0f}", True, _PANEL)
                    surface.blit(val_surf,
                                 (bx + bar_w // 2 - val_surf.get_width() // 2, by + 3))

            num = get_font(15).render(str(i + 1), True, _DIM)
            surface.blit(num, (bx + bar_w // 2 - num.get_width() // 2,
                               chart_y + chart_h + 4))

        self._draw_detail_legend(surface, idx, px + 18, py + ph - 44)

    def _bar_color_fn(self, idx: int):
        """Return a callable (cond, rt, ok) -> RGB for bar colouring."""
        if idx == 0:   # RT: correct=blue, timeout=dim
            return lambda cond, rt, ok: _BLUE if ok else _DIM
        elif idx == 1: # Stroop: congruent=blue, incongruent=red
            return lambda cond, rt, ok: _BLUE if cond == "congruent" else _RED
        elif idx == 2: # Flanker: congruent=blue, incongruent=orange
            return lambda cond, rt, ok: _BLUE if cond == "congruent" else (230, 126, 34)
        else:          # GoNoGo: go-hit=green, go-miss=dim, nogo-CR=dim, nogo-FA=red
            def gng(cond, rt, ok):
                if cond == "go":
                    return _GREEN if ok else _DIM
                return _DIM if ok else _RED   # nogo: ok=CR (grey), not ok=FA (red)
            return gng

    def _draw_detail_legend(self, surface: pygame.Surface, idx: int,
                            x: int, y: int) -> None:
        legend: list[tuple[tuple[int, int, int], str]] = []
        if idx == 0:
            legend = [(_BLUE, "trafiony"), (_DIM, "timeout")]
        elif idx == 1:
            legend = [(_BLUE, "zgodny"), (_RED, "niezgodny")]
        elif idx == 2:
            legend = [(_BLUE, "zgodny"), ((230, 126, 34), "niezgodny")]
        else:
            legend = [(_GREEN, "go: trafiony"),
                      (_DIM, "go: timeout / nogo: ok (CR)"),
                      (_RED, "nogo: fałszywy alarm")]
        for i, (color, label) in enumerate(legend):
            lx = x + i * 210
            pygame.draw.rect(surface, color, (lx, y + 5, 12, 12), border_radius=2)
            surf = get_font(17).render(label, True, _DIM)
            surface.blit(surf, (lx + 18, y + 3))

    # ── What-if panel (C) ──────────────────────────────────────────

    def _draw_what_if_panel(self, surface: pygame.Surface) -> None:
        px, py, pw, ph = self._WI_X, self._WI_Y, self._WI_W, self._WI_H
        pygame.draw.rect(surface, _PANEL, (px, py, pw, ph), border_radius=10)
        pygame.draw.rect(surface, _ORANGE, (px, py, pw, ph), 2, border_radius=10)

        title = get_font(28).render("Co by było gdyby?", True, _ORANGE)
        surface.blit(title, (px + 18, py + 14))
        close_hint = get_font(20).render("klik poza = zamknij", True, _DIM)
        surface.blit(close_hint, (px + pw - close_hint.get_width() - 14, py + 18))

        # Real session values for markers
        s = self._session
        real_stroop = (max(0.0, _effect(
            s.stroop.rt_ms, s.stroop.condition, "congruent", "incongruent"))
            if s.stroop else None)
        real_flanker = (max(0.0, _effect(
            s.flanker.rt_ms, s.flanker.condition, "congruent", "incongruent"))
            if s.flanker else None)
        real_fa = (sum(1 for c, ok in zip(s.gonogo.condition, s.gonogo.correct)
                       if c == "nogo" and not ok)
                   if s.gonogo else None)

        # Sliders
        self._draw_slider(surface, "stroop", "Efekt Stroopa:",
                          self._WI_STROOP_Y, self._wi_stroop, _WI_STROOP_MAX, real_stroop)
        self._draw_slider(surface, "flanker", "Efekt Flankera:",
                          self._WI_FLANKER_Y, self._wi_flanker, _WI_FLANKER_MAX, real_flanker)

        # GoNoGo FA — label on its own line, buttons on the row below
        fa_lbl = get_font(22).render("Fałszywe alarmy GoNoGo:", True, _WHITE)
        surface.blit(fa_lbl, (px + 18, self._WI_FA_Y + 6))
        for val in range(3):
            btn = self._fa_btn_rect(val)
            selected = val == self._wi_fa
            pygame.draw.rect(surface, _ORANGE if selected else _DIM, btn,
                             0 if selected else 1, border_radius=4)
            num = get_font(22).render(str(val), True,
                                      _PANEL if selected else _WHITE)
            surface.blit(num, (btn.centerx - num.get_width() // 2,
                               btn.centery - num.get_height() // 2))
        if real_fa is not None:
            real_fa_lbl = get_font(17).render(f"Twój wynik: {real_fa}", True, _ORANGE)
            surface.blit(real_fa_lbl,
                         (self._WI_TRACK_X + 3 * 52 + 10, self._WI_FA_BTN_Y + 8))

        # Separator
        sep_y = self._WI_FA_BTN_Y + 42
        pygame.draw.line(surface, _DIM, (px + 18, sep_y), (px + pw - 18, sep_y), 1)

        # Hypothetical profile
        prof_y = sep_y + 10
        phdr = get_font(22).render("Hipotetyczny profil:", True, _ORANGE)
        surface.blit(phdr, (px + 18, prof_y))
        for i, line in enumerate(
            self._hypothetical_profile(self._wi_stroop, self._wi_flanker, self._wi_fa)
        ):
            txt = get_font(20).render(line, True, _WHITE)
            surface.blit(txt, (px + 18, prof_y + 28 + i * 24))

    def _draw_slider(
        self, surface: pygame.Surface, name: str, label: str,
        y: int, value: float, max_val: float, real_val: float | None,
    ) -> None:
        lbl = get_font(22).render(label, True, _WHITE)
        surface.blit(lbl, (self._WI_X + 18, y + 4))

        tx, tw = self._WI_TRACK_X, self._WI_TRACK_W

        # Track background
        pygame.draw.rect(surface, _DIM, (tx, y + 10, tw, 6), border_radius=3)

        # Filled portion
        fill_w = int(value / max_val * tw)
        if fill_w > 0:
            pygame.draw.rect(surface, _BLUE, (tx, y + 10, fill_w, 6), border_radius=3)

        # Real-value marker (orange vertical bar)
        if real_val is not None:
            mx = tx + int(real_val / max_val * tw)
            pygame.draw.line(surface, _ORANGE, (mx, y - 4), (mx, y + 26), 3)
            rl = get_font(16).render(f"Twój wynik: {real_val:.0f} ms", True, _ORANGE)
            rlx = max(tx, min(mx - rl.get_width() // 2, tx + tw - rl.get_width()))
            surface.blit(rl, (rlx, y + 28))

        # Thumb circle at current value
        thumb_x = tx + fill_w
        pygame.draw.circle(surface, _WHITE, (thumb_x, y + 13), 9)

        # Current value label to the right
        val_lbl = get_font(22).render(f"{value:.0f} ms", True, _WHITE)
        surface.blit(val_lbl, (tx + tw + 14, y + 2))

    @staticmethod
    def _hypothetical_profile(stroop_eff: float, flanker_eff: float, fa: int) -> list[str]:
        lines: list[str] = []
        if stroop_eff < 40:
            lines.append("Odporność na interferencję: silna (<40 ms)")
        elif stroop_eff <= 80:
            lines.append(f"Odporność na interferencję: przeciętna ({stroop_eff:.0f} ms)")
        else:
            lines.append(f"Efekt Stroopa wyraźny — duża interferencja ({stroop_eff:.0f} ms)")

        if flanker_eff < 25:
            lines.append("Selektywna uwaga: bardzo dobra (<25 ms)")
        elif flanker_eff <= 60:
            lines.append(f"Selektywna uwaga: przeciętna ({flanker_eff:.0f} ms)")
        else:
            lines.append(f"Dystraktorzy spowalniają reakcję ({flanker_eff:.0f} ms)")

        if fa == 0:
            lines.append("Hamowanie impulsów: bezbłędne")
        elif fa == 1:
            lines.append("Hamowanie impulsów: dobre (drobne błędy)")
        else:
            lines.append("Tendencja do impulsywności — trudność z hamowaniem")
        return lines
