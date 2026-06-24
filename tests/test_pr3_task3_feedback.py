"""Tests for PR3 Task 3: session summaries and verdict lines."""

from pathlib import Path
import pygame
from cognitive_data_arcade.engine.i18n import PL
from cognitive_data_arcade.profile.manager import ProfileManager


def _pm(tmp_path: Path) -> ProfileManager:
    pm = ProfileManager(tmp_path / "profile.json")
    pm.load()
    return pm


def test_distribution_q_shows_summary(tmp_path) -> None:
    pygame.init()
    from cognitive_data_arcade.games.distribution_playground.scene import (
        DistributionPlaygroundScene,
    )

    scene = DistributionPlaygroundScene(_pm(tmp_path), PL)
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q, mod=0, unicode="q"))
    assert scene._show_summary is True
    assert not scene.is_done()  # summary is showing, not done yet


def test_distribution_summary_auto_exit(tmp_path) -> None:
    pygame.init()
    from cognitive_data_arcade.games.distribution_playground.scene import (
        DistributionPlaygroundScene,
    )

    scene = DistributionPlaygroundScene(_pm(tmp_path), PL)
    scene._show_summary = True
    scene._summary_timer = 0.0
    scene.update(10001)
    assert scene.is_done()


def test_classifier_round_result_has_verdict() -> None:
    pygame.init()
    from cognitive_data_arcade.games.classifier_battle.phase_round_result import (
        PhaseRoundResultScene,
    )

    result = {
        "round_idx": 0,
        "scenario_name": "Iris",
        "player_acc": 0.85,
        "clf_accs": {"knn": 0.80, "dt": 0.75},
        "score": 85,
    }
    scene = PhaseRoundResultScene(result, session_score=85, round_results=[result])
    assert hasattr(scene, "_verdict")
    assert scene._verdict in ("Wygrales!", "Prawie!", "Przegrales.")


def test_overfitting_round_result_has_gap_verdict() -> None:
    pygame.init()
    from cognitive_data_arcade.games.overfitting_monster.phase_round_result import (
        PhaseRoundResultScene,
    )

    result = {
        "round_idx": 0,
        "scenario_name": "Iris",
        "k": 3,
        "split_pct": 70,
        "train_acc": 0.95,
        "test_acc": 0.78,
        "gap": 17.0,
        "score": 120,
        "stars": 2,
    }
    scene = PhaseRoundResultScene(result, session_score=120, round_results=[result])
    assert hasattr(scene, "_gap_verdict")


def test_text_tokenizer_q_shows_summary(tmp_path) -> None:
    pygame.init()
    from cognitive_data_arcade.games.text_tokenizer.scene import TextTokenizerLabScene

    scene = TextTokenizerLabScene(_pm(tmp_path), PL)
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q, mod=0, unicode="q"))
    assert scene._show_summary is True
    assert not scene.is_done()


def test_word_weight_factory_q_shows_summary(tmp_path) -> None:
    pygame.init()
    from cognitive_data_arcade.games.word_weight_factory.scene import WordWeightFactoryScene

    scene = WordWeightFactoryScene(_pm(tmp_path), PL)
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q, mod=0, unicode="q"))
    assert scene._show_summary is True
    assert not scene.is_done()


def test_social_network_q_shows_summary(tmp_path) -> None:
    pygame.init()
    from cognitive_data_arcade.games.social_network.game import SocialNetworkScene

    scene = SocialNetworkScene(_pm(tmp_path), PL)
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q, mod=0, unicode="q"))
    assert scene._show_summary is True
    assert not scene.is_done()


def test_text_tokenizer_summary_auto_exit(tmp_path) -> None:
    pygame.init()
    from cognitive_data_arcade.games.text_tokenizer.scene import TextTokenizerLabScene

    scene = TextTokenizerLabScene(_pm(tmp_path), PL)
    scene._show_summary = True
    scene._summary_timer = 0.0
    scene.update(10001)
    assert scene.is_done()


def test_social_network_summary_auto_exit(tmp_path) -> None:
    pygame.init()
    from cognitive_data_arcade.games.social_network.game import SocialNetworkScene

    scene = SocialNetworkScene(_pm(tmp_path), PL)
    scene._show_summary = True
    scene._summary_timer = 0.0
    scene.update(10001)
    assert scene.is_done()


def test_recommendation_bubble_has_verdict() -> None:
    pygame.init()
    from cognitive_data_arcade.games.recommendation_bubble.game_state import GameState
    from cognitive_data_arcade.games.recommendation_bubble.phase_result import PhaseResultScene

    state = GameState()
    state.score_curator = 80
    state.diversity_act3 = 0.20  # strong bubble
    scene = PhaseResultScene(state)
    assert hasattr(scene, "_bubble_verdict")
    assert "mocna" in scene._bubble_verdict.lower() or "echo" in scene._bubble_verdict.lower()


def test_you_were_the_dataset_has_synthesis() -> None:
    pygame.init()
    from cognitive_data_arcade.games.you_were_the_dataset.game_state import GameState
    from cognitive_data_arcade.games.you_were_the_dataset.phase_result import PhaseResultScene

    state = GameState()
    # Try build_synthetic_profile, fall back if not available
    try:
        from cognitive_data_arcade.games.you_were_the_dataset.synthetic_data import (
            build_synthetic_profile,
        )

        state.profile = build_synthetic_profile()
    except (ImportError, AttributeError):
        pass
    scene = PhaseResultScene(state)
    assert hasattr(scene, "_synthesis")
    assert len(scene._synthesis) > 10
