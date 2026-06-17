from __future__ import annotations

import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")


def test_classify_challenges_count():
    from cognitive_data_arcade.games.human_vs_model.challenge_data import CLASSIFY_CHALLENGES
    assert len(CLASSIFY_CHALLENGES) == 3


def test_detect_challenges_count():
    from cognitive_data_arcade.games.human_vs_model.challenge_data import DETECT_CHALLENGES
    assert len(DETECT_CHALLENGES) == 3


def test_complete_challenges_count():
    from cognitive_data_arcade.games.human_vs_model.challenge_data import COMPLETE_CHALLENGES
    assert len(COMPLETE_CHALLENGES) == 3


def test_classify_answers_in_options():
    from cognitive_data_arcade.games.human_vs_model.challenge_data import CLASSIFY_CHALLENGES
    for c in CLASSIFY_CHALLENGES:
        assert c.answer in c.options, f"answer '{c.answer}' not in options {c.options}"


def test_complete_answers_in_options():
    from cognitive_data_arcade.games.human_vs_model.challenge_data import COMPLETE_CHALLENGES
    for c in COMPLETE_CHALLENGES:
        assert c.answer in c.options, f"answer '{c.answer}' not in options {c.options}"


def test_complete_four_options():
    from cognitive_data_arcade.games.human_vs_model.challenge_data import COMPLETE_CHALLENGES
    for c in COMPLETE_CHALLENGES:
        assert len(c.options) == 4, f"expected 4 options, got {len(c.options)}"


def test_classify_ai_fails_at_least_once():
    from cognitive_data_arcade.games.human_vs_model.challenge_data import CLASSIFY_CHALLENGES
    failures = [c for c in CLASSIFY_CHALLENGES if c.model_answer != c.answer]
    assert len(failures) >= 1


def test_difficulty_values():
    from cognitive_data_arcade.games.human_vs_model.challenge_data import (
        CLASSIFY_CHALLENGES, DETECT_CHALLENGES, COMPLETE_CHALLENGES,
    )
    for c in CLASSIFY_CHALLENGES:
        assert c.difficulty == 1
    for c in DETECT_CHALLENGES:
        assert c.difficulty == 2
    for c in COMPLETE_CHALLENGES:
        assert c.difficulty == 3


def test_game_scene_instantiates():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.human_vs_model.game import HumanVsModelScene
    scene = HumanVsModelScene()
    assert not scene.is_done()
    assert scene.next_scene() is None


def test_get_game_info_bilingual():
    from cognitive_data_arcade.engine.i18n import get_strings
    from cognitive_data_arcade.games.human_vs_model.info import get_game_info
    for lang in ("pl", "en"):
        strings = get_strings(lang)
        info = get_game_info(strings)
        assert info.title
        assert len(info.description_lines) >= 2
        assert len(info.key_bindings) >= 2
