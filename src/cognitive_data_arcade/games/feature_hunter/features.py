from __future__ import annotations

import random
from dataclasses import dataclass

from cognitive_data_arcade.games.feature_hunter.config import DifficultyConfig


@dataclass(frozen=True)
class Feature:
    name_pl: str
    name_en: str
    category: str       # "temporal"|"demographic"|"physiological"|"environmental"|"task_history"|"noise"
    correlation: float  # true r in [-1.0, 1.0]
    noise: float        # scatter spread multiplier [0.2, 0.6]
    x_label_pl: str
    y_label_pl: str

    @property
    def is_signal(self) -> bool:
        return abs(self.correlation) >= 0.25


# ---------------------------------------------------------------------------
# Feature bank — 60 entries across 6 categories (10 each)
# Target variable: reaction time in ms (higher = slower)
# ---------------------------------------------------------------------------
FEATURE_BANK: list[Feature] = [
    # --- temporal (10) ---
    Feature("Pora dnia", "time_of_day", "temporal", 0.75, 0.30, "Pora dnia (h)", "Czas reakcji (ms)"),
    Feature("Godziny snu", "sleep_hours", "temporal", 0.65, 0.35, "Godziny snu", "Czas reakcji (ms)"),
    Feature("Jakość snu", "sleep_quality", "temporal", 0.70, 0.30, "Jakość snu (1-10)", "Czas reakcji (ms)"),
    Feature("Czas od posiłku", "time_since_meal", "temporal", -0.45, 0.40, "Czas od posiłku (h)", "Czas reakcji (ms)"),
    Feature("Dzień tygodnia", "day_of_week", "temporal", 0.15, 0.52, "Dzień tygodnia (1-7)", "Czas reakcji (ms)"),
    Feature("Jet lag (h)", "jet_lag", "temporal", 0.38, 0.48, "Jet lag (h)", "Czas reakcji (ms)"),
    Feature("Deadline za (h)", "deadline_in", "temporal", 0.55, 0.35, "Czas do deadline (h)", "Czas reakcji (ms)"),
    Feature("Budzik vs natural", "alarm_clock", "temporal", 0.42, 0.44, "Budzik (1) vs natural (0)", "Czas reakcji (ms)"),
    Feature("Pora treningu", "last_exercise_time", "temporal", -0.32, 0.46, "Pora ostatniego treningu (h temu)", "Czas reakcji (ms)"),
    Feature("Miesiąc roku", "month", "temporal", 0.06, 0.54, "Miesiąc (1-12)", "Czas reakcji (ms)"),
    # --- demographic (10) ---
    Feature("Wiek", "age", "demographic", 0.55, 0.40, "Wiek (lata)", "Czas reakcji (ms)"),
    Feature("Lata edukacji", "years_education", "demographic", -0.40, 0.42, "Lata edukacji", "Czas reakcji (ms)"),
    Feature("Leworęczność", "handedness", "demographic", 0.10, 0.54, "Leworęczność (0/1)", "Czas reakcji (ms)"),
    Feature("Liczba języków", "num_languages", "demographic", -0.28, 0.50, "Liczba znanych języków", "Czas reakcji (ms)"),
    Feature("Muzyk", "musician", "demographic", -0.50, 0.36, "Muzyk (0/1)", "Czas reakcji (ms)"),
    Feature("Sportowiec", "athlete", "demographic", -0.38, 0.40, "Sportowiec (0/1)", "Czas reakcji (ms)"),
    Feature("Gracz (videogames)", "gamer", "demographic", -0.55, 0.34, "Gracz (0/1)", "Czas reakcji (ms)"),
    Feature("Płeć (biol.)", "sex", "demographic", -0.12, 0.52, "Płeć (0=K, 1=M)", "Czas reakcji (ms)"),
    Feature("Ostrość wzroku", "visual_acuity", "demographic", -0.30, 0.46, "Ostrość wzroku (logMAR)", "Czas reakcji (ms)"),
    Feature("Wzrost (cm)", "height_cm", "demographic", 0.03, 0.55, "Wzrost (cm)", "Czas reakcji (ms)"),
    # --- physiological (10) ---
    Feature("Kofeina (mg)", "caffeine_mg", "physiological", -0.60, 0.30, "Kofeina (mg, dzisiaj)", "Czas reakcji (ms)"),
    Feature("Poziom stresu", "stress_level", "physiological", 0.65, 0.30, "Poziom stresu (1-10)", "Czas reakcji (ms)"),
    Feature("Tętno spocz.", "resting_hr", "physiological", 0.45, 0.40, "Tętno spoczynkowe (bpm)", "Czas reakcji (ms)"),
    Feature("Alkohol wczoraj", "alcohol_yesterday", "physiological", 0.50, 0.36, "Alkohol wczoraj (j.alc.)", "Czas reakcji (ms)"),
    Feature("Ból głowy", "headache", "physiological", 0.55, 0.35, "Ból głowy (0-10)", "Czas reakcji (ms)"),
    Feature("Nawodnienie", "hydration", "physiological", -0.40, 0.40, "Nawodnienie (ml/dzień)", "Czas reakcji (ms)"),
    Feature("Glikemia", "blood_glucose", "physiological", -0.35, 0.44, "Poziom glukozy (mg/dL)", "Czas reakcji (ms)"),
    Feature("Temperatura ciała", "body_temp", "physiological", 0.32, 0.48, "Temperatura ciała (C)", "Czas reakcji (ms)"),
    Feature("Leki psychoaktywne", "psychoactive_meds", "physiological", 0.42, 0.42, "Leki (0/1)", "Czas reakcji (ms)"),
    Feature("Faza cyklu", "cycle_phase", "physiological", 0.22, 0.50, "Faza cyklu (1-4)", "Czas reakcji (ms)"),
    # --- environmental (10) ---
    Feature("Poziom hałasu", "noise_level", "environmental", 0.70, 0.28, "Poziom hałasu (dB)", "Czas reakcji (ms)"),
    Feature("Dystraktory", "distractors", "environmental", 0.60, 0.32, "Liczba dystraktorów", "Czas reakcji (ms)"),
    Feature("CO2 (ppm)", "co2_ppm", "environmental", 0.45, 0.40, "Stężenie CO2 (ppm)", "Czas reakcji (ms)"),
    Feature("Wielozadaniowość", "multitasking", "environmental", 0.50, 0.36, "Liczba otwartych aplikacji", "Czas reakcji (ms)"),
    Feature("Jasność ekranu", "screen_brightness", "environmental", -0.30, 0.46, "Jasność ekranu (%)", "Czas reakcji (ms)"),
    Feature("Temperatura pokoju", "room_temp", "environmental", 0.22, 0.50, "Temperatura pokoju (C)", "Czas reakcji (ms)"),
    Feature("Oświetlenie (lux)", "illuminance", "environmental", -0.26, 0.50, "Oświetlenie (lux)", "Czas reakcji (ms)"),
    Feature("Muzyka w tle (dB)", "background_music", "environmental", 0.35, 0.44, "Głośność muzyki (dB)", "Czas reakcji (ms)"),
    Feature("Ergonomia", "ergonomics", "environmental", -0.40, 0.40, "Ergonomia stanowiska (1-5)", "Czas reakcji (ms)"),
    Feature("Monitor Hz", "monitor_hz", "environmental", -0.16, 0.52, "Częst. odświeżania (Hz)", "Czas reakcji (ms)"),
    # --- task_history (10) ---
    Feature("Poprzedni RT", "previous_rt", "task_history", 0.80, 0.20, "Poprzedni czas reakcji (ms)", "Czas reakcji (ms)"),
    Feature("Liczba błędów", "error_count", "task_history", 0.65, 0.30, "Liczba błędów w sesji", "Czas reakcji (ms)"),
    Feature("Blok treningowy", "training_block", "task_history", -0.70, 0.25, "Blok treningowy (nr)", "Czas reakcji (ms)"),
    Feature("Numer sesji", "session_number", "task_history", -0.55, 0.35, "Numer sesji (od startu)", "Czas reakcji (ms)"),
    Feature("Nr próby w bloku", "trial_number", "task_history", -0.50, 0.36, "Nr próby w bloku", "Czas reakcji (ms)"),
    Feature("Trafność poprzednia", "previous_accuracy", "task_history", -0.60, 0.30, "Trafność w poprz. bloku (%)", "Czas reakcji (ms)"),
    Feature("Całkowity trening (h)", "total_training_h", "task_history", -0.65, 0.30, "Całkowity czas treningu (h)", "Czas reakcji (ms)"),
    Feature("Motywacja", "motivation", "task_history", -0.55, 0.34, "Motywacja (1-10)", "Czas reakcji (ms)"),
    Feature("Czas sesji (min)", "session_duration", "task_history", 0.45, 0.40, "Czas trwania sesji (min)", "Czas reakcji (ms)"),
    Feature("Przerwa od sesji (h)", "time_since_session", "task_history", 0.35, 0.44, "Przerwa od sesji (h)", "Czas reakcji (ms)"),
    # --- noise (10) ---
    Feature("Ulubiony kolor", "favourite_colour", "noise", 0.02, 0.55, "Ulubiony kolor (kod)", "Czas reakcji (ms)"),
    Feature("Rozmiar buta", "shoe_size", "noise", -0.01, 0.55, "Rozmiar buta (EU)", "Czas reakcji (ms)"),
    Feature("Liczba kotów", "cat_count", "noise", 0.03, 0.55, "Liczba kotów w domu", "Czas reakcji (ms)"),
    Feature("Znak zodiaku", "zodiac_sign", "noise", -0.02, 0.55, "Znak zodiaku (1-12)", "Czas reakcji (ms)"),
    Feature("Długość imienia", "name_length", "noise", 0.01, 0.55, "Długość imienia (znaki)", "Czas reakcji (ms)"),
    Feature("Gatunek filmów", "film_genre", "noise", 0.04, 0.55, "Ulubiony gatunek (kod)", "Czas reakcji (ms)"),
    Feature("Kolor włosów", "hair_colour", "noise", -0.03, 0.55, "Kolor włosów (kod)", "Czas reakcji (ms)"),
    Feature("Numer domu", "house_number", "noise", 0.02, 0.55, "Numer domu", "Czas reakcji (ms)"),
    Feature("Gatunek muzyki", "music_genre", "noise", -0.01, 0.55, "Ulubiony gatunek muzyki (kod)", "Czas reakcji (ms)"),
    Feature("Szczotkowanie zębów", "teeth_brushing", "noise", 0.03, 0.55, "Częst. szczotkowania (x/dzień)", "Czas reakcji (ms)"),
]


def draw_features(
    difficulty: DifficultyConfig,
    session_seed: int,
    round_idx: int,
) -> list[Feature]:
    """Return `difficulty.card_count` features sampled from the bank.

    Guarantees at least 1 noise feature and at least 1 signal feature.
    """
    rng = random.Random(session_seed * 100 + round_idx)

    signals = [
        f for f in FEATURE_BANK
        if abs(f.correlation) >= difficulty.min_signal_correlation
    ]
    noises = [
        f for f in FEATURE_BANK
        if abs(f.correlation) <= difficulty.max_noise_correlation
    ]

    n = difficulty.card_count
    # Ensure at least 1 noise and 1 signal
    noise_pick = rng.sample(noises, min(1, len(noises)))
    signal_pick = rng.sample(signals, min(n - 1, len(signals)))
    pool = noise_pick + signal_pick
    if len(pool) < n:
        # Fallback: fill from full bank avoiding duplicates
        extra = [f for f in FEATURE_BANK if f not in pool]
        pool += rng.sample(extra, n - len(pool))
    picked = rng.sample(pool, min(n, len(pool)))
    rng.shuffle(picked)
    return picked
