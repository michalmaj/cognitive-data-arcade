import json
import uuid
from dataclasses import asdict, dataclass, field
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
