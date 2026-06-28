# src/cognitive_data_arcade/ui/onboarding_scene.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.colors import BG as _BG
from cognitive_data_arcade.engine.fonts import get_font, get_font_medium
from cognitive_data_arcade.engine.scene import Scene

_W, _H = 1024, 768
_ACCENT = (99, 102, 241)
_TEXT = (240, 241, 255)
_DIM = (100, 110, 160)
_SURFACE = (22, 24, 40)
_BORDER = (45, 48, 80)
_ERROR = (239, 68, 68)


class OnboardingScene(Scene):
    """First-launch screen: collects alias and language, then routes to TitleScene."""

    def __init__(self, pm) -> None:
        self._pm = pm
        self._alias_buf = ""
        self._language = "pl"
        self._error = ""
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self._handle_key(event)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_click(event.pos)

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    def _handle_key(self, event: pygame.event.Event) -> None:
        k = event.key
        if k == pygame.K_ESCAPE:
            return
        if k == pygame.K_RETURN:
            self._try_submit()
        elif k == pygame.K_BACKSPACE:
            self._alias_buf = self._alias_buf[:-1]
            self._error = ""
        elif k == pygame.K_TAB:
            self._toggle_language()
        elif event.unicode.isprintable() and len(self._alias_buf) < 20:
            self._alias_buf += event.unicode
            self._error = ""

    def _handle_click(self, pos: tuple[int, int]) -> None:
        cx = _W // 2
        pl_rect = pygame.Rect(cx - 90, 440, 80, 36)
        en_rect = pygame.Rect(cx + 10, 440, 80, 36)
        if pl_rect.collidepoint(pos):
            self._language = "pl"
        elif en_rect.collidepoint(pos):
            self._language = "en"
        submit_rect = pygame.Rect(cx - 100, 510, 200, 44)
        if submit_rect.collidepoint(pos):
            self._try_submit()

    def _toggle_language(self) -> None:
        self._language = "en" if self._language == "pl" else "pl"

    def _try_submit(self) -> None:
        alias = self._alias_buf.strip()
        if not alias:
            self._error = "Podaj pseudonim" if self._language == "pl" else "Enter a nickname"
            return
        profile = self._pm.load()
        profile.alias = alias
        profile.language = self._language
        self._pm.save(profile)
        self._pm.set_onboarding_done()
        from cognitive_data_arcade.engine.i18n import get_strings
        from cognitive_data_arcade.ui.intro_scene import TitleScene

        strings = get_strings(self._language)
        self._next = TitleScene(self._pm, strings)
        self._done = True

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        cx = _W // 2

        title_surf = get_font_medium(42).render("Cognitive Data Arcade", True, _ACCENT)
        surface.blit(title_surf, (cx - title_surf.get_width() // 2, 120))

        if self._language == "pl":
            tagline = "32 gry z danych, statystyki i ML — Twoje wyniki, Twoje dane"
        else:
            tagline = "32 data science games — your results, your data"
        tag_surf = get_font(18).render(tagline, True, _DIM)
        surface.blit(tag_surf, (cx - tag_surf.get_width() // 2, 180))

        lbl = "Pseudonim" if self._language == "pl" else "Nickname"
        lbl_surf = get_font(16).render(lbl, True, _DIM)
        surface.blit(lbl_surf, (cx - 150, 268))

        box_rect = pygame.Rect(cx - 150, 290, 300, 44)
        border_col = _ACCENT if self._alias_buf else _BORDER
        pygame.draw.rect(surface, _SURFACE, box_rect, border_radius=6)
        pygame.draw.rect(surface, border_col, box_rect, 1, border_radius=6)
        display_text = self._alias_buf if self._alias_buf else ("student42")
        text_col = _TEXT if self._alias_buf else _DIM
        cursor = "|" if self._alias_buf else ""
        alias_surf = get_font(20).render(display_text + cursor, True, text_col)
        surface.blit(alias_surf, (cx - 150 + 10, 290 + (44 - alias_surf.get_height()) // 2))

        if self._error:
            err_surf = get_font(15).render(self._error, True, _ERROR)
            surface.blit(err_surf, (cx - err_surf.get_width() // 2, 340))

        lang_lbl = get_font(16).render("Jezyk / Language", True, _DIM)
        surface.blit(lang_lbl, (cx - lang_lbl.get_width() // 2, 415))

        pl_rect = pygame.Rect(cx - 90, 440, 80, 36)
        en_rect = pygame.Rect(cx + 10, 440, 80, 36)
        pygame.draw.rect(
            surface, _ACCENT if self._language == "pl" else _SURFACE, pl_rect, border_radius=6
        )
        pygame.draw.rect(surface, _BORDER, pl_rect, 1, border_radius=6)
        pygame.draw.rect(
            surface, _ACCENT if self._language == "en" else _SURFACE, en_rect, border_radius=6
        )
        pygame.draw.rect(surface, _BORDER, en_rect, 1, border_radius=6)
        pl_lbl = get_font(16).render("Polski", True, _TEXT)
        en_lbl = get_font(16).render("English", True, _TEXT)
        surface.blit(
            pl_lbl,
            (pl_rect.centerx - pl_lbl.get_width() // 2, pl_rect.centery - pl_lbl.get_height() // 2),
        )
        surface.blit(
            en_lbl,
            (en_rect.centerx - en_lbl.get_width() // 2, en_rect.centery - en_lbl.get_height() // 2),
        )

        note = (
            "Pseudonim jest lokalny — nie wysylamy danych nigdzie"
            if self._language == "pl"
            else "Nickname is local — we never send your data anywhere"
        )
        note_surf = get_font(14).render(note, True, _DIM)
        surface.blit(note_surf, (cx - note_surf.get_width() // 2, 490))

        submit_rect = pygame.Rect(cx - 100, 510, 200, 44)
        pygame.draw.rect(surface, _ACCENT, submit_rect, border_radius=8)
        btn_label = "Zaczynamy  >" if self._language == "pl" else "Start  >"
        btn_surf = get_font_medium(18).render(btn_label, True, _TEXT)
        surface.blit(
            btn_surf,
            (
                submit_rect.centerx - btn_surf.get_width() // 2,
                submit_rect.centery - btn_surf.get_height() // 2,
            ),
        )

        hint = "TAB — zmien jezyk" if self._language == "pl" else "TAB — switch language"
        hint_surf = get_font(13).render(hint, True, _DIM)
        surface.blit(hint_surf, (cx - hint_surf.get_width() // 2, 580))
