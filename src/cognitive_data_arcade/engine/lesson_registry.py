"""Canonical lesson registry for Cognitive Data Arcade.

This module is the single source of truth for lesson metadata:
lesson numbers, slugs, display titles, and lesson kinds.

Game construction is handled separately in ui/game_launcher.py.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class LessonKind(Enum):
    """Classification of a lesson by its interactive component.

    PLAYABLE: the lesson has a runnable game or interactive scene.
    THEORY:   the lesson has educational content but no playable component.
    HIDDEN:   the lesson exists internally but is not shown in the UI
              (e.g. its content is subsumed by another lesson).
    """

    PLAYABLE = "playable"
    THEORY = "theory"
    HIDDEN = "hidden"


@dataclass(frozen=True)
class LessonSpec:
    """Immutable description of one lesson.

    Attributes:
        number:   Lesson number (1-based, matches course README numbering).
        slug:     Machine-readable identifier, matches the task_name used in
                  CSV logs and SessionResult (e.g. "reaction_time", "stroop").
        title_en: English display title shown in the menu.
        kind:     Whether the lesson is playable, theory-only, or hidden.
    """

    number: int
    slug: str
    title_en: str
    kind: LessonKind


_P = LessonKind.PLAYABLE
_H = LessonKind.HIDDEN

LESSON_REGISTRY: tuple[LessonSpec, ...] = (
    LessonSpec(1,  "big_data_map",           "Big Data in Cognitive Science",  _P),
    LessonSpec(2,  "reaction_time",           "Reaction Time Lab",              _P),
    LessonSpec(3,  "event_log_detective",     "Event Log Detective",            _P),
    LessonSpec(4,  "data_quality_lab",        "Data Quality Lab",               _P),
    # L05 content (Missing Values) is subsumed by L04 in the UI — hidden, not removed.
    LessonSpec(5,  "missing_values",          "Missing Values and Outliers",    _H),
    LessonSpec(6,  "eda_sandbox",             "EDA Sandbox",                    _P),
    LessonSpec(7,  "stroop",                  "Stroop Challenge",               _P),
    LessonSpec(8,  "flanker",                 "Flanker Arena",                  _P),
    LessonSpec(9,  "go_no_go",               "Go/No-Go Guard",                 _P),
    LessonSpec(10, "n_back",                 "N-Back Memory Grid",             _P),
    LessonSpec(11, "visual_search",          "Visual Search Lab",              _P),
    LessonSpec(12, "cognitive_dashboard",    "Cognitive Dashboard",            _P),
    LessonSpec(13, "distribution_playground","Distribution Playground",        _P),
    LessonSpec(14, "correlation_trap",       "Correlation Trap",               _P),
    LessonSpec(15, "hypothesis_arena",       "Hypothesis Arena",               _P),
    LessonSpec(16, "prediction_slider",      "Prediction Slider",              _P),
    LessonSpec(17, "feature_hunter",         "Feature Hunter",                 _P),
    LessonSpec(18, "classifier_battle",      "Classifier Battle",              _P),
    LessonSpec(19, "overfitting_monster",    "Overfitting Monster",            _P),
    LessonSpec(20, "anomaly_alert",          "Anomaly Alert",                  _P),
    LessonSpec(21, "text_tokenizer_lab",     "Text Tokenizer Lab",             _P),
    LessonSpec(22, "word_weight_factory",    "Word Weight Factory",            _P),
    LessonSpec(23, "emotion_classifier",     "Emotion Classifier",             _P),
    LessonSpec(24, "semantic_space_explorer","Semantic Space Explorer",        _P),
    LessonSpec(25, "topic_detective",        "Topic Detective",                _P),
    LessonSpec(26, "human_vs_model",         "Human vs Model",                 _P),
    LessonSpec(27, "social_network_simulator","Social Network Simulator",      _P),
    LessonSpec(28, "misinformation_spread",  "Misinformation Spread",          _P),
    LessonSpec(29, "recommendation_bubble",  "Recommendation Bubble",          _P),
    LessonSpec(30, "bias_blind_spot",        "Bias Blind Spot",                _P),
    LessonSpec(31, "you_were_the_dataset",   "You Were the Dataset",           _P),
    LessonSpec(32, "architects_trial",       "The Architect's Trial",          _P),
)

_REGISTRY_BY_NUMBER: dict[int, LessonSpec] = {ls.number: ls for ls in LESSON_REGISTRY}


def lesson_available(lesson_num: int) -> bool:
    """Return True if a lesson with this number exists in the registry."""
    return lesson_num in _REGISTRY_BY_NUMBER


def get_lesson(lesson_num: int) -> LessonSpec | None:
    """Return the LessonSpec for a given number, or None if not found."""
    return _REGISTRY_BY_NUMBER.get(lesson_num)
