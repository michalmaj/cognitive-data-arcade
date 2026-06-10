from __future__ import annotations
import pytest
import pygame

@pytest.fixture(autouse=True)
def pygame_init():
    pygame.init()
    pygame.display.set_mode((800, 600))
    yield
    pygame.quit()


def _make_event(etype: int, **kw) -> pygame.event.Event:
    return pygame.event.Event(etype, kw)


def test_no_popup_initially():
    from cognitive_data_arcade.engine.context_popup import ContextInfo, ContextPopup
    popup = ContextPopup()
    surf = pygame.display.get_surface()
    assert surf is not None
    popup.draw(surf)  # should not crash


def test_right_click_inside_registered_rect_shows_popup():
    from cognitive_data_arcade.engine.context_popup import ContextInfo, ContextPopup
    popup = ContextPopup()
    rect = pygame.Rect(100, 100, 200, 50)
    info = ContextInfo(title="Test", body="Body text", impact="Impact text")
    popup.register(rect, info)

    event = _make_event(pygame.MOUSEBUTTONDOWN, button=3, pos=(150, 120))
    consumed = popup.handle_event(event)
    assert consumed is True
    assert popup.is_visible()


def test_right_click_outside_does_not_show_popup():
    from cognitive_data_arcade.engine.context_popup import ContextInfo, ContextPopup
    popup = ContextPopup()
    rect = pygame.Rect(100, 100, 200, 50)
    info = ContextInfo(title="Test", body="Body", impact="Impact")
    popup.register(rect, info)

    event = _make_event(pygame.MOUSEBUTTONDOWN, button=3, pos=(10, 10))
    popup.handle_event(event)
    assert not popup.is_visible()


def test_esc_dismisses_popup():
    from cognitive_data_arcade.engine.context_popup import ContextInfo, ContextPopup
    popup = ContextPopup()
    rect = pygame.Rect(100, 100, 200, 50)
    popup.register(rect, ContextInfo(title="T", body="B", impact="I"))
    popup.handle_event(_make_event(pygame.MOUSEBUTTONDOWN, button=3, pos=(150, 120)))
    assert popup.is_visible()

    popup.handle_event(_make_event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode=""))
    assert not popup.is_visible()


def test_left_click_dismisses_popup():
    from cognitive_data_arcade.engine.context_popup import ContextInfo, ContextPopup
    popup = ContextPopup()
    rect = pygame.Rect(100, 100, 200, 50)
    popup.register(rect, ContextInfo(title="T", body="B", impact="I"))
    popup.handle_event(_make_event(pygame.MOUSEBUTTONDOWN, button=3, pos=(150, 120)))
    popup.handle_event(_make_event(pygame.MOUSEBUTTONDOWN, button=1, pos=(10, 10)))
    assert not popup.is_visible()


def test_clear_removes_all_registrations():
    from cognitive_data_arcade.engine.context_popup import ContextInfo, ContextPopup
    popup = ContextPopup()
    rect = pygame.Rect(100, 100, 200, 50)
    popup.register(rect, ContextInfo(title="T", body="B", impact="I"))
    popup.clear()
    popup.handle_event(_make_event(pygame.MOUSEBUTTONDOWN, button=3, pos=(150, 120)))
    assert not popup.is_visible()


def test_second_right_click_replaces_popup():
    from cognitive_data_arcade.engine.context_popup import ContextInfo, ContextPopup
    popup = ContextPopup()
    r1 = pygame.Rect(10, 10, 100, 40)
    r2 = pygame.Rect(200, 10, 100, 40)
    popup.register(r1, ContextInfo(title="First", body="B1", impact="I1"))
    popup.register(r2, ContextInfo(title="Second", body="B2", impact="I2"))
    popup.handle_event(_make_event(pygame.MOUSEBUTTONDOWN, button=3, pos=(50, 30)))
    popup.handle_event(_make_event(pygame.MOUSEBUTTONDOWN, button=3, pos=(250, 30)))
    assert popup.is_visible()
    assert popup.current_title() == "Second"
