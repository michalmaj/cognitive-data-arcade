import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import date, timedelta
from pathlib import Path

_LEVELS = [
    (5000, "⚡ Mind Hacker"),
    (3000, "🧠 Cognitive Scientist"),
    (1500, "📊 Data Analyst"),
    (500, "🔍 Data Explorer"),
    (0, "🌱 Data Seedling"),
]


def level_title(total_points: int) -> str:
    for threshold, title in _LEVELS:
        if total_points >= threshold:
            return title


@dataclass
class Profile:
    alias: str = "anonymous"
    device_uuid: str = ""
    arcade_points: int = 0
    science_points: int = 0
    badges: list[str] = field(default_factory=list)
    completed_lessons: list[int] = field(default_factory=list)
    language: str = "pl"
    music_enabled: bool = True
    sfx_enabled: bool = True
    music_volume: float = 0.7
    sfx_volume: float = 0.8
    fullscreen: bool = False
    seen_intro: bool = False
    current_module_idx: int | None = None
    seen_act_intros: list[int] = field(default_factory=list)
    quiz_results: dict[str, bool] = field(default_factory=dict)
    streak_days: int = 0
    last_active_date: str = ""  # ISO date "YYYY-MM-DD", empty = never


class ProfileManager:
    def __init__(self, path: Path) -> None:
        self._path = path

    def load(self) -> Profile:
        if not self._path.exists():
            profile = Profile(device_uuid=str(uuid.uuid4()))
            self.save(profile)
            return profile
        data = json.loads(self._path.read_text(encoding="utf-8"))
        known = {f for f in Profile.__dataclass_fields__}
        filtered = {k: v for k, v in data.items() if k in known}
        return Profile(**filtered)

    def save(self, profile: Profile) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(json.dumps(asdict(profile), indent=2), encoding="utf-8")

    def add_ap(self, points: int) -> Profile:
        profile = self.load()
        profile.arcade_points += points
        self.save(profile)
        return profile

    def add_sp(self, points: int) -> Profile:
        profile = self.load()
        profile.science_points += points
        self.save(profile)
        return profile

    def award_badge(self, badge_id: str) -> Profile:
        profile = self.load()
        if badge_id not in profile.badges:
            profile.badges.append(badge_id)
            self.save(profile)
        return profile

    def complete_lesson(self, lesson_number: int) -> Profile:
        profile = self.load()
        if lesson_number not in profile.completed_lessons:
            profile.completed_lessons.append(lesson_number)
            self.save(profile)
        return profile

    def set_language(self, lang: str) -> Profile:
        profile = self.load()
        profile.language = lang
        self.save(profile)
        return profile

    def set_fullscreen(self, enabled: bool) -> Profile:
        profile = self.load()
        profile.fullscreen = enabled
        self.save(profile)
        return profile

    def set_seen_intro(self, seen: bool) -> Profile:
        profile = self.load()
        profile.seen_intro = seen
        self.save(profile)
        return profile

    def set_current_module(self, idx: int) -> Profile:
        profile = self.load()
        profile.current_module_idx = idx
        self.save(profile)
        return profile

    def clear_current_module(self) -> Profile:
        profile = self.load()
        profile.current_module_idx = None
        self.save(profile)
        return profile

    def reset_progress(self) -> Profile:
        profile = self.load()
        profile.arcade_points = 0
        profile.science_points = 0
        profile.badges = []
        profile.completed_lessons = []
        self.save(profile)
        return profile

    def reset_module_progress(self) -> Profile:
        profile = self.load()
        profile.current_module_idx = None
        profile.seen_intro = False
        self.save(profile)
        return profile

    def set_seen_act_intro(self, module_idx: int) -> Profile:
        profile = self.load()
        if module_idx not in profile.seen_act_intros:
            profile.seen_act_intros.append(module_idx)
            self.save(profile)
        return profile

    def record_quiz_result(self, lesson_num: int, correct: bool) -> Profile:
        profile = self.load()
        key = f"L{lesson_num}"
        if key not in profile.quiz_results:
            profile.quiz_results[key] = correct
            self.save(profile)
        return profile

    def touch_streak(self, today: date) -> Profile:
        profile = self.load()
        today_str = today.isoformat()
        yesterday_str = (today - timedelta(days=1)).isoformat()
        if profile.last_active_date == today_str:
            return profile
        if profile.last_active_date == yesterday_str:
            profile.streak_days += 1
        else:
            profile.streak_days = 1
        profile.last_active_date = today_str
        for threshold, badge_id in [
            (3, "streak_3"),
            (7, "streak_7"),
            (30, "streak_30"),
        ]:
            if profile.streak_days >= threshold and badge_id not in profile.badges:
                profile.badges.append(badge_id)
        self.save(profile)
        return profile

    def reset_all(self) -> Profile:
        profile = self.load()
        fresh = Profile(
            device_uuid=profile.device_uuid,
            alias=profile.alias,
            language=profile.language,
            music_enabled=profile.music_enabled,
            sfx_enabled=profile.sfx_enabled,
            music_volume=profile.music_volume,
            sfx_volume=profile.sfx_volume,
            fullscreen=profile.fullscreen,
        )
        self.save(fresh)
        return fresh

    def export_progress(self, path: Path) -> None:
        import datetime
        from importlib.metadata import PackageNotFoundError, version

        _MODULE_LESSONS = [
            [1, 2, 3, 4, 6],
            [7, 8, 9, 10, 11, 12],
            [13, 14, 15, 16],
            [17, 18, 19, 20],
            [21, 22, 23, 24, 25, 26],
            [27, 28, 29, 30, 31, 32],
        ]

        profile = self.load()
        completed_set = set(profile.completed_lessons)

        try:
            app_version = version("cognitive-data-arcade")
        except PackageNotFoundError:
            app_version = "unknown"

        quiz = profile.quiz_results
        if quiz:
            correct = sum(1 for v in quiz.values() if v)
            quiz_accuracy_pct: int | None = round(100 * correct / len(quiz))
        else:
            quiz_accuracy_pct = None

        module_completion = {
            str(i + 1): {
                "done": sum(1 for n in lessons if n in completed_set),
                "total": len(lessons),
            }
            for i, lessons in enumerate(_MODULE_LESSONS)
        }

        data = {
            "alias": profile.alias,
            "exported_at": datetime.datetime.now().isoformat(),
            "app_version": app_version,
            "completed_lessons": sorted(profile.completed_lessons),
            "completed_count": len(profile.completed_lessons),
            "arcade_points": profile.arcade_points,
            "sp_points": profile.science_points,
            "streak_days": profile.streak_days,
            "last_active_date": profile.last_active_date,
            "quiz_results": profile.quiz_results,
            "quiz_accuracy_pct": quiz_accuracy_pct,
            "badges": profile.badges,
            "module_completion": module_completion,
        }

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
