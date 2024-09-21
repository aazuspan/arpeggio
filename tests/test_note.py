import pytest

from arpeggio import note


def test_duration_to_millis():
    assert note.Duration(1, 4).to_millis(bpm=60, beats_per_measure=4) == 1_000
    assert note.Duration(1, 16).to_millis(bpm=60, beats_per_measure=4) == 250
    assert note.Duration(1, 2).to_millis(bpm=120, beats_per_measure=4) == 1_000
    assert note.Duration(1, 4).to_millis(bpm=60, beats_per_measure=1) == 250


def test_note_semitone_calculation():
    # A4 plus 3 semitones is C5
    assert (note.Note(440) + 3) == pytest.approx(523.251, rel=1e5)
    # A3 plus 12 semitones is A3
    assert (note.Note(440) - 12) == 220
    # C1 plus 28 semitones is E3
    assert (note.Note(32.703) + 28) == pytest.approx(164.813, rel=1e5)
