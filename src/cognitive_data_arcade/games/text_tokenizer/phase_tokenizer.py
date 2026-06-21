from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.text_tokenizer.engine import TokenizerState
from cognitive_data_arcade.games.text_tokenizer.widgets import SharedState

_BG = (15, 15, 35)
_PANEL = (18, 18, 42)
_WHITE = (240, 240, 240)
_DIM = (120, 120, 160)
_AMBER = (243, 156, 18)
_GREEN = (46, 204, 113)
_PURPLE = (155, 89, 182)
_LEFT_W = 220
_PHASE_H = 636


class _Toggle:
    def __init__(self, label: str, hint: str, x: int, y: int, default: bool) -> None:
        self.label = label
        self.hint = hint
        self.x, self.y = x, y
        self.on = default
        self.rect = pygame.Rect(x, y, _LEFT_W - 16, 44)

    def handle_click(self, pos: tuple[int, int]) -> bool:
        if self.rect.collidepoint(pos):
            self.on = not self.on
            return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        knob_x = self.x + 36 if self.on else self.x + 2
        track_col = _GREEN if self.on else (60, 60, 80)
        pygame.draw.rect(surface, track_col, (self.x, self.y + 12, 32, 14), border_radius=7)
        pygame.draw.circle(surface, _WHITE, (knob_x + 6, self.y + 19), 6)
        font = get_font(12)
        lbl = font.render(self.label, True, _WHITE if self.on else _DIM)
        surface.blit(lbl, (self.x + 44, self.y + 10))
        hint_s = get_font(10).render(self.hint, True, (80, 80, 120))
        surface.blit(hint_s, (self.x + 44, self.y + 26))


class PhaseTokenizerScene(Scene):
    def __init__(self, state: SharedState) -> None:
        self._state = state
        self._selected_idx: int | None = None
        self._done = False

        self._toggles = [
            _Toggle("Male litery", '"CZAS" -> "czas"', 8, 60, default=True),
            _Toggle("Usun interpunkcje", '"reakcji," -> "reakcji"', 8, 112, default=True),
            _Toggle("Usun stop words", "ze, sie, i, w...", 8, 164, default=False),
        ]
        self._chip_rects: list[pygame.Rect] = []

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for tog in self._toggles:
                if tog.handle_click(event.pos):
                    self._state.lowercase = self._toggles[0].on
                    self._state.rm_punct = self._toggles[1].on
                    self._state.rm_stops = self._toggles[2].on
                    self._selected_idx = None
                    return
            for idx, rect in enumerate(self._chip_rects):
                if rect.collidepoint(event.pos):
                    self._selected_idx = idx if self._selected_idx != idx else None
                    return

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return None

    def draw(self, surface: pygame.Surface, result: TokenizerState | None = None) -> None:  # type: ignore[override]
        if result is None:
            return
        surface.fill(_BG)

        # Left panel
        pygame.draw.rect(surface, _PANEL, (0, 0, _LEFT_W, _PHASE_H))
        hdr = get_font(12).render("PIPELINE KROKOW", True, _PURPLE)
        surface.blit(hdr, (8, 12))

        for tog in self._toggles:
            tog.draw(surface)

        # Stats
        y = 230
        pygame.draw.line(surface, (40, 40, 70), (8, y), (_LEFT_W - 8, y))
        y += 10
        stats_hdr = get_font(12).render("STATYSTYKI", True, _PURPLE)
        surface.blit(stats_hdr, (8, y))
        y += 22
        for label, val, col in [
            ("Tokenow (raw):", str(len(result.raw_tokens)), _WHITE),
            ("Tokenow (clean):", str(len(result.tokens)), _GREEN),
            ("Unikalnych:", str(result.unique_count), _AMBER),
        ]:
            lbl_s = get_font(12).render(label, True, _DIM)
            val_s = get_font(12).render(val, True, col)
            surface.blit(lbl_s, (8, y))
            surface.blit(val_s, (_LEFT_W - 8 - val_s.get_width(), y))
            y += 22

        # Right panel — token chips
        rx = _LEFT_W + 8
        ry = 10
        font_chip = get_font(11)
        surface.blit(
            get_font(11).render("TOKENY (kliknij token aby zobaczyc szczegoly):", True, _DIM),
            (rx, ry),
        )
        ry += 20

        stops: set[str] = set()
        if not self._state.rm_stops:
            from cognitive_data_arcade.games.text_tokenizer.stop_words import (
                STOP_WORDS_PL,
                STOP_WORDS_EN,
            )

            stops = STOP_WORDS_PL if self._state.lang == "pl" else STOP_WORDS_EN

        chip_rects: list[pygame.Rect] = []
        cx, cy = rx, ry
        for i, tok in enumerate(result.tokens):
            is_stop = tok.lower() in stops
            is_sel = i == self._selected_idx
            tw = font_chip.size(tok)[0] + 12
            if cx + tw > 1016:
                cx = rx
                cy += 22
            chip_rect = pygame.Rect(cx, cy, tw, 18)
            chip_rects.append(chip_rect)

            if is_sel:
                bg, border, col = (20, 30, 50), _AMBER, _AMBER
            elif is_stop:
                bg, border, col = (30, 30, 40), (60, 60, 80), _DIM
            else:
                bg, border, col = (15, 35, 20), _GREEN, _GREEN
            pygame.draw.rect(surface, bg, chip_rect, border_radius=3)
            pygame.draw.rect(surface, border, chip_rect, 1, border_radius=3)
            tok_s = font_chip.render(tok, True, col)
            surface.blit(tok_s, (cx + 6, cy + (18 - tok_s.get_height()) // 2))
            cx += tw + 6

        self._chip_rects = chip_rects
        cy += 28

        # Selected token detail
        if self._selected_idx is not None and self._selected_idx < len(result.tokens):
            tok = result.tokens[self._selected_idx]
            count = result.freq.get(tok, 0)
            positions = [i for i, t in enumerate(result.tokens) if t == tok]
            detail = f'"{tok}"  pojawia sie {count}x  pozycje: {positions[:6]}'
            det_s = get_font(11).render(detail, True, _AMBER)
            surface.blit(det_s, (rx, cy))

        # Insight banner
        insight = self._make_insight(result, stops)
        iy = _PHASE_H - 40
        pygame.draw.rect(surface, (20, 15, 35), (_LEFT_W, iy - 6, 1024 - _LEFT_W, 46))
        pygame.draw.line(surface, _PURPLE, (_LEFT_W, iy - 6), (_LEFT_W, iy + 40), 3)
        ins_s = get_font(11).render(insight[:110], True, (200, 180, 220))
        surface.blit(ins_s, (rx, iy + 4))

    def _make_insight(self, result: TokenizerState, stops: set[str]) -> str:
        if not self._toggles[0].on:
            lowers = [t.lower() for t in result.raw_tokens]
            has_case_dup = any(t != t.lower() and t.lower() in lowers for t in result.raw_tokens)
            if has_case_dup:
                return (
                    "Bez malych liter te same slowa to rozne tokeny — "
                    "slownik jest sztucznie wiekszy."
                )
        if self._toggles[2].on and stops:
            removed = sum(1 for t in result.raw_tokens if t.lower() in stops)
            if removed:
                pct = round(100 * removed / max(1, len(result.raw_tokens)))
                return f"Usunieto {removed} stop words — slownik skurczyl sie o ~{pct}%."
        return "Kliknij token zeby zobaczyc ile razy wystepuje w tekscie."
