from __future__ import annotations

import csv
import datetime
import enum
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

import pygame

from cognitive_data_arcade.engine import audio
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.visual_search.config import (
    FEEDBACK_MS,
    FIXATION_MS,
    ITI_MS,
    TIMEOUT_MS,
    VSConfig,
)
from cognitive_data_arcade.games.visual_search.stimuli import (
    Item,
    draw_item,
    generate_items,
)
from cognitive_data_arcade.profile.manager import ProfileManager

_W, _H = 1024, 768
_BG    = (15, 15, 35)
_WHITE  = (240, 240, 240)
_DIM    = (120, 120, 160)
_GREEN  = (39, 174, 96)
_RED    = (231, 76, 60)
_ORANGE = (243, 156, 18)
_LETTER_SIZE_PT = 38


class _Phase(enum.Enum):
    FIXATION    = "fixation"
    SEARCH      = "search"
    FEEDBACK    = "feedback"
    ITI         = "iti"
    BLOCK_BREAK = "block_break"
    SUMMARY     = "summary"
    DONE        = "done"


@dataclass(frozen=True)
class _TrialRecord:
    participant_id: str
    session_id: str
    trial_id: int
    mode: str
    condition: str
    set_size: int
    target_present: bool
    response: str      # "present" | "absent" | "timeout"
    correct: bool
    rt_ms: float       # float("nan") on timeout
    timestamp: str


def _generate_block(trials_per_block: int, condition: str) -> list[dict]:
    half = trials_per_block // 2
    trials: list[dict] = (
        [{"condition": condition, "target_present": True}]  * half +
        [{"condition": condition, "target_present": False}] * half
    )
    random.shuffle(trials)
    return trials


def _write_trial(csv_path: Path, record: _TrialRecord) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not csv_path.exists()
    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(record).keys()))
        if write_header:
            writer.writeheader()
        writer.writerow(asdict(record))


