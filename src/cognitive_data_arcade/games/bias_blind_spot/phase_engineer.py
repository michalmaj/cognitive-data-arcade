# src/cognitive_data_arcade/games/bias_blind_spot/phase_engineer.py
"""Act 2 -- Engineer: 3 mandatory rounds of feature removal."""

from __future__ import annotations
import pygame
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.bias_blind_spot.game_state import (
    GameState,
    FEATURES,
    STARTING_BIAS,
    STARTING_ACC,
    compute_round_result,
    compute_score_engineer,
)

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    WHITE as _WHITE,
    DIM as _DIM,
    GREEN as _GREEN,
    RED as _RED,
    ORANGE as _ORANGE,
)

_W, _H = 1024, 768
_PANEL = (16, 20, 36)
_C_ENG = (39, 174, 96)

_FEAT_LEFT = 60
_FEAT_TOP = 100
_FEAT_W = 320
_FEAT_H = 44
_FEAT_GAP = 12

_TRAIN_BTN = pygame.Rect(420, 560, 200, 50)

_HINT_ZIP = "Wskazowka: zip_code r=0.71 -- sprobuj go usunac"
_HINT_DEBT = "Wskazowka: debt_ratio r=0.41 -- kolejne proxy"

_REVEAL = [
    "Usunalem zip_code -- bias spada, ale nie znika.",
    "Usunalem kolejne proxy. Bias maleje, dokladnosc spada.",
    "Nie mozna jednoczesnie: usunac bias i zachowac dokladnosc.",
]


def _feat_btn(idx: int) -> pygame.Rect:
    return pygame.Rect(_FEAT_LEFT, _FEAT_TOP + idx * (_FEAT_H + _FEAT_GAP), _FEAT_W, _FEAT_H)


