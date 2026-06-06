# src/cognitive_data_arcade/games/data_cleaning/generator.py
from __future__ import annotations

import enum
import math
import random
from dataclasses import dataclass


class ErrorType(enum.Enum):
    NEGATIVE_RT = "negative_rt"
    OUTLIER_PLACEHOLDER = "outlier_placeholder"
    MISSING_VALUE = "missing_value"
    DUPLICATE_ROW = "duplicate_row"
    WRONG_FORMAT_ACCURACY = "wrong_format_accuracy"


@dataclass
class DataRow:
    participant_id: int
    session: int
    trial: int
    rt_ms: float | None
    accuracy: float | None


@dataclass
class CleaningSession:
    rows: list[DataRow]
    ground_truth: dict[int, ErrorType]  # row_index → ErrorType; not shown to student


_OUTLIER_VALUES = (9999.0, -99.0, 0.0)

# ── Easy-mode feedback text shown in IDENTIFY phase ─────────────────────────────

IDENTIFY_HINTS_EN: dict[ErrorType, str] = {
    ErrorType.NEGATIVE_RT: "Good catch! RT cannot be negative — this is invalid data.",
    ErrorType.OUTLIER_PLACEHOLDER: "Good catch! 9999/-99/0 is a placeholder, not a real RT.",
    ErrorType.MISSING_VALUE: "Good catch! Missing RT means the participant did not respond.",
    ErrorType.DUPLICATE_ROW: "Good catch! Same participant_id + trial as another row — duplicate.",
    ErrorType.WRONG_FORMAT_ACCURACY: "Good catch! Accuracy 85 means 85% — should be stored as 0.85.",
}

IDENTIFY_HINTS_PL: dict[ErrorType, str] = {
    ErrorType.NEGATIVE_RT: "Dobry wynik! RT nie może być ujemny — te dane są nieprawidłowe.",
    ErrorType.OUTLIER_PLACEHOLDER: "Dobry wynik! 9999/-99/0 to znacznik zastępczy, nie prawdziwy RT.",
    ErrorType.MISSING_VALUE: "Dobry wynik! Brakujący RT oznacza, że uczestnik nie odpowiedział.",
    ErrorType.DUPLICATE_ROW: "Dobry wynik! Ten sam participant_id + trial co inny wiersz — duplikat.",
    ErrorType.WRONG_FORMAT_ACCURACY: "Dobry wynik! Dokładność 85 oznacza 85% — powinna być zapisana jako 0.85.",
}

FALSE_FLAG_HINT_EN = "This value looks fine — no data quality issue detected."
FALSE_FLAG_HINT_PL = "Ta wartość wygląda prawidłowo — nie wykryto problemu z jakością danych."

# ── Fix-phase feedback lookup ────────────────────────────────────────────────────

_FIX_FEEDBACK: dict[tuple[ErrorType, str], str] = {
    (ErrorType.NEGATIVE_RT, "delete"): "correct",
    (ErrorType.NEGATIVE_RT, "median"): "suboptimal",
    (ErrorType.NEGATIVE_RT, "keep"): "wrong",
    (ErrorType.OUTLIER_PLACEHOLDER, "delete"): "correct",
    (ErrorType.OUTLIER_PLACEHOLDER, "median"): "suboptimal",
    (ErrorType.OUTLIER_PLACEHOLDER, "keep"): "wrong",
    (ErrorType.MISSING_VALUE, "delete"): "correct",
    (ErrorType.MISSING_VALUE, "median"): "correct",
    (ErrorType.MISSING_VALUE, "keep"): "wrong",
    (ErrorType.DUPLICATE_ROW, "delete"): "correct",
    (ErrorType.DUPLICATE_ROW, "median"): "wrong",
    (ErrorType.DUPLICATE_ROW, "keep"): "wrong",
    (ErrorType.WRONG_FORMAT_ACCURACY, "fix_format"): "correct",
    (ErrorType.WRONG_FORMAT_ACCURACY, "delete"): "suboptimal",
    (ErrorType.WRONG_FORMAT_ACCURACY, "median"): "wrong",
    (ErrorType.WRONG_FORMAT_ACCURACY, "keep"): "wrong",
}

