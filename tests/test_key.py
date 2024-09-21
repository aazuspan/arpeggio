import pytest

from arpeggio import key, note


def test_get_key_by_name():
    amaj = key.Key.from_name("A", "Major")
    assert amaj.tonic == note.Note(440.0)
    assert amaj.mode == [2, 2, 1, 2, 2, 2, 1]

    csharpmin = key.Key.from_name("C#", "Minor")
    assert csharpmin.tonic == pytest.approx(277.183, rel=1e5)
    assert csharpmin.mode == [2, 1, 2, 2, 1, 2, 2]
