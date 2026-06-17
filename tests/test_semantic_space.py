from __future__ import annotations

import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")


def test_words_all_in_valid_clusters():
    from cognitive_data_arcade.games.semantic_space.word_data import WORDS, CLUSTERS
    for key, wd in WORDS.items():
        assert wd["cluster"] in CLUSTERS, f"{key} has unknown cluster {wd['cluster']}"


def test_coordinates_in_range():
    from cognitive_data_arcade.games.semantic_space.word_data import WORDS
    for key, wd in WORDS.items():
        assert 0.0 <= wd["x"] <= 1.0, f"{key} x={wd['x']} out of range"
        assert 0.0 <= wd["y"] <= 1.0, f"{key} y={wd['y']} out of range"


def test_similarities_all_50():
    from cognitive_data_arcade.games.semantic_space.word_data import WORDS, SIMILARITIES
    assert len(SIMILARITIES) == len(WORDS)
    for key in WORDS:
        assert key in SIMILARITIES, f"{key} missing from SIMILARITIES"
        assert len(SIMILARITIES[key]) == 8


def test_similarities_keys_exist():
    from cognitive_data_arcade.games.semantic_space.word_data import WORDS, SIMILARITIES
    for word, neighbors in SIMILARITIES.items():
        for neighbor_key, sim in neighbors:
            assert neighbor_key in WORDS, f"neighbor {neighbor_key!r} not in WORDS"
            assert 0.0 <= sim <= 1.0, f"sim {sim} out of range for {word}->{neighbor_key}"


def test_analogies_structure():
    from cognitive_data_arcade.games.semantic_space.word_data import ANALOGIES
    assert len(ANALOGIES) == 4
    for tup in ANALOGIES:
        assert len(tup) == 7, f"Expected 7-tuple, got {len(tup)}"
        a, b, c, answer, distractors, expl_pl, expl_en = tup
        assert isinstance(distractors, list) and len(distractors) == 3
        assert isinstance(expl_pl, str) and expl_pl
        assert isinstance(expl_en, str) and expl_en


def test_bridge_words_reference_valid_clusters():
    from cognitive_data_arcade.games.semantic_space.word_data import BRIDGE_WORDS, CLUSTERS, WORDS
    for word_key, clusters, difficulty in BRIDGE_WORDS:
        assert word_key in WORDS, f"{word_key} not in WORDS"
        for c in clusters:
            assert c in CLUSTERS, f"{c} not a valid cluster"
        assert difficulty in (2, 3)


def test_build_session_length():
    from cognitive_data_arcade.games.semantic_space.missions import build_session
    assert len(build_session()) == 8


def test_build_session_types():
    from cognitive_data_arcade.games.semantic_space.missions import build_session
    types = [m.type for m in build_session()]
    assert types.count("neighbors") == 2
    assert types.count("odd_one_out") == 2
    assert types.count("bridge") == 2
    assert types.count("analogy") == 2


def test_build_session_difficulty_ascending():
    from cognitive_data_arcade.games.semantic_space.missions import build_session
    session = build_session()
    assert session[0].difficulty == 1
    assert session[1].difficulty == 1
    assert session[-1].difficulty == 3


def test_neighbors_answers_in_words():
    from cognitive_data_arcade.games.semantic_space.missions import build_session
    from cognitive_data_arcade.games.semantic_space.word_data import WORDS
    for m in build_session():
        if m.type == "neighbors":
            for key in m.answers:
                assert key in WORDS


def test_analogy_missions_have_formula():
    from cognitive_data_arcade.games.semantic_space.missions import build_session
    for m in build_session():
        if m.type == "analogy":
            assert "=" in m.formula
            assert len(m.answers) == 1
            assert len(m.distractors) == 3


def test_game_scene_instantiates():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.semantic_space.game import SemanticSpaceScene
    scene = SemanticSpaceScene()
    assert not scene.is_done()
    assert scene.next_scene() is None


def test_phase_intro_renders():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.semantic_space.phase_intro import PhaseIntroScene
    scene = PhaseIntroScene()
    surf = pygame.Surface((1024, 720))
    assert not scene.is_done()
    scene.draw(surf)   # must not raise
    assert scene.next_scene() is None


def test_phase_intro_advances_on_space():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.semantic_space.phase_intro import PhaseIntroScene
    scene = PhaseIntroScene()
    # 3 slides: first 2 advance slide index, 3rd triggers scene transition
    for _ in range(3):
        ev = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE, "mod": 0, "unicode": " ", "scancode": 0})
        scene.handle_event(ev)
    assert scene.is_done()
    assert scene.next_scene() is not None


def test_phase_mission_renders():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.semantic_space.missions import build_session
    from cognitive_data_arcade.games.semantic_space.phase_mission import PhaseMissionScene
    session = build_session()
    scene = PhaseMissionScene(missions=session, round_idx=0, session_score=0, round_results=[])
    surf = pygame.Surface((1024, 720))
    assert not scene.is_done()
    scene.draw(surf)   # must not raise


def test_phase_mission_space_no_submit_when_empty():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.semantic_space.missions import build_session
    from cognitive_data_arcade.games.semantic_space.phase_mission import PhaseMissionScene
    session = build_session()
    scene = PhaseMissionScene(missions=session, round_idx=0, session_score=0, round_results=[])
    ev = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE, "mod": 0, "unicode": " ", "scancode": 0})
    scene.handle_event(ev)
    assert not scene.is_done()   # neighbors needs 3 selected first


def test_phase_mission_analogy_scene_renders():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.semantic_space.missions import build_session
    from cognitive_data_arcade.games.semantic_space.phase_mission import PhaseMissionScene
    session = build_session()
    # Mission 6 (idx=6) is analogy type
    scene = PhaseMissionScene(missions=session, round_idx=6, session_score=0, round_results=[])
    surf = pygame.Surface((1024, 720))
    scene.draw(surf)   # must not raise


def test_phase_result_renders():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.semantic_space.phase_result import PhaseResultScene
    results = [
        {"type": "neighbors",   "correct": True,  "score": 30},
        {"type": "odd_one_out", "correct": False, "score": 0},
        {"type": "bridge",      "correct": True,  "score": 25},
        {"type": "analogy",     "correct": True,  "score": 30},
    ]
    scene = PhaseResultScene(session_score=85, round_results=results)
    surf = pygame.Surface((1024, 720))
    assert not scene.is_done()
    scene.draw(surf)   # must not raise
    assert scene.next_scene() is None


def test_lesson_24_content_structure():
    from cognitive_data_arcade.lessons.lesson_24 import CONTENT
    for lang in ("pl", "en"):
        assert lang in CONTENT
        for key in ("theory", "notes", "tasks"):
            assert key in CONTENT[lang]
            assert len(CONTENT[lang][key]) >= 2
