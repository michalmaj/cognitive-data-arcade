from pathlib import Path
from cognitive_data_arcade.engine.assets import assets_dir


def test_assets_dir_returns_path():
    result = assets_dir()
    assert isinstance(result, Path)


def test_assets_dir_ends_with_assets():
    result = assets_dir()
    assert result.name == "assets"


def test_assets_dir_resolves_to_project_root_in_dev():
    result = assets_dir()
    # In dev mode the parent directory is the project root containing pyproject.toml
    assert (result.parent / "pyproject.toml").exists()
