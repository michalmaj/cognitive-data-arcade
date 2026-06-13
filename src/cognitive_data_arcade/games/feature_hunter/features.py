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
    hint_pl: str = ""

    @property
    def is_signal(self) -> bool:
        return abs(self.correlation) >= 0.25


# ---------------------------------------------------------------------------
# Feature bank — 60 entries across 6 categories (10 each)
# Target variable: reaction time in ms (higher = slower)
# ---------------------------------------------------------------------------
FEATURE_BANK: list[Feature] = [
    # --- temporal (10) ---
    Feature("Pora dnia", "time_of_day", "temporal", 0.75, 0.30, "Pora dnia (h)", "Czas reakcji (ms)",
            "Reakcje są wolniejsze wieczorem — rytm dobowy silnie moduluje sprawność poznawczą."),
    Feature("Godziny snu", "sleep_hours", "temporal", 0.65, 0.35, "Godziny snu", "Czas reakcji (ms)",
            "Więcej snu = szybsza reakcja. Nawet 1h niedoboru wyraźnie spowalnia RT."),
    Feature("Jakość snu", "sleep_quality", "temporal", 0.70, 0.30, "Jakość snu (1-10)", "Czas reakcji (ms)",
            "Nie tylko długość, ale jakość snu ma znaczenie — niespokojny sen zwiększa RT."),
    Feature("Czas od posiłku", "time_since_meal", "temporal", -0.45, 0.40, "Czas od posiłku (h)", "Czas reakcji (ms)",
            "Głód spowalnia — im dłużej po posiłku, tym wolniejsze reakcje (spadek glukozy we krwi)."),
    Feature("Dzień tygodnia", "day_of_week", "temporal", 0.15, 0.52, "Dzień tygodnia (1-7)", "Czas reakcji (ms)",
            "Słaba zależność — poniedziałek i piątek nie różnią się znacząco w RT."),
    Feature("Jet lag (h)", "jet_lag", "temporal", 0.38, 0.48, "Jet lag (h)", "Czas reakcji (ms)",
            "Zaburzenie rytmu dobowego spowalnia reakcje proporcjonalnie do przesunięcia stref czasowych."),
    Feature("Deadline za (h)", "deadline_in", "temporal", 0.55, 0.35, "Czas do deadline (h)", "Czas reakcji (ms)",
            "Presja czasowa mobilizuje uwagę — deadline jutro przyspiesza RT bardziej niż deadline za tydzień."),
    Feature("Budzik vs natural", "alarm_clock", "temporal", 0.42, 0.44, "Budzik (1) vs natural (0)", "Czas reakcji (ms)",
            "Przebudzenie z alarmem zostawia resztkowe zmęczenie — naturalne przebudzenie daje lepszy RT."),
    Feature("Pora treningu", "last_exercise_time", "temporal", -0.32, 0.46, "Pora ostatniego treningu (h temu)", "Czas reakcji (ms)",
            "Ćwiczenia fizyczne kilka godzin wcześniej przyśpieszają RT — efekt pobudzenia układu nerwowego."),
    Feature("Miesiąc roku", "month", "temporal", 0.06, 0.54, "Miesiąc (1-12)", "Czas reakcji (ms)",
            "Brak sezonowego efektu — miesiąc roku nie jest użytecznym predyktorem RT."),
    # --- demographic (10) ---
    Feature("Wiek", "age", "demographic", 0.55, 0.40, "Wiek (lata)", "Czas reakcji (ms)",
            "RT rośnie z wiekiem — mózg przetwarza wolniej po 30. roku życia (norma biologiczna)."),
    Feature("Lata edukacji", "years_education", "demographic", -0.40, 0.42, "Lata edukacji", "Czas reakcji (ms)",
            "Więcej lat edukacji = szybszy RT — trening poznawczy ma wymierny wpływ na refleks."),
    Feature("Leworęczność", "handedness", "demographic", 0.10, 0.54, "Leworęczność (0/1)", "Czas reakcji (ms)",
            "Brak istotnego wpływu — ręczność nie jest dobrym predyktorem RT."),
    Feature("Liczba języków", "num_languages", "demographic", -0.28, 0.50, "Liczba znanych języków", "Czas reakcji (ms)",
            "Bilingwizm przyspiesza — przełączanie języków trenuje hamowanie i kontrolę wykonawczą."),
    Feature("Muzyk", "musician", "demographic", -0.50, 0.36, "Muzyk (0/1)", "Czas reakcji (ms)",
            "Muzycy mają krótszy RT — lata treningu rytmu i precyzji ruchu poprawiają refleks."),
    Feature("Sportowiec", "athlete", "demographic", -0.38, 0.40, "Sportowiec (0/1)", "Czas reakcji (ms)",
            "Regularny sport przyspiesza RT — lepsza sprawność układu nerwowo-ruchowego."),
    Feature("Gracz (videogames)", "gamer", "demographic", -0.55, 0.34, "Gracz (0/1)", "Czas reakcji (ms)",
            "Gracze action są szybsi — intensywny trening percepcji i reakcji przekłada się na krótszy RT."),
    Feature("Płeć (biol.)", "sex", "demographic", -0.12, 0.52, "Płeć (0=K, 1=M)", "Czas reakcji (ms)",
            "Brak istotnej różnicy płciowej w RT — płeć biologiczna nie jest dobrym predyktorem."),
    Feature("Ostrość wzroku", "visual_acuity", "demographic", -0.30, 0.46, "Ostrość wzroku (logMAR)", "Czas reakcji (ms)",
            "Lepsza ostrość wzroku = szybsze przetwarzanie bodźców i krótszy RT."),
    Feature("Wzrost (cm)", "height_cm", "demographic", 0.03, 0.55, "Wzrost (cm)", "Czas reakcji (ms)",
            "Wzrost nie ma związku z RT — typowy szum demograficzny."),
    # --- physiological (10) ---
    Feature("Kofeina (mg)", "caffeine_mg", "physiological", -0.60, 0.30, "Kofeina (mg, dzisiaj)", "Czas reakcji (ms)",
            "Kofeina przyspiesza RT — blokuje adenozynę i zwiększa czujność układu nerwowego."),
    Feature("Poziom stresu", "stress_level", "physiological", 0.65, 0.30, "Poziom stresu (1-10)", "Czas reakcji (ms)",
            "Wysoki stres poznawczy spowalnia RT — przeciąża zasoby uwagi i pamięć roboczą."),
    Feature("Tętno spocz.", "resting_hr", "physiological", 0.45, 0.40, "Tętno spoczynkowe (bpm)", "Czas reakcji (ms)",
            "Wyższe tętno spoczynkowe wiąże się z wolniejszym RT — wskaźnik przeciążenia układu autonomicznego."),
    Feature("Alkohol wczoraj", "alcohol_yesterday", "physiological", 0.50, 0.36, "Alkohol wczoraj (j.alc.)", "Czas reakcji (ms)",
            "Kac spowalnia — resztkowy alkohol i niedobór snu po spożyciu wyraźnie zwiększają RT."),
    Feature("Ból głowy", "headache", "physiological", 0.55, 0.35, "Ból głowy (0-10)", "Czas reakcji (ms)",
            "Ból głowy obciąża zasoby poznawcze i wyraźnie spowalnia reakcje."),
    Feature("Nawodnienie", "hydration", "physiological", -0.40, 0.40, "Nawodnienie (ml/dzień)", "Czas reakcji (ms)",
            "Odwodnienie upośledza przewodnictwo nerwowe — odpowiednie nawodnienie przyspiesza RT."),
    Feature("Glikemia", "blood_glucose", "physiological", -0.35, 0.44, "Poziom glukozy (mg/dL)", "Czas reakcji (ms)",
            "Optymalna glikemia przyspiesza mózg — zbyt niska lub zbyt wysoka spowalnia RT."),
    Feature("Temperatura ciała", "body_temp", "physiological", 0.32, 0.48, "Temperatura ciała (C)", "Czas reakcji (ms)",
            "Lekko podwyższona temperatura (infekcja) spowalnia RT — zasoby kierowane są na układ odpornościowy."),
    Feature("Leki psychoaktywne", "psychoactive_meds", "physiological", 0.42, 0.42, "Leki (0/1)", "Czas reakcji (ms)",
            "Leki psychoaktywne mogą przyspieszyć lub spowolnić RT zależnie od rodzaju i dawki."),
    Feature("Faza cyklu", "cycle_phase", "physiological", 0.22, 0.50, "Faza cyklu (1-4)", "Czas reakcji (ms)",
            "Słaby efekt — faza cyklu menstruacyjnego ma minimalny wpływ na RT."),
    # --- environmental (10) ---
    Feature("Poziom hałasu", "noise_level", "environmental", 0.70, 0.28, "Poziom hałasu (dB)", "Czas reakcji (ms)",
            "Hałas powyżej 65 dB wyraźnie spowalnia RT — odwraca uwagę i obciąża pamięć roboczą."),
    Feature("Dystraktory", "distractors", "environmental", 0.60, 0.32, "Liczba dystraktorów", "Czas reakcji (ms)",
            "Więcej dystraktorów = dłuższy RT — uwaga musi filtrować więcej konkurujących bodźców."),
    Feature("CO2 (ppm)", "co2_ppm", "environmental", 0.45, 0.40, "Stężenie CO2 (ppm)", "Czas reakcji (ms)",
            "Wysokie CO2 (>1000 ppm) upośledza poznanie — słaba wentylacja spowalnia RT."),
    Feature("Wielozadaniowość", "multitasking", "environmental", 0.50, 0.36, "Liczba otwartych aplikacji", "Czas reakcji (ms)",
            "Otwarte aplikacje rozpraszają — przełączanie kontekstu kosztuje zasoby poznawcze i czas."),
    Feature("Jasność ekranu", "screen_brightness", "environmental", -0.30, 0.46, "Jasność ekranu (%)", "Czas reakcji (ms)",
            "Zbyt ciemny ekran wymaga wysiłku wzrokowego — optymalna jasność przyspiesza przetwarzanie bodźca."),
    Feature("Temperatura pokoju", "room_temp", "environmental", 0.22, 0.50, "Temperatura pokoju (C)", "Czas reakcji (ms)",
            "Słaby efekt — zbyt gorąco lub zimno nieznacznie spowalnia RT przez dyskomfort."),
    Feature("Oświetlenie (lux)", "illuminance", "environmental", -0.26, 0.50, "Oświetlenie (lux)", "Czas reakcji (ms)",
            "Słabe oświetlenie spowalnia przetwarzanie bodźców wzrokowych i wydłuża RT."),
    Feature("Muzyka w tle (dB)", "background_music", "environmental", 0.35, 0.44, "Głośność muzyki (dB)", "Czas reakcji (ms)",
            "Głośna muzyka (>70 dB) spowalnia — cicha muzyka instrumentalna może lekko pomagać skupieniu."),
    Feature("Ergonomia", "ergonomics", "environmental", -0.40, 0.40, "Ergonomia stanowiska (1-5)", "Czas reakcji (ms)",
            "Dobre stanowisko redukuje zmęczenie mięśni i utrzymuje RT na niskim poziomie przez dłuższy czas."),
    Feature("Monitor Hz", "monitor_hz", "environmental", -0.16, 0.52, "Częst. odświeżania (Hz)", "Czas reakcji (ms)",
            "Częstotliwość odświeżania słabo wpływa na RT — efekt jest poniżej progu percepcji."),
    # --- task_history (10) ---
    Feature("Poprzedni RT", "previous_rt", "task_history", 0.80, 0.20, "Poprzedni czas reakcji (ms)", "Czas reakcji (ms)",
            "Najsilniejszy predyktor — wolna reakcja w jednej próbie przepowiada wolną w kolejnej."),
    Feature("Liczba błędów", "error_count", "task_history", 0.65, 0.30, "Liczba błędów w sesji", "Czas reakcji (ms)",
            "Więcej błędów = wolniejszy RT — kompromis szybkość–dokładność działa w obie strony."),
    Feature("Blok treningowy", "training_block", "task_history", -0.70, 0.25, "Blok treningowy (nr)", "Czas reakcji (ms)",
            "RT maleje z kolejnymi blokami — efekt uczenia się i rozgrzewki układu nerwowego."),
    Feature("Numer sesji", "session_number", "task_history", -0.55, 0.35, "Numer sesji (od startu)", "Czas reakcji (ms)",
            "RT skraca się z doświadczeniem — regularne sesje treningowe przynoszą stały postęp."),
    Feature("Nr próby w bloku", "trial_number", "task_history", -0.50, 0.36, "Nr próby w bloku", "Czas reakcji (ms)",
            "Pierwsze próby są wolniejsze — RT stabilizuje się po kilku próbach rozgrzewkowych."),
    Feature("Trafność poprzednia", "previous_accuracy", "task_history", -0.60, 0.30, "Trafność w poprz. bloku (%)", "Czas reakcji (ms)",
            "Wyższa trafność w poprzednim bloku = szybszy RT teraz — dobra forma poznawcza się utrzymuje."),
    Feature("Całkowity trening (h)", "total_training_h", "task_history", -0.65, 0.30, "Całkowity czas treningu (h)", "Czas reakcji (ms)",
            "Łączny czas treningu silnie przewiduje RT — doświadczenie jest kluczowym czynnikiem."),
    Feature("Motywacja", "motivation", "task_history", -0.55, 0.34, "Motywacja (1-10)", "Czas reakcji (ms)",
            "Wysoka motywacja przyspiesza RT — zaangażowanie poznawcze ma wymierny, mierzalny efekt."),
    Feature("Czas sesji (min)", "session_duration", "task_history", 0.45, 0.40, "Czas trwania sesji (min)", "Czas reakcji (ms)",
            "Długie sesje spowalniają — zmęczenie zadaniem narasta po ok. 30 min ciągłej pracy."),
    Feature("Przerwa od sesji (h)", "time_since_session", "task_history", 0.35, 0.44, "Przerwa od sesji (h)", "Czas reakcji (ms)",
            "Krótka przerwa (2–4h) pozwala na regenerację i przyspiesza RT w kolejnej sesji."),
    # --- noise (10) ---
    Feature("Ulubiony kolor", "favourite_colour", "noise", 0.02, 0.55, "Ulubiony kolor (kod)", "Czas reakcji (ms)",
            "Kolor ulubiony to czysty szum — zero związku z szybkością reakcji."),
    Feature("Rozmiar buta", "shoe_size", "noise", -0.01, 0.55, "Rozmiar buta (EU)", "Czas reakcji (ms)",
            "Rozmiar buta nie ma żadnego wpływu na RT — klasyczny przykład cechy-szumu."),
    Feature("Liczba kotów", "cat_count", "noise", 0.03, 0.55, "Liczba kotów w domu", "Czas reakcji (ms)",
            "Liczba kotów w domu nie koreluje z RT — to oczywisty szum."),
    Feature("Znak zodiaku", "zodiac_sign", "noise", -0.02, 0.55, "Znak zodiaku (1-12)", "Czas reakcji (ms)",
            "Astrologia nie przewiduje RT — brak jakiegokolwiek mechanizmu biologicznego."),
    Feature("Długość imienia", "name_length", "noise", 0.01, 0.55, "Długość imienia (znaki)", "Czas reakcji (ms)",
            "Długość imienia to szum — żaden mechanizm nie łączy jej z szybkością reakcji."),
    Feature("Gatunek filmów", "film_genre", "noise", 0.04, 0.55, "Ulubiony gatunek (kod)", "Czas reakcji (ms)",
            "Preferowany gatunek filmowy nie wpływa na RT — szum preferencji kulturowych."),
    Feature("Kolor włosów", "hair_colour", "noise", -0.03, 0.55, "Kolor włosów (kod)", "Czas reakcji (ms)",
            "Kolor włosów nie ma związku z RT — szum genetyczno-kosmetyczny."),
    Feature("Numer domu", "house_number", "noise", 0.02, 0.55, "Numer domu", "Czas reakcji (ms)",
            "Numer domu to szum — przypadkowa liczba bez żadnego związku z poznaniem."),
    Feature("Gatunek muzyki", "music_genre", "noise", -0.01, 0.55, "Ulubiony gatunek muzyki (kod)", "Czas reakcji (ms)",
            "Preferowany gatunek muzyki nie przewiduje RT — brak mechanizmu przyczynowego."),
    Feature("Szczotkowanie zębów", "teeth_brushing", "noise", 0.03, 0.55, "Częst. szczotkowania (x/dzień)", "Czas reakcji (ms)",
            "Częstość szczotkowania zębów to szum — brak związku z szybkością reakcji."),
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
    signal_pick = rng.sample(signals, min(max(1, n - 1), len(signals)))
    pool = noise_pick + signal_pick
    if len(pool) < n:
        # Fallback: fill from full bank avoiding duplicates
        extra = [f for f in FEATURE_BANK if f not in pool]
        pool += rng.sample(extra, n - len(pool))
    picked = rng.sample(pool, min(n, len(pool)))
    rng.shuffle(picked)
    return picked
