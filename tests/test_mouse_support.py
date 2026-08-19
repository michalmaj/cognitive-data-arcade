from unittest.mock import MagicMock

import pygame
import pytest

from cognitive_data_arcade.engine.mouse import hit

pygame.init()
pygame.display.set_mode((1024, 768))


def test_hit_inside():
    rect = pygame.Rect(10, 10, 100, 50)
    assert hit(rect, (50, 30))


def test_hit_outside():
    rect = pygame.Rect(10, 10, 100, 50)
    assert not hit(rect, (200, 200))


def test_hit_edge():
    rect = pygame.Rect(10, 10, 100, 50)
    assert hit(rect, (10, 10))


def test_hit_just_outside():
    rect = pygame.Rect(10, 10, 100, 50)
    assert not hit(rect, (110, 60))


def _make_menu():
    from cognitive_data_arcade.ui.menu import LessonMenuScene

    pm = MagicMock()
    pm.load.return_value = MagicMock(
        alias="Test",
        device_uuid="x",
        arcade_points=0,
        science_points=0,
        badges=[],
        completed_lessons=[],
        music_enabled=True,
        sfx_enabled=True,
        music_volume=1.0,
        sfx_volume=1.0,
    )
    from cognitive_data_arcade.engine.i18n import get_strings

    strings = get_strings("en")
    return LessonMenuScene(pm, strings)


def test_menu_sidebar_mousemotion_hovers_item():
    pygame.init()
    menu = _make_menu()
    # Module 1 header: virtual y 0-31
    # item 0: virtual y 32-67 → screen y = 56 + 32 = 88, center = 88+18 = 106
    event = pygame.event.Event(pygame.MOUSEMOTION, pos=(100, 106), buttons=(0, 0, 0))
    menu.handle_event(event)
    assert menu._hovered == 0


def test_menu_sidebar_click_selects_item():
    pygame.init()
    menu = _make_menu()
    # item 1: virtual y 68-103 → screen y = 56 + 68 = 124, center = 124+18 = 142
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(100, 142), button=1)
    menu.handle_event(event)
    assert menu._selected == 1


def test_menu_sidebar_click_does_not_show_popup():
    pygame.init()
    menu = _make_menu()
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(100, 142), button=1)
    menu.handle_event(event)
    assert not getattr(menu, "_popup_visible", False)


def test_menu_teoria_available_for_lesson_1():
    menu = _make_menu()
    menu._selected = 0  # lesson 1
    assert menu._teoria_available()


def test_menu_teoria_available_for_lesson_3():
    menu = _make_menu()
    menu._selected = 2  # lesson 3 (index 2) — now has content
    assert menu._teoria_available()


from cognitive_data_arcade.engine.pause import GameInfo, PausableGame


@pytest.fixture(autouse=False)
def _display_1024():
    """Ensure the pygame display is 1024x768 for pause menu coordinate tests."""
    pygame.display.set_mode((1024, 768))
    yield


def _make_pausable():
    inner = MagicMock()
    inner.is_done.return_value = False
    info = GameInfo(title="T", description_lines=[], key_bindings=[])
    pm = MagicMock()
    pm.load.return_value = MagicMock(
        music_enabled=True, sfx_enabled=True, music_volume=1.0, sfx_volume=1.0
    )
    from cognitive_data_arcade.engine.i18n import get_strings

    strings = get_strings("en")
    return PausableGame(inner, info, lambda: inner, strings, pm)


def test_pause_mousemotion_sets_selected(_display_1024):
    pg = _make_pausable()
    pg._paused = True
    # panel at px=342, py=234. Item 1 at y=306+40=346
    event = pygame.event.Event(pygame.MOUSEMOTION, pos=(512, 350))
    pg.handle_event(event)
    assert pg._selected == 1


def test_pause_mousebuttondown_confirms(_display_1024):
    pg = _make_pausable()
    pg._paused = True
    pg._selected = 4  # quit item
    # item 4 at y = 306 + 4*40 = 466
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(512, 466), button=1)
    pg.handle_event(event)
    assert pg._done


