import arpeggio


def test_parse_valid_program():
    prog = """
    @bpm 120
    @key C#_Major

    ~ This is a track
    track
        @instrument sine

        | 6 . 2 . . . 1 .
        | 3+2+1+. 6 . 5 . [x3]
        | 3 . 2 . . . 1 .
    end

    ~ Another track
    track
        @instrument square

        | 1 . . . . . . . [x4]
    end
    """
    parser = arpeggio.parser.Parser()
    song = parser.parse(prog)
    assert song.config == {"bpm": 120, "key": "C#_Major"}
    assert len(song.tracks) == 2

    track = song.tracks[0]
    assert track.config == {"instrument": "sine"}
    assert len(track.lines) == 3
    assert len(track.lines[1]) == 5 * 3


def test_parse_whitespace():
    # Spaces within a song were breaking LALR parsing
    prog = """
    track
        @instrument sine
    
    end
    """
    parser = arpeggio.parser.Parser()
    parser.parse(prog)
