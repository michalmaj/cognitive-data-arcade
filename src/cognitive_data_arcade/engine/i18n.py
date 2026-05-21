from __future__ import annotations

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


@dataclass
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
    badge_names: dict[str, str]


EN = Strings(
    language="en",
    menu_title="Cognitive Data Arcade",
    menu_subtitle="↑↓ navigate   P profile   L language: EN   ESC quit",
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
    badge_names=_BADGE_NAMES_EN,
)

PL = Strings(
    language="pl",
    menu_title="Cognitive Data Arcade",
    menu_subtitle="↑↓ nawigacja   P profil   L język: PL   ESC wyjście",
    session_complete="Sesja Zakończona",
    session_subtitle="oto co dziś zrobiło Twoje mózg",
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
    badge_names=_BADGE_NAMES_PL,
)


def get_strings(lang: str) -> Strings:
    return PL if lang == "pl" else EN


def level_title(total_points: int, strings: Strings) -> str:
    if total_points >= 5000:
        return strings.level_hacker
    if total_points >= 3000:
        return strings.level_scientist
    if total_points >= 1500:
        return strings.level_analyst
    if total_points >= 500:
        return strings.level_explorer
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
