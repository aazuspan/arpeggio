"""Convert an Arpeggio AST to a playable song."""

import inspect
from typing import Any

import arpeggio.arp_ast as ast
from arpeggio import engine

DEFAULT_KEY = "C_major"
DEFAULT_INSTRUMENT = "sine"


class InterpreterError(Exception): ...


def _interpret_key(key_name: Any) -> engine.Key:
    if not isinstance(key_name, str) or "_" not in key_name:
        raise InterpreterError("Key must be a string in the format 'tonic_mode'.")

    try:
        tonic, mode = key_name.split("_")
        return engine.Key.from_name(tonic, mode)
    except Exception as e:
        raise InterpreterError(f"Invalid key: {key_name}") from e


def _interpret_instrument(instrument_name: Any) -> type[engine.Instrument]:
    if not isinstance(instrument_name, str):
        raise InterpreterError("Instrument must be a string.")

    try:
        return engine.get_instrument(instrument_name)
    except Exception as e:
        raise InterpreterError(f"Invalid instrument: {instrument_name}") from e


def _validate_config_params(cls, params: dict) -> None:
    expected_params = inspect.signature(cls).parameters.keys()
    invalid_params = [p for p in params if p not in expected_params]
    if invalid_params:
        raise InterpreterError(f"Unsupported configuration option: {invalid_params}")


def interpret(parsed: ast.Song) -> engine.Song:
    # TODO: Do a validation pass over the AST to raise errors and warnings, e.g. for
    # invalid intervals, instruments, mismatched line lengths, etc.

    key = _interpret_key(parsed.config.pop("key", DEFAULT_KEY))

    _validate_config_params(engine.Song, parsed.config)
    song = engine.Song(key=key, **parsed.config)  # type: ignore

    for track in parsed.tracks:
        instrument = _interpret_instrument(
            track.config.pop("instrument", DEFAULT_INSTRUMENT)
        )
        _validate_config_params(engine.Track, track.config)
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
