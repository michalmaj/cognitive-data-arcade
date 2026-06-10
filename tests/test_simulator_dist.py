# tests/test_simulator_dist.py
from __future__ import annotations
import numpy as np
from cognitive_data_arcade.games.distribution_playground.simulator import (
    SimResult, CompareResult,
)

def test_simresult_has_expected_fields():
    r = SimResult(
        samples=np.array([400.0, 420.0]),
        mean=410.0, median=410.0, sd=10.0, iqr=20.0, skewness=0.0,
        dist_type="normal", params={"mu": 400, "sigma": 80, "N": 50},
    )
    assert r.dist_type == "normal"
    assert len(r.samples) == 2

def test_compareresult_has_expected_fields():
    c = CompareResult(delta_mean=50.0, cohens_d=0.8, p_value=0.03, sd_ratio=1.0)
    assert c.p_value == 0.03
