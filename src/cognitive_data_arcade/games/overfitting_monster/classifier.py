from __future__ import annotations

import numpy as np
from sklearn.neighbors import KNeighborsClassifier


def split_data(
    X: np.ndarray,
    y: np.ndarray,
    split_pct: int,
    seed: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Shuffle and split X, y into train/test sets.

    split_pct: integer 50-80 (percentage of data used for training).
    seed: round seed; offset internally to avoid correlation with data generation.
    Returns (X_train, y_train, X_test, y_test).
    """
    n = len(X)
    rng = np.random.default_rng(seed + 1_000_000)
    idx = rng.permutation(n)
    n_train = max(2, round(n * split_pct / 100))
    return X[idx[:n_train]], y[idx[:n_train]], X[idx[n_train:]], y[idx[n_train:]]


def knn_accuracies(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    k: int,
) -> dict[str, float]:
    """Fit KNN(k) on train, evaluate on both train and test.

    Returns {"train": float, "test": float}.
    """
    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(X_train, y_train)
    return {
        "train": float(clf.score(X_train, y_train)),
        "test": float(clf.score(X_test, y_test)),
    }


def compute_gap_stars(train_acc: float, test_acc: float) -> int:
    """Return generalisation star rating (1-3) based on train-test gap.

    gap < 5 pp  -> 3 stars (+20 pts bonus)
    5 <= gap < 15 pp -> 2 stars (+10 pts bonus)
    gap >= 15 pp -> 1 star (+0 pts bonus)
    """
    gap = (train_acc - test_acc) * 100
    if gap < 5.0:
        return 3
    if gap < 15.0:
        return 2
    return 1


def compute_round_score(test_acc: float, stars: int) -> int:
    """Round score = round(test_acc * 100) + generalisation bonus."""
    bonus = {3: 20, 2: 10, 1: 0}[stars]
    return round(test_acc * 100) + bonus
