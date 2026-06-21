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


def test_phase_domain_picker_renders():
    import pygame

    pygame.init()
    surface = pygame.Surface((1024, 720))
    from cognitive_data_arcade.games.architects_trial.game_state import GameState
    from cognitive_data_arcade.games.architects_trial.phase_domain_picker import (
        PhaseDomainPickerScene,
    )

    state = GameState()
    scene = PhaseDomainPickerScene(state)
    scene.update(0)
    scene.draw(surface)
    assert not scene.is_done()
    pygame.quit()


def test_phase_act_renders():
    import pygame

    pygame.init()
    surface = pygame.Surface((1024, 720))
    from cognitive_data_arcade.games.architects_trial.game_state import GameState
    from cognitive_data_arcade.games.architects_trial.phase_act import PhaseActScene

    state = GameState()
    state.domain = "social"
    scene = PhaseActScene(state, act_num=1)
    scene.update(0)
    scene.draw(surface)
    assert not scene.is_done()
    pygame.quit()


def test_phase_act_applies_score_deltas():
    from cognitive_data_arcade.games.architects_trial.game_state import GameState
    from cognitive_data_arcade.games.architects_trial.domain_data import DOMAIN_DATA

    state = GameState()
    state.domain = "social"
    card = DOMAIN_DATA["social"]["act1_cards"][0]  # "registries": f+10, c+20, e+10
    state.fairness_score = min(100, max(0, state.fairness_score + card.fairness_delta))
    state.compliance_score = min(100, max(0, state.compliance_score + card.compliance_delta))
    state.effectiveness_score = min(
        100, max(0, state.effectiveness_score + card.effectiveness_delta)
    )
    state.decisions.append(card.key)
    assert state.fairness_score == 10
    assert state.compliance_score == 20
    assert state.effectiveness_score == 10
    assert state.decisions == ["registries"]


def test_phase_consequences_renders():
    import pygame

    pygame.init()
    surface = pygame.Surface((1024, 720))
    from cognitive_data_arcade.games.architects_trial.game_state import GameState
    from cognitive_data_arcade.games.architects_trial.phase_consequences import (
        PhaseConsequencesScene,
    )

    state = GameState()
    state.domain = "social"
    state.decisions = ["registries", "minimize_fn", "kpi_interventions"]
    scene = PhaseConsequencesScene(state)
    scene.update(500)
    scene.draw(surface)
    assert not scene.is_done()
    pygame.quit()


def test_phase_tribunal_renders():
    import pygame

    pygame.init()
    surface = pygame.Surface((1024, 720))
    from cognitive_data_arcade.games.architects_trial.game_state import GameState
    from cognitive_data_arcade.games.architects_trial.phase_tribunal import PhaseTribunalScene

    state = GameState()
    state.domain = "social"
    state.decisions = ["registries", "minimize_fn", "kpi_interventions"]
    state.fairness_score = 15
    state.compliance_score = 40
    state.effectiveness_score = 60
    scene = PhaseTribunalScene(state)
    scene.update(0)
    scene.draw(surface)
    assert not scene.is_done()
    pygame.quit()


def test_phase_result_renders():
    import pygame

    pygame.init()
    surface = pygame.Surface((1024, 720))
    from cognitive_data_arcade.games.architects_trial.game_state import GameState
    from cognitive_data_arcade.games.architects_trial.phase_result import PhaseResultScene

    state = GameState()
    state.domain = "social"
    state.fairness_score = 45
    state.compliance_score = 55
    state.effectiveness_score = 70
    scene = PhaseResultScene(state)
    scene.update(0)
    scene.draw(surface)
    assert not scene.is_done()
    pygame.quit()


def test_game_renders_3_frames():
    import pygame

    pygame.init()
    surface = pygame.Surface((1024, 720))
    from cognitive_data_arcade.games.architects_trial.game import ArchitectsTrialScene

    scene = ArchitectsTrialScene()
    for _ in range(3):
        scene.update(16)
        scene.draw(surface)
    assert not scene.is_done()
    pygame.quit()


def test_lesson_32_structure():
    from cognitive_data_arcade.lessons.lesson_32 import CONTENT

    for lang in ("pl", "en"):
        assert lang in CONTENT
        assert len(CONTENT[lang]["theory"]) == 4
        assert len(CONTENT[lang]["notes"]) == 2
        assert len(CONTENT[lang]["tasks"]) == 3


def test_menu_has_architects_trial():
    from cognitive_data_arcade.ui.menu import _LESSONS

    nums = [n for n, _ in _LESSONS]
    assert 32 in nums


def test_menu_order_30_before_31():
    from cognitive_data_arcade.ui.menu import _LESSONS

    nums = [n for n, _ in _LESSONS]
    assert nums.index(32) < nums.index(31)
