from __future__ import annotations

import pygame
import pytest

from cognitive_data_arcade.engine.i18n import EN, PL
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.ui.reflection_scene import ReflectionScene

_FAKE_REFLECTION = {
    "pl": {
        "title": "Test — Refleksja",
        "cards": [
            {"label": "Karta A", "color": "indigo", "text": "Treść karty A po polsku."},
            {"label": "Karta B", "color": "orange", "text": "Treść karty B po polsku."},
            {"label": "Karta C", "color": "green", "text": "Treść karty C po polsku."},
        ],
        "question": "Pytanie refleksyjne po polsku?",
    },
    "en": {
        "title": "Test — Reflection",
        "cards": [
            {"label": "Card A", "color": "indigo", "text": "Card A content in English."},
            {"label": "Card B", "color": "orange", "text": "Card B content in English."},
            {"label": "Card C", "color": "green", "text": "Card C content in English."},
        ],
        "question": "Reflection question in English?",
    },
}


class _BackScene(Scene):
    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt_ms: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pass

    def is_done(self) -> bool:
        return False


@pytest.fixture(autouse=True)
def pg():
    pygame.init()
    pygame.display.set_mode((1280, 720))
    yield
    pygame.quit()


def _make_scene(strings=EN) -> ReflectionScene:
    return ReflectionScene(_FAKE_REFLECTION, strings, _BackScene())


def test_construct_no_crash() -> None:
    scene = _make_scene()
    assert not scene.is_done()


def test_draw_en_no_crash() -> None:
    scene = _make_scene(EN)
    surface = pygame.Surface((1280, 720))
    scene.draw(surface)  # must not raise


def test_draw_pl_no_crash() -> None:
    scene = _make_scene(PL)
    surface = pygame.Surface((1280, 720))
    scene.draw(surface)  # must not raise


def test_esc_sets_done_and_returns_back() -> None:
    back = _BackScene()
    scene = ReflectionScene(_FAKE_REFLECTION, EN, back)
    assert not scene.is_done()
    esc = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
    scene.handle_event(esc)
    assert scene.is_done()
    assert scene.next_scene() is back


def test_mouse_click_sets_done_and_returns_back() -> None:
    back = _BackScene()
    scene = ReflectionScene(_FAKE_REFLECTION, EN, back)
    click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(640, 360))
    scene.handle_event(click)
    assert scene.is_done()
    assert scene.next_scene() is back


def test_not_done_before_any_event() -> None:
    scene = _make_scene()
    assert scene.next_scene() is None
