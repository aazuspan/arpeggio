"""Convert an Arpeggio AST to a playable song."""

from typing import Any

import arpeggio.arp_ast as ast
from arpeggio import engine

DEFAULT_KEY = "C_major"
DEFAULT_INSTRUMENT = "sine"


def _interpret_key(key_name: Any) -> engine.Key:
    if not isinstance(key_name, str) or "_" not in key_name:
        raise ValueError("Key must be a string in the format 'tonic_mode'.")

    tonic, mode = key_name.split("_")
    return engine.Key.from_name(tonic, mode)


def _interpret_instrument(instrument_name: Any) -> type[engine.Instrument]:
    if not isinstance(instrument_name, str):
        raise ValueError("Instrument must be a string.")
    return engine.get_instrument(instrument_name)


def interpret(parsed: ast.Song) -> engine.Song:
    # TODO: Do a validation pass over the AST to raise errors and warnings, e.g. for
    # invalid intervals, instruments, mismatched line lengths, etc.

    key = _interpret_key(parsed.config.pop("key", DEFAULT_KEY))
    song = engine.Song(key=key, **parsed.config)  # type: ignore

    for track in parsed.tracks:
        instrument = _interpret_instrument(
            track.config.pop("instrument", DEFAULT_INSTRUMENT)
        )
        t = song.add_track(instrument=instrument, **track.config)

        symbols = [s for line in track.lines for s in line]
        for symbol, duration in symbols:
            if isinstance(symbol, ast.Rest):
                t.rest(
                    duration=engine.note.Duration(
                        duration.numerator, duration.denominator
                    )
                )
            elif isinstance(symbol, ast.Interval):
                t.play(
                    interval=symbol.value,
                    octave=symbol.octave,
                    duration=engine.note.Duration(
                        duration.numerator, duration.denominator
                    ),
                )

    return song
