from cognitive_data_arcade.engine.i18n import EN, PL

_ELD_ATTRS = [
    "eld_hint_key",
    "eld_report_title",
    "eld_score_fmt",
    "eld_play_again",
    "eld_consequence_fmt",
    "eld_confirm_hint",
]


def test_en_has_all_eld_strings():
    for attr in _ELD_ATTRS:
        assert hasattr(EN, attr), f"EN missing {attr}"
        assert getattr(EN, attr), f"EN.{attr} is empty"


def test_pl_has_all_eld_strings():
    for attr in _ELD_ATTRS:
        assert hasattr(PL, attr), f"PL missing {attr}"
        assert getattr(PL, attr), f"PL.{attr} is empty"


def test_eld_strings_differ_between_languages():
    for attr in _ELD_ATTRS:
        en_val = getattr(EN, attr)
        pl_val = getattr(PL, attr)
        assert en_val != pl_val, f"EN and PL have the same value for {attr}"
