# src/cognitive_data_arcade/games/flanker/game.py
from __future__ import annotations

import csv
import datetime
import enum
import random
from dataclasses import asdict, dataclass
from pathlib import Path

import pygame

from cognitive_data_arcade.engine.badges import BadgeEngine, SessionResult
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.flanker.config import FlankerConfig
from cognitive_data_arcade.profile.manager import ProfileManager

_BG = (10, 10, 20)
_WHITE = (240, 240, 240)
_DIM = (70, 70, 112)
_ORANGE = (243, 156, 18)
_RED = (231, 76, 60)
_GREEN = (39, 174, 96)
_W, _H = 1024, 768


class _Phase(enum.Enum):
    ITI = "iti"
    FIXATION = "fixation"
    STIMULUS = "stimulus"
    FEEDBACK = "feedback"
    BETWEEN_BLOCKS = "between_blocks"
    DONE = "done"


@dataclass(frozen=True)
class _TrialRecord:
    participant_id: str
    session_id: str
    trial_id: int
    task_name: str
    condition: str
    target_direction: str
    correct: bool
    reaction_time_ms: float
    timestamp: str


def _generate_trials(config: FlankerConfig) -> list[dict]:
    per_combo = config.num_trials // 4
    trials: list[dict] = []
    for condition in ("congruent", "incongruent"):
        for direction in ("left", "right"):
            for _ in range(per_combo):
                trials.append({"condition": condition, "target_direction": direction})
    random.shuffle(trials)
    return trials


def _write_trial(path: Path, record: _TrialRecord) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(record).keys()))
        if write_header:
            writer.writeheader()
        writer.writerow(asdict(record))


