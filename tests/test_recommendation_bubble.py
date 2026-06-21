import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")


def test_diversity_uniform():
    from cognitive_data_arcade.games.recommendation_bubble.game_state import (
        diversity,
        uniform_profile,
    )

    p = uniform_profile()
    assert abs(diversity(p) - 0.8) < 0.01


def test_diversity_single_category():
    from cognitive_data_arcade.games.recommendation_bubble.game_state import (
        diversity,
        CATEGORIES,
    )

    p = {cat: 0.0 for cat in CATEGORIES}
    p["SPORT"] = 1.0
    assert diversity(p) == 0.0


def test_profile_from_clicks_normalises():
    from cognitive_data_arcade.games.recommendation_bubble.game_state import (
        profile_from_clicks,
        CATEGORIES,
    )

    clicks = {cat: 0 for cat in CATEGORIES}
    clicks["SPORT"] = 8
    clicks["NAUKA"] = 2
    p = profile_from_clicks(clicks)
    assert abs(p["SPORT"] - 0.8) < 0.01
    assert abs(sum(p.values()) - 1.0) < 1e-9


def test_profile_from_clicks_empty_returns_uniform():
    from cognitive_data_arcade.games.recommendation_bubble.game_state import (
        profile_from_clicks,
        CATEGORIES,
        uniform_profile,
    )

    clicks = {cat: 0 for cat in CATEGORIES}
    p = profile_from_clicks(clicks)
    u = uniform_profile()
    for cat in CATEGORIES:
        assert abs(p[cat] - u[cat]) < 1e-9


def test_curated_profile_counts_slots():
    from cognitive_data_arcade.games.recommendation_bubble.game_state import (
        curated_profile,
    )

    slots = ["SPORT", "SPORT", "SPORT", "NAUKA", "POLITYKA", "MUZYKA"]
    p = curated_profile(slots)
    assert abs(p["SPORT"] - 0.5) < 0.01
    assert abs(sum(p.values()) - 1.0) < 1e-9


def test_generate_slots_dominated_by_heavy_category():
    from cognitive_data_arcade.games.recommendation_bubble.game_state import (
        generate_slots,
        CATEGORIES,
    )

    profile = {cat: 0.0 for cat in CATEGORIES}
    profile["SPORT"] = 1.0
    slots = generate_slots(profile, n=6, seed=42)
    assert all(s == "SPORT" for s in slots)


def test_game_state_defaults():
    from cognitive_data_arcade.games.recommendation_bubble.game_state import (
        GameState,
        CATEGORIES,
    )

    gs = GameState()
    assert set(gs.bubble.keys()) == set(CATEGORIES)
    assert abs(sum(gs.bubble.values()) - 1.0) < 1e-9
    assert gs.score_curator == 0
    assert gs.score_algo == 0
    assert gs.diversity_act1 == 0.0
    assert gs.diversity_act2 == 0.0
    assert gs.diversity_act3 == 0.0
    assert gs.algo_clicked_cats == []


def test_engagement_values():
    from cognitive_data_arcade.games.recommendation_bubble.game_state import (
        ENGAGEMENT,
        CATEGORIES,
    )

    assert all(cat in ENGAGEMENT for cat in CATEGORIES)
    assert ENGAGEMENT["SPORT"] == max(ENGAGEMENT.values())


def test_phase_intro_renders():
    import pygame

    pygame.init()
    from cognitive_data_arcade.games.recommendation_bubble.phase_intro import PhaseIntroScene
    from cognitive_data_arcade.games.recommendation_bubble.game_state import GameState

    scene = PhaseIntroScene(GameState())
    surface = pygame.Surface((1024, 720))
    scene.draw(surface)
    pygame.quit()


def test_phase_intro_advances_on_keydown():
    import pygame

    pygame.init()
    from cognitive_data_arcade.games.recommendation_bubble.phase_intro import PhaseIntroScene
    from cognitive_data_arcade.games.recommendation_bubble.game_state import GameState

    scene = PhaseIntroScene(GameState())
    assert not scene.is_done()
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    assert scene.is_done()
    assert scene.next_scene() is not None
    pygame.quit()


