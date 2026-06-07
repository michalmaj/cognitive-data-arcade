from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import pygame

from cognitive_data_arcade.engine import audio
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import ProfileManager

_BG_PANEL = (18, 18, 42)
_BORDER = (42, 42, 80)
_WHITE = (240, 240, 240)
_HIGHLIGHT = (243, 156, 18)
_DIM = (100, 100, 150)
_KEY_COLOR = (39, 174, 96)

_MENU_ITEMS = 5


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
        audio.play_music("game")
        self._font_title = get_font(52)
        self._font_item = get_font(34)
        self._font_key = get_font(30)
        self._font_hint = get_font(26)

    def _update_pause_selected(self, pos: tuple[int, int]) -> None:
        from cognitive_data_arcade.engine.mouse import hit
        surf = pygame.display.get_surface()
        if surf is None:
            return
        w, h = surf.get_size()
        panel_w, panel_h = 340, 300
        px = (w - panel_w) // 2
        py = (h - panel_h) // 2
        item_y = py + 72
        for i in range(_MENU_ITEMS):
            rect = pygame.Rect(px, item_y, panel_w, 36)
            if hit(rect, pos):
                self._selected = i
                break
            item_y += 40

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._sub_scene is not None:
            self._sub_scene.handle_event(event)
            if self._sub_scene.is_done():
                self._sub_scene = None
            return
        if not self._paused:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._paused = True
                self._show_keyref = False
                self._selected = 0
                audio.play_sfx("pause")
            else:
                self._inner.handle_event(event)
            return
        if self._show_keyref:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._show_keyref = False
            return
        # pause menu active
        if event.type == pygame.MOUSEMOTION:
            self._update_pause_selected(event.pos)
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._update_pause_selected(event.pos)
            audio.play_sfx("select")
            self._activate()
            return
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self._paused = False
        elif event.key == pygame.K_UP:
            self._selected = max(0, self._selected - 1)
        elif event.key == pygame.K_DOWN:
            self._selected = min(_MENU_ITEMS - 1, self._selected + 1)
        elif event.key == pygame.K_RETURN:
            audio.play_sfx("select")
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
            from cognitive_data_arcade.ui.options_scene import OptionsScene

            self._sub_scene = OptionsScene(self._pm, self._strings, back_scene=None)
        elif self._selected == 4:
            from cognitive_data_arcade.ui.menu import LessonMenuScene

            self._next = LessonMenuScene(self._pm, self._strings)
            self._done = True

    def _draw_dim(self, surface: pygame.Surface) -> None:
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

    def _draw_pause_menu(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        panel_w, panel_h = 340, 300
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
            self._strings.pause_options,
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
        bindings = self._game_info.key_bindings
        n = len(bindings)
        max_key_w = max(
            (self._font_key.size(k)[0] for k, _ in bindings), default=80
        )
        key_col_w = max_key_w + 16
        panel_w = max(400, 24 + key_col_w + 200 + 24)
        panel_h = 56 + n * 36 + 40
        px = (w - panel_w) // 2
        py = (h - panel_h) // 2
        pygame.draw.rect(
            surface, _BG_PANEL, (px, py, panel_w, panel_h), border_radius=8
        )
        pygame.draw.rect(
            surface, _BORDER, (px, py, panel_w, panel_h), 1, border_radius=8
        )
        desc_x = px + 24 + key_col_w
        ky = py + 16
        for key, desc in bindings:
            key_surf = self._font_key.render(key, True, _KEY_COLOR)
            surface.blit(key_surf, (px + 24, ky))
            desc_surf = self._font_key.render(desc, True, _WHITE)
            surface.blit(desc_surf, (desc_x, ky))
            ky += 36
        hint = self._font_hint.render(self._strings.pause_hint_esc_back, True, _DIM)
        surface.blit(
            hint, (px + panel_w // 2 - hint.get_width() // 2, py + panel_h - 28)
        )
