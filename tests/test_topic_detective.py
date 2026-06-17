from __future__ import annotations

import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")


def test_topics_have_enough_words():
    from cognitive_data_arcade.games.topic_detective.topic_data import TOPICS
    for key, td in TOPICS.items():
        assert len(td["words"]) >= 10, f"{key} has only {len(td['words'])} words"


def test_documents_weights_sum_to_one():
    from cognitive_data_arcade.games.topic_detective.topic_data import DOCUMENTS
    for i, doc in enumerate(DOCUMENTS):
        total = sum(doc["weights"].values())
        assert abs(total - 1.0) <= 0.01, f"doc {i} weights sum to {total}"


def test_documents_dominant_is_max_weight():
    from cognitive_data_arcade.games.topic_detective.topic_data import DOCUMENTS
    for i, doc in enumerate(DOCUMENTS):
        max_key = max(doc["weights"], key=lambda k: doc["weights"][k])
        assert doc["dominant"] == max_key, (
            f"doc {i}: dominant={doc['dominant']} but max weight is {max_key}"
        )


def test_intruder_not_in_topic_words():
    from cognitive_data_arcade.games.topic_detective.topic_data import INTRUDER_SETS, TOPICS
    for s in INTRUDER_SETS:
        topic_words = TOPICS[s["topic"]]["words"]
        assert s["intruder"] not in topic_words, (
            f"intruder '{s['intruder']}' found in topic '{s['topic']}' words"
        )


def test_intruder_sets_count():
    from cognitive_data_arcade.games.topic_detective.topic_data import INTRUDER_SETS
    assert len(INTRUDER_SETS) == 8


def test_intruder_set_words_length():
    from cognitive_data_arcade.games.topic_detective.topic_data import INTRUDER_SETS
    for i, s in enumerate(INTRUDER_SETS):
        assert len(s["words"]) == 8, f"intruder set {i} has {len(s['words'])} words, expected 8"


def test_data_counts():
    from cognitive_data_arcade.games.topic_detective.topic_data import DOCUMENTS, TOPICS
    assert len(TOPICS) == 5
    assert len(DOCUMENTS) == 15


def test_build_session_length():
    from cognitive_data_arcade.games.topic_detective.missions import build_session
    assert len(build_session()) == 8


def test_build_session_order():
    from cognitive_data_arcade.games.topic_detective.missions import build_session
    types = [m.type for m in build_session()]
    assert types[:3] == ["name_topic", "name_topic", "name_topic"]
    assert types[3:6] == ["assign_doc", "assign_doc", "assign_doc"]
    assert types[6:] == ["intruder", "intruder"]


def test_build_session_difficulty_ascending():
    from cognitive_data_arcade.games.topic_detective.missions import build_session
    session = build_session()
    assert [m.difficulty for m in session] == [1, 1, 2, 1, 2, 2, 2, 3]


def test_game_scene_instantiates():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.topic_detective.game import TopicDetectiveScene
    scene = TopicDetectiveScene()
    assert not scene.is_done()
    assert scene.next_scene() is None


def test_phase_intro_renders():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.topic_detective.phase_intro import PhaseIntroScene
    scene = PhaseIntroScene()
    surf = pygame.Surface((1024, 720))
    assert not scene.is_done()
    scene.draw(surf)
    assert scene.next_scene() is None


def test_phase_intro_advances_on_space():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.topic_detective.phase_intro import PhaseIntroScene
    scene = PhaseIntroScene()
    for _ in range(3):
        ev = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE, "mod": 0, "unicode": " ", "scancode": 0})
        scene.handle_event(ev)
    assert scene.is_done()
    assert scene.next_scene() is not None


def test_phase_mission_name_topic_renders():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.topic_detective.missions import build_session
    from cognitive_data_arcade.games.topic_detective.phase_mission import PhaseMissionScene
    session = build_session()
    # Mission 0 is name_topic
    scene = PhaseMissionScene(missions=session, round_idx=0, session_score=0, round_results=[])
    surf = pygame.Surface((1024, 720))
    assert not scene.is_done()
    scene.draw(surf)


def test_phase_mission_assign_doc_renders():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.topic_detective.missions import build_session
    from cognitive_data_arcade.games.topic_detective.phase_mission import PhaseMissionScene
    session = build_session()
    # Mission 3 is assign_doc
    scene = PhaseMissionScene(missions=session, round_idx=3, session_score=0, round_results=[])
    surf = pygame.Surface((1024, 720))
    assert not scene.is_done()
    scene.draw(surf)


def test_phase_mission_intruder_renders():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.topic_detective.missions import build_session
    from cognitive_data_arcade.games.topic_detective.phase_mission import PhaseMissionScene
    session = build_session()
    # Mission 6 is intruder
    scene = PhaseMissionScene(missions=session, round_idx=6, session_score=0, round_results=[])
    surf = pygame.Surface((1024, 720))
    assert not scene.is_done()
    scene.draw(surf)


def test_phase_result_renders():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.topic_detective.phase_result import PhaseResultScene
    results = [
        {"type": "name_topic", "correct": True,  "score": 15},
        {"type": "name_topic", "correct": False, "score": 0},
        {"type": "name_topic", "correct": True,  "score": 15},
        {"type": "assign_doc", "correct": True,  "score": 20},
        {"type": "assign_doc", "correct": False, "score": 0},
        {"type": "assign_doc", "correct": True,  "score": 20},
        {"type": "intruder",   "correct": True,  "score": 25},
        {"type": "intruder",   "correct": False, "score": 0},
    ]
    scene = PhaseResultScene(session_score=95, round_results=results)
    surf = pygame.Surface((1024, 720))
    assert not scene.is_done()
    scene.draw(surf)
    assert scene.next_scene() is None


def test_lesson_25_content_structure():
    from cognitive_data_arcade.lessons.lesson_25 import CONTENT
    for lang in ("pl", "en"):
        assert lang in CONTENT
        for key in ("theory", "notes", "tasks"):
            assert key in CONTENT[lang], f"missing {key} in {lang}"
            assert len(CONTENT[lang][key]) >= 2, f"{lang}.{key} has too few items"


def test_menu_has_lesson_25():
    from cognitive_data_arcade.ui.menu import _LESSONS
    nums = [n for n, _ in _LESSONS]
    assert 25 in nums
