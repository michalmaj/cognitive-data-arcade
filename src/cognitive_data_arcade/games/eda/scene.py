# src/cognitive_data_arcade/games/eda/scene.py
from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
)
from cognitive_data_arcade.engine.colors import (
    DIM as _DIM,
)
from cognitive_data_arcade.engine.colors import (
    WHITE as _WHITE,
)
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.eda.simulator import simulate
from cognitive_data_arcade.games.eda.ui_controls import ControlPanel
from cognitive_data_arcade.games.eda.ui_results import ChartPanel, ResultsPanel

if TYPE_CHECKING:
    from cognitive_data_arcade.engine.i18n import Strings
    from cognitive_data_arcade.profile.manager import ProfileManager

_ACTIVE = (243, 156, 18)

_PANEL_X, _PANEL_Y = 60, 30
_PANEL_W, _PANEL_H = 680, 530
_VISIBLE_LINES = 24

_LEGEND_LINES: list[tuple[str, bool]] = [
    ("LEGENDA SUWAKÓW", True),
    ("", False),
    ("N — UCZESTNICY", True),
    ("Liczba uczestników na warunek.", False),
    ("Większe N = bardziej stabilne wyniki.", False),
    ("Typowy zakres: 10-30 w lab, 100+ online.", False),
    ("", False),
    ("BAZOWY RT (ms)", True),
    ("Średni czas reakcji w warunku 1 (bez efektu).", False),
    ("Typowo: 300-500 ms dla prostego RT.", False),
    ("Stroop / Flanker mogą być wolniejsze.", False),
    ("", False),
    ("RÓŻNICA EFEKTU (ms)", True),
    ("O ile ms wolniejszy jest warunek 2 od warunku 1.", False),
    ("To jest efekt który chcesz wykryć.", False),
    ("Mały efekt: < 20 ms. Duży: > 80 ms.", False),
    ("", False),
    ("SZUM / SD (ms)", True),
    ("Odchylenie standardowe rozkładu RT.", False),
    ("Im większy szum względem efektu, tym trudniej", False),
    ("wykryć różnicę. Typowo: 60-120 ms w lab.", False),
    ("", False),
    ("% OUTLIERÓW", True),
    ("Odsetek prób z 'luką uwagową' (800-1500 ms).", False),
    ("Outliery zaburzają średnią i t-test.", False),
    ("Porównaj linię pełną/przerywaną na histogramie.", False),
    ("", False),
    ("Zamknij: naciśnij L", False),
]

_HELP_LINES: list[tuple[str, bool]] = [
    ("EDA SANDBOX — POMOC", True),
    ("", False),
    ("Co to jest?", True),
    ("Wcielasz się w badacza projektującego eksperyment RT.", False),
    ("RT (czas reakcji) mierzy jak szybko uczestnik", False),
    ("odpowiada na bodziec. Dwa warunki = dwa zestawy prób.", False),
    ("Cel: sprawdzić czy warunki różnią się RT.", False),
    ("", False),
    ("Pętla badania:", True),
    ("1. Postaw hipotezę: wpisz próg różnicy (ms)", False),
    ("2. Ustaw parametry suwakami (N, efekt, szum...)", False),
    ("3. Kliknij GENERUJ lub naciśnij ENTER", False),
    ("4. Sprawdź wyniki — potwierdzona czy obalona?", False),
    ("5. Zmodyfikuj parametry i powtórz.", False),
    ("", False),
    ("Histogramy — jak czytać?", True),
    ("Każdy histogram = rozkład RT w jednym warunku.", False),
    ("Oś X = czas reakcji (ms). Oś Y = liczba prób.", False),
    ("Szerokość histogramu = szum (SD).", False),
    ("Przesunięcie średnich = efekt.", False),
    ("Pełna biała linia = średnia z outlierami.", False),
    ("Przerywana biała linia = średnia bez outlierów.", False),
    ("Pomarańczowe słupki = outliery (800-1500 ms).", False),
    ("", False),
    ("Efekt vs. szum — kluczowa intuicja:", True),
    ("Cohen's d = efekt / szum.", False),
    ("d = 0.2: mały efekt (trudno wykryć).", False),
    ("d = 0.5: średni efekt.", False),
    ("d = 0.8: duży efekt (łatwo wykryć).", False),
    ("Jeśli szum = 80 ms i efekt = 40 ms, d = 0.5.", False),
    ("Zwiększ N żeby wykryć mały efekt przy dużym szumie.", False),
    ("", False),
    ("t-statistic i p-value:", True),
    ("t = różnica średnich / błąd standardowy.", False),
    ("Większe |t| = grupy bardziej się różnią względem szumu.", False),
    ("p = prawdopodob. uzysk. takiego wyniku GDY efekt = 0.", False),
    ("p < 0.05 = istotny statystycznie (konwencja APA).", False),
    ("Uwaga: p > 0.05 NIE znaczy 'brak efektu'.", False),
    ("Może znaczyć: za mało uczestników (za małe N).", False),
    ("", False),
    ("Outliery i ich wpływ:", True),
    ("Outliery zaburzają średnią i zwiększają wariancję.", False),
    ("Jeden outlier 1500 ms może przesunąć średnią", False),
    ("o kilkadziesiąt ms przy N=10.", False),
    ("t-test na surowych danych uwzględnia outliery —", False),
    ("dlatego t jest mniej czuły gdy outliery są obecne.", False),
    ("Porównaj linię pełną / przerywaną na histogramie.", False),
    ("", False),
    ("Praktyczne wskazówki:", True),
    ("- Zacznij od N=20, efekt=50, szum=80, outl=5%.", False),
    ("- Zwiększ N do 100: wyniki bardziej stabilne.", False),
    ("- Ustaw efekt=0: p powinna być losowa (false pos.).", False),
    ("- Zwiększ outliery do 20%: obserwuj co dzieje się", False),
    ("  z linią pełną vs przerywaną na histogramie.", False),
    ("", False),
    ("Klawisze:", True),
    ("ENTER / klik GENERUJ — generuj nowe dane", False),
    ("TAB — następny suwak", False),
    ("LEWO / PRAWO — zmień wartość suwaka", False),
    ("L — legenda suwaków", False),
    ("H — ta pomoc", False),
    ("ESC — menu pauzy", False),
    ("", False),
    ("(przewijaj kółkiem myszy)", False),
]


