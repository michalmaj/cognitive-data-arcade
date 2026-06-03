from __future__ import annotations

import types
from collections.abc import Mapping
from dataclasses import dataclass

_THRESHOLDS = [0, 500, 1500, 3000, 5000]

_BADGE_NAMES_EN: dict[str, str] = {
    "quick_reflex": "Quick Reflex",
    "sharpshooter": "Sharpshooter",
    "high_accuracy": "High Accuracy",
    "clean_data": "Clean Data",
    "first_game": "First Game",
}

_BADGE_NAMES_PL: dict[str, str] = {
    "quick_reflex": "Błyskawiczny",
    "sharpshooter": "Snajper",
    "high_accuracy": "Wysoka Celność",
    "clean_data": "Czyste Dane",
    "first_game": "Pierwsza Gra",
}


@dataclass(frozen=True)
class Strings:
    language: str
    # Menu
    menu_title: str
    menu_subtitle: str
    # Session summary
    session_complete: str
    session_subtitle: str
    label_arcade_points: str
    label_science_points: str
    label_accuracy: str
    label_avg_rt: str
    label_new_badges: str
    label_no_new_badges: str
    hint_space: str
    hint_p: str
    hint_esc: str
    label_level_up: str
    # Profile screen
    profile_title: str
    label_lessons: str
    label_badges_earned: str
    label_back: str
    label_edit_alias: str
    # Level titles (include emoji)
    level_seedling: str
    level_explorer: str
    level_analyst: str
    level_scientist: str
    level_hacker: str
    # Badge names keyed by badge_id
    badge_names: Mapping[str, str]
    # Reaction Time Lab
    rt_instructions: str
    rt_too_early: str
    rt_between_blocks: str
    rt_get_ready: str
    rt_hint_space: str
    rt_too_slow: str
    # Analysis
    analysis_title: str
    analysis_hint_esc: str
    analysis_hint_s: str
    label_median_rt: str
    picker_title: str
    picker_no_sessions: str
    # Stroop Challenge
    stroop_title: str
    stroop_instructions: str
    stroop_pick_preset: str
    stroop_difficulty_easy: str
    stroop_difficulty_medium: str
    stroop_difficulty_hard: str
    stroop_hint_ink: str
    stroop_too_slow: str
    stroop_analysis_title: str
    label_facilitation: str
    label_interference: str
    label_stroop_effect: str
    stroop_picker_title: str
    stroop_picker_no_sessions: str
    # Pause menu
    pause_title: str
    pause_restart: str
    pause_how_to_play: str
    pause_keyref: str
    pause_quit: str
    pause_hint_resume: str
    pause_hint_esc_back: str
    # How to play screen
    howtoplay_hint_skip: str
    # N-Back Level Scene
    nback_level_title: str
    nback_level_1: str
    nback_level_2: str
    nback_level_3: str
    nback_level_adaptive: str
    nback_level_hint: str
    # Options scene
    pause_options: str
    options_title: str
    options_music: str
    options_sfx: str
    options_hint: str
    # Lesson reader
    lesson_theory: str
    lesson_notes: str
    lesson_tasks: str
    lesson_reader_hint: str
    # Popups
    label_play_game: str
    label_theory_lesson: str
    label_esc_close: str


