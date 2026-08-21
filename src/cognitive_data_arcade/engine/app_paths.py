from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppPaths:
    """Immutable set of application directories.

    Separates read-only assets from writable user data so that the app can
    run correctly regardless of the process working directory.
    """

    profile_dir: Path
    generated_data_dir: Path
    export_dir: Path
    asset_dir: Path

    def __post_init__(self) -> None:
        # Enforce absolute paths at construction time so callers catch bugs early.
        for field_name in ("profile_dir", "generated_data_dir", "export_dir", "asset_dir"):
            p: Path = getattr(self, field_name)
            if not p.is_absolute():
                raise ValueError(f"AppPaths.{field_name} must be absolute, got: {p!r}")


def default_app_paths() -> AppPaths:
    """Return production AppPaths rooted at ~/.cognitive_data_arcade."""
    from cognitive_data_arcade.engine.assets import assets_dir

    base = Path.home() / ".cognitive_data_arcade"
    return AppPaths(
        profile_dir=base,
        generated_data_dir=base / "data" / "generated",
        export_dir=base / "exports",
        asset_dir=assets_dir(),
    )