def test_phase_user_click_increments_category():
    import pygame

    pygame.init()
    from cognitive_data_arcade.games.recommendation_bubble.phase_user import PhaseUserScene
    from cognitive_data_arcade.games.recommendation_bubble.game_state import GameState

    scene = PhaseUserScene(GameState())
    # click on first bar (SPORT row y=120..189)
    scene.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(512, 155)))
    assert scene._clicks["SPORT"] == 1
    pygame.quit()


def test_phase_user_timer_expires_with_enough_clicks():
    import pygame

    pygame.init()
    from cognitive_data_arcade.games.recommendation_bubble.phase_user import (
        PhaseUserScene,
        _MIN_CLICKS,
    )
    from cognitive_data_arcade.games.recommendation_bubble.game_state import GameState

    scene = PhaseUserScene(GameState())
    for _ in range(_MIN_CLICKS):
        scene._clicks["SPORT"] += 1
    scene.update(35_000.0)  # 35s > 30s limit
    assert scene.is_done()
    assert scene.next_scene() is not None
    pygame.quit()


def test_phase_user_timer_extends_when_too_few_clicks():
    import pygame

    pygame.init()
    from cognitive_data_arcade.games.recommendation_bubble.phase_user import PhaseUserScene
    from cognitive_data_arcade.games.recommendation_bubble.game_state import GameState

    scene = PhaseUserScene(GameState())
    # no clicks, advance past 30s — should NOT be done (extends timer)
    scene.update(31_000.0)
    assert not scene.is_done()
    pygame.quit()


def test_phase_interlude_space_advances():
    import pygame

    pygame.init()
    from cognitive_data_arcade.games.recommendation_bubble.phase_interlude import (
        PhaseInterludeScene,
    )
    from cognitive_data_arcade.games.recommendation_bubble.game_state import GameState

    scene = PhaseInterludeScene(GameState(), next_act="curator")
    assert not scene.is_done()
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    assert scene.is_done()
    assert scene.next_scene() is not None
    pygame.quit()


def test_phase_interlude_algo_next():
    import pygame

    pygame.init()
    from cognitive_data_arcade.games.recommendation_bubble.phase_interlude import (
        PhaseInterludeScene,
    )
    from cognitive_data_arcade.games.recommendation_bubble.game_state import GameState

    scene = PhaseInterludeScene(GameState(), next_act="algo")
    scene.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    from cognitive_data_arcade.games.recommendation_bubble.phase_algo import PhaseAlgoScene

    assert isinstance(scene.next_scene(), PhaseAlgoScene)
    pygame.quit()


def test_phase_curator_swap_decrements_counter():
    import pygame

    pygame.init()
    from cognitive_data_arcade.games.recommendation_bubble.phase_curator import PhaseCuratorScene
    from cognitive_data_arcade.games.recommendation_bubble.game_state import GameState

    scene = PhaseCuratorScene(GameState())
    initial_swaps = scene._swaps_left
    scene._selected_slot = 0
    scene._do_swap("NAUKA")
    assert scene._swaps_left == initial_swaps - 1
    pygame.quit()


def test_phase_curator_no_swap_when_exhausted():
    import pygame

    pygame.init()
    from cognitive_data_arcade.games.recommendation_bubble.phase_curator import PhaseCuratorScene
    from cognitive_data_arcade.games.recommendation_bubble.game_state import GameState

    scene = PhaseCuratorScene(GameState())
    scene._swaps_left = 0
    scene._selected_slot = 0
    original = scene._slots[0]
    scene._do_swap("NAUKA")
    assert scene._slots[0] == original
    pygame.quit()


