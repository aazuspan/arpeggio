"""Musical notes and chords."""

from __future__ import annotations

from fractions import Fraction
from typing import TypeVar

NoteDuration_T = TypeVar("NoteDuration_T", bound="NoteDuration")


class NoteDuration:
    """A note duration."""

    fraction: Fraction

    @classmethod
    def to_millis(cls, bpm: int, beats_per_measure: int = 4) -> float:
        """Return the number of milliseconds this note duration lasts."""
        return float((60_000 * cls.fraction / bpm) * beats_per_measure)


class WholeNote(NoteDuration):
    fraction = Fraction(1, 1)


class HalfNote(NoteDuration):
    fraction = Fraction(1, 2)


class QuarterNote(NoteDuration):
    fraction = Fraction(1, 4)


class EighthNote(NoteDuration):
    fraction = Fraction(1, 8)


class SixteenthNote(NoteDuration):
    fraction = Fraction(1, 16)


class ThirtySecondNote(NoteDuration):
    fraction = Fraction(1, 32)


class Note:
    """A musical note."""

    def __init__(self, frequency: float):
        self.frequency = frequency

    def __repr__(self) -> str:
        return f"<Note {self.frequency:.2f}>"

    def __sub__(self, semitones: int) -> Note:
        """Return the frequency of the note a number of semitones below this note."""
        return Note(self.frequency / 2 ** (semitones / 12))

    def __add__(self, semitones: int) -> Note:
        """Return the frequency of the note a number of semitones above this note."""
        return Note(self.frequency * 2 ** (semitones / 12))


class Chord:
    def __init__(self, notes: list[Note]):
        self.notes = notes


STANDARD_PITCH = 440.0
STANDARD_NOTE = Note(STANDARD_PITCH)
NOTES: dict[str, Note] = {
    "C": STANDARD_NOTE - 9,
    "Cm": STANDARD_NOTE - 9,
    "C#": STANDARD_NOTE - 8,
    "Db": STANDARD_NOTE - 8,
    "C#m": STANDARD_NOTE - 8,
    "Dbm": STANDARD_NOTE - 8,
    "D": STANDARD_NOTE - 7,
    "Dm": STANDARD_NOTE - 7,
    "D#": STANDARD_NOTE - 6,
    "Eb": STANDARD_NOTE - 6,
    "D#m": STANDARD_NOTE - 6,
    "Ebm": STANDARD_NOTE - 6,
    "E": STANDARD_NOTE - 5,
    "Em": STANDARD_NOTE - 5,
    "F": STANDARD_NOTE - 4,
    "Fm": STANDARD_NOTE - 4,
    "F#": STANDARD_NOTE - 3,
    "Gb": STANDARD_NOTE - 3,
    "F#m": STANDARD_NOTE - 3,
    "Gbm": STANDARD_NOTE - 3,
    "G": STANDARD_NOTE - 2,
    "Gm": STANDARD_NOTE - 2,
    "G#": STANDARD_NOTE - 1,
    "Ab": STANDARD_NOTE - 1,
    "G#m": STANDARD_NOTE - 1,
    "Abm": STANDARD_NOTE - 1,
    "A": STANDARD_NOTE,
    "Am": STANDARD_NOTE,
    "A#": STANDARD_NOTE + 1,
    "Bb": STANDARD_NOTE + 1,
    "A#m": STANDARD_NOTE + 1,
    "Bbm": STANDARD_NOTE + 1,
    "B": STANDARD_NOTE + 2,
    "Bm": STANDARD_NOTE + 2,
}
