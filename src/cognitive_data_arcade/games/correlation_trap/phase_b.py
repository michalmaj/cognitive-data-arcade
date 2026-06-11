from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import pygame

from cognitive_data_arcade.engine.chart import figure_to_surface
from cognitive_data_arcade.engine.context_popup import ContextInfo, ContextPopup
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.correlation_trap.simulator import (
    Scenario, generate_correlated, _SCENARIOS,
)

_BG      = (15, 15, 35)
_PANEL   = (18, 18, 42)
_WHITE   = (240, 240, 240)
_DIM     = (120, 120, 160)
_ORANGE  = (243, 156, 18)
_GREEN   = ( 39, 174,  96)
_RED     = (231,  76,  60)
_BLUE    = ( 52, 152, 219)
_FIG_BG  = "#0f0f23"
_AX_BG   = "#1a1a3e"

_AREA_H   = 672
_TOP_H    = 64
_BTN_H    = 40
_BTN_AREA = 56
_SCATTER_W = 716
_SCATTER_H = _AREA_H - _TOP_H - _BTN_AREA - 8
_VERDICT_W = 1024 - _SCATTER_W
_CHART_W   = 700
_CHART_H   = _SCATTER_H - 20
_DPI       = 100

_BTN_W = (1024 - 48) // 3
_BTN_Y = _AREA_H - _BTN_AREA + 8
_BTN_POSITIONS = [16, 16 + _BTN_W + 8, 16 + 2 * (_BTN_W + 8)]

_POPUPS_B: dict[str, ContextInfo] = {
    "scatter": ContextInfo(
        title="Scatter — wykres korelacji",
        body=(
            "r pokazuje sile liniowego zwiazku miedzy zmiennymi.\n"
            "Nie mowi nic o kierunku przyczynowosci!"
        ),
        impact="Wysoka korelacja jest konieczna, ale nie wystarczajaca dla przyczynowosci.",
    ),
    "btn_yes": ContextInfo(
        title="Przyczynowosc (causation)",
        body=(
            "A -> B gdy manipulacja A (eksperyment) zmienia B.\n"
            "Wymaga: temporalnosc, sila, specyficznosc, koherencja."
        ),
        impact="Tylko eksperymenty z randomizacja (RCT) pozwalaja wnioskowac o przyczynowosci.",
    ),
    "btn_no": ContextInfo(
        title="Korelacja bez przyczynowosci",
        body=(
            "Przyczyny korelacji bez zwiazku przyczynowego:\n"
            "1) Zmienna ukryta  2) Przypadek (male N)  3) Trend czasowy"
        ),
        impact="Liczba obserwacji nie wyklucza zmiennej ukrytej!",
    ),
    "confound_reveal": ContextInfo(
        title="Zmienna ukryta (confounding variable)",
        body=(
            "Trzecia zmienna Z wplywa zarowno na X jak i Y.\n"
            "Powoduje pozorna korelacje X<->Y bez zwiazku przyczynowego."
        ),
        impact="Kontroluj zmienne ukryte przez randomizacje lub dopasowywanie.",
    ),
    "r_display": ContextInfo(
        title="Interpretacja wyswietlanego r",
        body=(
            "Wysoka r NIE dowodzi przyczynowosci.\n"
            "Lody i utonecia maja r=0.88 ale lody nie zabijaja!"
        ),
        impact="Sila korelacji nie informuje o mechanizmie przyczynowym.",
    ),
}


