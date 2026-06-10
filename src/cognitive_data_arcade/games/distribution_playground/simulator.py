# src/cognitive_data_arcade/games/distribution_playground/simulator.py
from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass
class SimResult:
    samples:   np.ndarray
    mean:      float
    median:    float
    sd:        float
    iqr:       float
    skewness:  float
    dist_type: str        # "normal" | "uniform" | "exgaussian"
    params:    dict[str, float]


@dataclass
class CompareResult:
    delta_mean: float    # mean_b - mean_a
    cohens_d:   float    # (mean_a - mean_b) / pooled_sd
    p_value:    float    # Welch t-test
    sd_ratio:   float    # sd_a / sd_b
