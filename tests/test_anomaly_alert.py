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


def test_element_point_is_anomaly():
    from cognitive_data_arcade.games.anomaly_alert.detector import Element
    el = Element(10.0, 20.0, 0.0, 0.0, True, "spike")
    assert el.is_anomaly
    assert el.w_px == 0.0


def test_compute_round_score_perfect():
    from cognitive_data_arcade.games.anomaly_alert.detector import compute_round_score
    assert compute_round_score(2, 0, 10) == 50    # 2×20 + 10


def test_compute_round_score_no_bonus():
    from cognitive_data_arcade.games.anomaly_alert.detector import compute_round_score
    assert compute_round_score(2, 0, 0) == 40     # 2×20


def test_compute_round_score_with_penalty():
    from cognitive_data_arcade.games.anomaly_alert.detector import compute_round_score
    assert compute_round_score(1, 2, 10) == 20    # 1×20 − 2×5 + 10


def test_compute_round_score_clamped_at_zero():
    from cognitive_data_arcade.games.anomaly_alert.detector import compute_round_score
    assert compute_round_score(0, 10, 0) == 0     # would be −50, clamped


def test_find_clicked_element_point_hit():
    from cognitive_data_arcade.games.anomaly_alert.detector import Element, find_clicked_element
    els = [Element(100.0, 200.0, 0.0, 0.0, True, "A")]
    assert find_clicked_element(els, (107, 206)) == 0  # within 14 px


def test_find_clicked_element_point_miss():
    from cognitive_data_arcade.games.anomaly_alert.detector import Element, find_clicked_element
    els = [Element(100.0, 200.0, 0.0, 0.0, True, "A")]
    assert find_clicked_element(els, (130, 230)) is None  # ~42 px away


def test_find_clicked_element_rect_hit():
    from cognitive_data_arcade.games.anomaly_alert.detector import Element, find_clicked_element
    els = [Element(50.0, 80.0, 30.0, 40.0, False, "bar")]
    assert find_clicked_element(els, (65, 100)) == 0


def test_find_clicked_element_rect_miss():
    from cognitive_data_arcade.games.anomaly_alert.detector import Element, find_clicked_element
    els = [Element(50.0, 80.0, 30.0, 40.0, False, "bar")]
    assert find_clicked_element(els, (200, 300)) is None


def test_find_clicked_element_returns_first_hit():
    from cognitive_data_arcade.games.anomaly_alert.detector import Element, find_clicked_element
    els = [
        Element(100.0, 100.0, 0.0, 0.0, False, "A"),
        Element(100.0, 100.0, 0.0, 0.0, True,  "B"),
    ]
    assert find_clicked_element(els, (100, 100)) == 0
