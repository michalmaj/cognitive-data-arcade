from cognitive_data_arcade.engine.badges import BADGE_REGISTRY
from cognitive_data_arcade.engine.i18n import (
    EN,
    PL,
    get_strings,
    level_progress,
    level_title,
)


def test_get_strings_pl_returns_pl() -> None:
    assert get_strings("pl") is PL


def test_get_strings_en_returns_en() -> None:
    assert get_strings("en") is EN


def test_get_strings_unknown_returns_en() -> None:
    assert get_strings("fr") is EN


def test_en_and_pl_have_different_menu_subtitle() -> None:
    assert EN.menu_subtitle != PL.menu_subtitle


def test_en_language_field() -> None:
    assert EN.language == "en"


def test_pl_language_field() -> None:
    assert PL.language == "pl"


def test_all_badge_ids_in_en_badge_names() -> None:
    for badge in BADGE_REGISTRY:
        assert badge.badge_id in EN.badge_names, f"Missing EN name for {badge.badge_id}"


def test_all_badge_ids_in_pl_badge_names() -> None:
    for badge in BADGE_REGISTRY:
        assert badge.badge_id in PL.badge_names, f"Missing PL name for {badge.badge_id}"


def test_level_title_boundaries_en() -> None:
    assert level_title(0, EN) == EN.level_seedling
    assert level_title(499, EN) == EN.level_seedling
    assert level_title(500, EN) == EN.level_explorer
    assert level_title(1500, EN) == EN.level_analyst
    assert level_title(3000, EN) == EN.level_scientist
    assert level_title(5000, EN) == EN.level_hacker
    assert level_title(9999, EN) == EN.level_hacker


def test_level_title_boundaries_pl() -> None:
    assert level_title(0, PL) == PL.level_seedling
    assert level_title(499, PL) == PL.level_seedling
    assert level_title(500, PL) == PL.level_explorer
    assert level_title(1500, PL) == PL.level_analyst
    assert level_title(3000, PL) == PL.level_scientist
    assert level_title(5000, PL) == PL.level_hacker


def test_level_progress_in_first_level() -> None:
    current, total = level_progress(0)
    assert current == 0
    assert total == 500


def test_level_progress_mid_level() -> None:
    current, total = level_progress(750)
    assert current == 250  # 750 - 500
    assert total == 1000  # 1500 - 500


def test_level_progress_at_max_level() -> None:
    current, total = level_progress(5000)
    assert current == 1
    assert total == 1


def test_level_progress_above_max_level() -> None:
    current, total = level_progress(9999)
    assert current == 1
    assert total == 1


def test_en_rt_strings_are_non_trivial() -> None:
    assert len(EN.rt_instructions) > 20
    assert len(EN.rt_too_early) > 2
    assert len(EN.rt_between_blocks) > 10
    assert len(EN.rt_get_ready) > 2
    assert len(EN.rt_hint_space) > 2
    assert len(EN.rt_too_slow) > 2
    assert "\n" in EN.rt_instructions


def test_pl_rt_strings_are_non_trivial() -> None:
    assert len(PL.rt_instructions) > 20
    assert len(PL.rt_too_early) > 2
    assert len(PL.rt_between_blocks) > 10
    assert len(PL.rt_get_ready) > 2
    assert len(PL.rt_hint_space) > 2
    assert len(PL.rt_too_slow) > 2
    assert "\n" in PL.rt_instructions


def test_en_and_pl_rt_strings_differ() -> None:
    assert EN.rt_instructions != PL.rt_instructions
    assert EN.rt_too_early != PL.rt_too_early
    assert EN.rt_between_blocks != PL.rt_between_blocks
    assert EN.rt_get_ready != PL.rt_get_ready
    assert EN.rt_hint_space != PL.rt_hint_space
    assert EN.rt_too_slow != PL.rt_too_slow


def test_en_has_analysis_strings() -> None:
    assert len(EN.analysis_title) > 5
    assert len(EN.analysis_hint_esc) > 2
    assert len(EN.analysis_hint_s) > 2
    assert len(EN.label_median_rt) > 2
    assert len(EN.picker_title) > 2
    assert len(EN.picker_no_sessions) > 10


def test_pl_has_analysis_strings() -> None:
    assert len(PL.analysis_title) > 5
    assert len(PL.picker_no_sessions) > 10


def test_en_and_pl_analysis_strings_differ() -> None:
    assert EN.analysis_title != PL.analysis_title
    assert EN.picker_no_sessions != PL.picker_no_sessions
    assert EN.analysis_hint_esc != PL.analysis_hint_esc
