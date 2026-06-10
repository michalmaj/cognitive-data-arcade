from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.cognitive_dashboard.profile import cognitive_profile
from cognitive_data_arcade.games.cognitive_dashboard.session import DashboardSession, TaskResult
from cognitive_data_arcade.profile.manager import ProfileManager

_BG      = (26, 26, 46)
_WHITE   = (240, 240, 240)
_DIM     = (100, 100, 150)
_ORANGE  = (243, 156, 18)
_W, _H   = 1024, 768

_TASK_COLORS = [
    (52, 152, 219),   # RT - blue
    (231, 76, 60),    # Stroop - red
    (230, 126, 34),   # Flanker - orange
    (39, 174, 96),    # GoNoGo - green
]
_TASK_NAMES = ["RT Lab", "Stroop", "Flanker", "Go/No-Go"]

_TILE_W, _TILE_H = 420, 190
_TILE_GAP = 40
_TILES_LEFT = (_W - 2 * _TILE_W - _TILE_GAP) // 2
_ROW1_Y = 130
_ROW2_Y = _ROW1_Y + _TILE_H + 24


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


class CognitiveDashboardScene(Scene):
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

    def _show_synthetic_button(self) -> bool:
        s = self._session
        return s.rt is None and s.stroop is None and s.flanker is None and s.gonogo is None

    def _task_result(self, idx: int) -> TaskResult | None:
        return [self._session.rt, self._session.stroop,
                self._session.flanker, self._session.gonogo][idx]

    def _launch_task(self, idx: int) -> None:
        s = self._session
        pm, strings = self._pm, self._strings

        def back() -> Scene:
            return CognitiveDashboardScene(s, strings, pm)

        from cognitive_data_arcade.games.cognitive_dashboard.mini_tasks import (
            MiniFlankerScene,
            MiniGoNoGoScene,
            MiniRTScene,
            MiniStroopScene,
        )
        factories = [
            lambda: MiniRTScene(s, back),
            lambda: MiniStroopScene(s, back),
            lambda: MiniFlankerScene(s, back),
            lambda: MiniGoNoGoScene(s, back),
        ]
        self._next = factories[idx]()
        self._done = True

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from cognitive_data_arcade.ui.menu import LessonMenuScene
                self._next = LessonMenuScene(self._pm, self._strings)
                self._done = True
            elif event.key == pygame.K_LEFT:
                self._selected = max(0, self._selected - 1)
            elif event.key == pygame.K_RIGHT:
                self._selected = min(3, self._selected + 1)
            elif event.key == pygame.K_UP:
                self._selected = max(0, self._selected - 2)
            elif event.key == pygame.K_DOWN:
                self._selected = min(3, self._selected + 2)
            elif event.key == pygame.K_RETURN:
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
            for i in range(4):
                if _tile_rect(i).collidepoint(event.pos):
                    self._selected = i
                    self._launch_task(i)
                    return

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        w, h = surface.get_size()

        title = get_font(42).render("Cognitive Dashboard", True, _WHITE)
        surface.blit(title, (40, 46))

        esc_hint = get_font(24).render("ESC = menu", True, _DIM)
        surface.blit(esc_hint, (w - esc_hint.get_width() - 20, 50))

        for i in range(4):
            self._draw_tile(surface, i)

        if self._session.is_complete():
            self._draw_profile(surface)
        elif self._show_synthetic_button():
            self._draw_synthetic_button(surface, w, h)

        hint = get_font(22).render("strzalki + ENTER = zagraj zadanie", True, _DIM)
        surface.blit(hint, (w // 2 - hint.get_width() // 2, h - 34))

    def _draw_tile(self, surface: pygame.Surface, idx: int) -> None:
        rect = _tile_rect(idx)
        color = _TASK_COLORS[idx]
        result = self._task_result(idx)
        selected = idx == self._selected

        if result is not None:
            pygame.draw.rect(surface, color, rect, border_radius=8)
            tc = _BG
        else:
            border_color = color if selected else _DIM
            pygame.draw.rect(surface, border_color, rect, 2 if not selected else 3, border_radius=8)
            tc = _WHITE if selected else _DIM

        name = get_font(30).render(_TASK_NAMES[idx], True, tc)
        surface.blit(name, (rect.x + 16, rect.y + 14))

        if result is None:
            lbl = get_font(24).render("ENTER = zagraj", True, tc)
            surface.blit(lbl, (rect.x + 16, rect.y + 56))
        else:
            self._draw_tile_metrics(surface, rect, idx, result)

    def _draw_tile_metrics(self, surface: pygame.Surface, rect: pygame.Rect, idx: int, result: TaskResult) -> None:
        font = get_font(24)
        tc = _BG
        y = rect.y + 48

        avg = _avg_rt(result.rt_ms)
        acc = _accuracy(result.correct)
        surface.blit(font.render(f"avg RT: {avg:.0f} ms", True, tc), (rect.x + 16, y))
        y += 28
        surface.blit(font.render(f"trafnosc: {acc:.0f}%", True, tc), (rect.x + 16, y))
        y += 28

        if idx == 1:  # Stroop
            eff = _effect(result.rt_ms, result.condition, "congruent", "incongruent")
            surface.blit(font.render(f"efekt Stroopa: {eff:+.0f} ms", True, tc), (rect.x + 16, y))
        elif idx == 2:  # Flanker
            eff = _effect(result.rt_ms, result.condition, "congruent", "incongruent")
            surface.blit(font.render(f"efekt Flankera: {eff:+.0f} ms", True, tc), (rect.x + 16, y))
        elif idx == 3:  # GoNoGo
            fa = sum(1 for c, ok in zip(result.condition, result.correct) if c == "nogo" and not ok)
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

    def _draw_synthetic_button(self, surface: pygame.Surface, w: int, h: int) -> None:
        btn_rect = pygame.Rect(w // 2 - 200, h - 110, 400, 44)
        pygame.draw.rect(surface, _DIM, btn_rect, border_radius=6)
        lbl = get_font(24).render("S = wygeneruj dane losowe", True, _WHITE)
        surface.blit(lbl, (btn_rect.centerx - lbl.get_width() // 2,
                           btn_rect.centery - lbl.get_height() // 2))