def test_session_picker_mousemotion_sets_selected():
    import pathlib
    import tempfile

    from cognitive_data_arcade.ui.session_picker import SessionPickerScene

    pm = MagicMock()
    from cognitive_data_arcade.engine.i18n import get_strings

    strings = get_strings("en")
    with tempfile.TemporaryDirectory() as d:
        # Create at least 3 dummy session CSV files so idx 2 is valid
        header = "reaction_time_ms,correct\n"
        for i in range(3):
            p = pathlib.Path(d) / f"session_{i:02d}.csv"
            p.write_text(header + "250,True\n300,False\n")
        sp = SessionPickerScene(pathlib.Path(d), strings, pm)
        # row 2 at y = 44 + 2*64 = 172
        event = pygame.event.Event(pygame.MOUSEMOTION, pos=(200, 175))
        sp.handle_event(event)
        assert sp._selected == 2


def test_nback_mousemotion_sets_selected():
    from cognitive_data_arcade.ui.nback_level_scene import NBackLevelScene

    pm = MagicMock()
    from cognitive_data_arcade.engine.i18n import get_strings

    strings = get_strings("en")
    scene = NBackLevelScene(pm, strings)
    # option 1 at y = 160 + 1*56 = 216
    event = pygame.event.Event(pygame.MOUSEMOTION, pos=(200, 220))
    scene.handle_event(event)
    assert scene._selected == 1


def test_how_to_play_click_starts_game():
    from cognitive_data_arcade.engine.i18n import get_strings
    from cognitive_data_arcade.engine.pause import GameInfo
    from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

    info = GameInfo(title="T", description_lines=[], key_bindings=[])
    back = MagicMock()
    scene = HowToPlayScene(info, get_strings("en"), back_scene=back)
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(512, 400), button=1)
    scene.handle_event(event)
    assert scene.is_done()
    assert scene.next_scene() is back


def test_lesson_reader_right_click_advances():
    from cognitive_data_arcade.engine.i18n import get_strings
    from cognitive_data_arcade.ui.lesson_reader import LessonReaderScene

    strings = get_strings("en")
    scene = LessonReaderScene(1, strings, back_scene=None)
    initial = scene._idx
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(700, 400), button=1)
    scene.handle_event(event)
    assert scene._idx == (initial + 1) % len(scene._slides)


def test_lesson_reader_left_click_goes_back():
    from cognitive_data_arcade.engine.i18n import get_strings
    from cognitive_data_arcade.ui.lesson_reader import LessonReaderScene

    strings = get_strings("en")
    scene = LessonReaderScene(1, strings, back_scene=None)
    scene._idx = 2
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(200, 400), button=1)
    scene.handle_event(event)
    assert scene._idx == 1


def test_profile_click_edit_button_enters_edit_mode():
    from cognitive_data_arcade.engine.i18n import get_strings
    from cognitive_data_arcade.ui.profile_screen import ProfileScene

    pm = MagicMock()
    pm.load.return_value = MagicMock(
        alias="TestUser",
        arcade_points=0,
        science_points=0,
        badges=[],
        completed_lessons=[],
        quiz_results={},
    )
    back = MagicMock()
    scene = ProfileScene(pm, get_strings("en"), back)
    # Edit button is at Rect(220, h-50+15, 200, 24)
    # For 768h screen: footer_y = 768-50 = 718, button at y=733
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(300, 733), button=1)
    scene.handle_event(event)
    assert scene._editing_alias is True


def test_profile_click_outside_edit_does_not_break_keyboard():
    from cognitive_data_arcade.engine.i18n import get_strings
    from cognitive_data_arcade.ui.profile_screen import ProfileScene

    pm = MagicMock()
    pm.load.return_value = MagicMock(
        alias="TestUser",
        arcade_points=0,
        science_points=0,
        badges=[],
        completed_lessons=[],
        quiz_results={},
    )
    back = MagicMock()
    scene = ProfileScene(pm, get_strings("en"), back)
    # Click somewhere that is NOT the edit button
    click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(100, 100), button=1)
    scene.handle_event(click)
    assert not scene._editing_alias
    # ESC keyboard event should still work
    esc = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
    scene.handle_event(esc)
    assert scene.is_done()


def _make_options():
    pm = MagicMock()
    pm.load.return_value = MagicMock(
        music_enabled=True, sfx_enabled=True, music_volume=0.8, sfx_volume=0.8
    )
    from cognitive_data_arcade.engine.i18n import get_strings
    from cognitive_data_arcade.ui.options_scene import OptionsScene

    return OptionsScene(pm, get_strings("en"), back_scene=None)


