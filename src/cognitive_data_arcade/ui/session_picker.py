from __future__ import annotations

import csv
import datetime
from dataclasses import dataclass
from pathlib import Path

import pygame

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import ProfileManager

_BG = (10, 10, 20)
_ROW_BG = (14, 14, 32)
_ROW_ACTIVE_BG = (20, 20, 50)
_BORDER = (42, 42, 80)
_ORANGE = (243, 156, 18)
_WHITE = (240, 240, 240)
_DIM = (100, 100, 150)
_GREEN = (39, 174, 96)

_TOP_H = 44
_FOOTER_H = 30
_ROW_H = 64
_PAD_X = 20
_N_BINS = 8
_BAR_W = 5
_BAR_GAP = 2


@dataclass
class _SessionEntry:
    csv_path: Path
    date_str: str
    avg_rt: float
    accuracy: float
    n_trials: int
    n_correct: int
    bins: list[float]  # normalised bar heights [0.0–1.0], length == _N_BINS


class SessionPickerScene(Scene):
    def __init__(
        self,
        sessions_dir: Path,
        strings: Strings,
        profile_manager: ProfileManager,
    ) -> None:
        self._sessions_dir = sessions_dir
        self._strings = strings
        self._pm = profile_manager
        self._selected = 0
        self._done = False
        self._next: Scene | None = None
        pygame.font.init()
        self._font_title = pygame.font.SysFont(None, 32)
        self._font_row = pygame.font.SysFont(None, 24)
        self._font_hint = pygame.font.SysFont(None, 24)
        self._sessions = self._load_sessions()

    # ── data loading ──────────────────────────────────────────────────────────

    def _load_sessions(self) -> list[_SessionEntry]:
        if not self._sessions_dir.exists():
            return []
        paths = sorted(
            self._sessions_dir.glob("*.csv"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        entries: list[_SessionEntry] = []
        for path in paths:
            try:
                entries.append(self._parse(path))
            except Exception:
                pass
        return entries

    def _parse(self, path: Path) -> _SessionEntry:
        with path.open(encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        if not rows:
            raise ValueError("empty")
        rts = [
            float(r["reaction_time_ms"])
            for r in rows
            if float(r["reaction_time_ms"]) > 0
        ]
        n_trials = len(rows)
        n_correct = sum(1 for r in rows if str(r["correct"]).lower() in ("true", "1"))
        avg_rt = sum(rts) / len(rts) if rts else 0.0
        accuracy = n_correct / n_trials if n_trials else 0.0
        date_str = datetime.datetime.fromtimestamp(path.stat().st_mtime).strftime(
            "%Y-%m-%d"
        )
        return _SessionEntry(
            csv_path=path,
            date_str=date_str,
            avg_rt=avg_rt,
            accuracy=accuracy,
            n_trials=n_trials,
            n_correct=n_correct,
            bins=self._bins(rts),
        )

    def _bins(self, rts: list[float]) -> list[float]:
        if not rts:
            return [0.0] * _N_BINS
        lo, hi = min(rts), max(rts)
        if lo == hi:
            return [1.0] + [0.0] * (_N_BINS - 1)
        span = hi - lo
        counts = [0] * _N_BINS
        for rt in rts:
            idx = min(int((rt - lo) / span * _N_BINS), _N_BINS - 1)
            counts[idx] += 1
        peak = max(counts) or 1
        return [c / peak for c in counts]

    # ── Scene interface ───────────────────────────────────────────────────────

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_UP:
            self._selected = max(0, self._selected - 1)
        elif event.key == pygame.K_DOWN:
            self._selected = min(max(0, len(self._sessions) - 1), self._selected + 1)
        elif event.key == pygame.K_RETURN and self._sessions:
            self._open_analysis()
        elif event.key == pygame.K_ESCAPE:
            self._done = True

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        if not self._done:
            return None
        if self._next is not None:
            return self._next
        from cognitive_data_arcade.ui.menu import LessonMenuScene

        return LessonMenuScene(self._pm, self._strings)

    # ── private helpers ───────────────────────────────────────────────────────

    def _open_analysis(self) -> None:
        from cognitive_data_arcade.analytics.rt_analysis import (
            build_histogram,
            load_session,
            session_stats,
        )
        from cognitive_data_arcade.engine.chart import figure_to_surface
        from cognitive_data_arcade.ui.analysis_scene import AnalysisScene

        entry = self._sessions[self._selected]
        df = load_session(entry.csv_path)
        stats = session_stats(df)
        fig = build_histogram(df)
        chart = figure_to_surface(fig, (680, 550))
        self._next = AnalysisScene(chart, stats, self._strings, back_scene=self)
        self._done = True

    # ── draw ─────────────────────────────────────────────────────────────────

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        w, h = surface.get_size()

        title = self._font_title.render(self._strings.picker_title, True, _WHITE)
        surface.blit(title, (14, 10))
        pygame.draw.line(surface, _BORDER, (0, _TOP_H), (w, _TOP_H))

        if not self._sessions:
            msg = self._font_row.render(self._strings.picker_no_sessions, True, _DIM)
            surface.blit(msg, (w // 2 - msg.get_width() // 2, h // 2))
        else:
            self._draw_rows(surface, w)

        hint = self._font_hint.render("↑↓  ENTER  ESC", True, _DIM)
        surface.blit(hint, (w - hint.get_width() - 14, h - _FOOTER_H))

    def _draw_rows(self, surface: pygame.Surface, w: int) -> None:
        mini_total = _N_BINS * (_BAR_W + _BAR_GAP)
        mini_x0 = w - mini_total - _PAD_X

        for i, entry in enumerate(self._sessions):
            y = _TOP_H + i * _ROW_H
            active = i == self._selected
            pygame.draw.rect(
                surface, _ROW_ACTIVE_BG if active else _ROW_BG, (0, y, w, _ROW_H - 1)
            )
            if active:
                pygame.draw.rect(surface, _ORANGE, (0, y, 3, _ROW_H - 1))

            # Date + avg RT
            date_s = self._font_row.render(entry.date_str, True, _DIM)
            surface.blit(date_s, (_PAD_X, y + 8))

            rt_color = _GREEN if 0 < entry.avg_rt < 300 else _ORANGE
            rt_s = self._font_row.render(f"{entry.avg_rt:.0f} ms", True, rt_color)
            surface.blit(rt_s, (_PAD_X + 120, y + 8))

            acc_s = self._font_row.render(f"{entry.accuracy:.0%}", True, _WHITE)
            surface.blit(acc_s, (_PAD_X + 230, y + 8))

            trials_s = self._font_row.render(
                f"{entry.n_correct}/{entry.n_trials}", True, _DIM
            )
            surface.blit(trials_s, (_PAD_X + 120, y + 34))

            # Mini-bars (pygame-native)
            bar_area_h = _ROW_H - 16
            for j, height in enumerate(entry.bins):
                bx = mini_x0 + j * (_BAR_W + _BAR_GAP)
                bh = max(2, int(bar_area_h * height))
                pygame.draw.rect(
                    surface,
                    _ORANGE,
                    (bx, y + 8 + bar_area_h - bh, _BAR_W, bh),
                )