class FlankerGame(Scene):
    _ARROW_LEFT = "<"
    _ARROW_RIGHT = ">"

    def __init__(
        self,
        config: FlankerConfig,
        profile_manager: ProfileManager,
        strings: Strings,
        participant_id: str,
        session_id: str,
        csv_path: Path,
    ) -> None:
        self._config = config
        self._pm = profile_manager
        self._strings = strings
        self._participant_id = participant_id
        self._session_id = session_id
        self._csv_path = csv_path
        self._trials = _generate_trials(config)
        self._trial_idx = 0
        self._records: list[_TrialRecord] = []
        self._phase = _Phase.ITI
        self._phase_timer = 0.0
        self._iti_duration = float(random.randint(config.iti_min_ms, config.iti_max_ms))
        self._rt_start = 0
        self._last_correct = False
        self._last_rt = 0.0
        self._next_cache: Scene | None = None
        pygame.font.init()
        self._font_arrow = pygame.font.SysFont(None, 110)
        self._font_fix = pygame.font.SysFont(None, 80)
        self._font_fb = pygame.font.SysFont(None, 60)
        self._font_info = pygame.font.SysFont(None, 28)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if self._phase == _Phase.STIMULUS and event.key in (
            pygame.K_LEFT,
            pygame.K_RIGHT,
        ):
            rt_ms = float(pygame.time.get_ticks() - self._rt_start)
            t = self._trials[self._trial_idx]
            expected = (
                pygame.K_LEFT if t["target_direction"] == "left" else pygame.K_RIGHT
            )
            self._complete_trial(event.key == expected, rt_ms)
        elif self._phase == _Phase.BETWEEN_BLOCKS and event.key == pygame.K_SPACE:
            self._enter_iti()

    def update(self, dt_ms: float) -> None:
        if self._phase in (_Phase.BETWEEN_BLOCKS, _Phase.DONE):
            return
        self._phase_timer += dt_ms
        if self._phase == _Phase.ITI and self._phase_timer >= self._iti_duration:
            self._phase = _Phase.FIXATION
            self._phase_timer = 0.0
        elif (
            self._phase == _Phase.FIXATION
            and self._phase_timer >= self._config.fixation_duration_ms
        ):
            self._phase = _Phase.STIMULUS
            self._phase_timer = 0.0
            self._rt_start = pygame.time.get_ticks()
        elif (
            self._phase == _Phase.STIMULUS
            and self._phase_timer >= self._config.stimulus_duration_ms
        ):
            self._complete_trial(False, float(self._config.stimulus_duration_ms))
        elif (
            self._phase == _Phase.FEEDBACK
            and self._phase_timer >= self._config.feedback_duration_ms
        ):
            self._after_feedback()

    def is_done(self) -> bool:
        return self._phase == _Phase.DONE

    def next_scene(self) -> Scene | None:
        if not self.is_done():
            return None
        if self._next_cache is None:
            self._next_cache = self._build_next_scene()
        return self._next_cache

    def _enter_iti(self) -> None:
        self._phase = _Phase.ITI
        self._phase_timer = 0.0
        self._iti_duration = float(
            random.randint(self._config.iti_min_ms, self._config.iti_max_ms)
        )

    def _complete_trial(self, correct: bool, rt_ms: float) -> None:
        t = self._trials[self._trial_idx]
        record = _TrialRecord(
            participant_id=self._participant_id,
            session_id=self._session_id,
            trial_id=self._trial_idx + 1,
            task_name="flanker",
            condition=t["condition"],
            target_direction=t["target_direction"],
            correct=correct,
            reaction_time_ms=rt_ms,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        )
        self._records.append(record)
        _write_trial(self._csv_path, record)
        self._last_correct = correct
        self._last_rt = rt_ms
        self._trial_idx += 1
        self._phase = _Phase.FEEDBACK
        self._phase_timer = 0.0

    def _after_feedback(self) -> None:
        if self._trial_idx >= len(self._trials):
            self._phase = _Phase.DONE
        elif self._trial_idx % self._config.trials_per_block == 0:
            self._phase = _Phase.BETWEEN_BLOCKS
            self._phase_timer = 0.0
        else:
            self._enter_iti()

    def _stimulus_text(self) -> str:
        t = self._trials[self._trial_idx]
        target = (
            self._ARROW_LEFT if t["target_direction"] == "left" else self._ARROW_RIGHT
        )
        flanker = self._ARROW_RIGHT if target == self._ARROW_LEFT else self._ARROW_LEFT
        if t["condition"] == "congruent":
            flanker = target
        return f"{flanker} {flanker} {target} {flanker} {flanker}"

    def _build_next_scene(self) -> Scene:
        from cognitive_data_arcade.ui.session_summary import SessionSummaryScene

        valid_rts = [
            r.reaction_time_ms
            for r in self._records
            if r.reaction_time_ms < self._config.stimulus_duration_ms
        ]
        correct_count = sum(1 for r in self._records if r.correct)
        avg_rt = sum(valid_rts) / len(valid_rts) if valid_rts else 0.0
        min_rt = min(valid_rts) if valid_rts else 0.0
        max_rt = max(valid_rts) if valid_rts else 0.0

        con_rts = [
            r.reaction_time_ms
            for r in self._records
            if r.condition == "congruent"
            and r.correct
            and r.reaction_time_ms < self._config.stimulus_duration_ms
        ]
        inc_rts = [
            r.reaction_time_ms
            for r in self._records
            if r.condition == "incongruent"
            and r.correct
            and r.reaction_time_ms < self._config.stimulus_duration_ms
        ]
        sp = 0
        if con_rts and inc_rts:
            flanker_effect = sum(inc_rts) / len(inc_rts) - sum(con_rts) / len(con_rts)
            accuracy = correct_count / len(self._records)
            if flanker_effect > 50.0 and accuracy >= 0.80:
                sp = self._config.sp_flanker_effect_bonus

        session = SessionResult(
            task_name="flanker",
            participant_id=self._participant_id,
            session_id=self._session_id,
            total_trials=len(self._records),
            correct_trials=correct_count,
            avg_reaction_time_ms=avg_rt,
            min_reaction_time_ms=min_rt,
            max_reaction_time_ms=max_rt,
            arcade_points_earned=correct_count * self._config.ap_per_correct,
            science_points_earned=sp,
        )

        profile_before = self._pm.load()
        badge_engine = BadgeEngine()
        new_badge_ids = badge_engine.evaluate(session, profile_before)
        self._pm.add_ap(session.arcade_points_earned)
        if sp > 0:
            self._pm.add_sp(sp)
        for bid in new_badge_ids:
            self._pm.award_badge(bid)
        profile_after = self._pm.load()

        def _analysis_factory(
            csv_path: Path, strings: Strings, back_scene: Scene
        ) -> Scene:
            from cognitive_data_arcade.ui.flanker_analysis_scene import (
                FlankerAnalysisScene,
            )

            return FlankerAnalysisScene(csv_path, strings, back_scene)

        return SessionSummaryScene(
            session=session,
            new_badge_ids=new_badge_ids,
            profile_before=profile_before,
            profile_after=profile_after,
            strings=self._strings,
            profile_manager=self._pm,
            csv_path=self._csv_path,
            analysis_factory=_analysis_factory,
        )

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        cx, cy = _W // 2, _H // 2
        if self._phase == _Phase.FIXATION:
            fix = self._font_fix.render("+", True, _WHITE)
            surface.blit(fix, (cx - fix.get_width() // 2, cy - fix.get_height() // 2))
        elif self._phase == _Phase.STIMULUS:
            text = self._stimulus_text()
            rendered = self._font_arrow.render(text, True, _WHITE)
            surface.blit(
                rendered,
                (cx - rendered.get_width() // 2, cy - rendered.get_height() // 2),
            )
        elif self._phase == _Phase.FEEDBACK:
            symbol = "OK" if self._last_correct else "X"
            color = _GREEN if self._last_correct else _RED
            fb = self._font_fb.render(f"{symbol}  {self._last_rt:.0f} ms", True, color)
            surface.blit(fb, (cx - fb.get_width() // 2, cy - fb.get_height() // 2))
        elif self._phase == _Phase.BETWEEN_BLOCKS:
            done = self._trial_idx
            total = len(self._trials)
            msg = self._font_fb.render(f"Przerwa  {done}/{total}", True, _WHITE)
            surface.blit(msg, (cx - msg.get_width() // 2, cy - 40))
            hint = self._font_info.render("SPACE aby kontynuowac", True, _DIM)
            surface.blit(hint, (cx - hint.get_width() // 2, cy + 40))
        prog = self._trial_idx / max(len(self._trials), 1)
        pygame.draw.rect(surface, _DIM, (0, _H - 4, _W, 4))
        pygame.draw.rect(surface, _ORANGE, (0, _H - 4, int(_W * prog), 4))
