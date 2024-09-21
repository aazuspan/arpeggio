from arpeggio import mode


def test_mode_semitones():
    assert mode.get_mode("Major").semitones_to(1, 1) == 12
    assert mode.get_mode("Major").semitones_to(1, -2) == -24

    assert mode.get_mode("Major").semitones_to(3) == 4
    assert mode.get_mode("Major").semitones_to(5) == 7

    assert mode.get_mode("Minor").semitones_to(3) == 3
    assert mode.get_mode("Minor").semitones_to(5) == 7
