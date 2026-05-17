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


class ProfileManager:
    def __init__(self, path: Path) -> None:
        self._path = path

    def load(self) -> Profile:
        if not self._path.exists():
            profile = Profile(device_uuid=str(uuid.uuid4()))
            self.save(profile)
            return profile
        data = json.loads(self._path.read_text(encoding="utf-8"))
        return Profile(**data)

    def save(self, profile: Profile) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(
            json.dumps(asdict(profile), indent=2), encoding="utf-8"
        )

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
