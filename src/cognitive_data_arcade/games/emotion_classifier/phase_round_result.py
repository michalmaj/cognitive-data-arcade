# src/cognitive_data_arcade/games/emotion_classifier/phase_round_result.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
)
from cognitive_data_arcade.engine.colors import (
    DIM as _DIM,
)
from cognitive_data_arcade.engine.colors import (
    GREEN as _GREEN,
)
from cognitive_data_arcade.engine.colors import (
    ORANGE as _ORANGE,
)
from cognitive_data_arcade.engine.colors import (
    PURPLE as _PURPLE,
)
from cognitive_data_arcade.engine.colors import (
    RED as _RED,
)
from cognitive_data_arcade.engine.colors import (
    WHITE as _WHITE,
)
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.emotion_classifier.lexicon import (
    TRAP_LABELS,
    classify,
)
from cognitive_data_arcade.games.emotion_classifier.sentences import Sentence

_W, _H = 1024, 768
_PANEL = (18, 18, 42)
_AMBER = (240, 165, 0)
_GREY = (80, 80, 100)

_VERDICT_COLORS = {"positive": _GREEN, "negative": _RED, "neutral": _DIM, "mixed": _PURPLE}
_VERDICT_TEXT = {
    "positive": "POZYTYWNY",
    "negative": "NEGATYWNY",
    "neutral": "NEUTRALNY",
    "mixed": "MIESZANY",
}

_NEGATION_WORDS = {"nie", "nikt", "żadnych", "żadne", "nigdy"}