class PhaseBScene(Scene):
    def __init__(self) -> None:
        self._done    = False
        self._idx     = 0
        self._correct = 0
        self._state   = "waiting"   # "waiting" | "revealed" | "summary"
        self._was_correct = False
        self._chart_surf: pygame.Surface | None = None
        self._popup   = ContextPopup()
        self._btn_rects: list[pygame.Rect] = []
        self._load_scenario()

    def _scenario(self) -> Scenario:
        return _SCENARIOS[self._idx]

    def _load_scenario(self) -> None:
        s = self._scenario()
        seed = hash(s.key) & 0xFFFF
        result = generate_correlated(s.r_display, noise=0.0, n=s.n, seed=seed)
        self._chart_surf = _render_chart(result, s.r_display)
        self._state = "waiting"
        self._was_correct = False
        self._build_button_rects()
        self._register_popups()

    def _build_button_rects(self) -> None:
        self._btn_rects = [
            pygame.Rect(_BTN_POSITIONS[i], _BTN_Y, _BTN_W, _BTN_H)
            for i in range(3)
        ]

    def _register_popups(self) -> None:
        self._popup.clear()
        scatter_rect = pygame.Rect(0, _TOP_H, _SCATTER_W, _SCATTER_H)
        r_rect       = pygame.Rect(_SCATTER_W - 90, _TOP_H + 10, 88, 22)
        self._popup.register(scatter_rect,        _POPUPS_B["scatter"])
        self._popup.register(self._btn_rects[0],  _POPUPS_B["btn_yes"])
        self._popup.register(self._btn_rects[1],  _POPUPS_B["btn_no"])
        self._popup.register(r_rect,              _POPUPS_B["r_display"])

    def _answer(self, is_yes: bool) -> None:
        s = self._scenario()
        self._was_correct = (is_yes == s.is_causal)
        if self._was_correct:
            self._correct += 1
        self._state = "revealed"
        confound_rect = pygame.Rect(_SCATTER_W + 4, _TOP_H + 100, _VERDICT_W - 8, 44)
        self._popup.register(confound_rect, _POPUPS_B["confound_reveal"])

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._popup.handle_event(event):
            return
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return
        pos = event.pos
        if self._state == "waiting":
            if self._btn_rects[0].collidepoint(pos):
                self._answer(True)
            elif self._btn_rects[1].collidepoint(pos):
                self._answer(False)
        elif self._state == "revealed":
            if self._btn_rects[2].collidepoint(pos):
                self._idx += 1
                if self._idx >= len(_SCENARIOS):
                    self._state = "summary"
                else:
                    self._load_scenario()
        elif self._state == "summary":
            if self._btn_rects[0].collidepoint(pos):   # restart
                self._idx = 0
                self._correct = 0
                self._load_scenario()

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def draw(self, surface: pygame.Surface, offset_y: int = 0) -> None:
        area = pygame.Surface((1024, _AREA_H))
        area.fill(_BG)

        if self._state == "summary":
            _draw_summary(area, self._correct)
        else:
            self._draw_quiz(area)

        self._popup.draw(area)
        surface.blit(area, (0, offset_y))

    def _draw_quiz(self, area: pygame.Surface) -> None:
        s = self._scenario()
        font_ctr = get_font(14)
        font_claim = get_font(15)
        font_btn = get_font(14)

        # top bar
        pygame.draw.rect(area, (18, 18, 42), (0, 0, 1024, _TOP_H))
        ctr_text = f"{self._idx + 1} / {len(_SCENARIOS)}"
        area.blit(font_ctr.render(ctr_text, True, _ORANGE), (12, 10))
        _blit_wrapped(area, font_claim, s.claim_pl, _WHITE, 70, 10, 1024 - 70 - 12)

        # scatter
        if self._chart_surf:
            area.blit(self._chart_surf, (0, _TOP_H + 4))

        # verdict panel (shown after answering)
        if self._state == "revealed":
            vx = _SCATTER_W
            pygame.draw.rect(area, (18, 18, 42), (vx, _TOP_H, _VERDICT_W, _SCATTER_H))
            pygame.draw.line(area, (46, 46, 96), (vx, _TOP_H), (vx, _TOP_H + _SCATTER_H))
            f14 = get_font(14)
            f13 = get_font(13)
            if s.is_causal:
                verdict_lbl = "Tak! Przyczynowosc"
                verdict_col = _GREEN
            else:
                verdict_lbl = "Pulapka!"
                verdict_col = _RED
            area.blit(f14.render(verdict_lbl, True, verdict_col), (vx + 8, _TOP_H + 12))
            if s.confound_pl:
                area.blit(f13.render("Zmienna ukryta:", True, _ORANGE), (vx + 8, _TOP_H + 38))
                area.blit(f13.render(s.confound_pl, True, _WHITE), (vx + 8, _TOP_H + 58))
            _blit_wrapped(area, f13, s.explanation_pl, _DIM, vx + 8, _TOP_H + 90, _VERDICT_W - 16)
            if self._was_correct:
                area.blit(f14.render("+10 pkt", True, _GREEN), (vx + 8, _TOP_H + _SCATTER_H - 30))

        # buttons
        _draw_button(area, font_btn, "TAK — przyczynowosc", self._btn_rects[0],
                     (26, 74, 42), (39, 174, 96), visible=(self._state == "waiting"))
        _draw_button(area, font_btn, "NIE — pulapka",       self._btn_rects[1],
                     (74, 26, 26), (231, 76, 60), visible=(self._state == "waiting"))
        _draw_button(area, font_btn, "Dalej ->",            self._btn_rects[2],
                     (18, 18, 60), (52, 152, 219), visible=(self._state == "revealed"))


