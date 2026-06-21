# src/cognitive_data_arcade/games/emotion_classifier/phase_round.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.emotion_classifier.lexicon import (
    LEXICON,
    TRAP_HINTS,
    classify,
    compute_round_score,
)
from cognitive_data_arcade.games.emotion_classifier.sentences import Sentence

_W, _H = 1024, 768
_PANEL_X = 744
_PANEL_W = 280
_TOP_H = 50
from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    WHITE as _WHITE,
    DIM as _DIM,
    GREEN as _GREEN,
    RED as _RED,
    PURPLE as _PURPLE,
)

_TOP_BG = (12, 12, 30)
_PANEL_BG = (12, 12, 30)
_AMBER = (240, 165, 0)
_GREY = (80, 80, 100)
_LEFT_PAD = 20
_CHIP_H = 26
_CHIP_PAD_X = 10
_CHIP_GAP = 8
_CHIP_ROW_H = 38
_CHIP_Y = 120

_SUBMIT_RECT = pygame.Rect(_PANEL_X // 2 - 120, _H - 80, 240, 48)


class PhaseRoundScene(Scene):
    def __init__(
        self,
        sentences: list[Sentence],
        round_idx: int,
        session_score: int,
        round_results: list[dict],
    ) -> None:
        self._sentences = sentences
        self._sentence = sentences[round_idx]
        self._round_idx = round_idx
        self._session_score = session_score
        self._round_results = round_results
        self._tagged: dict[str, str] = {}  # word → "positive" | "negative"
        self._start_ticks: int = pygame.time.get_ticks()
        self._hint_visible: bool = False
        self._chip_rects: list[tuple[pygame.Rect, str]] = []
        self._chips_built: bool = False
        self._done = False
        self._next: Scene | None = None

    # ── events ─────────────────────────────────────────────────────────────────

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._done:
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self._submit()
            return
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        # Check SUBMIT button (left-click)
        if event.button == 1 and _SUBMIT_RECT.collidepoint(event.pos):
            self._submit()
            return

        # Check word chips
        for rect, word in self._chip_rects:
            if rect.collidepoint(event.pos):
                key = word.rstrip(".,;:!?").lower()
                if event.button == 1:
                    if self._tagged.get(key) == "positive":
                        del self._tagged[key]
                    else:
                        self._tagged[key] = "positive"
                elif event.button == 3:
                    if self._tagged.get(key) == "negative":
                        del self._tagged[key]
                    else:
                        self._tagged[key] = "negative"
                return

        # Right-click on sentence area (not on a chip) → show hint
        if event.button == 3:
            self._hint_visible = True

    def _submit(self) -> None:
        elapsed_s = (pygame.time.get_ticks() - self._start_ticks) / 1000.0
        correct_pts, wrong_pts, beat_bonus, speed_bonus = compute_round_score(
            self._tagged, self._sentence.word_scores, self._sentence.truth, elapsed_s
        )
        round_score = max(0, correct_pts + wrong_pts + beat_bonus + speed_bonus)
        result = {
            "trap": self._sentence.trap,
            "beat_lexicon": beat_bonus > 0,
            "correct_pts": correct_pts,
            "wrong_pts": wrong_pts,
            "beat_bonus": beat_bonus,
            "speed_bonus": speed_bonus,
            "round_score": round_score,
        }
        from cognitive_data_arcade.games.emotion_classifier.phase_round_result import (
            PhaseRoundResultScene,
        )

        self._next = PhaseRoundResultScene(
            sentences=self._sentences,
            sentence=self._sentence,
            tagged_words=dict(self._tagged),
            result=result,
            round_idx=self._round_idx,
            session_score=self._session_score + round_score,
            round_results=self._round_results + [result],
        )
        self._done = True

    # ── update / draw ───────────────────────────────────────────────────────────

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        self._draw_top_bar(surface)
        self._draw_sentence_area(surface)
        self._draw_right_panel(surface)

    def _draw_top_bar(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _TOP_BG, (0, 0, _W, _TOP_H))
        pygame.draw.line(surface, _GREY, (0, _TOP_H), (_W, _TOP_H))
        title = get_font(15).render("EMOTION CLASSIFIER", True, _PURPLE)
        surface.blit(title, (20, (_TOP_H - title.get_height()) // 2))
        rnd = get_font(13).render(f"Runda {self._round_idx + 1} / 8", True, _DIM)
        surface.blit(rnd, (_W // 2 - rnd.get_width() // 2, (_TOP_H - rnd.get_height()) // 2))
        score = get_font(14).render(f"Wynik: {self._session_score} pkt", True, _AMBER)
        surface.blit(score, (_PANEL_X - score.get_width() - 20, (_TOP_H - score.get_height()) // 2))

    def _draw_sentence_area(self, surface: pygame.Surface) -> None:
        instr = get_font(12).render(
            "Oznacz słowa jako pozytywne (LPM) lub negatywne (PPM):", True, _DIM
        )
        surface.blit(instr, (_LEFT_PAD, _TOP_H + 16))

        if not self._chips_built:
            self._build_chips()

        font = get_font(13)
        for rect, word in self._chip_rects:
            tag = self._tagged.get(word.rstrip(".,;:!?").lower())
            if tag == "positive":
                pygame.draw.rect(surface, _GREEN, rect, border_radius=13)
                col = _WHITE
            elif tag == "negative":
                pygame.draw.rect(surface, _RED, rect, border_radius=13)
                col = _WHITE
            else:
                col = _DIM
            lbl = font.render(word, True, col)
            surface.blit(
                lbl, (rect.x + _CHIP_PAD_X, rect.y + (rect.height - lbl.get_height()) // 2)
            )

        # Legend
        legend_y = (
            max(r.bottom for r, _ in self._chip_rects) + 16 if self._chip_rects else _CHIP_Y + 40
        )
        lp = get_font(11).render("LPM = pozytywne", True, _GREEN)
        rp = get_font(11).render("PPM = negatywne", True, _RED)
        dk = get_font(11).render("klik ponownie = odznacz", True, _DIM)
        surface.blit(lp, (_LEFT_PAD, legend_y))
        surface.blit(rp, (_LEFT_PAD + lp.get_width() + 16, legend_y))
        surface.blit(dk, (_LEFT_PAD + lp.get_width() + rp.get_width() + 32, legend_y))

        # Hint box
        if self._hint_visible:
            hint_text = TRAP_HINTS.get(self._sentence.trap, "")
            self._draw_hint_box(surface, hint_text, legend_y + 36)

        # SUBMIT button
        pygame.draw.rect(surface, _PURPLE, _SUBMIT_RECT, border_radius=8)
        btn_lbl = get_font(15).render("ZATWIERDŹ (SPACJA)", True, _WHITE)
        surface.blit(
            btn_lbl,
            (
                _SUBMIT_RECT.centerx - btn_lbl.get_width() // 2,
                _SUBMIT_RECT.centery - btn_lbl.get_height() // 2,
            ),
        )

    def _build_chips(self) -> None:
        font = get_font(13)
        words = self._sentence.text.split()
        x, y = _LEFT_PAD, _CHIP_Y
        self._chip_rects = []
        for word in words:
            w = font.size(word)[0] + _CHIP_PAD_X * 2
            if x + w > _PANEL_X - _LEFT_PAD:
                x = _LEFT_PAD
                y += _CHIP_ROW_H
            rect = pygame.Rect(x, y, w, _CHIP_H)
            self._chip_rects.append((rect, word))
            x += w + _CHIP_GAP
        self._chips_built = True

    def _draw_hint_box(self, surface: pygame.Surface, text: str, y: int) -> None:
        font = get_font(12)
        lbl = font.render(text, True, _AMBER)
        pad = 10
        box = pygame.Rect(_LEFT_PAD - 4, y - 4, lbl.get_width() + pad * 2, lbl.get_height() + pad)
        pygame.draw.rect(surface, (20, 18, 40), box, border_radius=4)
        pygame.draw.rect(surface, _AMBER, box, 1, border_radius=4)
        surface.blit(lbl, (_LEFT_PAD + pad - 4, y + 2))

    def _draw_right_panel(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _PANEL_BG, (_PANEL_X, 0, _PANEL_W, _H))
        pygame.draw.line(surface, _GREY, (_PANEL_X, 0), (_PANEL_X, _H))

        y = _TOP_H + 18
        hdr = get_font(11).render("LEKSYKON WIDZI", True, _PURPLE)
        surface.blit(hdr, (_PANEL_X + 16, y))
        y += 28

        font13 = get_font(13)
        font11 = get_font(11)
        total = 0
        for word, tag in self._tagged.items():
            lex_score = LEXICON.get(word, None)
            row_bg = (25, 40, 25) if tag == "positive" else (40, 25, 25)
            row = pygame.Rect(_PANEL_X + 8, y, _PANEL_W - 16, 26)
            pygame.draw.rect(surface, row_bg, row, border_radius=4)
            col = _GREEN if tag == "positive" else _RED
            wlbl = font13.render(word, True, col)
            surface.blit(wlbl, (_PANEL_X + 16, y + (26 - wlbl.get_height()) // 2))
            if lex_score is not None:
                total += lex_score
                slbl = font11.render(f"{lex_score:+d}", True, _GREEN if lex_score > 0 else _RED)
            else:
                slbl = font11.render("nie w słowniku", True, _GREY)
            surface.blit(
                slbl,
                (_PANEL_X + _PANEL_W - slbl.get_width() - 16, y + (26 - slbl.get_height()) // 2),
            )
            y += 30

        pygame.draw.line(surface, _GREY, (_PANEL_X + 8, y + 4), (_PANEL_X + _PANEL_W - 8, y + 4))
        y += 14
        sum_lbl = font11.render("Suma:", True, _DIM)
        surface.blit(sum_lbl, (_PANEL_X + 16, y))
        total_col = _GREEN if total > 0 else (_RED if total < 0 else _DIM)
        total_lbl = font13.render(f"{total:+d}", True, total_col)
        surface.blit(total_lbl, (_PANEL_X + _PANEL_W - total_lbl.get_width() - 16, y))
        y += 34

        # Live verdict
        if self._tagged:
            ws = {w: LEXICON[w] for w in self._tagged if w in LEXICON}
            verdict, _ = classify(ws)
        else:
            verdict = "neutral"
        vcol = _GREEN if verdict == "positive" else (_RED if verdict == "negative" else _DIM)
        vtext = {"positive": "POZYTYWNY", "negative": "NEGATYWNY", "neutral": "NEUTRALNY"}[verdict]
        border_col = vcol
        vbox = pygame.Rect(_PANEL_X + 8, y, _PANEL_W - 16, 52)
        pygame.draw.rect(surface, (20, 20, 40), vbox, border_radius=6)
        pygame.draw.rect(surface, border_col, vbox, 1, border_radius=6)
        vlbl_h = get_font(10).render("Werdykt leksykonu", True, _DIM)
        surface.blit(vlbl_h, (vbox.centerx - vlbl_h.get_width() // 2, y + 6))
        vlbl = get_font(17).render(vtext, True, vcol)
        surface.blit(vlbl, (vbox.centerx - vlbl.get_width() // 2, y + 22))
        y += 62

        note = get_font(10).render("Leksykon liczy sumę wag.", True, _GREY)
        surface.blit(note, (_PANEL_X + 16, y))
        note2 = get_font(10).render("Negacja? Ironia? Sam nie rozumie.", True, _GREY)
        surface.blit(note2, (_PANEL_X + 16, y + 14))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
