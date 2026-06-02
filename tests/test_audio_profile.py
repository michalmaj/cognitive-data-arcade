from cognitive_data_arcade.profile.manager import Profile, ProfileManager


def test_profile_audio_defaults():
    p = Profile()
    assert p.music_enabled is True
    assert p.sfx_enabled is True
    assert p.music_volume == 0.7
    assert p.sfx_volume == 0.8


def test_profile_audio_round_trip(tmp_path):
    pm = ProfileManager(tmp_path / "profile.json")
    profile = pm.load()
    profile.music_volume = 0.42
    profile.sfx_enabled = False
    pm.save(profile)
    loaded = pm.load()
    assert loaded.music_volume == 0.42
    assert loaded.sfx_enabled is False
