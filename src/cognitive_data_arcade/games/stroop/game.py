from __future__ import annotations

import csv
import datetime
import enum
import random
from dataclasses import asdict, dataclass
from pathlib import Path

import pygame

from cognitive_data_arcade.engine import audio
from cognitive_data_arcade.engine.badges import BadgeEngine, SessionResult
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.stroop.config import COLORS, EASY, HARD, MEDIUM, StroopConfig
from cognitive_data_arcade.profile.manager import ProfileManager

_BG = (10, 10, 20)
_WHITE = (240, 240, 240)
_DIM = (70, 70, 112)
_ORANGE = (243, 156, 18)
_RED = (231, 76, 60)
_HIGHLIGHT = (243, 156, 18)
_W, _H = 1024, 768
_PROGRESS_H = 4
_FOOTER_H = 40

_COLOR_TO_RESPONSE: dict[str, str] = {
    "red": "r",
    "green": "g",
    "blue": "b",
    "yellow": "y",
}


class _Phase(enum.Enum):
    PRESET_SELECT = "preset_select"
    INSTRUCTIONS = "instructions"
    COUNTDOWN = "countdown"
    ITI = "iti"
    STIMULUS = "stimulus"
    FEEDBACK = "feedback"
    BETWEEN_BLOCKS = "between_blocks"
    DONE = "done"


@dataclass
class _Stimulus:
    word: str
    ink_name: str
    ink_rgb: tuple[int, int, int]
    expected_key: int
    condition: str
    word_color: str


@dataclass(frozen=True)
class _TrialRecord:
    participant_id: str
    session_id: str
    trial_id: int
    task_name: str
    condition: str
    stimulus: str
    ink_color: str
    word_color: str
    expected_response: str
    actual_response: str
    correct: bool
    reaction_time_ms: float
    timestamp: str


def _write_trial(path: Path, record: _TrialRecord) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(record).keys()))
        if write_header:
            writer.writeheader()
        writer.writerow(asdict(record))


