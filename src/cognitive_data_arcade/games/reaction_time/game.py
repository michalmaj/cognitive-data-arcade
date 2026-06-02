from __future__ import annotations

import csv
import datetime
import enum
from dataclasses import asdict, dataclass
from pathlib import Path

import pygame

from cognitive_data_arcade.engine import audio
from cognitive_data_arcade.engine.badges import BadgeEngine, SessionResult
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.reaction_time.config import ReactionTimeConfig
from cognitive_data_arcade.profile.manager import ProfileManager

# ── colours ──────────────────────────────────────────────────────────────────
_BG = (10, 10, 20)
_TARGET_OFF = (30, 30, 60)
_TARGET_ON = (243, 156, 18)
_DIM_BORDER = (42, 42, 80)
_BRIGHT_BORDER = (243, 156, 18)
_WHITE = (240, 240, 240)
_DIM = (70, 70, 112)
_RED = (231, 76, 60)

# ── layout ────────────────────────────────────────────────────────────────────
_W, _H = 1024, 768
_TARGET_CX, _TARGET_CY = _W // 2, _H // 2
_TARGET_R = 35
_DISTRACTOR_POSITIONS = [(280, 220), (744, 240), (480, 580)]
_PROGRESS_H = 4
_FOOTER_H = 30


class _Phase(enum.Enum):
    INSTRUCTIONS = "instructions"
    COUNTDOWN = "countdown"
    ITI = "iti"
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
    stimulus: str
    expected_response: str
    actual_response: str
    correct: bool
    reaction_time_ms: float
    timestamp: str
    distractor_count: int


def _write_trial(path: Path, record: _TrialRecord) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(record).keys()))
        if write_header:
            writer.writeheader()
        writer.writerow(asdict(record))


def _compute_ap(config: ReactionTimeConfig, correct_trials: int, avg_rt: float) -> int:
    """Return Arcade Points earned from a session. Pure function — no side effects."""
    ap = correct_trials * config.ap_per_correct
    if 0 < avg_rt < config.fast_rt_threshold_ms:
        ap += config.ap_bonus_fast
    if (
        config.num_trials > 0
        and correct_trials / config.num_trials >= config.accuracy_bonus_threshold
    ):
        ap += config.ap_bonus_accurate
    return ap


