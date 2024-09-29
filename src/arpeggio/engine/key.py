"""Musical keys and modes."""

from __future__ import annotations

from arpeggio.engine.note import Chord, Note, get_note


class Mode(list[int]):
    def semitones_to(self, interval: int, octave: int = 0) -> int:
        """Return the number of semitones from the tonic to the note at an interval."""
        if interval < 1 or interval > len(self):
            raise ValueError(f"Interval must be in range [1, {len(self)}].")

        # Intervals are one-indexed
        return sum(self[: interval - 1]) + 12 * octave


class Key:
    tonic: Note
    mode: Mode

    def __init__(self, tonic: Note, mode: Mode):
        self.tonic = tonic
        self.mode = mode

    @property
    def scale(self, octave: int = 0) -> tuple[Note, ...]:
        return tuple([self.note(i, octave) for i in range(1, 9)])

    def note(self, interval: int, octave: int = 0) -> Note:
        """
        Return the note at a given interval and octave offset from the tonic.

        Notes outside the interval range will wrap to the next octave.
        """
        # Wrap the interval by an octave if necessary
        wrapped_interval = (interval - 1) % len(self.mode) + 1
        wrapped_octave = octave + (interval - 1) // len(self.mode)

        return self.tonic + self.mode.semitones_to(wrapped_interval, wrapped_octave)

    def chord(self, interval: int, octave: int = 0) -> Chord:
        """Return the triad at a given interval and octave offset from the tonic."""
        return Chord(
            [
                self.note(interval, octave),
                self.note(interval + 2, octave),
                self.note(interval + 4, octave),
            ]
        )

    @classmethod
    def from_name(cls, note: str, mode: str) -> Key:
        """Return the key with the given name."""
        return cls(get_note(note), get_mode(mode))


modes = {
    "Ionian": Mode([2, 2, 1, 2, 2, 2, 1]),
    "Major": Mode([2, 2, 1, 2, 2, 2, 1]),
    "Aeolian": Mode([2, 1, 2, 2, 1, 2, 2]),
    "Minor": Mode([2, 1, 2, 2, 1, 2, 2]),
    "Dorian": Mode([2, 1, 2, 2, 2, 1, 2]),
    "Phrygian": Mode([1, 2, 2, 2, 1, 2, 2]),
    "Lydian": Mode([2, 2, 2, 1, 2, 2, 1]),
    "Mixolydian": Mode([2, 2, 1, 2, 2, 1, 2]),
    "Locrian": Mode([1, 2, 2, 1, 2, 2, 2]),
    "HarmonicMinor": Mode([2, 1, 2, 2, 1, 3, 1]),
    "MelodicMinor": Mode([2, 1, 2, 2, 2, 2, 1]),
}


def get_mode(name: str) -> Mode:
    """Return the mode with the given name."""
    return {k.lower(): v for k, v in modes.items()}[name.lower()]
