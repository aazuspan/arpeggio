import arpeggio


def test_mode_semitones():
    assert arpeggio.engine.get_mode("Major").semitones_to(1, 1) == 12
    assert arpeggio.engine.get_mode("Major").semitones_to(1, -2) == -24

    assert arpeggio.engine.get_mode("Major").semitones_to(3) == 4
    assert arpeggio.engine.get_mode("Major").semitones_to(5) == 7

    assert arpeggio.engine.get_mode("Minor").semitones_to(3) == 3
    assert arpeggio.engine.get_mode("Minor").semitones_to(5) == 7