class VisualSearchGame(Scene):
    def __init__(
        self,
        config: VSConfig,
        pm: ProfileManager,
        strings: Strings,
        participant_id: str,
        session_id: str,
        csv_path: Path,
    ) -> None:
        self._config = config
        self._pm = pm
        self._strings = strings
        self._pid = participant_id
        self._sid = session_id
        self._csv_path = csv_path

        self._rng = random.Random()
        feature_block = _generate_block(config.trials_per_block, "feature")
        conjunction_block = _generate_block(config.trials_per_block, "conjunction")
        self._trials: list[dict] = feature_block + conjunction_block
        self._trial_idx: int = 0
        self._records: list[_TrialRecord] = []

        self._phase = _Phase.FIXATION
        self._phase_timer: float = 0.0
        self._rt_start: int = 0
        self._current_items: list[Item] = []
        self._last_correct: bool = False
        self._last_rt: float = 0.0
        self._next_scene_cache: Optional[Scene] = None

        self._font_fix  = get_font(60)
        self._font_fb   = get_font(48)
        self._font_info = get_font(24)
        self._font_stim = get_font(_LETTER_SIZE_PT)
        self._font_sum  = get_font(28)

        self._load_trial()

    def _load_trial(self) -> None:
        if self._trial_idx >= len(self._trials):
            return
        t = self._trials[self._trial_idx]
        self._current_items = generate_items(
            self._config.mode,
            t["condition"],
            t["target_present"],
            self._config.set_size,
            self._rng,
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if self._phase == _Phase.SEARCH:
            if event.key == pygame.K_f:
                self._respond("absent")
            elif event.key == pygame.K_j:
                self._respond("present")
        elif self._phase == _Phase.BLOCK_BREAK:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._phase = _Phase.ITI
                self._phase_timer = 0.0
        elif self._phase == _Phase.SUMMARY:
            if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                self._phase = _Phase.DONE

    def update(self, dt_ms: float) -> None:
        if self._phase in (_Phase.BLOCK_BREAK, _Phase.SUMMARY, _Phase.DONE):
            return
        self._phase_timer += dt_ms
        if self._phase == _Phase.FIXATION and self._phase_timer >= FIXATION_MS:
            self._phase = _Phase.SEARCH
            self._phase_timer = 0.0
            self._rt_start = pygame.time.get_ticks()
        elif self._phase == _Phase.SEARCH and self._phase_timer >= TIMEOUT_MS:
            self._respond("timeout")
        elif self._phase == _Phase.FEEDBACK and self._phase_timer >= FEEDBACK_MS:
            self._after_feedback()
        elif self._phase == _Phase.ITI and self._phase_timer >= ITI_MS:
            self._phase = _Phase.FIXATION
            self._phase_timer = 0.0

    def _respond(self, response: str) -> None:
        t = self._trials[self._trial_idx]
        if response == "timeout":
            rt_ms = float("nan")
            correct = not t["target_present"]
        else:
            rt_ms = float(pygame.time.get_ticks() - self._rt_start)
            expected = "present" if t["target_present"] else "absent"
            correct = (response == expected)

        record = _TrialRecord(
            participant_id=self._pid,
            session_id=self._sid,
            trial_id=self._trial_idx + 1,
            mode=self._config.mode,
            condition=t["condition"],
            set_size=self._config.set_size,
            target_present=t["target_present"],
            response=response,
            correct=correct,
            rt_ms=rt_ms,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        )
        self._records.append(record)
        _write_trial(self._csv_path, record)
        self._last_correct = correct
        self._last_rt = rt_ms
        audio.play_sfx("correct" if correct else "wrong")
        self._trial_idx += 1
        self._phase = _Phase.FEEDBACK
        self._phase_timer = 0.0

    def _after_feedback(self) -> None:
        n = self._config.trials_per_block
        if self._trial_idx >= len(self._trials):
            self._phase = _Phase.SUMMARY
        elif self._trial_idx == n:
            self._phase = _Phase.BLOCK_BREAK
            self._phase_timer = 0.0
        else:
            self._phase = _Phase.ITI
            self._phase_timer = 0.0
            self._load_trial()

    def is_done(self) -> bool:
        return self._phase == _Phase.DONE

    def next_scene(self) -> Scene | None:
        if not self.is_done():
            return None
        if self._next_scene_cache is None:
            from cognitive_data_arcade.ui.menu import LessonMenuScene
            self._next_scene_cache = LessonMenuScene(self._pm, self._strings)
        return self._next_scene_cache

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        cx, cy = _W // 2, _H // 2

        if self._phase == _Phase.FIXATION:
            fix = self._font_fix.render("+", True, _WHITE)
            surface.blit(fix, (cx - fix.get_width() // 2, cy - fix.get_height() // 2))

        elif self._phase == _Phase.SEARCH:
            for item in self._current_items:
                draw_item(surface, item, self._font_stim)
            hint = self._font_info.render("F = brak   J = jest", True, _DIM)
            surface.blit(hint, (cx - hint.get_width() // 2, _H - 40))

        elif self._phase == _Phase.FEEDBACK:
            symbol = "OK" if self._last_correct else "X"
            color  = _GREEN if self._last_correct else _RED
            rt_text = f"{self._last_rt:.0f} ms" if not math.isnan(self._last_rt) else "limit czasu"
            fb = self._font_fb.render(f"{symbol}  {rt_text}", True, color)
            surface.blit(fb, (cx - fb.get_width() // 2, cy - fb.get_height() // 2))

        elif self._phase == _Phase.BLOCK_BREAK:
            done  = self._trial_idx
            total = len(self._trials)
            msg  = self._font_fb.render(f"Koniec bloku 1 - {done}/{total}", True, _WHITE)
            hint = self._font_info.render("Teraz szukanie zlezone. ENTER aby kontynuowac.", True, _DIM)
            surface.blit(msg,  (cx - msg.get_width() // 2, cy - 40))
            surface.blit(hint, (cx - hint.get_width() // 2, cy + 40))

        elif self._phase == _Phase.SUMMARY:
            self._draw_summary(surface)

        if self._phase not in (_Phase.SUMMARY, _Phase.DONE):
            prog = self._trial_idx / max(len(self._trials), 1)
            pygame.draw.rect(surface, _DIM,    (0, _H - 4, _W, 4))
            pygame.draw.rect(surface, _ORANGE, (0, _H - 4, int(_W * prog), 4))

    def _draw_summary(self, surface: pygame.Surface) -> None:
        cx = _W // 2
        y  = 100
        title = self._font_fb.render("Wyniki sesji", True, _WHITE)
        surface.blit(title, (cx - title.get_width() // 2, y))
        y += 70

        col_rt  = cx - 60
        col_acc = cx + 120
        surface.blit(self._font_info.render("Warunek", True, _DIM),    (cx - 260, y))
        surface.blit(self._font_info.render("Sredni RT", True, _DIM),  (col_rt,   y))
        surface.blit(self._font_info.render("Trafnosc", True, _DIM),   (col_acc,  y))
        y += 40

        for condition, label in (("feature", "Feature (proste)"), ("conjunction", "Zlezone")):
            rts = [
                r.rt_ms for r in self._records
                if r.condition == condition and r.correct and not math.isnan(r.rt_ms)
            ]
            trials_cond = [r for r in self._records if r.condition == condition]
            n_correct = sum(1 for r in trials_cond if r.correct)
            n_total   = len(trials_cond)
            mean_rt   = sum(rts) / len(rts) if rts else 0.0
            acc_pct   = 100.0 * n_correct / n_total if n_total else 0.0

            lbl   = self._font_sum.render(label, True, _WHITE)
            rt_s  = self._font_sum.render(f"{mean_rt:.0f} ms", True, _ORANGE)
            acc_s = self._font_sum.render(f"{acc_pct:.0f} %",  True, _ORANGE)
            surface.blit(lbl,   (cx - 260, y))
            surface.blit(rt_s,  (col_rt,   y))
            surface.blit(acc_s, (col_acc,  y))
            y += 50

        hint = self._font_info.render("ENTER / ESC - wyjdz", True, _DIM)
        surface.blit(hint, (cx - hint.get_width() // 2, y + 40))
