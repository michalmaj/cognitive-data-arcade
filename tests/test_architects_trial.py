# tests/test_architects_trial.py
"""Tests for L30 The Architect's Trial."""
from __future__ import annotations


def test_game_state_defaults():
    from cognitive_data_arcade.games.architects_trial.game_state import GameState
    s = GameState()
    assert s.domain == ""
    assert s.decisions == []
    assert s.fairness_score == 0
    assert s.compliance_score == 0
    assert s.effectiveness_score == 0
    assert s.tribunal_response == ""


def test_domain_data_has_all_domains():
    from cognitive_data_arcade.games.architects_trial.domain_data import DOMAIN_DATA
    for domain in ("social", "hiring", "triage"):
        assert domain in DOMAIN_DATA
        d = DOMAIN_DATA[domain]
        assert "title" in d
        assert "institution" in d
        assert len(d["act1_cards"]) >= 2
        assert len(d["act2_cards"]) >= 2
        assert len(d["act3_cards"]) >= 2
        assert isinstance(d["act4_consequences"], dict)
        assert len(d["act4_consequences"]) >= 3


def test_decision_card_deltas_reasonable():
    from cognitive_data_arcade.games.architects_trial.domain_data import DOMAIN_DATA
    for domain_data in DOMAIN_DATA.values():
        for act_key in ("act1_cards", "act2_cards", "act3_cards"):
            for card in domain_data[act_key]:
                assert -40 <= card.fairness_delta <= 40
                assert -40 <= card.compliance_delta <= 40
                assert -40 <= card.effectiveness_delta <= 40


def test_compute_verdict_zatwierdzony():
    from cognitive_data_arcade.games.architects_trial.game_state import compute_verdict
    assert compute_verdict(70, 65, 80) == "ZATWIERDZONY"


def test_compute_verdict_odrzucony_low_fairness():
    from cognitive_data_arcade.games.architects_trial.game_state import compute_verdict
    assert compute_verdict(15, 60, 70) == "ODRZUCONY"


def test_compute_verdict_odrzucony_low_compliance():
    from cognitive_data_arcade.games.architects_trial.game_state import compute_verdict
    assert compute_verdict(60, 18, 70) == "ODRZUCONY"


def test_compute_verdict_zawieszony():
    from cognitive_data_arcade.games.architects_trial.game_state import compute_verdict
    assert compute_verdict(25, 55, 70) == "ZAWIESZONY"


def test_compute_verdict_zalecenia():
    from cognitive_data_arcade.games.architects_trial.game_state import compute_verdict
    assert compute_verdict(45, 55, 50) == "ZATWIERDZONY Z ZALECENIAMI"


def test_score_clamped_to_100():
    from cognitive_data_arcade.games.architects_trial.game_state import GameState
    s = GameState()
    s.fairness_score = 90
    s.fairness_score = min(100, max(0, s.fairness_score + 50))
    assert s.fairness_score == 100


def test_phase_intro_renders():
    import pygame
    pygame.init()
    surface = pygame.Surface((1024, 720))
    from cognitive_data_arcade.games.architects_trial.game_state import GameState
    from cognitive_data_arcade.games.architects_trial.phase_intro import PhaseIntroScene
    state = GameState()
    scene = PhaseIntroScene(state)
    scene.update(100)
    scene.draw(surface)
    assert not scene.is_done()
    pygame.quit()
