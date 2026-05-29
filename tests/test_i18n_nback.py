from cognitive_data_arcade.engine.i18n import EN, PL

def test_nback_strings_en():
    assert EN.nback_level_title == "N-Back Memory Grid"
    assert EN.nback_level_1 == "1-Back"
    assert EN.nback_level_2 == "2-Back"
    assert EN.nback_level_3 == "3-Back"
    assert EN.nback_level_adaptive == "Adaptive"
    assert EN.nback_level_hint == "ESC — back"

def test_nback_strings_pl():
    assert PL.nback_level_title == "N-Back Memory Grid"
    assert PL.nback_level_1 == "1-Back"
    assert PL.nback_level_2 == "2-Back"
    assert PL.nback_level_3 == "3-Back"
    assert PL.nback_level_adaptive == "Adaptacyjny"
    assert PL.nback_level_hint == "ESC — wróć"