EN = Strings(
    language="en",
    menu_title="Cognitive Data Arcade",
    menu_subtitle="UP/DN  navigate   O  options   T  theory   P  profile   L  lang: EN   ESC  quit",
    session_complete="Session Complete",
    session_subtitle="here's what your brain did today",
    label_arcade_points="Arcade Points",
    label_science_points="Science Points",
    label_accuracy="Accuracy",
    label_avg_rt="Avg RT",
    label_new_badges="New badges",
    label_no_new_badges="no new badges this session",
    hint_space="SPACE  continue",
    hint_p="P  profile",
    hint_esc="ESC  menu",
    label_level_up="Level up!",
    profile_title="Profile",
    label_lessons="Lessons (30)",
    label_badges_earned="Badges",
    label_back="ESC  back",
    label_edit_alias="E  edit alias",
    level_seedling="🌱 Data Seedling",
    level_explorer="🔍 Data Explorer",
    level_analyst="📊 Data Analyst",
    level_scientist="🧠 Cognitive Scientist",
    level_hacker="⚡ Mind Hacker",
    badge_names=types.MappingProxyType(_BADGE_NAMES_EN),
    rt_instructions=(
        "Watch the centre circle.\n"
        "Press SPACE as fast as you can when it lights up.\n"
        "Ignore the other circles.\n"
        "\n"
        "Press SPACE to start."
    ),
    rt_too_early="Too early!",
    rt_between_blocks="Break — press SPACE to continue",
    rt_get_ready="Get ready…",
    rt_hint_space="SPACE — react",
    rt_too_slow="Too slow",
    analysis_title="Reaction Time Analysis",
    analysis_hint_esc="ESC  back",
    analysis_hint_s="S  analyse",
    label_median_rt="Median RT",
    picker_title="Select Session",
    picker_no_sessions="No sessions yet — play RT Lab first",
    stroop_title="Stroop Challenge",
    stroop_instructions=(
        "A word will appear in coloured ink.\n"
        "Press the key matching the INK COLOUR — ignore what the word says.\n"
        "\n"
        "Active colour keys are shown at the bottom of the screen.\n"
        "\n"
        "Press SPACE to start."
    ),
    stroop_pick_preset="Choose difficulty",
    stroop_difficulty_easy="2 colors",
    stroop_difficulty_medium="3 colors",
    stroop_difficulty_hard="4 colors",
    stroop_hint_ink="Name the INK colour — ignore the word",
    stroop_too_slow="Too slow",
    stroop_analysis_title="Stroop Effect Analysis",
    label_facilitation="Facilitation",
    label_interference="Interference",
    label_stroop_effect="Stroop Effect",
    stroop_picker_title="Select Stroop Session",
    stroop_picker_no_sessions="No sessions yet — play Stroop first",
    pause_title="PAUSED",
    pause_restart="Restart",
    pause_how_to_play="How to play",
    pause_keyref="Quick ref",
    pause_quit="Quit",
    pause_hint_resume="ESC — resume",
    pause_hint_esc_back="ESC — back",
    howtoplay_hint_skip="SPACE — skip",
    nback_level_title="N-Back Memory Grid",
    nback_level_1="1-Back",
    nback_level_2="2-Back",
    nback_level_3="3-Back",
    nback_level_adaptive="Adaptive",
    nback_level_hint="ESC — back",
    pause_options="Options",
    options_title="Options",
    options_music="Music",
    options_sfx="SFX",
    options_hint="LEFT / RIGHT  volume    ENTER  toggle    ESC  back",
    lesson_theory="Theory",
    lesson_notes="Notes",
    lesson_tasks="Tasks",
    lesson_reader_hint="SPACE / RIGHT  next    LEFT  back    ESC  menu",
    label_play_game="Play",
    label_theory_lesson="Theory",
    label_esc_close="ESC — close",
)

