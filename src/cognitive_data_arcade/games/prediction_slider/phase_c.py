# src/cognitive_data_arcade/games/prediction_slider/phase_c.py
from __future__ import annotations

import numpy as np
import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.prediction_slider.simulator import fit_line

_BG     = (15,  15,  35)
_PANEL  = (18,  18,  42)
_WHITE  = (240, 240, 240)
_DIM    = (120, 120, 160)
_ORANGE = (243, 156,  18)
_GREEN  = ( 39, 174,  96)
_RED    = (231,  76,  60)
_GRAY   = ( 80,  80, 100)
_BLUE   = ( 52, 152, 219)

_LEFT_W   = 300
_AREA_H   = 672
_AREA_W   = 1024
_CANVAS_X = _LEFT_W          # 300
_CANVAS_W = _AREA_W - _LEFT_W  # 724
_PAD      = 50

_PLOT_LEFT  = _CANVAS_X + _PAD    # 350
_PLOT_RIGHT = _AREA_W - _PAD      # 974
_PLOT_TOP   = _PAD                # 50
_PLOT_BOT   = _AREA_H - _PAD     # 622

_X_MIN, _X_MAX = -0.5, 11.0
_Y_MIN, _Y_MAX = -1.0, 13.0


def _d2p(xd: float, yd: float) -> tuple[int, int]:
    rx = (xd - _X_MIN) / (_X_MAX - _X_MIN)
    ry = (yd - _Y_MIN) / (_Y_MAX - _Y_MIN)
    px = _PLOT_LEFT + int(rx * (_PLOT_RIGHT - _PLOT_LEFT))
    py = _PLOT_BOT  - int(ry * (_PLOT_BOT  - _PLOT_TOP))
    return px, py


def _p2d(px: int, py: int) -> tuple[float, float]:
    rx = (px - _PLOT_LEFT) / max(1, _PLOT_RIGHT - _PLOT_LEFT)
    ry = (_PLOT_BOT - py)  / max(1, _PLOT_BOT  - _PLOT_TOP)
    return _X_MIN + rx * (_X_MAX - _X_MIN), _Y_MIN + ry * (_Y_MAX - _Y_MIN)


def _draw_dashed_line(surface, color, p0, p1, width=1, dash=10, gap=6):
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    length = max(1.0, (dx ** 2 + dy ** 2) ** 0.5)
    nx, ny = dx / length, dy / length
    d, drawing = 0.0, True
    while d < length:
        seg = min(dash if drawing else gap, length - d)
        if drawing:
            xa, ya = int(p0[0] + nx * d), int(p0[1] + ny * d)
            xb, yb = int(p0[0] + nx * (d + seg)), int(p0[1] + ny * (d + seg))
            pygame.draw.line(surface, color, (xa, ya), (xb, yb), width)
        d += seg
        drawing = not drawing


def _draw_regression_line(surface, slope, intercept, color, width, dashed=False):
    p0 = _d2p(_X_MIN, slope * _X_MIN + intercept)
    p1 = _d2p(_X_MAX, slope * _X_MAX + intercept)
    if dashed:
        _draw_dashed_line(surface, color, p0, p1, width)
    else:
        pygame.draw.line(surface, color, p0, p1, width)


