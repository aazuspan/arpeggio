"""Musical notes and chords."""

from __future__ import annotations

from fractions import Fraction


class Duration(Fraction):
    """A note duration, in fractions of a whole note."""

    def to_millis(self, bpm: int, beats_per_measure: int = 4) -> float:
        """Return the number of milliseconds this note duration lasts."""
        return float((60_000 * float(self) / bpm) * beats_per_measure)


WholeNote = Duration(1, 1)
HalfNote = Duration(1, 2)
QuarterNote = Duration(1, 4)
EighthNote = Duration(1, 8)
SixteenthNote = Duration(1, 16)


class Note(float):
    """A musical note."""

    def __repr__(self) -> str:
        return f"<Note {self:.2f}>"

    def __sub__(self, semitones: int | float) -> Note:
        """Return the frequency of the note a number of semitones below this note."""
        return Note(self / 2 ** (semitones / 12))

    def __add__(self, semitones: int | float) -> Note:
        """Return the frequency of the note a number of semitones above this note."""
        return Note(self * 2 ** (semitones / 12))


class Chord(list[Note]):
    """A collection of notes."""


STANDARD_PITCH = 440.0
STANDARD_NOTE = Note(STANDARD_PITCH)

notes: dict[str, Note] = {
    "C": STANDARD_NOTE - 9,
    "C#": STANDARD_NOTE - 8,
    "Db": STANDARD_NOTE - 8,
    "D": STANDARD_NOTE - 7,
    "D#": STANDARD_NOTE - 6,
    "Eb": STANDARD_NOTE - 6,
    "E": STANDARD_NOTE - 5,
    "F": STANDARD_NOTE - 4,
    "F#": STANDARD_NOTE - 3,
    "Gb": STANDARD_NOTE - 3,
    "G": STANDARD_NOTE - 2,
    "G#": STANDARD_NOTE - 1,
    "Ab": STANDARD_NOTE - 1,
    "A": STANDARD_NOTE,
    "A#": STANDARD_NOTE + 1,
    "Bb": STANDARD_NOTE + 1,
    "B": STANDARD_NOTE + 2,
}


def get_note(name: str) -> Note:
    """Return the note with the given name."""
    return {k.lower(): v for k, v in notes.items()}[name.lower()]
