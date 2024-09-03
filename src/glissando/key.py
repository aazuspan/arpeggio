"""Musical keys and modes."""

from __future__ import annotations

from abc import ABC

from .note import NOTES, Chord, Note


class Mode(ABC):
    """A mode defines intervals between notes."""

    intervals: list[int]

    @classmethod
    def semitones_to(cls, interval: int, octave: int = 0) -> int:
        """Return the number of semitones from the tonic to the note at an interval."""
        if interval < 1 or interval > len(cls.intervals):
            raise ValueError(f"Interval must be in range [1, {len(cls.intervals)}].")

        # Intervals are one-indexed
        return sum(cls.intervals[: interval - 1]) + 12 * octave


class Key(ABC):
    tonic: Note
    mode: Mode

    def __init__(self, tonic: Note | str, mode: Mode):
        if isinstance(tonic, str):
            tonic = NOTES[tonic]

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
        wrapped_interval = (interval - 1) % len(self.mode.intervals) + 1
        wrapped_octave = octave + (interval - 1) // len(self.mode.intervals)

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


class Ionian(Mode):
    """Ionian diatonic major scale."""

    intervals = [2, 2, 1, 2, 2, 2, 1]


class Aeolian(Mode):
    """Aeolian diatonic natural minor scale."""

    intervals = [2, 1, 2, 2, 1, 2, 2]


Major = Ionian
Minor = Aeolian


class Dorian(Mode):
    """Dorian diatonic scale."""

    intervals = [2, 1, 2, 2, 2, 1, 2]


class Phrygian(Mode):
    """Phrygian diatonic scale."""

    intervals = [1, 2, 2, 2, 1, 2, 2]


class Lydian(Mode):
    """Lydian diatonic scale."""

    intervals = [2, 2, 2, 1, 2, 2, 1]


class Mixolydian(Mode):
    """Mixolydian diatonic scale."""

    intervals = [2, 2, 1, 2, 2, 1, 2]


class Locrian(Mode):
    """Locrian diatonic scale."""

    intervals = [1, 2, 2, 1, 2, 2, 2]


class HarmonicMinor(Mode):
    """Harmonic minor scale."""

    intervals = [2, 1, 2, 2, 1, 3, 1]


class MelodicMinor(Mode):
    """Melodic minor scale."""

    intervals = [2, 1, 2, 2, 2, 2, 1]