class PhaseEngineerScene(Scene):
    def __init__(self, state: GameState) -> None:
        self._state = state
        self._round = 1
        self._removed: set[str] = set()
        self._selected: set[str] = set()
        self._trained = False
        self._bias = STARTING_BIAS
        self._accuracy = STARTING_ACC
        self._show_advance = False
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self._show_advance:
            self._next_round_or_finish()
            return
        if self._trained or event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return
        pos = event.pos
        for i, feat in enumerate(FEATURES):
            if feat in self._removed:
                continue
            if _feat_btn(i).collidepoint(pos):
                if feat in self._selected:
                    self._selected.discard(feat)
                else:
                    self._selected.add(feat)
                return
        if _TRAIN_BTN.collidepoint(pos):
            self._do_train()

    def _do_train(self) -> None:
        self._removed |= self._selected
        self._bias, self._accuracy = compute_round_result(frozenset(self._removed))
        self._state.bias_rounds.append(self._bias)
        self._state.accuracy_rounds.append(self._accuracy)
        self._trained = True
        self._show_advance = True

    def _next_round_or_finish(self) -> None:
        if self._round < 3:
            self._round += 1
            self._selected = set()
            self._trained = False
            self._show_advance = False
        else:
            bias_reduction = STARTING_BIAS - self._bias
            self._state.score_engineer = compute_score_engineer(bias_reduction, self._accuracy)
            lines = [
                ("Runda 3 zakonczona.", _C_ENG),
                (
                    f"Finalny bias: {self._bias:.0f}pp -- Dokladnosc: {self._accuracy * 100:.0f}%",
                    _DIM,
                ),
                ("", (0, 0, 0)),
                ("SPACJA aby kontynuowac", (60, 60, 80)),
            ]
            from cognitive_data_arcade.games.bias_blind_spot.phase_interlude import (
                PhaseInterludeScene,
            )

            self._next = PhaseInterludeScene(self._state, lines, "regulator")
            self._done = True

    def _bias_color(self, bias: float) -> tuple[int, int, int]:
        if bias > 20:
            return _RED
        if bias > 10:
            return _ORANGE
        return _GREEN

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 56))
        title = get_font(20).render(f"Akt 2: Inzynier -- Runda {self._round}/3", True, _WHITE)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))

        f13 = get_font(13)
        f11 = get_font(11)

        feat_label = f11.render("DOSTEPNE CECHY -- kliknij aby usunac:", True, _DIM)
        surface.blit(feat_label, (_FEAT_LEFT, _FEAT_TOP - 22))

        for i, feat in enumerate(FEATURES):
            btn_r = _feat_btn(i)
            removed = feat in self._removed
            selected = feat in self._selected
            if removed:
                bg = (30, 16, 16)
                border = _RED
                label_col = (100, 80, 80)
            elif selected:
                bg = (40, 60, 40)
                border = _GREEN
                label_col = _GREEN
            else:
                bg = _PANEL
                border = _DIM
                label_col = _WHITE
            pygame.draw.rect(surface, bg, btn_r, border_radius=5)
            pygame.draw.rect(surface, border, btn_r, 1, border_radius=5)
            prefix = "[X] " if removed else ("[>] " if selected else "[ ] ")
            ls = f13.render(prefix + feat, True, label_col)
            surface.blit(ls, (btn_r.x + 12, btn_r.y + btn_r.h // 2 - ls.get_height() // 2))

        race_r = pygame.Rect(_FEAT_LEFT, _FEAT_TOP + 5 * (_FEAT_H + _FEAT_GAP), _FEAT_W, _FEAT_H)
        pygame.draw.rect(surface, (20, 20, 24), race_r, border_radius=5)
        pygame.draw.rect(surface, (50, 50, 60), race_r, 1, border_radius=5)
        rs = f13.render("race  [BRAK W DANYCH]", True, (60, 60, 70))
        surface.blit(rs, (race_r.x + 12, race_r.y + race_r.h // 2 - rs.get_height() // 2))

        sx = 440
        sy = 100
        stats_lbl = f11.render("WYNIKI PO TRENINGU:", True, _DIM)
        surface.blit(stats_lbl, (sx, sy))
        sy += 24

        bias_col = self._bias_color(self._bias)
        bias_s = f13.render(f"Bias gap: {self._bias:.0f} pp", True, bias_col)
        surface.blit(bias_s, (sx, sy))
        sy += 28

        bar_max_w = 440
        bar_w = int((self._bias / 40.0) * bar_max_w)
        pygame.draw.rect(surface, (40, 40, 50), (sx, sy, bar_max_w, 18), border_radius=3)
        if bar_w > 0:
            pygame.draw.rect(surface, bias_col, (sx, sy, bar_w, 18), border_radius=3)
        sy += 30

        acc_s = f13.render(f"Dokladnosc: {self._accuracy * 100:.0f}%", True, _WHITE)
        surface.blit(acc_s, (sx, sy))
        sy += 40

        if self._trained and self._round == 1 and "zip_code" not in self._removed:
            hint_s = f11.render(_HINT_ZIP, True, _ORANGE)
            surface.blit(hint_s, (sx, sy))
            sy += 22
        elif not self._trained and self._round == 2:
            hint_s = f11.render(_HINT_DEBT, True, _ORANGE)
            surface.blit(hint_s, (sx, sy))
            sy += 22

        if self._trained:
            reveal = _REVEAL[self._round - 1]
            rv_s = f11.render(reveal, True, _DIM)
            surface.blit(rv_s, (sx, sy + 10))

        if not self._trained:
            pygame.draw.rect(surface, _C_ENG, _TRAIN_BTN, border_radius=8)
            tl = get_font(18).render("TRENUJ", True, (0, 0, 0))
            surface.blit(
                tl,
                (
                    _TRAIN_BTN.x + _TRAIN_BTN.w // 2 - tl.get_width() // 2,
                    _TRAIN_BTN.y + _TRAIN_BTN.h // 2 - tl.get_height() // 2,
                ),
            )

        if self._show_advance:
            sp = f11.render("SPACJA -- nastepna runda", True, (80, 80, 100))
            surface.blit(sp, (_W // 2 - sp.get_width() // 2, _H - 40))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