def test_options_mousemotion_hover_row1():
    opts = _make_options()
    # row 1 is at y=200
    event = pygame.event.Event(pygame.MOUSEMOTION, pos=(100, 205))
    opts.handle_event(event)
    assert opts._focused == 1


def test_options_mousebuttondown_slider_updates_volume():
    opts = _make_options()
    # music bar at x=230, w=220. Click at x=340 → vol = (340-230)/220 ≈ 0.5
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(340, 130), button=1)
    opts.handle_event(event)
    assert abs(opts._music_vol - (340 - 230) / 220) < 0.01


def test_options_drag_updates_volume():
    opts = _make_options()
    opts._dragging = True
    opts._focused = 0
    event = pygame.event.Event(pygame.MOUSEMOTION, pos=(340, 130))
    opts.handle_event(event)
    assert abs(opts._music_vol - (340 - 230) / 220) < 0.01


def test_options_mousebuttonup_stops_drag():
    opts = _make_options()
    opts._dragging = True
    event = pygame.event.Event(pygame.MOUSEBUTTONUP, pos=(400, 130), button=1)
    opts.handle_event(event)
    assert not opts._dragging


def _make_bdm():
    pm = MagicMock()
    from cognitive_data_arcade.engine.i18n import get_strings
    from cognitive_data_arcade.games.big_data_map.game import BigDataMapGame

    return BigDataMapGame(get_strings("en"), pm)


def test_bdm_node_rects_populated():
    bdm = _make_bdm()
    # _node_by_pos is built in __init__ for all 31 lessons
    from cognitive_data_arcade.games.big_data_map.concept_data import CONCEPT_NODES

    assert len(bdm._node_by_pos) == len(CONCEPT_NODES)


def test_bdm_click_node_selects_it():
    bdm = _make_bdm()
    # Click the first node (initially already selected) -> should not navigate (no factory)
    first_rect, first_node = bdm._node_by_pos[0]
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, pos=(first_rect.centerx, first_rect.centery), button=1
    )
    # First click on already-selected node tries to navigate; no factory -> nothing happens
    bdm.handle_event(event)
    # With no factory, done stays False and no navigation
    assert bdm.is_done() is False


def test_bdm_click_second_node_selects_it():
    bdm = _make_bdm()
    # Click a node that is not currently selected
    second_rect, second_node = bdm._node_by_pos[3]
    # Ensure it's not the default selection
    if bdm._selected == second_node.lesson_num:
        second_rect, second_node = bdm._node_by_pos[5]
    event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, pos=(second_rect.centerx, second_rect.centery), button=1
    )
    bdm.handle_event(event)
    assert bdm._selected == second_node.lesson_num


import pathlib
import tempfile


def _make_stroop():
    pm = MagicMock()
    pm.load.return_value = MagicMock(
        alias="T",
        device_uuid="x",
        arcade_points=0,
        science_points=0,
        badges=[],
        completed_lessons=[],
    )
    from cognitive_data_arcade.engine.i18n import get_strings
    from cognitive_data_arcade.games.stroop.config import STANDARD
    from cognitive_data_arcade.games.stroop.game import StroopGame

    strings = get_strings("en")
    with tempfile.TemporaryDirectory() as d:
        return StroopGame(STANDARD, pm, strings, "p1", "s1", pathlib.Path(d) / "test.csv")


def test_stroop_has_color_rects():
    sg = _make_stroop()
    assert hasattr(sg, "_color_rects")


def test_stroop_preset_mousemotion_sets_idx():
    sg = _make_stroop()
    # preset options at y=280, 336, 392 (280 + i*56)
    event = pygame.event.Event(pygame.MOUSEMOTION, pos=(512, 340))
    sg.handle_event(event)
    assert sg._preset_idx == 1  # y=340 is closest to option 1 (y=336)


def test_stroop_preset_mouseclick_confirms():
    sg = _make_stroop()
    from cognitive_data_arcade.games.stroop.game import _Phase

    # Draw first to populate preset rects
    surf = pygame.display.get_surface()
    sg.draw(surf)
    # click option 0 rect area
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(512, 285), button=1)
    sg.handle_event(event)
    assert sg._phase == _Phase.INSTRUCTIONS
