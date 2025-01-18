"""Convert an Arpeggio AST to a playable song."""

import arpeggio.arp_ast as ast
from arpeggio import engine

DEFAULT_KEY = "C_major"
DEFAULT_INSTRUMENT = "sine"


def interpret(parsed: ast.Song, filename: str = "<stdin>") -> engine.Song:
    song = engine.Song.validate(parsed.config, filename=filename)

    for parsed_track in parsed.tracks:
        track = engine.Track.validate(
            parsed_track.config,
            sample_rate=song.sample_rate,
            key=song.key,
            bpm=song.bpm,
            filename=filename,
        )
        song.tracks.append(track)

        symbols = [s for line in parsed_track.lines for s in line]
        for symbol, duration in symbols:
            if isinstance(symbol, ast.Rest):
                track.rest(
                    duration=engine.note.Duration(
                        duration.numerator, duration.denominator
                    )
                )
            elif isinstance(symbol, ast.Interval):
                track.play(
                    interval=symbol.value,
                    octave=symbol.octave,
                    duration=engine.note.Duration(
                        duration.numerator, duration.denominator
                    ),
                )

    return song
