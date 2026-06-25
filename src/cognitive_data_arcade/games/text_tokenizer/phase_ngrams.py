from __future__ import annotations

from collections import Counter

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.text_tokenizer.engine import TokenizerState
from cognitive_data_arcade.games.text_tokenizer.widgets import SharedState

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    WHITE as _WHITE,
    DIM as _DIM,
    BLUE as _BLUE,
    PURPLE as _PURPLE,
)

_AMBER = (243, 156, 18)
_PHASE_H = 636

_SIZES = [(1, "Unigramy (1)"), (2, "Bigramy (2)"), (3, "Trigramy (3)")]


class PhaseNgramsScene(Scene):
    def __init__(self, state: SharedState) -> None:
        self._state = state
        self._done = False
        self._btn_rects: list[pygame.Rect] = []

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self._btn_rects):
                if rect.collidepoint(event.pos):
                    self._state.ngram_n = _SIZES[i][0]
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

        # Selector row
        font_12 = get_font(12)
        font_11 = get_font(11)
        x, y = 12, 12
        self._btn_rects = []
        for i, (n, label) in enumerate(_SIZES):
            active = self._state.ngram_n == n
            bw = font_12.size(label)[0] + 20
            rect = pygame.Rect(x, y, bw, 28)
            self._btn_rects.append(rect)
            bg = (50, 50, 90) if active else (20, 20, 40)
            border = _AMBER if active else (50, 50, 80)
            pygame.draw.rect(surface, bg, rect, border_radius=4)
            pygame.draw.rect(surface, border, rect, 1, border_radius=4)
            col = _AMBER if active else _DIM
            lbl_s = font_12.render(label, True, col)
            surface.blit(lbl_s, (x + 10, y + (28 - lbl_s.get_height()) // 2))
            x += bw + 8

        # N-gram chips
        counts = Counter(result.ngrams)
        cy = 56
        cx = 12
        for gram, count in sorted(counts.items(), key=lambda kv: -kv[1]):
            label = "[" + " - ".join(gram) + "]"
            lw = font_11.size(label)[0] + 12
            badge_w = (font_11.size(f"x{count}")[0] + 8) if count > 1 else 0
            total_w = lw + badge_w
            if cx + total_w > 1012:
                cx = 12
                cy += 26
            if cy > _PHASE_H - 60:
                break

            is_repeat = count > 1
            bg = (15, 25, 45) if is_repeat else (20, 20, 35)
            border = _BLUE if is_repeat else (50, 50, 80)
            col = _BLUE if is_repeat else _DIM

            chip_rect = pygame.Rect(cx, cy, lw, 20)
            pygame.draw.rect(surface, bg, chip_rect, border_radius=3)
            pygame.draw.rect(surface, border, chip_rect, 1, border_radius=3)
            tok_s = font_11.render(label, True, col)
            surface.blit(tok_s, (cx + 6, cy + (20 - tok_s.get_height()) // 2))

            if is_repeat:
                badge_rect = pygame.Rect(cx + lw, cy, badge_w, 20)
                pygame.draw.rect(surface, _BLUE, badge_rect, border_radius=3)
                bs = font_11.render(f"x{count}", True, _WHITE)
                surface.blit(bs, (cx + lw + 4, cy + (20 - bs.get_height()) // 2))

            cx += total_w + 8

        # Insight banner
        insight = self._make_insight(result, counts)
        iy = _PHASE_H - 40
        pygame.draw.rect(surface, (20, 15, 35), (0, iy - 6, 1024, 46))
        pygame.draw.line(surface, _PURPLE, (0, iy - 6), (0, iy + 40), 3)
        ins_s = font_11.render(insight[:115], True, (200, 180, 220))
        surface.blit(ins_s, (12, iy + 4))

    def _make_insight(self, result: TokenizerState, counts: Counter) -> str:
        n = self._state.ngram_n
        if n >= 3 and len(result.tokens) < 6:
            return "Tekst za krotki na powtarzajace się trigramy — sprobuj dluzszego."
        repeated = [(g, c) for g, c in counts.items() if c > 1]
        if repeated and n > 1:
            top = max(repeated, key=lambda x: x[1])
            gram_str = " ".join(top[0])
            return (
                f'"{gram_str}" pojawia się {top[1]}x — '
                f"n-gramy wykrywaja kolokacje, ktorych unigramy nie widza."
            )
        return "N-gramy = sekwencje N sasiadujacych tokenow. Niebieskie = powtarzajace się."