class PhaseRoundResultScene(Scene):
    def __init__(
        self,
        sentences: list[Sentence],
        sentence: Sentence,
        tagged_words: dict[str, str],
        result: dict,
        round_idx: int,
        session_score: int,
        round_results: list[dict],
    ) -> None:
        self._sentences = sentences
        self._sentence = sentence
        self._tagged = tagged_words
        self._result = result
        self._round_idx = round_idx
        self._session_score = session_score
        self._round_results = round_results
        self._done = False
        self._next: Scene | None = None

        lexicon_verdict, _ = classify(sentence.word_scores)
        player_ws = {w: sentence.word_scores[w] for w in tagged_words if w in sentence.word_scores}
        player_verdict, _ = classify(player_ws)
        self._lexicon_verdict = lexicon_verdict
        self._player_verdict = player_verdict

    def handle_event(self, event: pygame.event.Event) -> None:
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
            or event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            self._advance()

    def _advance(self) -> None:
        if self._round_idx + 1 < len(self._sentences):
            from cognitive_data_arcade.games.emotion_classifier.phase_round import PhaseRoundScene

            self._next = PhaseRoundScene(
                sentences=self._sentences,
                round_idx=self._round_idx + 1,
                session_score=self._session_score,
                round_results=self._round_results,
            )
        else:
            from cognitive_data_arcade.games.emotion_classifier.phase_session_result import (
                PhaseSessionResultScene,
            )

            self._next = PhaseSessionResultScene(
                session_score=self._session_score,
                round_results=self._round_results,
            )
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        self._draw_header(surface)
        y = 70
        y = self._draw_annotated_sentence(surface, y)
        y += 16
        y = self._draw_verdict_boxes(surface, y)
        y += 16
        y = self._draw_trap_callout(surface, y)
        y += 16
        self._draw_score_row(surface, y)

    def _draw_header(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 54))
        hdr = get_font(22).render(f"Wynik rundy {self._round_idx + 1} / 8", True, _WHITE)
        surface.blit(hdr, (_W // 2 - hdr.get_width() // 2, 14))

    def _draw_annotated_sentence(self, surface: pygame.Surface, y: int) -> int:
        lbl = get_font(11).render("Zdanie z adnotacjami leksykonu:", True, _DIM)
        surface.blit(lbl, (40, y))
        y += 22
        font14 = get_font(14)
        font10 = get_font(10)
        x = 40
        chip_h = 24
        score_h = 16
        row_h = score_h + chip_h + 6
        for word in self._sentence.text.split():
            w = font14.size(word)[0] + 20
            if x + w > _W - 40:
                x = 40
                y += row_h + 4
            score_val = self._sentence.word_scores.get(word, None)
            is_negation = word.lower() in _NEGATION_WORDS
            if score_val is not None and score_val > 0:
                pygame.draw.rect(surface, _GREEN, (x, y + score_h + 2, w, chip_h), border_radius=12)
                col = _WHITE
                s_lbl = font10.render(f"+{score_val}", True, _GREEN)
                surface.blit(s_lbl, (x + w // 2 - s_lbl.get_width() // 2, y))
            elif score_val is not None and score_val < 0:
                pygame.draw.rect(surface, _RED, (x, y + score_h + 2, w, chip_h), border_radius=12)
                col = _WHITE
                s_lbl = font10.render(f"{score_val}", True, _RED)
                surface.blit(s_lbl, (x + w // 2 - s_lbl.get_width() // 2, y))
            elif is_negation:
                pygame.draw.rect(
                    surface, _ORANGE, (x, y + score_h + 2, w, chip_h), border_radius=12
                )
                col = _WHITE
                neg_lbl = font10.render("NEG!", True, _ORANGE)
                surface.blit(neg_lbl, (x + w // 2 - neg_lbl.get_width() // 2, y))
            else:
                col = _DIM
            wlbl = font14.render(word, True, col)
            surface.blit(wlbl, (x + 10, y + score_h + 2 + (chip_h - wlbl.get_height()) // 2))
            x += w + 6
        return y + row_h + 8

    def _draw_verdict_boxes(self, surface: pygame.Surface, y: int) -> int:
        box_w = (_W - 80 - 24) // 3
        boxes = [
            ("Leksykon powiedział", self._lexicon_verdict),
            ("Prawdziwy sentyment", self._sentence.truth),
            ("Ty powiedziałeś", self._player_verdict),
        ]
        for i, (label, verdict) in enumerate(boxes):
            bx = 40 + i * (box_w + 12)
            col = _VERDICT_COLORS.get(verdict, _DIM)
            bg_map = {_GREEN: (26, 42, 26), _RED: (42, 26, 26), _PURPLE: (26, 26, 42)}
            bg = bg_map.get(col, (26, 26, 42))
            box = pygame.Rect(bx, y, box_w, 72)
            pygame.draw.rect(surface, bg, box, border_radius=8)
            pygame.draw.rect(surface, col, box, 2, border_radius=8)
            hdr_lbl = get_font(10).render(label, True, _DIM)
            surface.blit(hdr_lbl, (bx + box_w // 2 - hdr_lbl.get_width() // 2, y + 8))
            vtext = _VERDICT_TEXT.get(verdict, verdict.upper())
            vlbl = get_font(18).render(vtext, True, col)
            surface.blit(vlbl, (bx + box_w // 2 - vlbl.get_width() // 2, y + 26))
        return y + 80

    def _draw_trap_callout(self, surface: pygame.Surface, y: int) -> int:
        trap_label = TRAP_LABELS.get(self._sentence.trap, self._sentence.trap)
        explanation = self._sentence.explanation
        pygame.draw.rect(surface, (18, 18, 42), (40, y, _W - 80, 70), border_radius=6)
        pygame.draw.rect(surface, _ORANGE, (40, y, 4, 70))
        tlbl = get_font(11).render(trap_label, True, _ORANGE)
        surface.blit(tlbl, (54, y + 8))
        elbl = get_font(12).render(explanation, True, _WHITE)
        surface.blit(elbl, (54, y + 28))
        return y + 78

    def _draw_score_row(self, surface: pygame.Surface, y: int) -> None:
        r = self._result
        parts = [
            (f"Trafione tagi: +{r['correct_pts']}", _GREEN if r["correct_pts"] else _DIM),
            (f"Błędy: {r['wrong_pts']}", _RED if r["wrong_pts"] else _DIM),
            (f"Pobiłeś leksykon: +{r['beat_bonus']}", _AMBER if r["beat_bonus"] else _DIM),
            (f"Szybkość: +{r['speed_bonus']}", _PURPLE if r["speed_bonus"] else _DIM),
        ]
        x = 40
        for text, col in parts:
            lbl = get_font(13).render(text, True, col)
            surface.blit(lbl, (x, y + 12))
            x += lbl.get_width() + 24

        total_lbl = get_font(18).render(f"+{r['round_score']} pkt", True, _AMBER)
        surface.blit(total_lbl, (_W - 300, y + 6))

        btn = pygame.Rect(_W - 200, y + 2, 160, 44)
        pygame.draw.rect(surface, _PANEL, btn, border_radius=6)
        pygame.draw.rect(surface, _GREY, btn, 1, border_radius=6)
        blbl = get_font(13).render("DALEJ (SPACJA)", True, _WHITE)
        surface.blit(
            blbl, (btn.centerx - blbl.get_width() // 2, btn.centery - blbl.get_height() // 2)
        )

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
