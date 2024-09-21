import pytest

from arpeggio.parser import Parser


def test_parse_valid_program():
    prog = """
    @bpm 120
    @key C#_Major

    ~ This is a track
    track
        @instrument sine

        6 . 2 . . . 1 .
        3+2+1+. 6 . 5 . [x3]
        3 . 2 . . . 1 .
    end

    ~ Another track
    track
        @instrument square

        1 . . . . . . . [x4]
    end
    """
    parser = Parser()
    song = parser.parse(prog)
    assert song.config == {"bpm": 120, "key": "C#_Major"}
    assert len(song.tracks) == 2

    track = song.tracks[0]
    assert track.config == {"instrument": "sine"}
    assert len(track.lines) == 3
    assert len(track.lines[1]) == 5 * 3


@pytest.mark.parametrize("source", ["", "~ comment"])
def test_parse_empty_program(source):
    """An empty program should parse without errors."""
    parser = Parser()
    ast = parser.parse(source)

    assert not parser.diagnostics
    assert ast.config == {}
    assert ast.tracks == []
