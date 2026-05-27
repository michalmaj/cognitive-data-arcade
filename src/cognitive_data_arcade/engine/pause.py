from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import pygame

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import ProfileManager

_BG_PANEL = (18, 18, 42)
_BORDER = (42, 42, 80)
_WHITE = (240, 240, 240)
_HIGHLIGHT = (243, 156, 18)
_DIM = (100, 100, 150)
_KEY_COLOR = (39, 174, 96)

_MENU_ITEMS = 4


@dataclass(frozen=True)
class GameInfo:
    title: str
    description_lines: list[str]
    key_bindings: list[tuple[str, str]]


class PausableGame(Scene):
    def __init__(
        self,
        inner: Scene,
        game_info: GameInfo,
        restart_factory: Callable[[], Scene],
        strings: Strings,
        profile_manager: ProfileManager,
    ) -> None:
        self._inner = inner
        self._game_info = game_info
        self._restart_factory = restart_factory
        self._strings = strings
        self._pm = profile_manager
        self._paused = False
        self._show_keyref = False
        self._selected = 0
        self._sub_scene: Scene | None = None
        self._done = False
        self._next: Scene | None = None
        pygame.font.init()
        self._font_title = pygame.font.SysFont(None, 52)
        self._font_item = pygame.font.SysFont(None, 34)
        self._font_key = pygame.font.SysFont(None, 30)
        self._font_hint = pygame.font.SysFont(None, 26)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if self._sub_scene is not None:
            self._sub_scene.handle_event(event)
            if self._sub_scene.is_done():
                self._sub_scene = None
                self._paused = False
            return
        if not self._paused:
            if event.key == pygame.K_ESCAPE:
                self._paused = True
                self._show_keyref = False
                self._selected = 0
            else:
                self._inner.handle_event(event)
        elif self._show_keyref:
            if event.key == pygame.K_ESCAPE:
                self._show_keyref = False
        else:
            if event.key == pygame.K_ESCAPE:
                self._paused = False
            elif event.key == pygame.K_UP:
                self._selected = max(0, self._selected - 1)
            elif event.key == pygame.K_DOWN:
                self._selected = min(_MENU_ITEMS - 1, self._selected + 1)
            elif event.key == pygame.K_RETURN:
                self._activate()

    def update(self, dt_ms: float) -> None:
        if self._sub_scene is not None:
            self._sub_scene.update(dt_ms)
            return
        if not self._paused:
            self._inner.update(dt_ms)
        if self._inner.is_done() and not self._done:
            self._next = self._inner.next_scene()
            self._done = True

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    def draw(self, surface: pygame.Surface) -> None:
        if self._sub_scene is not None:
            self._sub_scene.draw(surface)
            return
        self._inner.draw(surface)
        if self._paused:
            self._draw_dim(surface)
            if self._show_keyref:
                self._draw_keyref(surface)
            else:
                self._draw_pause_menu(surface)

    def _activate(self) -> None:
        if self._selected == 0:
            self._next = self._restart_factory()
            self._done = True
        elif self._selected == 1:
            from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

            self._sub_scene = HowToPlayScene(
                self._game_info, self._strings, back_scene=None
            )
        elif self._selected == 2:
            self._show_keyref = True
        elif self._selected == 3:
            from cognitive_data_arcade.ui.menu import LessonMenuScene

            self._next = LessonMenuScene(self._pm, self._strings)
            self._done = True

    def _draw_dim(self, surface: pygame.Surface) -> None:
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

    def _draw_pause_menu(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        panel_w, panel_h = 340, 260
        px = (w - panel_w) // 2
        py = (h - panel_h) // 2
        pygame.draw.rect(
            surface, _BG_PANEL, (px, py, panel_w, panel_h), border_radius=8
        )
        pygame.draw.rect(
            surface, _BORDER, (px, py, panel_w, panel_h), 1, border_radius=8
        )
        title = self._font_title.render(self._strings.pause_title, True, _WHITE)
        surface.blit(title, (px + panel_w // 2 - title.get_width() // 2, py + 12))
        labels = [
            self._strings.pause_restart,
            self._strings.pause_how_to_play,
            self._strings.pause_keyref,
            self._strings.pause_quit,
        ]
        item_y = py + 72
        for i, label in enumerate(labels):
            color = _HIGHLIGHT if i == self._selected else _DIM
            surf = self._font_item.render(label, True, color)
            surface.blit(surf, (px + panel_w // 2 - surf.get_width() // 2, item_y))
            item_y += 40
        hint = self._font_hint.render(self._strings.pause_hint_resume, True, _DIM)
        surface.blit(
            hint, (px + panel_w // 2 - hint.get_width() // 2, py + panel_h - 28)
        )

    def _draw_keyref(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        n = len(self._game_info.key_bindings)
        panel_w = 400
        panel_h = 56 + n * 36 + 40
        px = (w - panel_w) // 2
        py = (h - panel_h) // 2
        pygame.draw.rect(
            surface, _BG_PANEL, (px, py, panel_w, panel_h), border_radius=8
        )
        pygame.draw.rect(
            surface, _BORDER, (px, py, panel_w, panel_h), 1, border_radius=8
        )
        ky = py + 16
        for key, desc in self._game_info.key_bindings:
            key_surf = self._font_key.render(key, True, _KEY_COLOR)
            surface.blit(key_surf, (px + 24, ky))
            desc_surf = self._font_key.render(desc, True, _WHITE)
            surface.blit(desc_surf, (px + 130, ky))
            ky += 36
        hint = self._font_hint.render(self._strings.pause_hint_esc_back, True, _DIM)
        surface.blit(
            hint, (px + panel_w // 2 - hint.get_width() // 2, py + panel_h - 28)
        )
