# tests/test_anomaly_alert.py
from __future__ import annotations


def test_scenarios_count():
    from cognitive_data_arcade.games.anomaly_alert.scenarios import SCENARIOS
    assert len(SCENARIOS) == 6


def test_scenarios_chart_types_unique():
    from cognitive_data_arcade.games.anomaly_alert.scenarios import SCENARIOS
    types = [s.chart_type for s in SCENARIOS]
    assert len(set(types)) == 6


def test_scenarios_fixed_order():
    from cognitive_data_arcade.games.anomaly_alert.scenarios import SCENARIOS
    expected = ["timeseries", "barchart", "scatter", "histogram", "boxplot", "heatmap"]
    assert [s.chart_type for s in SCENARIOS] == expected


def test_scenarios_anomaly_count():
    from cognitive_data_arcade.games.anomaly_alert.scenarios import SCENARIOS
    for s in SCENARIOS:
        assert s.n_anomalies == 2


def test_polish_diacritics_in_scenarios():
    from cognitive_data_arcade.games.anomaly_alert.scenarios import SCENARIOS
    required = ["ą", "ę", "ś", "ź", "ż", "ó", "ń", "ł", "ć"]
    all_text = " ".join(s.name_pl + s.hint_pl + s.insight_pl for s in SCENARIOS)
    missing = [ch for ch in required if ch not in all_text]
    assert not missing, f"Missing Polish diacritics: {missing}"