_FIX_CORRECT_EN: dict[ErrorType, str] = {
    ErrorType.NEGATIVE_RT: "Correct! Negative RT is invalid — deleting removes the error.",
    ErrorType.OUTLIER_PLACEHOLDER: "Correct! Placeholder values (9999/-99/0) are not real data — deleted.",
    ErrorType.MISSING_VALUE: "Correct! Missing RT can be removed or replaced with the median.",
    ErrorType.DUPLICATE_ROW: "Correct! Duplicate rows inflate the dataset — copy deleted.",
    ErrorType.WRONG_FORMAT_ACCURACY: "Correct! Accuracy 85 means 85% — dividing by 100 gives 0.85.",
}

_FIX_SUBOPTIMAL_EN: dict[ErrorType, str] = {
    ErrorType.NEGATIVE_RT: "Possible but not optimal. The value was never real — deletion is safer.",
    ErrorType.OUTLIER_PLACEHOLDER: "Possible but not optimal. Placeholder was not real — deletion is safer.",
    ErrorType.MISSING_VALUE: "Both options are valid here — well done.",
    ErrorType.DUPLICATE_ROW: "Incorrect: imputation does not fix a duplicate — delete the copy.",
    ErrorType.WRONG_FORMAT_ACCURACY: "Possible but not optimal — fixing the format preserves the data point.",
}

_FIX_WRONG_EN: dict[ErrorType, str] = {
    ErrorType.NEGATIVE_RT: "Incorrect: keeping a negative RT will bias your mean RT.",
    ErrorType.OUTLIER_PLACEHOLDER: "Incorrect: placeholder values distort statistics — do not keep them.",
    ErrorType.MISSING_VALUE: "Incorrect: a None RT will cause errors in downstream analysis.",
    ErrorType.DUPLICATE_ROW: "Incorrect: duplicate rows inflate your n and distort effect sizes.",
    ErrorType.WRONG_FORMAT_ACCURACY: "Incorrect: an accuracy of 85 is not a valid proportion — fix it.",
}

_FIX_CORRECT_PL: dict[ErrorType, str] = {
    ErrorType.NEGATIVE_RT: "Prawidłowo! Ujemny RT jest nieprawidłowy — usunięcie wiersza to dobry wybór.",
    ErrorType.OUTLIER_PLACEHOLDER: "Prawidłowo! Wartości zastępcze (9999/-99/0) to nie prawdziwe dane — usunięto.",
    ErrorType.MISSING_VALUE: "Prawidłowo! Brakujący RT można usunąć lub zastąpić medianą.",
    ErrorType.DUPLICATE_ROW: "Prawidłowo! Duplikaty zawyżają n — kopia usunięta.",
    ErrorType.WRONG_FORMAT_ACCURACY: "Prawidłowo! Dokładność 85 oznacza 85% — podzielenie przez 100 daje 0.85.",
}

_FIX_SUBOPTIMAL_PL: dict[ErrorType, str] = {
    ErrorType.NEGATIVE_RT: "Możliwe, ale nie optymalne. Wartość była fałszywa — usunięcie jest bezpieczniejsze.",
    ErrorType.OUTLIER_PLACEHOLDER: "Możliwe, ale nie optymalne. Znacznik zastępczy nie był prawdziwą daną.",
    ErrorType.MISSING_VALUE: "Obie opcje są tutaj prawidłowe — dobra robota.",
    ErrorType.DUPLICATE_ROW: "Nieprawidłowo: imputacja nie naprawia duplikatu — usuń kopię.",
    ErrorType.WRONG_FORMAT_ACCURACY: "Możliwe, ale nie optymalne — naprawa formatu zachowuje punkt danych.",
}

