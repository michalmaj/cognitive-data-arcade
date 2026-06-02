from __future__ import annotations

import pygame
import pytest

from cognitive_data_arcade.engine import audio
from cognitive_data_arcade.engine.i18n import EN, PL
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.ui.lesson_reader import LessonReaderScene


@pytest.fixture(autouse=True)
def audio_ready():
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.font.init()
    audio._sfx = {}  # skip SFX generation
    yield
    pygame.mixer.quit()


def _key(k: int) -> pygame.event.Event:
    return pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode="")


class _Back(Scene):
    def handle_event(self, e): pass
    def update(self, dt): pass
    def draw(self, s): pass
    def is_done(self): return False


# --- lesson 01 exists (created in Task 2) ---

def test_space_navigates_forward():
    scene = LessonReaderScene(1, EN, None)
    assert scene._idx == 0
    scene.handle_event(_key(pygame.K_SPACE))
    assert scene._idx == 1


def test_right_also_navigates_forward():
    scene = LessonReaderScene(1, EN, None)
    scene.handle_event(_key(pygame.K_RIGHT))
    assert scene._idx == 1


def test_left_on_first_slide_does_nothing():
    scene = LessonReaderScene(1, EN, None)
    scene.handle_event(_key(pygame.K_LEFT))
    assert scene._idx == 0
    assert not scene.is_done()


def test_backspace_on_first_slide_does_nothing():
    scene = LessonReaderScene(1, EN, None)
    scene.handle_event(_key(pygame.K_BACKSPACE))
    assert scene._idx == 0


def test_space_on_last_slide_sets_done():
    scene = LessonReaderScene(1, EN, None)
    for _ in range(200):
        if scene.is_done():
            break
        scene.handle_event(_key(pygame.K_SPACE))
    assert scene.is_done()


def test_esc_returns_back_scene():
    back = _Back()
    scene = LessonReaderScene(1, EN, back)
    scene.handle_event(_key(pygame.K_ESCAPE))
    assert scene.is_done()
    assert scene.next_scene() is back


def test_missing_lesson_immediately_done():
    scene = LessonReaderScene(99, EN, None)
    scene.handle_event(_key(pygame.K_SPACE))
    assert scene.is_done()


def test_not_done_before_last_slide():
    scene = LessonReaderScene(1, EN, None)
    assert not scene.is_done()


def test_next_scene_none_when_not_done():
    scene = LessonReaderScene(1, EN, None)
    assert scene.next_scene() is None


def test_draw_does_not_crash():
    pygame.display.init()
    surface = pygame.Surface((1024, 768))
    scene = LessonReaderScene(1, PL, None)
    scene.draw(surface)


def test_pl_content_loads():
    scene = LessonReaderScene(1, PL, None)
    assert len(scene._slides) > 0
    assert scene._slides[0][0] == "theory"