class PhaseCScene(Scene):
    def __init__(self) -> None:
        self._done = False
        rng = np.random.default_rng(42)
        self._x_base = np.linspace(0.0, 10.0, 20)
        self._y_base = 0.8 * self._x_base + 2.0 + rng.normal(0, 0.5, 20)
        bs, bi, br2, _ = fit_line(self._x_base, self._y_base)
        self._base_slope = bs
        self._base_intercept = bi
        self._base_r2 = br2
        self._out_x = 5.0
        self._out_y = 6.0
        self._dragging = False
        self._show_baseline = True

    def _all_xy(self) -> tuple[np.ndarray, np.ndarray]:
        x = np.append(self._x_base, self._out_x)
        y = np.append(self._y_base, self._out_y)
        return x, y

    def _current_fit(self) -> tuple[float, float, float]:
        x, y = self._all_xy()
        slope, intercept, r2, _ = fit_line(x, y)
        return slope, intercept, r2

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            ox, oy = _d2p(self._out_x, self._out_y)
            px, py = event.pos
            if (px - ox) ** 2 + (py - oy) ** 2 <= 14 ** 2:
                self._dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._dragging = False
        elif event.type == pygame.MOUSEMOTION and self._dragging:
            xd, yd = _p2d(event.pos[0], event.pos[1])
            self._out_x = float(np.clip(xd, _X_MIN + 0.1, _X_MAX - 0.1))
            self._out_y = float(np.clip(yd, _Y_MIN + 0.1, _Y_MAX - 0.1))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self._show_baseline = not self._show_baseline

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _LEFT_W, _AREA_H))
        cur_slope, cur_intercept, cur_r2 = self._current_fit()
        self._draw_stats(surface, cur_slope, cur_r2)
        self._draw_canvas(surface, cur_slope, cur_intercept)

    def _draw_stats(self, surface, cur_slope, cur_r2) -> None:
        font_sm = get_font(14)
        font_md = get_font(17)
        font_hd = get_font(20)
        surface.blit(font_hd.render("Wpływ outlieru", True, _ORANGE), (12, 16))
        y = 60
        surface.blit(font_sm.render("Linia bazowa (bez outlieru):", True, _DIM), (12, y))
        y += 18
        surface.blit(font_sm.render("Slope:", True, _DIM), (12, y))
        surface.blit(font_md.render(f"{self._base_slope:.3f}", True, _GRAY), (12, y + 14))
        y += 36
        surface.blit(font_sm.render("R²:", True, _DIM), (12, y))
        surface.blit(font_md.render(f"{self._base_r2:.3f}", True, _GRAY), (12, y + 14))
        y += 52
        surface.blit(font_sm.render("Linia z outlierem:", True, _DIM), (12, y))
        y += 18
        d_slope = abs(cur_slope - self._base_slope)
        slope_col = _ORANGE if d_slope > 0.3 else _WHITE
        surface.blit(font_sm.render("Slope:", True, _DIM), (12, y))
        surface.blit(font_md.render(f"{cur_slope:.3f}", True, slope_col), (12, y + 14))
        y += 36
        dr2 = self._base_r2 - cur_r2
        r2_col = _RED if dr2 > 0.2 else _WHITE
        surface.blit(font_sm.render("R²:", True, _DIM), (12, y))
        surface.blit(font_md.render(f"{cur_r2:.3f}", True, r2_col), (12, y + 14))
        y += 52
        surface.blit(font_sm.render("Wpływ outlieru:", True, _DIM), (12, y))
        y += 18
        surface.blit(font_sm.render("deltaSlope:", True, _DIM), (12, y))
        surface.blit(font_md.render(f"{d_slope:.3f}", True, slope_col), (12, y + 14))
        y += 52
        if self._out_x < 0.0 or self._out_x > 10.0:
            warn = get_font(13).render("Punkt poza danymi --", True, _RED)
            warn2 = get_font(13).render("duża dźwignia!", True, _RED)
            surface.blit(warn, (8, y))
            surface.blit(warn2, (8, y + 16))
            y += 38
        hint = get_font(12).render("PPM = pokaż/ukryj linię bazową", True, _DIM)
        surface.blit(hint, (8, _AREA_H - 20))

    def _draw_canvas(self, surface, cur_slope, cur_intercept) -> None:
        pygame.draw.rect(surface, (12, 12, 30), (_CANVAS_X, 0, _CANVAS_W, _AREA_H))
        # axes ticks (light grid lines)
        for xv in range(0, 11, 2):
            p = _d2p(xv, _Y_MIN)
            pygame.draw.line(surface, (30, 30, 60), p, _d2p(xv, _Y_MAX), 1)
        for yv in range(0, 14, 2):
            p = _d2p(_X_MIN, yv)
            pygame.draw.line(surface, (30, 30, 60), p, _d2p(_X_MAX, yv), 1)
        # baseline line
        if self._show_baseline:
            _draw_regression_line(surface, self._base_slope, self._base_intercept,
                                   _GRAY, 2, dashed=True)
        # current line
        _draw_regression_line(surface, cur_slope, cur_intercept, _RED, 2)
        # base points
        for xv, yv in zip(self._x_base, self._y_base):
            px, py = _d2p(xv, yv)
            pygame.draw.circle(surface, _BLUE, (px, py), 5)
        # outlier point
        ox, oy = _d2p(self._out_x, self._out_y)
        pygame.draw.circle(surface, _RED, (ox, oy), 10)
        pygame.draw.circle(surface, _WHITE, (ox, oy), 10, 2)
        # hint
        hint = get_font(12).render("Przeciągnij czerwony punkt", True, _DIM)
        surface.blit(hint, (_CANVAS_X + 8, _AREA_H - 20))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return None
