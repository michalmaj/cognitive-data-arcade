from __future__ import annotations

import pygame
from cognitive_data_arcade.engine.fonts import get_font

from cognitive_data_arcade.engine.badges import (
    BADGE_ICONS,
    BADGE_REGISTRY,
    Badge,
    _MODULE_BADGES,
    _SPECIAL_BADGES,
    earned_badges,
    load_badge_icon,
    load_icon,
)
from cognitive_data_arcade.engine.i18n import Strings, level_progress, level_title
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import Profile, ProfileManager

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    WHITE as _TITLE_COLOR,
    ORANGE as _HIGHLIGHT_COLOR,
)

_ITEM_COLOR = (160, 160, 160)
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
        self._export_msg: str = ""
        self._export_msg_ttl: float = 0.0
        pygame.font.init()
        self._font_sm = get_font(22)
        self._font_med = get_font(28)
        self._font_large = get_font(46)
        self._font_label = get_font(24)

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
        elif event.key == pygame.K_r:
            from cognitive_data_arcade.ui.reset_confirm_scene import ResetConfirmScene

            self._next = ResetConfirmScene(self._pm, self._strings, self._back)
        elif event.key == pygame.K_s:
            from cognitive_data_arcade.ui.syllabus_scene import SyllabusScene

            self._next = SyllabusScene(self._pm, self._strings, self._back)
        elif event.key == pygame.K_x:
            import pathlib

            out = pathlib.Path.home() / f"cda_progress_{self._profile.alias}.json"
            self._pm.export_progress(out)
            self._export_msg = str(out)
            self._export_msg_ttl = 4000.0

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
        if self._export_msg_ttl > 0:
            self._export_msg_ttl -= dt_ms
            if self._export_msg_ttl <= 0:
                self._export_msg = ""

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
        surface.blit(av_surf, (48 - av_surf.get_width() // 2, 48 - av_surf.get_height() // 2))

        alias_text = (self._alias_buffer + "|") if self._editing_alias else self._profile.alias
        alias_surf = self._font_med.render(alias_text, True, _TITLE_COLOR)
        surface.blit(alias_surf, (94, 12))

        lvl_surf = self._font_sm.render(lvl, True, _HIGHLIGHT_COLOR)
        surface.blit(lvl_surf, (94, 38))

        cur, rng = level_progress(total_points)
        bar_x, bar_y, bar_w, bar_h = 94, 64, 280, 8
        pygame.draw.rect(surface, _BORDER_COLOR, (bar_x, bar_y, bar_w, bar_h), border_radius=4)
        fill = int(bar_w * cur / rng) if rng > 0 else bar_w
        fill = min(fill, bar_w)
        if fill > 0:
            pygame.draw.rect(
                surface, _HIGHLIGHT_COLOR, (bar_x, bar_y, fill, bar_h), border_radius=4
            )

        pts_surf = self._font_sm.render(f"{total_points} AP+SP", True, _DIM_COLOR)
        surface.blit(pts_surf, (bar_x + bar_w + 10, bar_y - 3))

        # ---- LEFT COLUMN ----
        pygame.draw.line(surface, _BORDER_COLOR, (_LEFT_W, _TOPBAR_H), (_LEFT_W, h - _FOOTER_H))
        y = _TOPBAR_H + 18

        ap_lbl = self._font_sm.render(self._strings.label_arcade_points, True, _DIM_COLOR)
        surface.blit(ap_lbl, (15, y))
        y += 20
        ap_val = self._font_large.render(str(self._profile.arcade_points), True, _HIGHLIGHT_COLOR)
        surface.blit(ap_val, (15, y))
        y += 46

        sp_lbl = self._font_sm.render(self._strings.label_science_points, True, _DIM_COLOR)
        surface.blit(sp_lbl, (15, y))
        y += 20
        sp_val = self._font_large.render(str(self._profile.science_points), True, _SP_COLOR)
        surface.blit(sp_val, (15, y))
        y += 52

        pygame.draw.line(surface, _BORDER_COLOR, (15, y), (_LEFT_W - 15, y))
        y += 16

        lessons_lbl = self._font_sm.render(self._strings.label_lessons, True, _DIM_COLOR)
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
            pygame.draw.rect(surface, color, (dx, dy, dot_size, dot_size), border_radius=3)

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

        _ICON_SIZE = 36
        for i, badge in enumerate(self._badge_registry):
            col = i % cols
            row = i // cols
            bx = right_x + col * (card_w + card_gap)
            by = ry + row * (card_h + card_gap)
            is_earned = badge.badge_id in self._profile.badges
            border_col = _HIGHLIGHT_COLOR if is_earned else _BORDER_COLOR
            pygame.draw.rect(surface, _PANEL_BG, (bx, by, card_w, card_h), border_radius=6)
            pygame.draw.rect(surface, border_col, (bx, by, card_w, card_h), 1, border_radius=6)
            icon_png = load_icon(BADGE_ICONS.get(badge.badge_id, ""), size=_ICON_SIZE)
            if icon_png:
                if not is_earned:
                    dark = pygame.Surface((_ICON_SIZE, _ICON_SIZE), pygame.SRCALPHA)
                    dark.blit(icon_png, (0, 0))
                    dark.fill((0, 0, 0, 160), special_flags=pygame.BLEND_RGBA_MULT)
                    icon_png = dark
                surface.blit(icon_png, (bx + (card_w - _ICON_SIZE) // 2, by + 10))
            name = (
                self._strings.badge_names.get(badge.badge_id, badge.badge_id)
                if is_earned
                else "???"
            )
            name_color = _HIGHLIGHT_COLOR if is_earned else _DIM_COLOR
            name_surf = self._font_sm.render(name, True, name_color)
            surface.blit(name_surf, (bx + card_w // 2 - name_surf.get_width() // 2, by + 54))

        # ---- Module completion badges ----
        ry += (1 + len(self._badge_registry) // cols) * (card_h + card_gap) + 14
        mod_lbl = self._font_sm.render(
            "Odznaki modulow" if self._strings.language == "pl" else "Module badges",
            True,
            _DIM_COLOR,
        )
        surface.blit(mod_lbl, (right_x, ry))
        ry += 26

        completed_set = set(self._profile.completed_lessons)
        mod_earned = {b.id for b in earned_badges(completed_set)}
        mod_icon_size = 36
        mod_card_w = 90
        mod_card_h = 60
        mod_gap = 6
        all_mod_badges = _MODULE_BADGES + _SPECIAL_BADGES
        for i, mb in enumerate(all_mod_badges):
            bx = right_x + i * (mod_card_w + mod_gap)
            by = ry
            is_earned = mb.id in mod_earned
            border_col = _HIGHLIGHT_COLOR if is_earned else _BORDER_COLOR
            pygame.draw.rect(surface, _PANEL_BG, (bx, by, mod_card_w, mod_card_h), border_radius=5)
            pygame.draw.rect(
                surface, border_col, (bx, by, mod_card_w, mod_card_h), 1, border_radius=5
            )
            icon = load_badge_icon(mb, size=mod_icon_size)
            if icon:
                if not is_earned:
                    dark = pygame.Surface((mod_icon_size, mod_icon_size), pygame.SRCALPHA)
                    dark.blit(icon, (0, 0))
                    dark.fill((0, 0, 0, 160), special_flags=pygame.BLEND_RGBA_MULT)
                    icon = dark
                surface.blit(icon, (bx + (mod_card_w - mod_icon_size) // 2, by + 4))
            name = mb.name_pl if self._strings.language == "pl" else mb.name_en
            name_surf = get_font(13).render(
                name[:10], True, _HIGHLIGHT_COLOR if is_earned else _DIM_COLOR
            )
            surface.blit(
                name_surf, (bx + mod_card_w // 2 - name_surf.get_width() // 2, by + mod_card_h - 18)
            )

        # ---- FOOTER ----
        footer_y = h - _FOOTER_H
        pygame.draw.line(surface, _BORDER_COLOR, (0, footer_y), (w, footer_y))
        pygame.draw.rect(surface, _PANEL_BG, (0, footer_y, w, _FOOTER_H))

        back_surf = self._font_label.render(self._strings.label_back, True, _DIM_COLOR)
        surface.blit(back_surf, (28, footer_y + 15))

        edit_surf = self._font_label.render(self._strings.label_edit_alias, True, _DIM_COLOR)
        surface.blit(edit_surf, (200, footer_y + 15))

        reset_surf = self._font_label.render(self._strings.label_reset, True, (160, 60, 60))
        surface.blit(reset_surf, (390, footer_y + 15))

        syllabus_surf = self._font_label.render(self._strings.label_syllabus, True, _DIM_COLOR)
        surface.blit(syllabus_surf, (600, footer_y + 15))

        export_surf = self._font_label.render(self._strings.label_export, True, _DIM_COLOR)
        surface.blit(export_surf, (760, footer_y + 15))

        if self._export_msg:
            msg_font = get_font(16)
            msg_surf = msg_font.render(self._export_msg, True, (74, 222, 128))
            surface.blit(msg_surf, (w // 2 - msg_surf.get_width() // 2, footer_y - 22))
