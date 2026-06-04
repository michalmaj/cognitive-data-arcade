from cognitive_data_arcade.games.event_log_detective.scenarios import (
    SCENARIOS, Scenario, Decision, Option,
)


def test_three_scenarios():
    assert len(SCENARIOS) == 3


def test_scenario_ids():
    assert [s.id for s in SCENARIOS] == [1, 2, 3]


def test_scenario1_has_six_decisions():
    assert len(SCENARIOS[0].decisions) == 6


def test_scenario2_has_seven_decisions():
    assert len(SCENARIOS[1].decisions) == 7


def test_scenario3_has_six_decisions():
    assert len(SCENARIOS[2].decisions) == 6


def test_each_decision_has_at_least_one_correct_option():
    for scenario in SCENARIOS:
        for dec in scenario.decisions:
            n_correct = sum(1 for opt in dec.options if opt.is_correct)
            assert n_correct >= 1, (
                f"Decision '{dec.title_en}' in scenario {scenario.id} has no correct option"
            )


def test_each_decision_has_2_to_4_options():
    for scenario in SCENARIOS:
        for dec in scenario.decisions:
            assert 2 <= len(dec.options) <= 4, (
                f"Decision '{dec.title_en}' has {len(dec.options)} options"
            )


def test_wrong_options_have_easy_consequence():
    for scenario in SCENARIOS:
        for dec in scenario.decisions:
            for opt in dec.options:
                if not opt.is_correct:
                    assert opt.consequence_easy_en, (
                        f"Wrong option '{opt.label_en}' in '{dec.title_en}' has no consequence"
                    )


def test_all_strings_nonempty():
    for scenario in SCENARIOS:
        assert scenario.title_en
        assert scenario.title_pl
        assert scenario.intro_en
        assert scenario.intro_pl
        for dec in scenario.decisions:
            assert dec.title_en
            assert dec.title_pl
            assert dec.context_en
            assert dec.context_pl
            assert dec.hint_medium_en
            assert dec.hint_medium_pl
            assert dec.report_en
            assert dec.report_pl
