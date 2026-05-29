from __future__ import annotations

import pytest

from cognitive_data_arcade.engine.i18n import EN, PL


@pytest.mark.parametrize("strings", [PL, EN])
def test_flanker_game_info(strings) -> None:
    from cognitive_data_arcade.engine.pause import GameInfo
    from cognitive_data_arcade.games.flanker.info import get_game_info

    info = get_game_info(strings)
    assert isinstance(info, GameInfo)
    assert info.title
    assert len(info.description_lines) >= 2
    assert len(info.key_bindings) >= 2


@pytest.mark.parametrize("strings", [PL, EN])
def test_gono_game_info(strings) -> None:
    from cognitive_data_arcade.engine.pause import GameInfo
    from cognitive_data_arcade.games.gono.info import get_game_info

    info = get_game_info(strings)
    assert isinstance(info, GameInfo)
    assert info.title
    assert len(info.description_lines) >= 2
    assert len(info.key_bindings) >= 2


@pytest.mark.parametrize("strings", [PL, EN])
def test_stroop_game_info(strings) -> None:
    from cognitive_data_arcade.engine.pause import GameInfo
    from cognitive_data_arcade.games.stroop.info import get_game_info

    info = get_game_info(strings)
    assert isinstance(info, GameInfo)
    assert info.title
    assert len(info.description_lines) >= 2
    assert len(info.key_bindings) >= 2


@pytest.mark.parametrize("strings", [PL, EN])
def test_rt_game_info(strings) -> None:
    from cognitive_data_arcade.engine.pause import GameInfo
    from cognitive_data_arcade.games.reaction_time.info import get_game_info

    info = get_game_info(strings)
    assert isinstance(info, GameInfo)
    assert info.title
    assert len(info.description_lines) >= 2
    assert len(info.key_bindings) >= 2


@pytest.mark.parametrize("strings", [PL, EN])
def test_nback_game_info(strings) -> None:
    from cognitive_data_arcade.engine.pause import GameInfo
    from cognitive_data_arcade.games.nback.info import get_game_info

    info = get_game_info(strings)
    assert isinstance(info, GameInfo)
    assert info.title == "N-Back Memory Grid"
    assert len(info.description_lines) >= 3
    assert len(info.key_bindings) >= 3
    # Key labels must be ASCII-safe (no Unicode arrows)
    for key, _ in info.key_bindings:
        assert key.isascii()
