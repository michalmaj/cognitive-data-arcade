from __future__ import annotations

import csv
import enum
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path

import pygame

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.nback.config import NBackConfig, Trial, generate_block
from cognitive_data_arcade.profile.manager import ProfileManager


class _Phase(enum.Enum):
    ITI = "iti"
    STIMULUS = "stimulus"
    RESPONSE_WINDOW = "response_window"
    BETWEEN_BLOCKS = "between_blocks"
    DONE = "done"


@dataclass(frozen=True)
class _TrialRecord:
    task_name: str
    participant_id: str
    session_id: str
    trial_id: int
    block_id: int
    n_level: int
    position: int
    letter: str
    pos_match: bool
    let_match: bool
    key_a_pressed: bool
    key_l_pressed: bool
    pos_correct: bool
    let_correct: bool
    rt_a_ms: float
    rt_l_ms: float


_N_MIN = 1
_N_MAX = 3


def _write_trial(csv_path: Path, record: _TrialRecord) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not csv_path.exists()
    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(record).keys()))
        if write_header:
            writer.writeheader()
        writer.writerow(asdict(record))


def _probit(p: float) -> float:
    c = (2.515517, 0.802853, 0.010328)
    d = (1.432788, 0.189269, 0.001308)
    t = math.sqrt(-2.0 * math.log(p if p <= 0.5 else 1.0 - p))
    num = c[0] + c[1] * t + c[2] * t * t
    den = 1.0 + d[0] * t + d[1] * t * t + d[2] * t * t * t
    z = t - num / den
    return -z if p <= 0.5 else z


