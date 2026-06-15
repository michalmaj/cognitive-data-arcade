# src/cognitive_data_arcade/games/word_weight_factory/step_corpus.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.word_weight_factory.corpus import CorpusState, _PRESETS
from cognitive_data_arcade.games.word_weight_factory.engine import WeightMatrix
from cognitive_data_arcade.games.text_tokenizer.stop_words import STOP_WORDS_EN, STOP_WORDS_PL

_BG     = (15, 15, 35)
_WHITE  = (240, 240, 240)
_DIM    = (120, 120, 160)
_AMBER  = (243, 156, 18)
_GREEN  = (46, 204, 113)
_PURPLE = (155, 89, 182)
_STEP_H = 672
_W      = 804


class StepCorpusScene(Scene):
    def __init__(self, state: CorpusState) -> None:
        self._state = state
        self._done = False

    def handle_event(self, event: pygame.event.Event) -> None:
        pass  # corpus panel handles all events

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return None

    def draw(self, surface: pygame.Surface, matrix: WeightMatrix | None = None) -> None:
        surface.fill(_BG)
        if matrix is None:
            return

        # Determine selected doc text and title
        docs = self._state.active_docs()
        sel = min(self._state.selected_idx, len(docs) - 1)
        if sel < 0:
            return
        title, text = docs[sel]

        # Title
        t_surf = get_font(13).render(f"Dokument: {title}", True, _AMBER)
        surface.blit(t_surf, (8, 8))

        # Raw text (word-wrapped)
        words = text.split()
        line, lines, max_w = "", [], _W - 16
        font12 = get_font(12)
        for w in words:
            test = (line + " " + w).strip()
            if font12.size(test)[0] > max_w:
                lines.append(line)
                line = w
            else:
                line = test
        if line:
            lines.append(line)
        y = 34
        for ln in lines[:8]:
            s = font12.render(ln, True, _WHITE)
            surface.blit(s, (8, y))
            y += font12.get_linesize()

        # Token chips
        stops = STOP_WORDS_PL if self._state.lang == "pl" else STOP_WORDS_EN
        import string as _str
        tokens = text.split()
        if self._state.lowercase:
            tokens = [t.lower() for t in tokens]
        if self._state.rm_punct:
            tokens = [t.strip(_str.punctuation) for t in tokens]
            tokens = [t for t in tokens if t]
        if self._state.rm_stops:
            tokens = [t for t in tokens if t.lower() not in stops]

        chip_x, chip_y = 8, y + 14
        font10 = get_font(10)
        for tok in tokens:
            is_stop = tok.lower() in stops
            cw = font10.size(tok)[0] + 10
            if chip_x + cw > _W - 8:
                chip_x = 8
                chip_y += 22
            border = (80, 80, 100) if is_stop else _GREEN
            col    = (80, 80, 100) if is_stop else _GREEN
            pygame.draw.rect(surface, (20, 20, 40), (chip_x, chip_y, cw, 18), border_radius=3)
            pygame.draw.rect(surface, border,       (chip_x, chip_y, cw, 18), 1, border_radius=3)
            lbl = font10.render(tok, True, col)
            surface.blit(lbl, (chip_x + 5, chip_y + (18 - lbl.get_height()) // 2))
            chip_x += cw + 5

        # Insight banner
        n_vocab = len(matrix.vocab)
        insight = (f"Slownik rosnie z kazdym nowym dokumentem. Teraz jest {n_vocab} tokenow wspolnych.")
        iy = _STEP_H - 40
        pygame.draw.rect(surface, (20, 15, 35), (0, iy - 6, _W, 46))
        pygame.draw.line(surface, _PURPLE, (0, iy - 6), (0, iy + 40), 3)
        ins = get_font(11).render(insight[:110], True, (200, 180, 220))
        surface.blit(ins, (8, iy + 4))
