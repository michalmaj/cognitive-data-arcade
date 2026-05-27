from __future__ import annotations

import csv
import math
import enum
import random
from dataclasses import asdict, dataclass
from pathlib import Path

import pygame

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.gono.config import GoNoGoConfig
from cognitive_data_arcade.profile.manager import ProfileManager


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
    trial_type: str  # "go" / "nogo"
    response: str  # "hit" / "miss" / "false_alarm" / "correct_rejection"
    correct: bool
    reaction_time_ms: float  # 0.0 if no response
    timestamp: str  # ISO 8601


def _generate_trials(config: GoNoGoConfig) -> list[dict[str, str]]:
    num_blocks = config.num_trials // config.trials_per_block
    go_per_block = round(config.go_ratio * config.trials_per_block)
    nogo_per_block = config.trials_per_block - go_per_block
    trials: list[dict[str, str]] = []
    for _ in range(num_blocks):
        block: list[dict[str, str]] = [{"trial_type": "go"}] * go_per_block + [
            {"trial_type": "nogo"}
        ] * nogo_per_block
        random.shuffle(block)
        trials.extend(block)
    return trials


def _write_trial(csv_path: Path, record: _TrialRecord) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not csv_path.exists()
    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(record).keys()))
        if write_header:
            writer.writeheader()
        writer.writerow(asdict(record))


def _probit(p: float) -> float:
    """Rational approximation of the inverse normal CDF (Abramowitz & Stegun)."""
    c = (2.515517, 0.802853, 0.010328)
    d = (1.432788, 0.189269, 0.001308)
    t = math.sqrt(-2.0 * math.log(p if p <= 0.5 else 1.0 - p))
    num = c[0] + c[1] * t + c[2] * t * t
    den = 1.0 + d[0] * t + d[1] * t * t + d[2] * t * t * t
    z = t - num / den
    return -z if p <= 0.5 else z


