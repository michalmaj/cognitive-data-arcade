from __future__ import annotations

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


def player_accuracy(
    polyline: list[tuple[float, float]],
    X: np.ndarray,
    y: np.ndarray,
) -> float:
    """
    polyline: list of (x, y) in normalised [0,1] space, top-to-bottom.
    X: (n, 2) data points in [0,1].
    y: (n,) integer labels 0 or 1.
    Returns fraction of correctly labelled points.
    """
    pred = predict_labels(polyline, X, y)
    return float(np.mean(pred == y))


def _interp_boundary_x(xs: np.ndarray, ys: np.ndarray, py: float) -> float:
    """X-coordinate of the boundary polyline at height py (all in [0,1] space)."""
    y_min, y_max = float(ys.min()), float(ys.max())
    if py <= y_min:
        return float(xs[int(np.argmin(ys))])
    if py >= y_max:
        return float(xs[int(np.argmax(ys))])
    for i in range(len(ys) - 1):
        y0, y1 = float(ys[i]), float(ys[i + 1])
        if min(y0, y1) <= py <= max(y0, y1):
            t = (py - y0) / (y1 - y0 + 1e-12)
            return float(xs[i] + t * (xs[i + 1] - xs[i]))
    # Fallback: x of nearest point
    return float(xs[int(np.argmin(np.abs(ys - py)))])


def predict_labels(
    polyline: list[tuple[float, float]],
    X: np.ndarray,
    y: np.ndarray,
) -> np.ndarray:
    """Return predicted integer label for each data point given the drawn boundary."""
    if len(polyline) < 2:
        return np.zeros(len(X), dtype=np.int32)

    xs_poly = np.array([p[0] for p in polyline], dtype=float)
    ys_poly = np.array([p[1] for p in polyline], dtype=float)

    sides = np.array([X[i, 0] < _interp_boundary_x(xs_poly, ys_poly, float(X[i, 1]))
                      for i in range(len(X))])
    left_class0 = int(np.sum((y == 0) & sides))
    right_class0 = int(np.sum((y == 0) & ~sides))
    if left_class0 >= right_class0:
        return np.where(sides, 0, 1).astype(np.int32)
    return np.where(sides, 1, 0).astype(np.int32)


def classifier_accuracies(
    X: np.ndarray, y: np.ndarray, seed: int = 0
) -> dict[str, float]:
    """5-fold cross-validated accuracy for three standard classifiers."""
    clfs: dict[str, object] = {
        "liniowy": LogisticRegression(max_iter=1000, random_state=seed),
        "knn": KNeighborsClassifier(n_neighbors=5),
        "drzewo": DecisionTreeClassifier(max_depth=3, random_state=seed),
    }
    n_splits = max(2, min(5, int(np.bincount(y.astype(int)).min())))
    result: dict[str, float] = {}
    for name, clf in clfs.items():
        scores = cross_val_score(clf, X, y, cv=n_splits, scoring="accuracy")
        result[name] = float(scores.mean())
    return result


def compute_round_score(player_acc: float, clf_accs: dict[str, float]) -> int:
    base = round(player_acc * 100)
    bonus = 0
    if player_acc > clf_accs["liniowy"]:
        bonus += 15
    if player_acc > clf_accs["knn"]:
        bonus += 20
    return base + bonus