class ReactionTimeGame(Scene):
    def __init__(
        self,
        config: ReactionTimeConfig,
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

        self._phase = _Phase.INSTRUCTIONS
        self._phase_timer = 0.0
        self._iti_duration = float(config.iti_min_ms)
        self._countdown_val = 3
        self._trial_index = 0
        self._last_rt: float | None = None
        self._early_press = False
        self._records: list[_TrialRecord] = []
        self._next_cache: Scene | None = None

        pygame.font.init()
        self._font_sm = pygame.font.SysFont(None, 26)
        self._font_med = pygame.font.SysFont(None, 36)
        self._font_lg = pygame.font.SysFont(None, 72)
        self._font_hint = pygame.font.SysFont(None, 24)

    # ── Scene interface ───────────────────────────────────────────────────────

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN or event.key != pygame.K_SPACE:
            return
        if self._phase == _Phase.INSTRUCTIONS:
            self._phase = _Phase.COUNTDOWN
            self._phase_timer = 0.0
            self._countdown_val = 3
        elif self._phase == _Phase.ITI:
            self._early_press = True
            self._phase_timer = 0.0
            self._iti_duration = self._rand_iti()
        elif self._phase == _Phase.STIMULUS:
            audio.play_sfx("select")
            self._complete_trial(rt=self._phase_timer, actual="space", correct=True)
        elif self._phase == _Phase.BETWEEN_BLOCKS:
            self._enter_iti()

    def update(self, dt_ms: float) -> None:
        if self._phase in (_Phase.INSTRUCTIONS, _Phase.DONE, _Phase.BETWEEN_BLOCKS):
            return
        self._phase_timer += dt_ms

        if self._phase == _Phase.COUNTDOWN:
            self._countdown_val = max(1, 3 - int(self._phase_timer / 1000.0))
            if self._phase_timer >= 3000.0:
                self._enter_iti()

        elif self._phase == _Phase.ITI:
            if self._phase_timer >= self._iti_duration:
                excess = self._phase_timer - self._iti_duration
                self._early_press = False
                self._phase = _Phase.STIMULUS
                self._phase_timer = excess

        elif self._phase == _Phase.STIMULUS:
            if self._phase_timer >= 10_000.0:
                self._complete_trial(rt=-1.0, actual="none", correct=False)

        elif self._phase == _Phase.FEEDBACK:
            if self._phase_timer >= self._config.feedback_duration_ms:
                self._after_feedback()

    def is_done(self) -> bool:
        return self._phase == _Phase.DONE

    def next_scene(self) -> Scene | None:
        if not self.is_done():
            return None
        if self._next_cache is None:
            self._next_cache = self._build_next_scene()
        return self._next_cache

    # ── internal helpers ──────────────────────────────────────────────────────

    def _rand_iti(self) -> float:
        import random

        return float(random.randint(self._config.iti_min_ms, self._config.iti_max_ms))

    def _enter_iti(self) -> None:
        self._phase = _Phase.ITI
        self._phase_timer = 0.0
        self._early_press = False
        self._iti_duration = self._rand_iti()

    def _complete_trial(self, rt: float, actual: str, correct: bool) -> None:
        record = _TrialRecord(
            participant_id=self._participant_id,
            session_id=self._session_id,
            trial_id=self._trial_index + 1,
            task_name="reaction_time",
            condition="simple",
            stimulus="circle",
            expected_response="space",
            actual_response=actual,
            correct=correct,
            reaction_time_ms=rt,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            distractor_count=self._config.distractor_count,
        )
        self._records.append(record)
        _write_trial(self._csv_path, record)
        self._last_rt = rt if correct else None
        self._trial_index += 1
        self._phase = _Phase.FEEDBACK
        self._phase_timer = 0.0

    def _after_feedback(self) -> None:
        if self._trial_index >= self._config.num_trials:
            self._phase = _Phase.DONE
        elif (
            self._trial_index % self._config.trials_per_block == 0
            and self._trial_index < self._config.num_trials
        ):
            self._phase = _Phase.BETWEEN_BLOCKS
            self._phase_timer = 0.0
        else:
            self._enter_iti()

    def _build_next_scene(self) -> Scene:
        from cognitive_data_arcade.ui.session_summary import SessionSummaryScene

        valid_rts = [
            r.reaction_time_ms for r in self._records if r.reaction_time_ms > 0
        ]
        correct_count = sum(1 for r in self._records if r.correct)
        avg_rt = sum(valid_rts) / len(valid_rts) if valid_rts else 0.0
        min_rt = min(valid_rts) if valid_rts else 0.0
        max_rt = max(valid_rts) if valid_rts else 0.0

        session = SessionResult(
            task_name="reaction_time",
            participant_id=self._participant_id,
            session_id=self._session_id,
            total_trials=self._config.num_trials,
            correct_trials=correct_count,
            avg_reaction_time_ms=avg_rt,
            min_reaction_time_ms=min_rt,
            max_reaction_time_ms=max_rt,
            arcade_points_earned=_compute_ap(self._config, correct_count, avg_rt),
            science_points_earned=0,
        )

        profile_before = self._pm.load()
        badge_engine = BadgeEngine()
        new_badge_ids = badge_engine.evaluate(session, profile_before)

        self._pm.add_ap(session.arcade_points_earned)
        for bid in new_badge_ids:
            self._pm.award_badge(bid)
        profile_after = self._pm.load()

        return SessionSummaryScene(
            session=session,
            new_badge_ids=new_badge_ids,
            profile_before=profile_before,
            profile_after=profile_after,
            strings=self._strings,
            profile_manager=self._pm,
            csv_path=self._csv_path,
        )

    # ── draw ─────────────────────────────────────────────────────────────────

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        w, h = surface.get_size()
        if self._phase == _Phase.INSTRUCTIONS:
            self._draw_instructions(surface, w, h)
        elif self._phase == _Phase.COUNTDOWN:
            self._draw_game_frame(surface, w, h)
            self._draw_countdown(surface, w, h)
        elif self._phase == _Phase.ITI:
            self._draw_game_frame(surface, w, h)
        elif self._phase == _Phase.STIMULUS:
            self._draw_game_frame(surface, w, h, stimulus_on=True)
        elif self._phase == _Phase.FEEDBACK:
            self._draw_game_frame(surface, w, h)
            self._draw_feedback(surface, w, h)
        elif self._phase == _Phase.BETWEEN_BLOCKS:
            self._draw_between_blocks(surface, w, h)

    def _draw_instructions(self, surface: pygame.Surface, w: int, h: int) -> None:
        lines = self._strings.rt_instructions.split("\n")
        y = h // 2 - len(lines) * 22
        for line in lines:
            if line:
                surf = self._font_med.render(line, True, _WHITE)
                surface.blit(surf, (w // 2 - surf.get_width() // 2, y))
            y += 44

    def _draw_countdown(self, surface: pygame.Surface, w: int, h: int) -> None:
        surf = self._font_lg.render(str(self._countdown_val), True, _TARGET_ON)
        surface.blit(
            surf, (w // 2 - surf.get_width() // 2, h // 2 - surf.get_height() // 2)
        )

    def _draw_game_frame(
        self, surface: pygame.Surface, w: int, h: int, stimulus_on: bool = False
    ) -> None:
        # Progress bar
        done = self._trial_index
        total = self._config.num_trials
        pygame.draw.rect(surface, _DIM_BORDER, (0, 0, w, _PROGRESS_H))
        if total > 0:
            fill = int(w * done / total)
            pygame.draw.rect(surface, _TARGET_ON, (0, 0, fill, _PROGRESS_H))

        # Trial counter
        label = self._font_sm.render(
            f"trial {self._trial_index + 1} / {total}", True, _DIM
        )
        surface.blit(label, (14, _PROGRESS_H + 6))

        # Fixation cross (hidden during stimulus)
        if not stimulus_on:
            fix = self._font_med.render("+", True, (60, 60, 100))
            surface.blit(
                fix,
                (_TARGET_CX - fix.get_width() // 2, _TARGET_CY - fix.get_height() // 2),
            )

        # Distractor circles
        for dx, dy in _DISTRACTOR_POSITIONS:
            pygame.draw.circle(surface, _TARGET_OFF, (dx, dy), _TARGET_R)
            pygame.draw.circle(surface, _DIM_BORDER, (dx, dy), _TARGET_R, 1)

        # Target circle
        if stimulus_on:
            pygame.draw.circle(
                surface, (80, 40, 0), (_TARGET_CX, _TARGET_CY), _TARGET_R + 14
            )
            pygame.draw.circle(
                surface, (160, 80, 0), (_TARGET_CX, _TARGET_CY), _TARGET_R + 7
            )
            pygame.draw.circle(surface, _TARGET_ON, (_TARGET_CX, _TARGET_CY), _TARGET_R)
            pygame.draw.circle(
                surface, _BRIGHT_BORDER, (_TARGET_CX, _TARGET_CY), _TARGET_R, 2
            )
        else:
            pygame.draw.circle(
                surface, _TARGET_OFF, (_TARGET_CX, _TARGET_CY), _TARGET_R
            )
            pygame.draw.circle(
                surface, _DIM_BORDER, (_TARGET_CX, _TARGET_CY), _TARGET_R, 1
            )

        # Early press warning
        if self._early_press:
            warn = self._font_med.render(self._strings.rt_too_early, True, _RED)
            surface.blit(warn, (w // 2 - warn.get_width() // 2, _TARGET_CY + 80))

        # Footer hint
        hint = self._font_hint.render(self._strings.rt_hint_space, True, _DIM)
        surface.blit(hint, (w // 2 - hint.get_width() // 2, h - _FOOTER_H))

    def _draw_feedback(self, surface: pygame.Surface, w: int, h: int) -> None:
        if self._last_rt is not None:
            text, color = f"{self._last_rt:.0f} ms", _TARGET_ON
        else:
            text, color = self._strings.rt_too_slow, _RED
        surf = self._font_lg.render(text, True, color)
        surface.blit(surf, (w // 2 - surf.get_width() // 2, _TARGET_CY + 90))

    def _draw_between_blocks(self, surface: pygame.Surface, w: int, h: int) -> None:
        surf = self._font_med.render(self._strings.rt_between_blocks, True, _WHITE)
        surface.blit(
            surf, (w // 2 - surf.get_width() // 2, h // 2 - surf.get_height() // 2)
        )
