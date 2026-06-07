# src/cognitive_data_arcade/games/eda/ui_controls.py
from __future__ import annotations

from dataclasses import dataclass

import pygame

from cognitive_data_arcade.engine.fonts import get_font

_TRACK = (42, 42, 80)
_DIM = (120, 120, 160)
_ACTIVE = (243, 156, 18)
_WHITE = (240, 240, 240)
_BG_INPUT = (26, 26, 46)

_THUMB_R = 8
_TRACK_H = 4
_SLIDER_GAP = 56
_SLIDER_W = 280


@dataclass
class SliderSpec:
    label: str
    min_val: int
    max_val: int
    default: int
    step: int


class Slider:
    def __init__(self, spec: SliderSpec, x: int, y: int, w: int = _SLIDER_W) -> None:
        self._spec = spec
        self._x = x
        self._y = y
        self._w = w
        self._value = spec.default
        self._dragging = False
        self.focused: bool = False

    @property
    def value(self) -> int:
        return self._value

    def _thumb_x(self) -> int:
        ratio = (self._value - self._spec.min_val) / max(1, self._spec.max_val - self._spec.min_val)
        return self._x + round(ratio * self._w)

    def _track_y(self) -> int:
        return self._y + 20

    def _set_from_pixel(self, px: int) -> None:
        ratio = (px - self._x) / max(1, self._w)
        steps = round(ratio * (self._spec.max_val - self._spec.min_val) / self._spec.step)
        raw = self._spec.min_val + steps * self._spec.step
        self._value = max(self._spec.min_val, min(self._spec.max_val, raw))

    def handle_mousedown(self, pos: tuple[int, int]) -> bool:
        px, py = pos
        ty = self._track_y()
        if self._x <= px <= self._x + self._w and abs(py - ty) <= _THUMB_R + 6:
            self._set_from_pixel(px)
            self._dragging = True
            self.focused = True
            return True
        return False

    def handle_mousemotion(self, pos: tuple[int, int], buttons: tuple) -> bool:
        if not buttons[0]:
            self._dragging = False
            return False
        if not self._dragging:
            return False
        old = self._value
        self._set_from_pixel(pos[0])
        return self._value != old

    def handle_keydown(self, key: int) -> bool:
        if key == pygame.K_LEFT:
            self._value = max(self._spec.min_val, self._value - self._spec.step)
            return True
        if key == pygame.K_RIGHT:
            self._value = min(self._spec.max_val, self._value + self._spec.step)
            return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        font_lbl = get_font(17)
        font_val = get_font(20)
        surface.blit(font_lbl.render(self._spec.label, True, _DIM), (self._x, self._y))
        ty = self._track_y()
        pygame.draw.rect(surface, _TRACK,
                         (self._x, ty - _TRACK_H // 2, self._w, _TRACK_H), border_radius=2)
        tx = self._thumb_x()
        filled = max(0, tx - self._x)
        if filled > 0:
            fill_color = _ACTIVE if self.focused else _DIM
            pygame.draw.rect(surface, fill_color,
                             (self._x, ty - _TRACK_H // 2, filled, _TRACK_H), border_radius=2)
        thumb_color = _ACTIVE if self.focused else _DIM
        pygame.draw.circle(surface, thumb_color, (tx, ty), _THUMB_R)
        val_str = f"{self._value}%" if self._spec.label.startswith("%") else str(self._value)
        surface.blit(font_val.render(val_str, True, _WHITE), (self._x + self._w + 10, ty - 10))


_SLIDER_SPECS = [
    SliderSpec("UCZESTNICY (N)", 5, 100, 20, 1),
    SliderSpec("BAZOWY RT (ms)", 300, 600, 400, 10),
    SliderSpec("ROZNICA EFEKTU (ms)", 0, 200, 40, 10),
    SliderSpec("SZUM / SD (ms)", 10, 200, 80, 10),
    SliderSpec("% OUTLIEROW", 0, 20, 5, 1),
]


class SliderGroup:
    def __init__(self, x: int = 30, y0: int = 80) -> None:
        self._sliders = [
            Slider(spec, x, y0 + i * _SLIDER_GAP)
            for i, spec in enumerate(_SLIDER_SPECS)
        ]
        self._focused_idx = 0
        self._sliders[0].focused = True

    @property
    def params(self) -> dict:
        s = self._sliders
        return {
            "n": s[0].value,
            "baseline_ms": s[1].value,
            "effect_ms": s[2].value,
            "noise_sd": s[3].value,
            "outlier_pct": s[4].value / 100.0,
        }

    def _set_focus(self, idx: int) -> None:
        self._sliders[self._focused_idx].focused = False
        self._focused_idx = idx
        self._sliders[idx].focused = True

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, s in enumerate(self._sliders):
                if s.handle_mousedown(event.pos):
                    self._set_focus(i)
                    return True
        elif event.type == pygame.MOUSEMOTION:
            return self._sliders[self._focused_idx].handle_mousemotion(event.pos, event.buttons)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                n = len(self._sliders)
                mods = pygame.key.get_mods()
                delta = -1 if (mods & pygame.KMOD_SHIFT) else 1
                self._set_focus((self._focused_idx + delta) % n)
                return True
            return self._sliders[self._focused_idx].handle_keydown(event.key)
        return False

    def draw(self, surface: pygame.Surface) -> None:
        for s in self._sliders:
            s.draw(surface)


class ControlPanel:
    def __init__(self) -> None:
        self._sliders = SliderGroup(x=30, y0=80)
        self._hyp_text: str = ""
        self._hyp_rect = pygame.Rect(30, 380, 200, 36)
        self._btn_rect = pygame.Rect(30, 432, 200, 40)
        self._hyp_focused: bool = False
        self._font = get_font(22)

    def get_params(self) -> dict:
        return self._sliders.params

    def get_hypothesis_threshold(self) -> int | None:
        return int(self._hyp_text) if self._hyp_text else None

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._btn_rect.collidepoint(event.pos):
                return "generate"
            if self._hyp_rect.collidepoint(event.pos):
                self._hyp_focused = True
                return None
            self._hyp_focused = False
            self._sliders.handle_event(event)
            return None
        if event.type == pygame.MOUSEMOTION:
            self._sliders.handle_event(event)
            return None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "generate"
            if self._hyp_focused:
                if event.key == pygame.K_BACKSPACE:
                    self._hyp_text = self._hyp_text[:-1]
                elif event.unicode.isdigit() and len(self._hyp_text) < 5:
                    self._hyp_text += event.unicode
                return None
            self._sliders.handle_event(event)
            return None
        return None

    def draw(self, surface: pygame.Surface) -> None:
        self._sliders.draw(surface)
        lbl = get_font(18).render("Hipoteza: roznica >=", True, _DIM)
        surface.blit(lbl, (30, 360))
        border = _ACTIVE if self._hyp_focused else _TRACK
        pygame.draw.rect(surface, _BG_INPUT, self._hyp_rect, border_radius=4)
        pygame.draw.rect(surface, border, self._hyp_rect, 2, border_radius=4)
        if self._hyp_text:
            txt = self._font.render(self._hyp_text + " ms", True, _WHITE)
        else:
            txt = self._font.render("___ ms", True, _DIM)
        surface.blit(txt, (self._hyp_rect.x + 8, self._hyp_rect.y + 6))
        pygame.draw.rect(surface, _ACTIVE, self._btn_rect, border_radius=6)
        btn_lbl = self._font.render("GENERUJ", True, (15, 15, 35))
        surface.blit(btn_lbl, btn_lbl.get_rect(center=self._btn_rect.center))
