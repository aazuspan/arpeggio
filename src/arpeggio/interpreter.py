"""Convert an Arpeggio AST to a playable song."""

import arpeggio.arp_ast as ast

from . import key, note
from .instrument import get_instrument
from .song import Song


def interpret(parsed: ast.Song) -> Song:
    # TODO: Do a validation pass over the AST to raise errors and warnings, e.g. for
    # invalid intervals, instruments, mismatched line lengths, etc.

    key_name = parsed.config.pop("key", "C_major")
    if not isinstance(key_name, str) or "_" not in key_name:
        raise ValueError("Key must be a string in the format 'tonic_mode'.")

    tonic, mode = key_name.split("_")
    k = key.Key.from_name(tonic, mode)
    song = Song(key=k, **parsed.config)  # type: ignore

    for track in parsed.tracks:
        instrument_name = track.config.pop("instrument", "sine")
        if not isinstance(instrument_name, str):
            raise ValueError("Instrument must be a string.")
        instrument = get_instrument(instrument_name)

        t = song.add_track(instrument=instrument, **track.config)

        symbols = [s for line in track.lines for s in line]
        for symbol, duration in symbols:
            if isinstance(symbol, ast.Rest):
                t.rest(duration=note.Duration(duration))
            elif isinstance(symbol, ast.Interval):
                t.play(
                    interval=symbol.value,
                    octave=symbol.octave,
                    duration=note.Duration(duration),
                )

    return song