_FIX_WRONG_PL: dict[ErrorType, str] = {
    ErrorType.NEGATIVE_RT: "Nieprawidłowo: zachowanie ujemnego RT zaburzy średni czas reakcji.",
    ErrorType.OUTLIER_PLACEHOLDER: "Nieprawidłowo: wartości zastępcze zniekształcają statystyki.",
    ErrorType.MISSING_VALUE: "Nieprawidłowo: None w RT spowoduje błędy w dalszej analizie.",
    ErrorType.DUPLICATE_ROW: "Nieprawidłowo: duplikaty zawyżają n i zniekształcają efekty.",
    ErrorType.WRONG_FORMAT_ACCURACY: "Nieprawidłowo: dokładność 85 to nie prawidłowa proporcja.",
}

_FALSE_POS_CORRECT_EN = "Good judgment — this row looks fine, no action needed."
_FALSE_POS_WRONG_EN = "Incorrect: this row has no data quality issue — keeping is the right choice."
_FALSE_POS_CORRECT_PL = "Dobra ocena — ten wiersz wygląda prawidłowo, żadna akcja nie jest potrzebna."
_FALSE_POS_WRONG_PL = "Nieprawidłowo: ten wiersz nie ma problemu z jakością — zachowanie go to właściwy wybór."


def get_fix_feedback(error_type: ErrorType | None, fix: str) -> str:
    """Return 'correct', 'suboptimal', or 'wrong'."""
    if error_type is None:
        return "correct" if fix == "keep" else "wrong"
    return _FIX_FEEDBACK.get((error_type, fix), "wrong")


def get_fix_feedback_text(
    error_type: ErrorType | None, fix: str, level: str, lang: str
) -> str:
    """Return human-readable feedback for the FIX phase."""
    if error_type is None:
        if level == "correct":
            return _FALSE_POS_CORRECT_PL if lang == "pl" else _FALSE_POS_CORRECT_EN
        return _FALSE_POS_WRONG_PL if lang == "pl" else _FALSE_POS_WRONG_EN

    if level == "correct":
        m = _FIX_CORRECT_PL if lang == "pl" else _FIX_CORRECT_EN
    elif level == "suboptimal":
        m = _FIX_SUBOPTIMAL_PL if lang == "pl" else _FIX_SUBOPTIMAL_EN
    else:
        m = _FIX_WRONG_PL if lang == "pl" else _FIX_WRONG_EN
    return m.get(error_type, "")


# ── Dataset generator ────────────────────────────────────────────────────────────