class StroopGame(Scene):
    def __init__(
        self,
        config: StroopConfig,
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
        self._key_to_color: dict[int, str] = {
            kc: name for _, name, _, kc in COLORS[:self._config.num_colors]
        }

        self._presets = [EASY, MEDIUM, HARD]
        self._preset_idx = 1  # middle (standard) default

        self._phase = _Phase.PRESET_SELECT
        self._phase_timer = 0.0
        self._iti_duration = float(config.iti_min_ms)
        self._countdown_val = 3
        self._trial_index = 0
        self._last_rt: float | None = None
        self._last_correct: bool | None = None
        self._stimulus_queue: list[_Stimulus] = []
        self._current_stimulus: _Stimulus | None = None
        self._records: list[_TrialRecord] = []
        self._next_cache: Scene | None = None
        self._color_rects: dict[str, pygame.Rect] = {}
        self._preset_rects: list[pygame.Rect] = []

        pygame.font.init()
        self._font_sm = pygame.font.SysFont(None, 26)
        self._font_med = pygame.font.SysFont(None, 36)
        self._font_lg = pygame.font.SysFont(None, 90)
        self._font_hint = pygame.font.SysFont(None, 24)
        self._font_key = pygame.font.SysFont(None, 28)

    # ── Scene interface ───────────────────────────────────────────────────────

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            from cognitive_data_arcade.engine.mouse import hit
            if self._phase == _Phase.PRESET_SELECT:
                for i, rect in enumerate(self._preset_rects):
                    if hit(rect, event.pos):
                        self._preset_idx = i
                        break
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            from cognitive_data_arcade.engine.mouse import hit
            if self._phase == _Phase.PRESET_SELECT:
                for i, rect in enumerate(self._preset_rects):
                    if hit(rect, event.pos):
                        self._preset_idx = i
                        self._config = self._presets[self._preset_idx]
                        self._key_to_color = {
                            kc: name for _, name, _, kc in COLORS[:self._config.num_colors]
                        }
                        self._phase = _Phase.INSTRUCTIONS
                        break
            elif self._phase == _Phase.STIMULUS:
                color_name_map = {"r": "red", "g": "green", "b": "blue", "y": "yellow"}
                for key, rect in self._color_rects.items():
                    if hit(rect, event.pos):
                        color = color_name_map[key]
                        correct = color == self._current_stimulus.ink_name
                        self._complete_trial(
                            rt=self._phase_timer,
                            actual=key,
                            correct=correct,
                        )
                        break
            return
        if event.type != pygame.KEYDOWN:
            return
        if self._phase == _Phase.PRESET_SELECT:
            self._handle_preset_select(event.key)
        elif self._phase == _Phase.INSTRUCTIONS:
            if event.key == pygame.K_SPACE:
                self._phase = _Phase.COUNTDOWN
                self._phase_timer = 0.0
                self._countdown_val = 3
        elif self._phase == _Phase.STIMULUS:
            if event.key in self._key_to_color:
                color = self._key_to_color[event.key]
                correct = color == self._current_stimulus.ink_name
                self._complete_trial(
                    rt=self._phase_timer,
                    actual=_COLOR_TO_RESPONSE[color],
                    correct=correct,
                )
        elif self._phase == _Phase.BETWEEN_BLOCKS:
            if event.key == pygame.K_SPACE:
                self._enter_iti()

    def _handle_preset_select(self, key: int) -> None:
        if key == pygame.K_UP:
            self._preset_idx = max(0, self._preset_idx - 1)
        elif key == pygame.K_DOWN:
            self._preset_idx = min(len(self._presets) - 1, self._preset_idx + 1)
        elif key in (pygame.K_SPACE, pygame.K_RETURN):
            self._config = self._presets[self._preset_idx]
            self._key_to_color = {
                kc: name for _, name, _, kc in COLORS[:self._config.num_colors]
            }
            self._phase = _Phase.INSTRUCTIONS

    def update(self, dt_ms: float) -> None:
        if self._phase in (
            _Phase.PRESET_SELECT,
            _Phase.INSTRUCTIONS,
            _Phase.DONE,
            _Phase.BETWEEN_BLOCKS,
        ):
            return
        self._phase_timer += dt_ms

        if self._phase == _Phase.COUNTDOWN:
            self._countdown_val = max(1, 3 - int(self._phase_timer / 1000.0))
            if self._phase_timer >= 3000.0:
                self._enter_iti()
        elif self._phase == _Phase.ITI:
            if self._phase_timer >= self._iti_duration:
                excess = self._phase_timer - self._iti_duration
                self._enter_stimulus(excess)
        elif self._phase == _Phase.STIMULUS:
            if self._phase_timer >= self._config.timeout_ms:
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
        return float(random.randint(self._config.iti_min_ms, self._config.iti_max_ms))

    def _enter_iti(self) -> None:
        self._phase = _Phase.ITI
        self._phase_timer = 0.0
        self._iti_duration = self._rand_iti()

    def _enter_stimulus(self, excess: float = 0.0) -> None:
        self._current_stimulus = self._next_stimulus()
        self._phase = _Phase.STIMULUS
        self._phase_timer = excess

    def _next_stimulus(self) -> _Stimulus:
        if not self._stimulus_queue:
            self._stimulus_queue = self._build_block()
        return self._stimulus_queue.pop(0)

    def _build_block(self) -> list[_Stimulus]:
        active = COLORS[:self._config.num_colors]
        stimuli: list[_Stimulus] = []
        for word, name, rgb, key in active:
            stimuli.append(_Stimulus(word, name, rgb, key, "congruent", name))
            stimuli.append(_Stimulus("XXXXX", name, rgb, key, "neutral", "none"))
        for word, name, _rgb, _key in active:
            wrong = [(n, r, k) for (w, n, r, k) in active if n != name]
            ink_name, ink_rgb, ink_key = random.choice(wrong)
            stimuli.append(
                _Stimulus(word, ink_name, ink_rgb, ink_key, "incongruent", name)
            )
        random.shuffle(stimuli)
        return stimuli

    def _complete_trial(self, rt: float, actual: str, correct: bool) -> None:
        stim = self._current_stimulus
        record = _TrialRecord(
            participant_id=self._participant_id,
            session_id=self._session_id,
            trial_id=self._trial_index + 1,
            task_name="stroop",
            condition=stim.condition,
            stimulus=stim.word,
            ink_color=stim.ink_name,
            word_color=stim.word_color,
            expected_response=_COLOR_TO_RESPONSE[stim.ink_name],
            actual_response=actual,
            correct=correct,
            reaction_time_ms=rt,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        )
        self._records.append(record)
        _write_trial(self._csv_path, record)
        self._last_rt = rt if rt > 0 else None
        self._last_correct = correct
        audio.play_sfx("correct" if correct else "wrong")
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
            task_name="stroop",
            participant_id=self._participant_id,
            session_id=self._session_id,
            total_trials=self._config.num_trials,
            correct_trials=correct_count,
            avg_reaction_time_ms=avg_rt,
            min_reaction_time_ms=min_rt,
            max_reaction_time_ms=max_rt,
            arcade_points_earned=correct_count * self._config.ap_per_correct,
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
            # csv_path intentionally omitted: Stroop analysis accessed via Z picker
        )

    # ── draw ─────────────────────────────────────────────────────────────────

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        w, h = surface.get_size()
        if self._phase == _Phase.PRESET_SELECT:
            self._draw_preset_select(surface, w, h)
        elif self._phase == _Phase.INSTRUCTIONS:
            self._draw_instructions(surface, w, h)
        elif self._phase == _Phase.COUNTDOWN:
            self._draw_game_frame(surface, w, h)
            self._draw_countdown(surface, w, h)
        elif self._phase in (_Phase.ITI, _Phase.STIMULUS):
            self._draw_game_frame(
                surface, w, h, show_stimulus=(self._phase == _Phase.STIMULUS)
            )
        elif self._phase == _Phase.FEEDBACK:
            self._draw_game_frame(surface, w, h)
            self._draw_feedback(surface, w, h)
        elif self._phase == _Phase.BETWEEN_BLOCKS:
            self._draw_between_blocks(surface, w, h)

    def _draw_preset_select(self, surface: pygame.Surface, w: int, h: int) -> None:
        title = self._font_med.render(self._strings.stroop_pick_preset, True, _WHITE)
        surface.blit(title, (w // 2 - title.get_width() // 2, 200))
        labels = [
            self._strings.stroop_difficulty_easy,
            self._strings.stroop_difficulty_medium,
            self._strings.stroop_difficulty_hard,
        ]
        self._preset_rects = []
        for i, label in enumerate(labels):
            color = _HIGHLIGHT if i == self._preset_idx else _DIM
            surf = self._font_med.render(label, True, color)
            x = w // 2 - surf.get_width() // 2
            y = 280 + i * 56
            surface.blit(surf, (x, y))
            self._preset_rects.append(
                pygame.Rect(x - 10, y - 4, surf.get_width() + 20, surf.get_height() + 8)
            )
        hint = self._font_hint.render("UP/DN  navigate   SPACE/ENTER  select", True, _DIM)
        surface.blit(hint, (w // 2 - hint.get_width() // 2, h - _FOOTER_H))

    def _draw_instructions(self, surface: pygame.Surface, w: int, h: int) -> None:
        lines = self._strings.stroop_instructions.split("\n")
        y = h // 2 - len(lines) * 22
        for line in lines:
            if line:
                surf = self._font_med.render(line, True, _WHITE)
                surface.blit(surf, (w // 2 - surf.get_width() // 2, y))
            y += 44

    def _draw_countdown(self, surface: pygame.Surface, w: int, h: int) -> None:
        surf = self._font_lg.render(str(self._countdown_val), True, _ORANGE)
        surface.blit(
            surf, (w // 2 - surf.get_width() // 2, h // 2 - surf.get_height() // 2)
        )

    def _draw_game_frame(
        self, surface: pygame.Surface, w: int, h: int, show_stimulus: bool = False
    ) -> None:
        pygame.draw.rect(surface, (42, 42, 80), (0, 0, w, _PROGRESS_H))
        if self._config.num_trials > 0:
            fill = int(w * self._trial_index / self._config.num_trials)
            pygame.draw.rect(surface, _ORANGE, (0, 0, fill, _PROGRESS_H))
        label = self._font_sm.render(
            f"trial {self._trial_index + 1} / {self._config.num_trials}", True, _DIM
        )
        surface.blit(label, (14, _PROGRESS_H + 6))

        if show_stimulus and self._current_stimulus is not None:
            stim = self._current_stimulus
            word_surf = self._font_lg.render(stim.word, True, stim.ink_rgb)
            surface.blit(
                word_surf,
                (w // 2 - word_surf.get_width() // 2, h // 2 - 60),
            )
            hint = self._font_hint.render(self._strings.stroop_hint_ink, True, _DIM)
            surface.blit(hint, (w // 2 - hint.get_width() // 2, h // 2 + 60))
        else:
            fix = self._font_med.render("+", True, (60, 60, 100))
            surface.blit(
                fix,
                (w // 2 - fix.get_width() // 2, h // 2 - fix.get_height() // 2),
            )

        self._draw_key_bar(surface, w, h)

    def _draw_key_bar(self, surface: pygame.Surface, w: int, h: int) -> None:
        bar_y = h - _FOOTER_H
        pygame.draw.line(surface, (42, 42, 80), (0, bar_y), (w, bar_y))
        active = COLORS[:self._config.num_colors]
        col_w = w // self._config.num_colors
        self._color_rects = {}
        for i, (word, name, rgb, key_const) in enumerate(active):
            letter = chr(key_const).upper()
            key = _COLOR_TO_RESPONSE[name]
            cx = i * col_w + col_w // 2
            self._color_rects[key] = pygame.Rect(i * col_w, bar_y, col_w, _FOOTER_H)
            k = self._font_key.render(letter, True, rgb)
            surface.blit(k, (cx - k.get_width() // 2, bar_y + 4))
            n = self._font_sm.render(word, True, rgb)
            surface.blit(n, (cx - n.get_width() // 2, bar_y + 22))

    def _draw_feedback(self, surface: pygame.Surface, w: int, h: int) -> None:
        if self._last_rt is not None and self._last_correct:
            text, color = f"{self._last_rt:.0f} ms", _ORANGE
        elif self._last_rt is not None:
            text, color = f"{self._last_rt:.0f} ms", _RED
        else:
            text, color = self._strings.stroop_too_slow, _RED
        surf = self._font_lg.render(text, True, color)
        surface.blit(surf, (w // 2 - surf.get_width() // 2, h // 2 + 80))

    def _draw_between_blocks(self, surface: pygame.Surface, w: int, h: int) -> None:
        surf = self._font_med.render(self._strings.rt_between_blocks, True, _WHITE)
        surface.blit(
            surf, (w // 2 - surf.get_width() // 2, h // 2 - surf.get_height() // 2)
        )