def test_phase_curator_score_stored_in_state():
    import pygame

    pygame.init()
    from cognitive_data_arcade.games.recommendation_bubble.phase_curator import PhaseCuratorScene
    from cognitive_data_arcade.games.recommendation_bubble.game_state import GameState

    scene = PhaseCuratorScene(GameState())
    scene.update(50_000.0)  # 50s > 45s limit
    assert scene.is_done()
    assert scene._state.score_curator >= 0
    pygame.quit()


def test_phase_algo_click_adds_engagement():
    import pygame

    pygame.init()
    from cognitive_data_arcade.games.recommendation_bubble.phase_algo import PhaseAlgoScene
    from cognitive_data_arcade.games.recommendation_bubble.game_state import GameState, ENGAGEMENT

    scene = PhaseAlgoScene(GameState())
    # force first tile to SPORT for deterministic test
    scene._displayed[0] = "SPORT"
    rect = scene._tile_rect(0)
    scene.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=rect.center))
    assert scene._score == ENGAGEMENT["SPORT"]
    pygame.quit()


def test_phase_algo_tile_replaced_after_click():
    import pygame

    pygame.init()
    from cognitive_data_arcade.games.recommendation_bubble.phase_algo import PhaseAlgoScene
    from cognitive_data_arcade.games.recommendation_bubble.game_state import GameState

    scene = PhaseAlgoScene(GameState())
    rect = scene._tile_rect(0)
    scene.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=rect.center))
    assert len(scene._displayed) == 6
    pygame.quit()


def test_phase_algo_score_stored_after_timeout():
    import pygame

    pygame.init()
    from cognitive_data_arcade.games.recommendation_bubble.phase_algo import PhaseAlgoScene
    from cognitive_data_arcade.games.recommendation_bubble.game_state import GameState

    scene = PhaseAlgoScene(GameState())
    scene.update(35_000.0)
    assert scene.is_done()
    assert scene._state.score_algo == scene._score
    pygame.quit()


def test_phase_result_stars_formula():
    import pygame

    pygame.init()
    from cognitive_data_arcade.games.recommendation_bubble.phase_result import PhaseResultScene
    from cognitive_data_arcade.games.recommendation_bubble.game_state import GameState

    gs = GameState()
    gs.score_curator = 70
    assert PhaseResultScene(gs)._stars == 3
    gs2 = GameState()
    gs2.score_curator = 50
    assert PhaseResultScene(gs2)._stars == 2
    gs3 = GameState()
    gs3.score_curator = 20
    assert PhaseResultScene(gs3)._stars == 1
    pygame.quit()


def test_phase_result_renders():
    import pygame

    pygame.init()
    from cognitive_data_arcade.games.recommendation_bubble.phase_result import PhaseResultScene
    from cognitive_data_arcade.games.recommendation_bubble.game_state import GameState

    scene = PhaseResultScene(GameState())
    surface = pygame.Surface((1024, 720))
    scene.draw(surface)
    pygame.quit()


def test_game_scene_instantiates():
    import pygame

    pygame.init()
    from cognitive_data_arcade.games.recommendation_bubble.game import RecommendationBubbleScene

    scene = RecommendationBubbleScene()
    assert scene is not None
    pygame.quit()


def test_game_renders_3_frames():
    import pygame

    pygame.init()
    surface = pygame.Surface((1024, 720))
    from cognitive_data_arcade.games.recommendation_bubble.game import RecommendationBubbleScene

    scene = RecommendationBubbleScene()
    for _ in range(3):
        scene.update(16.0)
        scene.draw(surface)
    pygame.quit()


def test_lesson_29_structure():
    from cognitive_data_arcade.lessons.lesson_29 import CONTENT

    for lang in ("pl", "en"):
        assert len(CONTENT[lang]["theory"]) == 4
        assert len(CONTENT[lang]["notes"]) == 2
        assert len(CONTENT[lang]["tasks"]) == 3


def test_menu_has_lesson_29():
    from cognitive_data_arcade.ui.menu import _LESSONS

    nums = [n for n, _ in _LESSONS]
    assert 29 in nums
