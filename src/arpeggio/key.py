"""Musical keys and modes."""

from __future__ import annotations

from arpeggio.mode import Mode, get_mode

from .note import Chord, Note, get_note


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