def generate_dataset(
    config: "DifficultyConfig",
    seed: int | None = None,
) -> CleaningSession:
    """Generate a synthetic RT dataset with injected errors per config."""
    from cognitive_data_arcade.games.data_cleaning.difficulty import DifficultyConfig
    rng = random.Random(seed)
    n_rows = config.rows

    clean_rows: list[DataRow] = []
    for i in range(n_rows):
        clean_rows.append(DataRow(
            participant_id=(i // 3) + 1,
            session=1,
            trial=(i % 3) + 1,
            rt_ms=round(rng.uniform(250.0, 750.0), 1),
            accuracy=round(rng.uniform(0.65, 1.00), 2),
        ))

    rows = [DataRow(r.participant_id, r.session, r.trial, r.rt_ms, r.accuracy)
            for r in clean_rows]

    n_errors = rng.randint(config.errors_min, config.errors_max)
    positions = rng.sample(range(n_rows), n_errors)
    error_types = list(ErrorType)
    ground_truth: dict[int, ErrorType] = {}

    for pos in positions:
        error_type = rng.choice(error_types)
        row = rows[pos]

        if error_type == ErrorType.NEGATIVE_RT:
            rows[pos] = DataRow(row.participant_id, row.session, row.trial,
                                float(-rng.randint(10, 200)), row.accuracy)
        elif error_type == ErrorType.OUTLIER_PLACEHOLDER:
            rows[pos] = DataRow(row.participant_id, row.session, row.trial,
                                rng.choice(_OUTLIER_VALUES), row.accuracy)
        elif error_type == ErrorType.MISSING_VALUE:
            rows[pos] = DataRow(row.participant_id, row.session, row.trial,
                                None, row.accuracy)
        elif error_type == ErrorType.DUPLICATE_ROW:
            candidates = [j for j in range(n_rows) if j != pos and j not in positions]
            if not candidates:
                candidates = [j for j in range(n_rows) if j != pos and j not in ground_truth]
            if not candidates:
                candidates = [j for j in range(n_rows) if j != pos]
            src_idx = rng.choice(candidates)
            src = clean_rows[src_idx]
            rows[pos] = DataRow(src.participant_id, src.session, src.trial,
                                src.rt_ms, src.accuracy)
        elif error_type == ErrorType.WRONG_FORMAT_ACCURACY:
            rows[pos] = DataRow(row.participant_id, row.session, row.trial,
                                row.rt_ms, float(round(row.accuracy * 100)))

        ground_truth[pos] = error_type

    return CleaningSession(rows=rows, ground_truth=ground_truth)


# ── Stats and scoring ────────────────────────────────────────────────────────────

def compute_stats(rows: list[DataRow]) -> dict[str, float]:
    """Summary statistics; filters out invalid/missing/wrong-format values."""
    valid_rt = [r.rt_ms for r in rows
                if r.rt_ms is not None and -50.0 < r.rt_ms < 9000.0
                and r.rt_ms not in _OUTLIER_VALUES]
    valid_acc = [r.accuracy for r in rows
                 if r.accuracy is not None and 0.0 <= r.accuracy <= 1.0]
    mean_rt = sum(valid_rt) / len(valid_rt) if valid_rt else 0.0
    var_rt = (sum((x - mean_rt) ** 2 for x in valid_rt) / (len(valid_rt) - 1)
              if len(valid_rt) > 1 else 0.0)
    mean_acc = sum(valid_acc) / len(valid_acc) if valid_acc else 0.0
    return {
        "n_rows": float(len(rows)),
        "mean_rt": mean_rt,
        "std_rt": math.sqrt(var_rt),
        "mean_accuracy": mean_acc,
    }


def apply_fixes(
    session: CleaningSession,
    flagged: set[int],
    fixes: dict[int, str],
) -> list[DataRow]:
    """Apply student fixes and return the cleaned row list."""
    rows = session.rows
    # Compute median RT from un-flagged rows (for imputation)
    clean_rt = sorted(r.rt_ms for i, r in enumerate(rows)
                      if r.rt_ms is not None and i not in flagged)
    if clean_rt:
        mid = len(clean_rt) // 2
        median_rt = (clean_rt[mid] if len(clean_rt) % 2 == 1
                     else (clean_rt[mid - 1] + clean_rt[mid]) / 2.0)
    else:
        median_rt = 500.0

    result: list[DataRow] = []
    for i, row in enumerate(rows):
        if i not in flagged:
            result.append(row)
            continue
        fix = fixes.get(i, "keep")
        if fix == "delete":
            continue
        elif fix == "median":
            result.append(DataRow(row.participant_id, row.session, row.trial,
                                  median_rt, row.accuracy))
        elif fix == "fix_format":
            new_acc = row.accuracy / 100.0 if row.accuracy is not None else None
            result.append(DataRow(row.participant_id, row.session, row.trial,
                                  row.rt_ms, new_acc))
        else:  # keep
            result.append(row)
    return result


def compute_score(
    session: CleaningSession,
    flagged: set[int],
    fixes: dict[int, str],
) -> tuple[int, int, int]:
    """
    Return (detection_component, fix_component, total_score).
    detection: 0-60 based on fraction of errors found.
    fix:       0-40 based on fraction of correct fixes among flagged rows.
    total:     detection + fix.
    """
    total_errors = len(session.ground_truth)
    found = flagged & set(session.ground_truth.keys())
    det_rate = len(found) / total_errors if total_errors > 0 else 0.0

    correct_fixes = sum(
        1 for idx in flagged
        if get_fix_feedback(session.ground_truth.get(idx), fixes.get(idx, "keep")) == "correct"
    )
    fix_rate = correct_fixes / len(flagged) if flagged else 0.0

    d = round(det_rate * 60)
    f = round(fix_rate * 40)
    return d, f, d + f
