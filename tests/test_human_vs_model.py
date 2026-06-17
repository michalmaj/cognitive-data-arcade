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


def test_phase_intro_renders():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.human_vs_model.phase_intro import PhaseIntroScene
    scene = PhaseIntroScene()
    surf = pygame.Surface((1024, 720))
    assert not scene.is_done()
    scene.draw(surf)
    assert scene.next_scene() is None


def test_phase_intro_advances_on_space():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.human_vs_model.phase_intro import PhaseIntroScene
    scene = PhaseIntroScene()
    for _ in range(3):
        ev = pygame.event.Event(pygame.KEYDOWN, {
            "key": pygame.K_SPACE, "mod": 0, "unicode": " ", "scancode": 0
        })
        scene.handle_event(ev)
    assert scene.is_done()
    assert scene.next_scene() is not None


def test_phase_classify_renders():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.human_vs_model.challenge_data import CLASSIFY_CHALLENGES
    from cognitive_data_arcade.games.human_vs_model.phase_classify import PhaseClassifyScene
    scene = PhaseClassifyScene(CLASSIFY_CHALLENGES, 0, 0, 0)
    surf = pygame.Surface((1024, 720))
    assert not scene.is_done()
    scene.draw(surf)


def test_phase_classify_submit_correct():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.human_vs_model.challenge_data import CLASSIFY_CHALLENGES
    from cognitive_data_arcade.games.human_vs_model.phase_classify import PhaseClassifyScene
    scene = PhaseClassifyScene(CLASSIFY_CHALLENGES, 0, 0, 0)
    # CLASSIFY_CHALLENGES[0].answer = "Pozytywny" at index 0 in options
    # Option buttons: y_start = 44+200=244, each h=42, step=52
    # Button 0 center: y = 244 + 0*52 + 21 = 265
    correct = CLASSIFY_CHALLENGES[0].answer
    opt_idx = CLASSIFY_CHALLENGES[0].options.index(correct)
    click_y = 44 + 200 + opt_idx * 52 + 21
    ev = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (256, click_y)})
    scene.handle_event(ev)
    scene.update(2000.0)  # skip AI thinking (> 1500ms)
    space = pygame.event.Event(pygame.KEYDOWN, {
        "key": pygame.K_SPACE, "mod": 0, "unicode": " ", "scancode": 0
    })
    scene.handle_event(space)
    assert scene.is_done()
    nxt = scene.next_scene()
    assert nxt is not None
    assert nxt._session_score >= 10


def test_phase_classify_beat_ai_bonus():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.human_vs_model.challenge_data import CLASSIFY_CHALLENGES
    from cognitive_data_arcade.games.human_vs_model.phase_classify import PhaseClassifyScene
    # CLASSIFY_CHALLENGES[0]: model_answer="Negatywny" != answer="Pozytywny" -> AI fails
    scene = PhaseClassifyScene(CLASSIFY_CHALLENGES, 0, 0, 0)
    correct = CLASSIFY_CHALLENGES[0].answer
    opt_idx = CLASSIFY_CHALLENGES[0].options.index(correct)
    click_y = 44 + 200 + opt_idx * 52 + 21
    ev = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (256, click_y)})
    scene.handle_event(ev)
    scene.update(2000.0)
    space = pygame.event.Event(pygame.KEYDOWN, {
        "key": pygame.K_SPACE, "mod": 0, "unicode": " ", "scancode": 0
    })
    scene.handle_event(space)
    assert scene.is_done()
    nxt = scene.next_scene()
    assert nxt._session_score >= 15  # base 10 + beat-AI bonus 5


def test_phase_detect_renders():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.human_vs_model.challenge_data import DETECT_CHALLENGES
    from cognitive_data_arcade.games.human_vs_model.phase_detect import PhaseDetectScene
    scene = PhaseDetectScene(DETECT_CHALLENGES, 0, 0, 0)
    surf = pygame.Surface((1024, 720))
    assert not scene.is_done()
    scene.draw(surf)


def test_phase_detect_submit_correct():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.human_vs_model.challenge_data import DETECT_CHALLENGES
    from cognitive_data_arcade.games.human_vs_model.phase_detect import PhaseDetectScene
    scene = PhaseDetectScene(DETECT_CHALLENGES, 0, 0, 0)
    # "Lewy" button center: x=133, y=406
    ev = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (133, 406)})
    scene.handle_event(ev)
    scene.update(2000.0)   # skip AI thinking
    space = pygame.event.Event(pygame.KEYDOWN, {
        "key": pygame.K_SPACE, "mod": 0, "unicode": " ", "scancode": 0
    })
    scene.handle_event(space)
    assert scene.is_done()
    nxt = scene.next_scene()
    assert nxt is not None
    assert nxt._session_score >= 30  # base 20 + beat-AI bonus 10


def test_phase_complete_renders():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.human_vs_model.challenge_data import COMPLETE_CHALLENGES
    from cognitive_data_arcade.games.human_vs_model.phase_complete import PhaseCompleteScene
    scene = PhaseCompleteScene(COMPLETE_CHALLENGES, 0, 0, 0)
    surf = pygame.Surface((1024, 720))
    assert not scene.is_done()
    scene.draw(surf)


def test_phase_complete_four_options_displayed():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.human_vs_model.challenge_data import COMPLETE_CHALLENGES
    from cognitive_data_arcade.games.human_vs_model.phase_complete import PhaseCompleteScene
    scene = PhaseCompleteScene(COMPLETE_CHALLENGES, 0, 0, 0)
    rects = scene._option_rects()
    assert len(rects) == 4


def test_phase_complete_submit_correct():
    import pygame; pygame.init()
    from cognitive_data_arcade.games.human_vs_model.challenge_data import COMPLETE_CHALLENGES
    from cognitive_data_arcade.games.human_vs_model.phase_complete import PhaseCompleteScene
    scene = PhaseCompleteScene(COMPLETE_CHALLENGES, 0, 0, 0)
    correct = COMPLETE_CHALLENGES[0].answer
    opt_idx = COMPLETE_CHALLENGES[0].options.index(correct)
    # _OPT_Y_START = 264, _OPT_H = 42, _OPT_STEP = 52
    click_y = 264 + opt_idx * 52 + 21
    ev = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (256, click_y)})
    scene.handle_event(ev)
    scene.update(2000.0)  # skip AI thinking
    space = pygame.event.Event(pygame.KEYDOWN, {
        "key": pygame.K_SPACE, "mod": 0, "unicode": " ", "scancode": 0
    })
    scene.handle_event(space)
    assert scene.is_done()
    nxt = scene.next_scene()
    assert nxt is not None
    assert nxt._session_score >= 30  # base score; could be 45 if beat-AI