def _draw_summary(area: pygame.Surface, correct: int) -> None:
    font = get_font(22)
    f16  = get_font(16)
    total = len(_SCENARIOS)
    lines = [
        (f"Wynik: {correct} / {total} poprawnych", font, _WHITE),
        ("", f16, _DIM),
        ("Kliknij by zagrac jeszcze raz.", f16, _DIM),
    ]
    y = _AREA_H // 2 - 40
    for line, f, col in lines:
        if not line:
            y += 20
            continue
        tw = f.size(line)[0]
        area.blit(f.render(line, True, col), ((1024 - tw) // 2, y))
        y += 40


def _draw_button(
    surface: pygame.Surface,
    font: pygame.font.Font,
    label: str,
    rect: pygame.Rect,
    bg: tuple,
    border: tuple,
    visible: bool,
) -> None:
    if not visible:
        return
    pygame.draw.rect(surface, bg, rect, border_radius=4)
    pygame.draw.rect(surface, border, rect, 1, border_radius=4)
    tw = font.size(label)[0]
    surface.blit(font.render(label, True, border),
                 (rect.x + (rect.w - tw) // 2, rect.y + (rect.h - font.get_height()) // 2))


def _blit_wrapped(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    color: tuple,
    x: int,
    y: int,
    max_w: int,
) -> None:
    for paragraph in text.split("\n"):
        words = paragraph.split()
        line = ""
        for word in words:
            test = f"{line} {word}".strip()
            if font.size(test)[0] <= max_w:
                line = test
            else:
                if line:
                    surface.blit(font.render(line, True, color), (x, y))
                    y += font.get_height() + 2
                line = word
        if line:
            surface.blit(font.render(line, True, color), (x, y))
            y += font.get_height() + 2


def _render_chart(result, r_display: float) -> pygame.Surface:
    fig, ax = plt.subplots(
        facecolor=_FIG_BG,
        figsize=(_CHART_W / _DPI, _CHART_H / _DPI),
        dpi=_DPI,
    )
    ax.set_facecolor(_AX_BG)
    ax.scatter(result.x, result.y, color="#3498db", alpha=0.65, s=18)
    m = float(r_display * result.y.std() / max(1e-9, result.x.std()))
    b = float(result.y.mean() - m * result.x.mean())
    x_line = [float(result.x.min()), float(result.x.max())]
    ax.plot(x_line, [m * xv + b for xv in x_line],
            color="#f39c12", linestyle="--", alpha=0.6)
    ax.text(0.98, 0.98, f"r = {r_display:+.2f}",
            transform=ax.transAxes, color="#f39c12",
            fontsize=10, va="top", ha="right")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color("#2a2a50")
    return figure_to_surface(fig, (_CHART_W, _CHART_H))
