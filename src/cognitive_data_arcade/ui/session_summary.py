from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.badges import SessionResult
from cognitive_data_arcade.engine.i18n import Strings, level_title
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import Profile, ProfileManager

_BG = (26, 26, 46)
_BANNER_BG = (26, 26, 62)
_TITLE_COLOR = (240, 240, 240)
_ITEM_COLOR = (160, 160, 160)
_HIGHLIGHT_COLOR = (243, 156, 18)
_SP_COLOR = (39, 174, 96)
_ACCENT_COLOR = (52, 152, 219)
_DIM_COLOR = (70, 70, 112)
_PANEL_BG = (18, 18, 42)
_BORDER_COLOR = (42, 42, 80)
_LEVEL_COLOR = (192, 132, 252)


class SessionSummaryScene(Scene):
    def __init__(
        self,
        session: SessionResult,
        new_badge_ids: list[str],
        profile_before: Profile,
        profile_after: Profile,
        strings: Strings,
        profile_manager: ProfileManager,
    ) -> None:
        self._session = session
        self._new_badge_ids = new_badge_ids
        self._profile_before = profile_before
        self._profile_after = profile_after
        self._strings = strings
        self._pm = profile_manager
        self._next: Scene | None = None
        self._done = False
        self._go_to_profile = False
        self._font_sm = pygame.font.SysFont(None, 24)
        self._font_title = pygame.font.SysFont(None, 56)
        self._font_sub = pygame.font.SysFont(None, 30)
        self._font_stat = pygame.font.SysFont(None, 52)
        self._font_hint = pygame.font.SysFont(None, 26)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE):
            self._done = True
        elif event.key == pygame.K_p:
            self._done = True
            self._go_to_profile = True

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        if self._next is not None:
            return self._next
        if not self._done:
            return None
        from cognitive_data_arcade.ui.menu import LessonMenuScene

        if self._go_to_profile:
            from cognitive_data_arcade.ui.profile_screen import ProfileScene

            back = LessonMenuScene()
            self._next = ProfileScene(self._pm, self._strings, back)
        else:
            self._next = LessonMenuScene()
        return self._next

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        w = surface.get_width()
        h = surface.get_height()

        # Lesson tag
        tag = self._font_sm.render(self._session.task_name, True, _DIM_COLOR)
        surface.blit(tag, (w // 2 - tag.get_width() // 2, 28))

        # Title
        title = self._font_title.render(
            self._strings.session_complete, True, _TITLE_COLOR
        )
        surface.blit(title, (w // 2 - title.get_width() // 2, 52))

        # Subtitle
        sub = self._font_sub.render(self._strings.session_subtitle, True, _ITEM_COLOR)
        surface.blit(sub, (w // 2 - sub.get_width() // 2, 110))

        # Divider
        pygame.draw.line(surface, _BORDER_COLOR, (100, 146), (w - 100, 146))

        # Stats row
        stats = [
            (
                self._strings.label_arcade_points,
                f"+{self._session.arcade_points_earned}",
                _HIGHLIGHT_COLOR,
            ),
            (
                self._strings.label_accuracy,
                f"{self._session.accuracy:.0%}",
                _ACCENT_COLOR,
            ),
            (
                self._strings.label_avg_rt,
                f"{self._session.avg_reaction_time_ms:.0f} ms",
                _ITEM_COLOR,
            ),
        ]
        box_w, box_h = 240, 100
        gap = 20
        total_box_w = 3 * box_w + 2 * gap
        box_x0 = (w - total_box_w) // 2
        box_y = 160

        for i, (label, value, color) in enumerate(stats):
            bx = box_x0 + i * (box_w + gap)
            pygame.draw.rect(
                surface, _PANEL_BG, (bx, box_y, box_w, box_h), border_radius=6
            )
            pygame.draw.rect(
                surface, _BORDER_COLOR, (bx, box_y, box_w, box_h), 1, border_radius=6
            )
            lbl = self._font_sm.render(label, True, _DIM_COLOR)
            surface.blit(lbl, (bx + box_w // 2 - lbl.get_width() // 2, box_y + 10))
            val = self._font_stat.render(value, True, color)
            surface.blit(val, (bx + box_w // 2 - val.get_width() // 2, box_y + 38))

        # Badges section
        section_y = box_y + box_h + 22
        lbl_new = self._font_sm.render(self._strings.label_new_badges, True, _DIM_COLOR)
        surface.blit(lbl_new, (box_x0, section_y))
        section_y += 24

        if self._new_badge_ids:
            pill_x = box_x0
            for bid in self._new_badge_ids:
                name = self._strings.badge_names.get(bid, bid)
                pill_surf = self._font_sm.render(f"✦ {name}", True, _HIGHLIGHT_COLOR)
                pill_w = pill_surf.get_width() + 20
                pill_h = 28
                pygame.draw.rect(
                    surface,
                    _PANEL_BG,
                    (pill_x, section_y, pill_w, pill_h),
                    border_radius=14,
                )
                pygame.draw.rect(
                    surface,
                    _HIGHLIGHT_COLOR,
                    (pill_x, section_y, pill_w, pill_h),
                    1,
                    border_radius=14,
                )
                surface.blit(pill_surf, (pill_x + 10, section_y + 5))
                pill_x += pill_w + 10
        else:
            no_badge = self._font_sm.render(
                self._strings.label_no_new_badges, True, _DIM_COLOR
            )
            surface.blit(no_badge, (box_x0, section_y))

        # Level-up banner (conditional)
        before_total = (
            self._profile_before.arcade_points + self._profile_before.science_points
        )
        after_total = (
            self._profile_after.arcade_points + self._profile_after.science_points
        )
        before_lvl = level_title(before_total, self._strings)
        after_lvl = level_title(after_total, self._strings)

        banner_y = section_y + 46
        if before_lvl != after_lvl:
            banner_rect = pygame.Rect(100, banner_y, w - 200, 44)
            pygame.draw.rect(surface, _BANNER_BG, banner_rect, border_radius=6)
            pygame.draw.rect(surface, _LEVEL_COLOR, banner_rect, 1, border_radius=6)
            lvl_text = (
                f"▲  {self._strings.label_level_up}  {before_lvl}  →  {after_lvl}"
            )
            lvl_surf = self._font_sm.render(lvl_text, True, _LEVEL_COLOR)
            surface.blit(lvl_surf, (w // 2 - lvl_surf.get_width() // 2, banner_y + 13))

        # Footer hints
        hints = [
            (self._strings.hint_space, _TITLE_COLOR),
            (self._strings.hint_p, _ITEM_COLOR),
            (self._strings.hint_esc, _ITEM_COLOR),
        ]
        hint_y = h - 40
        hint_total = sum(self._font_hint.size(t)[0] for t, _ in hints) + 60
        hint_x = (w - hint_total) // 2
        for hint_text, hint_color in hints:
            hs = self._font_hint.render(hint_text, True, hint_color)
            surface.blit(hs, (hint_x, hint_y))
            hint_x += hs.get_width() + 30
