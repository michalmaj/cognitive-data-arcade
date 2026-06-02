from __future__ import annotations

import pygame

from cognitive_data_arcade.engine import audio
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import ProfileManager

_BG = (26, 26, 46)
_WHITE = (240, 240, 240)
_ORANGE = (243, 156, 18)
_DIM = (100, 100, 150)
_GREEN = (39, 174, 96)
_GRAY = (50, 50, 80)
_STEP = 0.05


class OptionsScene(Scene):
    def __init__(
        self,
        pm: ProfileManager,
        strings: Strings,
        back_scene: Scene | None,
    ) -> None:
        self._pm = pm
        self._strings = strings
        self._back = back_scene
        self._done = False
        profile = pm.load()
        self._music_enabled: bool = profile.music_enabled
        self._sfx_enabled: bool = profile.sfx_enabled
        self._music_vol: float = profile.music_volume
        self._sfx_vol: float = profile.sfx_volume
        self._focused: int = 0  # 0=music row, 1=sfx row
        pygame.font.init()
        self._font_title = pygame.font.SysFont(None, 52)
        self._font_item = pygame.font.SysFont(None, 36)
        self._font_hint = pygame.font.SysFont(None, 26)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        key = event.key
        if key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
            self._save()
            self._done = True
        elif key == pygame.K_UP:
            self._focused = 0
        elif key == pygame.K_DOWN:
            self._focused = 1
        elif key == pygame.K_LEFT:
            self._change_volume(-_STEP)
        elif key == pygame.K_RIGHT:
            self._change_volume(_STEP)
        elif key == pygame.K_RETURN:
            self._toggle()

    def _change_volume(self, delta: float) -> None:
        if self._focused == 0:
            self._music_vol = max(0.0, min(1.0, self._music_vol + delta))
            audio.set_music_volume(self._music_vol)
        else:
            self._sfx_vol = max(0.0, min(1.0, self._sfx_vol + delta))
            audio.set_sfx_volume(self._sfx_vol)
        audio.play_sfx("navigate")

    def _toggle(self) -> None:
        if self._focused == 0:
            self._music_enabled = not self._music_enabled
            audio.set_music_enabled(self._music_enabled)
        else:
            self._sfx_enabled = not self._sfx_enabled
            audio.set_sfx_enabled(self._sfx_enabled)
        audio.play_sfx("select")

    def _save(self) -> None:
        profile = self._pm.load()
        profile.music_enabled = self._music_enabled
        profile.sfx_enabled = self._sfx_enabled
        profile.music_volume = self._music_vol
        profile.sfx_volume = self._sfx_vol
        self._pm.save(profile)

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._back if self._done else None

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        _, h = surface.get_size()

        title = self._font_title.render(self._strings.options_title, True, _WHITE)
        surface.blit(title, (40, 36))

        rows = [
            (self._strings.options_music, self._music_vol, self._music_enabled),
            (self._strings.options_sfx,   self._sfx_vol,   self._sfx_enabled),
        ]
        row_y = 120
        for i, (label, vol, enabled) in enumerate(rows):
            active = i == self._focused
            color = _ORANGE if active else _DIM
            prefix = ">" if active else " "
            lbl = self._font_item.render(f"{prefix} {label}", True, color)
            surface.blit(lbl, (40, row_y))

            bar_x, bar_y, bar_w, bar_h = 230, row_y + 8, 220, 18
            pygame.draw.rect(surface, _GRAY, (bar_x, bar_y, bar_w, bar_h), border_radius=4)
            fill = int(bar_w * vol)
            if fill > 0:
                pygame.draw.rect(surface, color, (bar_x, bar_y, fill, bar_h), border_radius=4)

            pct = self._font_item.render(f"{int(vol * 100):3d}%", True, color)
            surface.blit(pct, (bar_x + bar_w + 12, row_y))

            tog = self._font_item.render(
                "[ON ]" if enabled else "[OFF]", True, _GREEN if enabled else _DIM
            )
            surface.blit(tog, (bar_x + bar_w + 72, row_y))

            row_y += 80

        hint = self._font_hint.render(self._strings.options_hint, True, _DIM)
        surface.blit(hint, (40, h - 32))