class GoNoGoGame(Scene):
    _COLOR_GO = (39, 174, 96)
    _COLOR_NOGO = (231, 76, 60)
    _CIRCLE_RADIUS = 120

    def __init__(
        self,
        config: GoNoGoConfig,
        profile_manager: ProfileManager,
        strings: Strings,
        participant_id: str,
        session_id: str,
        csv_path: Path,
    ) -> None:
        self._config = config
        self._pm = profile_manager
        self._strings = strings
        self._pid = participant_id
        self._sid = session_id
        self._csv_path = csv_path
        self._trials = _generate_trials(config)
        self._trial_idx = 0
        self._phase = _Phase.ITI
        self._phase_timer = 0.0
        self._records: list[_TrialRecord] = []
        self._next: Scene | None = None
        self._responded = False
        self._iti_duration = float(random.randint(config.iti_min_ms, config.iti_max_ms))
        self._profile_before = profile_manager.load()
        pygame.font.init()
        self._font_fix = pygame.font.SysFont(None, 80)
        self._font_fb = pygame.font.SysFont(None, 60)
        self._font_hint = pygame.font.SysFont(None, 28)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if self._phase == _Phase.BETWEEN_BLOCKS and event.key == pygame.K_SPACE:
            self._phase = _Phase.ITI
            self._phase_timer = 0.0
            self._iti_duration = float(
                random.randint(self._config.iti_min_ms, self._config.iti_max_ms)
            )
            return
        if self._phase == _Phase.STIMULUS and event.key == pygame.K_SPACE:
            trial = self._trials[self._trial_idx]
            rt_ms = self._phase_timer
            if trial["trial_type"] == "go":
                self._complete_trial("hit", True, rt_ms)
            else:
                self._complete_trial("false_alarm", False, rt_ms)

    def update(self, dt_ms: float) -> None:
        if self._phase in (_Phase.BETWEEN_BLOCKS, _Phase.DONE):
            return
        self._phase_timer += dt_ms
        if self._phase == _Phase.ITI:
            if self._phase_timer >= self._iti_duration:
                self._phase = _Phase.FIXATION
                self._phase_timer = 0.0
        elif self._phase == _Phase.FIXATION:
            if self._phase_timer >= self._config.fixation_duration_ms:
                self._phase = _Phase.STIMULUS
                self._phase_timer = 0.0
        elif self._phase == _Phase.STIMULUS:
            if self._phase_timer >= self._config.stimulus_duration_ms:
                trial = self._trials[self._trial_idx]
                if trial["trial_type"] == "go":
                    self._complete_trial("miss", False, 0.0)
                else:
                    self._complete_trial("correct_rejection", True, 0.0)
        elif self._phase == _Phase.FEEDBACK:
            if self._phase_timer >= self._config.feedback_duration_ms:
                self._trial_idx += 1
                if self._trial_idx >= len(self._trials):
                    self._phase = _Phase.DONE
                    self._next = self._build_next_scene()
                elif self._trial_idx % self._config.trials_per_block == 0:
                    self._phase = _Phase.BETWEEN_BLOCKS
                    self._phase_timer = 0.0
                else:
                    self._phase = _Phase.ITI
                    self._phase_timer = 0.0
                    self._iti_duration = float(
                        random.randint(self._config.iti_min_ms, self._config.iti_max_ms)
                    )

    def _complete_trial(self, response: str, correct: bool, rt_ms: float) -> None:
        import datetime

        t = self._trials[self._trial_idx]
        record = _TrialRecord(
            participant_id=self._pid,
            session_id=self._sid,
            trial_id=self._trial_idx,
            task_name="gono",
            trial_type=t["trial_type"],
            response=response,
            correct=correct,
            reaction_time_ms=rt_ms,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        )
        self._records.append(record)
        _write_trial(self._csv_path, record)
        self._phase = _Phase.FEEDBACK
        self._phase_timer = 0.0

    def _build_next_scene(self) -> Scene:
        from cognitive_data_arcade.engine.badges import BadgeEngine, SessionResult
        from cognitive_data_arcade.ui.session_summary import SessionSummaryScene

        hits = [r for r in self._records if r.response == "hit"]
        ap_earned = len(hits) * self._config.ap_per_hit

        go_trials = [r for r in self._records if r.trial_type == "go"]
        nogo_trials = [r for r in self._records if r.trial_type == "nogo"]
        hit_rate = len(hits) / len(go_trials) if go_trials else 0.0
        fa_count = sum(1 for r in self._records if r.response == "false_alarm")
        fa_rate = fa_count / len(nogo_trials) if nogo_trials else 0.0
        hit_rate_c = max(0.01, min(0.99, hit_rate))
        fa_rate_c = max(0.01, min(0.99, fa_rate))
        d_prime = _probit(hit_rate_c) - _probit(fa_rate_c)
        sp_earned = (
            self._config.sp_dprime_bonus
            if d_prime >= self._config.dprime_threshold
            else 0
        )

        correct_count = sum(1 for r in self._records if r.correct)
        hit_rts = [r.reaction_time_ms for r in hits if r.reaction_time_ms > 0.0]
        avg_rt = sum(hit_rts) / len(hit_rts) if hit_rts else 0.0
        min_rt = min(hit_rts) if hit_rts else 0.0
        max_rt = max(hit_rts) if hit_rts else 0.0

        profile_before = self._profile_before
        badge_engine = BadgeEngine()
        session = SessionResult(
            task_name="gono",
            participant_id=self._pid,
            session_id=self._sid,
            total_trials=len(self._records),
            correct_trials=correct_count,
            avg_reaction_time_ms=avg_rt,
            min_reaction_time_ms=min_rt,
            max_reaction_time_ms=max_rt,
            arcade_points_earned=ap_earned,
            science_points_earned=sp_earned,
        )
        new_badges = badge_engine.evaluate(session, profile_before)
        self._pm.add_ap(ap_earned)
        if sp_earned:
            self._pm.add_sp(sp_earned)
        for bid in new_badges:
            self._pm.award_badge(bid)
        profile_after = self._pm.load()

        def _analysis_factory(
            csv_path: Path, strings: Strings, back_scene: Scene
        ) -> Scene:
            from cognitive_data_arcade.ui.gono_analysis_scene import GoNoGoAnalysisScene

            return GoNoGoAnalysisScene(csv_path, strings, back_scene)

        return SessionSummaryScene(
            session=session,
            new_badge_ids=new_badges,
            profile_before=profile_before,
            profile_after=profile_after,
            strings=self._strings,
            profile_manager=self._pm,
            csv_path=self._csv_path,
            analysis_factory=_analysis_factory,
        )

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((26, 26, 46))
        w, h = surface.get_width(), surface.get_height()
        cx, cy = w // 2, h // 2

        if self._phase == _Phase.ITI:
            pass  # blank

        elif self._phase == _Phase.FIXATION:
            fix = self._font_fix.render("+", True, (240, 240, 240))
            surface.blit(fix, (cx - fix.get_width() // 2, cy - fix.get_height() // 2))

        elif self._phase == _Phase.STIMULUS:
            trial = self._trials[self._trial_idx]
            color = self._COLOR_GO if trial["trial_type"] == "go" else self._COLOR_NOGO
            pygame.draw.circle(surface, color, (cx, cy), self._CIRCLE_RADIUS)

        elif self._phase == _Phase.FEEDBACK:
            last = self._records[-1] if self._records else None
            if last is not None:
                if last.correct:
                    fb_text = "OK"
                    fb_color = (39, 174, 96)
                else:
                    fb_text = "X"
                    fb_color = (231, 76, 60)
                fb = self._font_fb.render(fb_text, True, fb_color)
                surface.blit(fb, (cx - fb.get_width() // 2, cy - fb.get_height() // 2))

        elif self._phase == _Phase.BETWEEN_BLOCKS:
            msg = self._font_hint.render(
                "Block complete - SPACE to continue", True, (160, 160, 160)
            )
            surface.blit(msg, (cx - msg.get_width() // 2, cy - msg.get_height() // 2))

        elif self._phase == _Phase.DONE:
            pass

    def is_done(self) -> bool:
        return self._phase == _Phase.DONE

    def next_scene(self) -> Scene | None:
        if not self.is_done():
            return None
        return self._next