class NBackGame(Scene):
    _GRID_SIZE = 3
    _CELL_PX = 120
    _GRID_PAD = 20

    def __init__(
        self,
        config: NBackConfig,
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
        self._rng = random.Random()
        self._current_n: int = 1 if config.n is None else config.n
        self._block_idx = 0
        self._trial_in_block = 0
        self._trial_global = 0
        self._trials: list[Trial] = generate_block(
            self._current_n, config.trials_per_block, config.target_rate, self._rng
        )
        self._phase = _Phase.ITI
        self._phase_timer = 0.0
        self._stimulus_timer = 0.0
        self._key_a = False
        self._key_l = False
        self._rt_a = 0.0
        self._rt_l = 0.0
        self._records: list[_TrialRecord] = []
        self._next: Scene | None = None
        self._profile_before = profile_manager.load()
        pygame.font.init()
        self._font_letter = pygame.font.SysFont(None, 100)
        self._font_hint = pygame.font.SysFont(None, 28)
        self._font_block = pygame.font.SysFont(None, 40)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if self._phase in (_Phase.STIMULUS, _Phase.RESPONSE_WINDOW):
            if event.key == pygame.K_a and not self._key_a:
                self._key_a = True
                self._rt_a = self._stimulus_timer
            if event.key == pygame.K_l and not self._key_l:
                self._key_l = True
                self._rt_l = self._stimulus_timer

    def update(self, dt_ms: float) -> None:
        if self._phase == _Phase.DONE:
            return
        self._phase_timer += dt_ms
        if self._phase in (_Phase.STIMULUS, _Phase.RESPONSE_WINDOW):
            self._stimulus_timer += dt_ms

        if self._phase == _Phase.ITI:
            if self._phase_timer >= self._config.iti_ms:
                self._phase = _Phase.STIMULUS
                self._phase_timer = 0.0
                self._stimulus_timer = 0.0
                self._key_a = False
                self._key_l = False
                self._rt_a = 0.0
                self._rt_l = 0.0
        elif self._phase == _Phase.STIMULUS:
            if self._phase_timer >= self._config.stimulus_ms:
                self._phase = _Phase.RESPONSE_WINDOW
                self._phase_timer = 0.0
        elif self._phase == _Phase.RESPONSE_WINDOW:
            if self._phase_timer >= self._config.isi_ms:
                self._commit_trial()
        elif self._phase == _Phase.BETWEEN_BLOCKS:
            if self._phase_timer >= self._config.between_blocks_ms:
                self._start_next_block()

    def _commit_trial(self) -> None:
        trial = self._trials[self._trial_in_block]
        pos_correct = trial.pos_match == self._key_a
        let_correct = trial.let_match == self._key_l
        record = _TrialRecord(
            task_name="nback",
            participant_id=self._pid,
            session_id=self._sid,
            trial_id=self._trial_global + 1,
            block_id=self._block_idx + 1,
            n_level=self._current_n,
            position=trial.position,
            letter=trial.letter,
            pos_match=trial.pos_match,
            let_match=trial.let_match,
            key_a_pressed=self._key_a,
            key_l_pressed=self._key_l,
            pos_correct=pos_correct,
            let_correct=let_correct,
            rt_a_ms=self._rt_a,
            rt_l_ms=self._rt_l,
        )
        self._records.append(record)
        _write_trial(self._csv_path, record)
        self._trial_global += 1
        self._trial_in_block += 1

        if self._trial_in_block >= self._config.trials_per_block:
            self._block_idx += 1
            if self._block_idx >= self._config.num_blocks:
                self._phase = _Phase.DONE
                self._next = self._build_next_scene()
            else:
                if self._config.n is None:
                    self._evaluate_block()
                self._phase = _Phase.BETWEEN_BLOCKS
                self._phase_timer = 0.0
        else:
            self._phase = _Phase.ITI
            self._phase_timer = 0.0

    def _evaluate_block(self) -> None:
        block_records = self._records[-self._config.trials_per_block:]
        n = len(block_records)
        pos_acc = sum(1 for r in block_records if r.pos_correct) / n
        let_acc = sum(1 for r in block_records if r.let_correct) / n
        up = self._config.adaptive_up_threshold
        down = self._config.adaptive_down_threshold
        if pos_acc >= up and let_acc >= up:
            self._current_n = min(_N_MAX, self._current_n + 1)
        elif pos_acc < down or let_acc < down:
            self._current_n = max(_N_MIN, self._current_n - 1)

    def _start_next_block(self) -> None:
        self._trial_in_block = 0
        self._trials = generate_block(
            self._current_n, self._config.trials_per_block, self._config.target_rate, self._rng
        )
        self._phase = _Phase.ITI
        self._phase_timer = 0.0

    def _build_next_scene(self) -> Scene:
        from cognitive_data_arcade.engine.badges import BadgeEngine, SessionResult
        from cognitive_data_arcade.ui.session_summary import SessionSummaryScene

        ap = 0
        for r in self._records:
            if r.pos_match and r.key_a_pressed:
                ap += self._config.ap_per_hit
            elif not r.pos_match and r.key_a_pressed:
                ap += self._config.ap_per_false_alarm
            if r.let_match and r.key_l_pressed:
                ap += self._config.ap_per_hit
            elif not r.let_match and r.key_l_pressed:
                ap += self._config.ap_per_false_alarm
        ap_earned = max(0, ap)

        pos_targets = [r for r in self._records if r.pos_match]
        pos_non = [r for r in self._records if not r.pos_match]
        let_targets = [r for r in self._records if r.let_match]
        let_non = [r for r in self._records if not r.let_match]

        pos_hr = max(0.01, min(0.99, sum(r.key_a_pressed for r in pos_targets) / len(pos_targets) if pos_targets else 0.5))
        pos_far = max(0.01, min(0.99, sum(r.key_a_pressed for r in pos_non) / len(pos_non) if pos_non else 0.5))
        let_hr = max(0.01, min(0.99, sum(r.key_l_pressed for r in let_targets) / len(let_targets) if let_targets else 0.5))
        let_far = max(0.01, min(0.99, sum(r.key_l_pressed for r in let_non) / len(let_non) if let_non else 0.5))

        pos_dprime = _probit(pos_hr) - _probit(pos_far)
        let_dprime = _probit(let_hr) - _probit(let_far)
        threshold = self._config.dprime_threshold
        sp_earned = (
            self._config.sp_dprime_bonus
            if pos_dprime >= threshold and let_dprime >= threshold
            else 0
        )

        correct_count = sum(1 for r in self._records if r.pos_correct and r.let_correct)
        rt_a = [r.rt_a_ms for r in self._records if r.rt_a_ms > 0]
        avg_rt = sum(rt_a) / len(rt_a) if rt_a else 0.0

        badge_engine = BadgeEngine()
        session = SessionResult(
            task_name="nback",
            participant_id=self._pid,
            session_id=self._sid,
            total_trials=len(self._records),
            correct_trials=correct_count,
            avg_reaction_time_ms=avg_rt,
            min_reaction_time_ms=min(rt_a) if rt_a else 0.0,
            max_reaction_time_ms=max(rt_a) if rt_a else 0.0,
            arcade_points_earned=ap_earned,
            science_points_earned=sp_earned,
        )
        new_badges = badge_engine.evaluate(session, self._profile_before)
        self._pm.add_ap(ap_earned)
        if sp_earned:
            self._pm.add_sp(sp_earned)
        for bid in new_badges:
            self._pm.award_badge(bid)
        profile_after = self._pm.load()

        def _analysis_factory(csv_path: Path, strings: Strings, back_scene: Scene) -> Scene:
            from cognitive_data_arcade.ui.nback_analysis_scene import NBackAnalysisScene
            return NBackAnalysisScene(csv_path, strings, back_scene)

        return SessionSummaryScene(
            session=session,
            new_badge_ids=new_badges,
            profile_before=self._profile_before,
            profile_after=profile_after,
            strings=self._strings,
            profile_manager=self._pm,
            csv_path=self._csv_path,
            analysis_factory=_analysis_factory,
        )

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((26, 26, 46))
        w, h = surface.get_size()
        cx, cy = w // 2, h // 2

        grid_total = self._GRID_SIZE * self._CELL_PX + (self._GRID_SIZE - 1) * self._GRID_PAD
        grid_x = cx - grid_total // 2
        grid_y = cy - grid_total // 2 - 40

        if self._phase != _Phase.BETWEEN_BLOCKS:
            for cell in range(9):
                row, col = divmod(cell, self._GRID_SIZE)
                x = grid_x + col * (self._CELL_PX + self._GRID_PAD)
                y = grid_y + row * (self._CELL_PX + self._GRID_PAD)
                color = (50, 50, 80)
                if self._phase == _Phase.STIMULUS and self._trial_in_block < len(self._trials):
                    trial = self._trials[self._trial_in_block]
                    if cell == trial.position:
                        color = (243, 156, 18)
                pygame.draw.rect(surface, color, (x, y, self._CELL_PX, self._CELL_PX), border_radius=8)

            if self._phase == _Phase.STIMULUS and self._trial_in_block < len(self._trials):
                trial = self._trials[self._trial_in_block]
                letter_surf = self._font_letter.render(trial.letter, True, (240, 240, 240))
                surface.blit(
                    letter_surf,
                    (cx - letter_surf.get_width() // 2, grid_y + grid_total + 20),
                )
        else:
            msg = self._font_block.render(
                f"Block {self._block_idx}/{self._config.num_blocks} complete",
                True,
                (160, 160, 160),
            )
            surface.blit(msg, (cx - msg.get_width() // 2, cy - 20))

        hint = self._font_hint.render("A — position   L — letter", True, (100, 100, 150))
        surface.blit(hint, (cx - hint.get_width() // 2, h - 36))

    def is_done(self) -> bool:
        return self._phase == _Phase.DONE

    def next_scene(self) -> Scene | None:
        return self._next if self.is_done() else None