PL = Strings(
    language="pl",
    menu_title="Cognitive Data Arcade",
    menu_subtitle="UP/DN  nawigacja   O  opcje   T  teoria   P  profil   L  jezyk: PL   ESC  wyjscie",
    session_complete="Sesja Zakończona",
    session_subtitle="oto co dziś zrobił Twój mózg",
    label_arcade_points="Punkty Arcade",
    label_science_points="Punkty Nauki",
    label_accuracy="Dokładność",
    label_avg_rt="Śr. czas reakcji",
    label_new_badges="Nowe odznaki",
    label_no_new_badges="brak nowych odznak w tej sesji",
    hint_space="SPACJA  kontynuuj",
    hint_p="P  profil",
    hint_esc="ESC  menu",
    label_level_up="Awans!",
    profile_title="Profil",
    label_lessons="Lekcje (30)",
    label_badges_earned="Odznaki",
    label_back="ESC  wróć",
    label_edit_alias="E  edytuj alias",
    level_seedling="🌱 Siewca Danych",
    level_explorer="🔍 Odkrywca Danych",
    level_analyst="📊 Analityk Danych",
    level_scientist="🧠 Naukowiec Kognitywny",
    level_hacker="⚡ Haker Umysłu",
    badge_names=types.MappingProxyType(_BADGE_NAMES_PL),
    rt_instructions=(
        "Obserwuj środkowe kółko.\n"
        "Naciśnij SPACJĘ jak najszybciej gdy zaświeci.\n"
        "Ignoruj pozostałe kółka.\n"
        "\n"
        "Naciśnij SPACJĘ aby zacząć."
    ),
    rt_too_early="Zbyt wcześnie!",
    rt_between_blocks="Przerwa — naciśnij SPACJĘ aby kontynuować",
    rt_get_ready="Przygotuj się…",
    rt_hint_space="SPACJA — reaguj",
    rt_too_slow="Za wolno",
    analysis_title="Analiza Czasu Reakcji",
    analysis_hint_esc="ESC  wróć",
    analysis_hint_s="S  analiza",
    label_median_rt="Mediana RT",
    picker_title="Wybierz Sesję",
    picker_no_sessions="Brak sesji — najpierw zagraj w RT Lab",
    stroop_title="Wyzwanie Stroopa",
    stroop_instructions=(
        "Słowo pojawi się w kolorowym tuszu.\n"
        "Naciśnij klawisz koloru TUSZU — ignoruj znaczenie słowa.\n"
        "\n"
        "Aktywne klawisze kolorów widoczne są na dole ekranu.\n"
        "\n"
        "Naciśnij SPACJĘ aby zacząć."
    ),
    stroop_pick_preset="Wybierz poziom",
    stroop_difficulty_easy="2 kolory",
    stroop_difficulty_medium="3 kolory",
    stroop_difficulty_hard="4 kolory",
    stroop_hint_ink="Nazwij kolor TUSZU — ignoruj słowo",
    stroop_too_slow="Za wolno",
    stroop_analysis_title="Analiza Efektu Stroopa",
    label_facilitation="Facylitacja",
    label_interference="Interferencja",
    label_stroop_effect="Efekt Stroopa",
    stroop_picker_title="Wybierz Sesję Stroopa",
    stroop_picker_no_sessions="Brak sesji — najpierw zagraj w Stroop",
    pause_title="PAUZA",
    pause_restart="Restart",
    pause_how_to_play="Jak grać",
    pause_keyref="Ściągawka",
    pause_quit="Wyjdź",
    pause_hint_resume="ESC — wznów",
    pause_hint_esc_back="ESC — wróć",
    howtoplay_hint_skip="SPACJA — pomiń",
    nback_level_title="N-Back Memory Grid",
    nback_level_1="1-Back",
    nback_level_2="2-Back",
    nback_level_3="3-Back",
    nback_level_adaptive="Adaptacyjny",
    nback_level_hint="ESC — wróć",
    pause_options="Opcje",
    options_title="Opcje",
    options_music="Muzyka",
    options_sfx="Dzwieki",
    options_hint="LEWO / PRAWO  glosnosc    ENTER  przelacz    ESC  wróc",
    lesson_theory="Teoria",
    lesson_notes="Notatki",
    lesson_tasks="Zadania",
    lesson_reader_hint="SPACJA / PRAWO  dalej    LEWO  wstecz    ESC  menu",
    label_play_game="Graj",
    label_theory_lesson="Teoria",
    label_esc_close="ESC — zamknij",
)


def get_strings(lang: str) -> Strings:
    """Return the Strings instance for *lang*; falls back to EN for unknown locales."""
    return PL if lang == "pl" else EN


_LEVEL_ATTRS = [
    "level_seedling",
    "level_explorer",
    "level_analyst",
    "level_scientist",
    "level_hacker",
]


def level_title(total_points: int, strings: Strings) -> str:
    for i in range(len(_THRESHOLDS) - 1, -1, -1):
        if total_points >= _THRESHOLDS[i]:
            return getattr(strings, _LEVEL_ATTRS[i])
    return strings.level_seedling


def level_progress(total_points: int) -> tuple[int, int]:
    """Return (points_into_current_level, level_range) for a progress bar.

    At max level (>= 5000) returns (1, 1) so callers render a full bar.
    """
    for i in range(len(_THRESHOLDS) - 1):
        if total_points < _THRESHOLDS[i + 1]:
            low = _THRESHOLDS[i]
            high = _THRESHOLDS[i + 1]
            return (total_points - low, high - low)
    return (1, 1)