class EDAScene(Scene):
    def __init__(self, pm: ProfileManager | None = None, strings: Strings | None = None) -> None:
        self._pm = pm
        self._strings = strings
        self._generate_count: int = 0
        self._done: bool = False
        self._next: Scene | None = None
        self._controls = ControlPanel()
        self._charts = ChartPanel()
        self._results = ResultsPanel()
        self._show_legend: bool = False
        self._show_help: bool = False
        self._help_scroll: int = 0
        self._show_summary: bool = False
        self._summary_timer: float = 0.0
        self._session_start_ms: int = pygame.time.get_ticks()

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._show_summary:
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                self._summary_timer = 10_001
                self._done = True
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self._show_summary = True
                self._summary_timer = 0.0
                return
            if event.key == pygame.K_l:
                self._show_legend = not self._show_legend
                if self._show_legend:
                    self._show_help = False
                return
            if event.key == pygame.K_h:
                self._show_help = not self._show_help
                if self._show_help:
                    self._show_legend = False
                    self._help_scroll = 0
                return

        if event.type == pygame.MOUSEWHEEL and self._show_help:
            max_scroll = max(0, len(_HELP_LINES) - _VISIBLE_LINES)
            self._help_scroll = max(0, min(max_scroll, self._help_scroll - event.y))
            return

        if self._show_legend or self._show_help:
            return

        action = self._controls.handle_event(event)
        if action == "generate":
            self._generate_count += 1
            params = self._controls.get_params()
            threshold = self._controls.get_hypothesis_threshold()
            result = simulate(**params)
            self._charts.update(result)
            self._results.update(result, threshold)

    def update(self, dt_ms: float) -> None:
        if self._show_summary:
            self._summary_timer += dt_ms
            if self._summary_timer >= 10_000:
                self._done = True
            return

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        self._controls.draw(surface)
        self._charts.draw(surface, x=360, y=55)
        self._results.draw(surface, x=360, y=310)
        self._draw_key_hints(surface)
        if self._show_summary:
            self._draw_summary(surface)
        elif self._show_legend:
            self._draw_overlay(surface, _LEGEND_LINES, scroll=0)
        elif self._show_help:
            self._draw_overlay(surface, _HELP_LINES, scroll=self._help_scroll)

    def _draw_key_hints(self, surface: pygame.Surface) -> None:
        font = get_font(16)
        x = 30
        y = surface.get_height() - 28
        for key, label in (("L", "legenda"), ("H", "pomoc")):
            k = font.render(f"[{key}]", True, _ACTIVE)
            lb = font.render(f" {label}   ", True, _DIM)
            surface.blit(k, (x, y))
            x += k.get_width()
            surface.blit(lb, (x, y))
            x += lb.get_width()

    def _draw_overlay(
        self,
        surface: pygame.Surface,
        lines: list[tuple[str, bool]],
        scroll: int,
    ) -> None:
        dim = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 180))
        surface.blit(dim, (0, 0))

        panel = pygame.Surface((_PANEL_W, _PANEL_H), pygame.SRCALPHA)
        panel.fill((15, 15, 35, 245))
        surface.blit(panel, (_PANEL_X, _PANEL_Y))
        pygame.draw.rect(
            surface, _ACTIVE, (_PANEL_X, _PANEL_Y, _PANEL_W, _PANEL_H), 2, border_radius=8
        )

        font_hdr = get_font(20)
        font_body = get_font(18)
        y = _PANEL_Y + 18
        surface.set_clip(pygame.Rect(_PANEL_X + 2, _PANEL_Y + 2, _PANEL_W - 14, _PANEL_H - 4))
        for text, is_header in lines[scroll : scroll + _VISIBLE_LINES]:
            if not text:
                y += 8
                continue
            f = font_hdr if is_header else font_body
            color = _ACTIVE if is_header else _WHITE
            surface.blit(f.render(text, True, color), (_PANEL_X + 20, y))
            y += f.size("A")[1] + (6 if is_header else 2)
        surface.set_clip(None)

        max_scroll = max(0, len(lines) - _VISIBLE_LINES)
        if max_scroll > 0:
            pct = scroll / max_scroll
            bar_x = _PANEL_X + _PANEL_W - 10
            bar_y = _PANEL_Y + 10
            bar_h = _PANEL_H - 20
            thumb_h = max(20, round(_VISIBLE_LINES / len(lines) * bar_h))
            thumb_y = bar_y + round(pct * (bar_h - thumb_h))
            pygame.draw.rect(surface, (42, 42, 80), (bar_x, bar_y, 6, bar_h), border_radius=3)
            pygame.draw.rect(surface, _DIM, (bar_x, thumb_y, 6, thumb_h), border_radius=3)

    def _draw_summary(self, surface: pygame.Surface) -> None:
        w, h = surface.get_width(), surface.get_height()
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))

        panel_w, panel_h = 560, 280
        px = (w - panel_w) // 2
        py = (h - panel_h) // 2
        pygame.draw.rect(surface, (14, 14, 36), (px, py, panel_w, panel_h), border_radius=10)
        pygame.draw.rect(surface, (70, 70, 130), (px, py, panel_w, panel_h), 2, border_radius=10)

        elapsed_s = (pygame.time.get_ticks() - self._session_start_ms) // 1000
        mins, secs = divmod(elapsed_s, 60)
        sims = self._generate_count

        font_h = get_font(24)
        font_b = get_font(20)
        font_hint = get_font(14)
        lines = [
            ("Podsumowanie sesji", font_h, (200, 200, 240)),
            (f"Czas sesji: {mins}m {secs}s", font_b, (160, 160, 200)),
            (f"Symulacji wykonanych: {sims}", font_b, (160, 160, 200)),
            ("", font_b, (0, 0, 0)),
            ("Nacisnij dowolny klawisz lub kliknij", font_hint, (90, 90, 120)),
        ]
        y = py + 20
        for text, font, color in lines:
            if not text:
                y += 10
                continue
            s = font.render(text, True, color)
            surface.blit(s, (px + panel_w // 2 - s.get_width() // 2, y))
            y += font.get_height() + 8

    def _build_next_scene(self) -> Scene:
        from cognitive_data_arcade.engine.badges import BadgeEngine, SessionResult
        from cognitive_data_arcade.ui.session_summary import SessionSummaryScene

        ap = min(100, 30 + self._generate_count * 5)
        session = SessionResult(
            task_name="eda_sandbox",
            participant_id=self._pm.load().device_uuid,  # type: ignore[union-attr]
            session_id="eda_session",
            total_trials=self._generate_count,
            correct_trials=self._generate_count,
            avg_reaction_time_ms=0.0,
            min_reaction_time_ms=0.0,
            max_reaction_time_ms=0.0,
            arcade_points_earned=ap,
            science_points_earned=0,
        )
        profile_before = self._pm.load()  # type: ignore[union-attr]
        badge_engine = BadgeEngine()
        new_badge_ids = badge_engine.evaluate(session, profile_before)
        self._pm.add_ap(session.arcade_points_earned)  # type: ignore[union-attr]
        for bid in new_badge_ids:
            self._pm.award_badge(bid)  # type: ignore[union-attr]
        profile_after = self._pm.load()  # type: ignore[union-attr]
        return SessionSummaryScene(
            session=session,
            new_badge_ids=new_badge_ids,
            profile_before=profile_before,
            profile_after=profile_after,
            strings=self._strings,  # type: ignore[arg-type]
            profile_manager=self._pm,  # type: ignore[arg-type]
        )

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        if self._done and self._next is None and self._pm is not None:
            self._next = self._build_next_scene()
        return self._next if self._done else None
