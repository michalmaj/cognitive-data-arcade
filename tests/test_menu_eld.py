import pygame
from cognitive_data_arcade.engine.i18n import EN
from cognitive_data_arcade.ui.menu import LessonMenuScene
from cognitive_data_arcade.ui.event_log_level_scene import EventLogLevelScene


class _FakePM:
    class _Profile:
        device_uuid = "test-uuid"
        language = "en"

    def load(self):
        return self._Profile()

    def set_language(self, lang):
        pass


def _make_menu():
    pygame.init()
    return LessonMenuScene(_FakePM(), EN, selected=2)  # index 2 = lesson 3


def test_lesson3_selected_index():
    menu = _make_menu()
    assert menu._selected == 2


def test_lesson3_factory_returns_event_log_level_scene():
    menu = _make_menu()
    factory = menu._game_factory_for(3)
    assert factory is not None
    scene = factory()
    assert isinstance(scene, EventLogLevelScene)
