from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.badges import BADGE_REGISTRY, Badge
from cognitive_data_arcade.engine.i18n import Strings, level_progress, level_title
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import Profile, ProfileManager

_BG = (26, 26, 46)
_TITLE_COLOR = (240, 240, 240)
_ITEM_COLOR = (160, 160, 160)
_HIGHLIGHT_COLOR = (243, 156, 18)
_SP_COLOR = (39, 174, 96)
_DIM_COLOR = (70, 70, 112)
_PANEL_BG = (18, 18, 42)
_BORDER_COLOR = (42, 42, 80)

_TOPBAR_H = 96
_LEFT_W = 210
_FOOTER_H = 50


class ProfileScene(Scene):
    def __init__(
        self,
        profile_manager: ProfileManager,
        strings: Strings,
        back_scene: Scene,
    ) -> None:
        self._pm = profile_manager
        self._strings = strings
        self._back = back_scene
        self._profile: Profile = profile_manager.load()
        self._badge_registry: list[Badge] = BADGE_REGISTRY
        self._next: Scene | None = None
        self._editing_alias = False
        self._alias_buffer = ""
        pygame.font.init()
        self._font_sm = pygame.font.SysFont(None, 22)
        self._font_med = pygame.font.SysFont(None, 28)
        self._font_large = pygame.font.SysFont(None, 46)
        self._font_label = pygame.font.SysFont(None, 24)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self._editing_alias:
            surf = pygame.display.get_surface()
            h = surf.get_size()[1] if surf else 768
            footer_y = h - _FOOTER_H
            from cognitive_data_arcade.engine.mouse import hit
            edit_rect = pygame.Rect(220, footer_y + 15, 200, 24)
            if hit(edit_rect, event.pos):
                self._editing_alias = True
                self._alias_buffer = ""
            return
        if event.type != pygame.KEYDOWN:
            return

        if self._editing_alias:
            self._handle_alias_input(event)
            return

        if event.key == pygame.K_ESCAPE:
            self._next = self._back
        elif event.key == pygame.K_e:
            self._editing_alias = True
            self._alias_buffer = ""

    def _handle_alias_input(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_RETURN:
            if self._alias_buffer:
                self._profile.alias = self._alias_buffer
                self._pm.save(self._profile)
            self._editing_alias = False
        elif event.key == pygame.K_ESCAPE:
            self._editing_alias = False
            self._next = self._back
        elif event.key == pygame.K_BACKSPACE:
            self._alias_buffer = self._alias_buffer[:-1]
        elif event.unicode.isprintable() and len(self._alias_buffer) < 20:
            self._alias_buffer += event.unicode

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._next is not None

    def next_scene(self) -> Scene | None:
        return self._next

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        w, h = surface.get_size()

        total_points = self._profile.arcade_points + self._profile.science_points

        # ---- TOP BAR ----
        pygame.draw.rect(surface, _PANEL_BG, (0, 0, w, _TOPBAR_H))
        pygame.draw.line(surface, _BORDER_COLOR, (0, _TOPBAR_H), (w, _TOPBAR_H))

        lvl = level_title(total_points, self._strings)
        avatar_emoji = lvl.split()[0]
        pygame.draw.circle(surface, _BORDER_COLOR, (48, 48), 36)
        pygame.draw.circle(surface, _PANEL_BG, (48, 48), 34)
        av_surf = self._font_large.render(avatar_emoji, True, _HIGHLIGHT_COLOR)
        surface.blit(
            av_surf, (48 - av_surf.get_width() // 2, 48 - av_surf.get_height() // 2)
        )

        alias_text = (
            (self._alias_buffer + "|") if self._editing_alias else self._profile.alias
        )
        alias_surf = self._font_med.render(alias_text, True, _TITLE_COLOR)
        surface.blit(alias_surf, (94, 12))

        lvl_surf = self._font_sm.render(lvl, True, _HIGHLIGHT_COLOR)
        surface.blit(lvl_surf, (94, 38))

        cur, rng = level_progress(total_points)
        bar_x, bar_y, bar_w, bar_h = 94, 64, 280, 8
        pygame.draw.rect(
            surface, _BORDER_COLOR, (bar_x, bar_y, bar_w, bar_h), border_radius=4
        )
        fill = int(bar_w * cur / rng) if rng > 0 else bar_w
        fill = min(fill, bar_w)
        if fill > 0:
            pygame.draw.rect(
                surface, _HIGHLIGHT_COLOR, (bar_x, bar_y, fill, bar_h), border_radius=4
            )

        pts_surf = self._font_sm.render(f"{total_points} AP+SP", True, _DIM_COLOR)
        surface.blit(pts_surf, (bar_x + bar_w + 10, bar_y - 3))

        # ---- LEFT COLUMN ----
        pygame.draw.line(
            surface, _BORDER_COLOR, (_LEFT_W, _TOPBAR_H), (_LEFT_W, h - _FOOTER_H)
        )
        y = _TOPBAR_H + 18

        ap_lbl = self._font_sm.render(
            self._strings.label_arcade_points, True, _DIM_COLOR
        )
        surface.blit(ap_lbl, (15, y))
        y += 20
        ap_val = self._font_large.render(
            str(self._profile.arcade_points), True, _HIGHLIGHT_COLOR
        )
        surface.blit(ap_val, (15, y))
        y += 46

        sp_lbl = self._font_sm.render(
            self._strings.label_science_points, True, _DIM_COLOR
        )
        surface.blit(sp_lbl, (15, y))
        y += 20
        sp_val = self._font_large.render(
            str(self._profile.science_points), True, _SP_COLOR
        )
        surface.blit(sp_val, (15, y))
        y += 52

        pygame.draw.line(surface, _BORDER_COLOR, (15, y), (_LEFT_W - 15, y))
        y += 16

        lessons_lbl = self._font_sm.render(
            self._strings.label_lessons, True, _DIM_COLOR
        )
        surface.blit(lessons_lbl, (15, y))
        y += 22

        dot_size, dot_gap = 14, 4
        dot_cell = dot_size + dot_gap
        dots_per_row = 5
        completed = set(self._profile.completed_lessons)
        for i in range(30):
            col = i % dots_per_row
            row = i // dots_per_row
            dx = 15 + col * dot_cell
            dy = y + row * dot_cell
            color = _SP_COLOR if (i + 1) in completed else _BORDER_COLOR
            pygame.draw.rect(
                surface, color, (dx, dy, dot_size, dot_size), border_radius=3
            )

        # ---- RIGHT COLUMN ----
        right_x = _LEFT_W + 20
        right_w = w - right_x - 10
        ry = _TOPBAR_H + 14

        earned_count = len(self._profile.badges)
        total_count = len(self._badge_registry)
        badges_lbl = self._font_sm.render(
            f"{self._strings.label_badges_earned}  ({earned_count} / {total_count})",
            True,
            _DIM_COLOR,
        )
        surface.blit(badges_lbl, (right_x, ry))
        ry += 28

        cols = 3
        card_gap = 8
        card_w = (right_w - (cols - 1) * card_gap) // cols
        card_h = 82

        for i, badge in enumerate(self._badge_registry):
            col = i % cols
            row = i // cols
            bx = right_x + col * (card_w + card_gap)
            by = ry + row * (card_h + card_gap)
            earned = badge.badge_id in self._profile.badges
            border_col = _HIGHLIGHT_COLOR if earned else _BORDER_COLOR
            pygame.draw.rect(
                surface, _PANEL_BG, (bx, by, card_w, card_h), border_radius=6
            )
            pygame.draw.rect(
                surface, border_col, (bx, by, card_w, card_h), 1, border_radius=6
            )
            if earned:
                icon_surf = self._font_large.render(badge.icon, True, _HIGHLIGHT_COLOR)
                name = self._strings.badge_names.get(badge.badge_id, badge.badge_id)
                name_surf = self._font_sm.render(name, True, _HIGHLIGHT_COLOR)
            else:
                icon_surf = self._font_large.render("🔒", True, _BORDER_COLOR)
                name_surf = self._font_sm.render("???", True, _DIM_COLOR)
            surface.blit(
                icon_surf, (bx + card_w // 2 - icon_surf.get_width() // 2, by + 10)
            )
            surface.blit(
                name_surf, (bx + card_w // 2 - name_surf.get_width() // 2, by + 54)
            )

        # ---- FOOTER ----
        footer_y = h - _FOOTER_H
        pygame.draw.line(surface, _BORDER_COLOR, (0, footer_y), (w, footer_y))
        pygame.draw.rect(surface, _PANEL_BG, (0, footer_y, w, _FOOTER_H))

        back_surf = self._font_label.render(self._strings.label_back, True, _DIM_COLOR)
        surface.blit(back_surf, (28, footer_y + 15))

        edit_surf = self._font_label.render(
            self._strings.label_edit_alias, True, _DIM_COLOR
        )
        surface.blit(edit_surf, (220, footer_y + 15))
