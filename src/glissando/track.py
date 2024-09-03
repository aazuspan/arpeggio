"""Tracks that arrange and render individual sounds."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydub import AudioSegment

from .instrument import Instrument
from .note import Chord, Note, NoteDuration_T, QuarterNote

if TYPE_CHECKING:
    from .song import Song


class Track:
    def __init__(self, instrument: type[Instrument], song: Song, volume: float = 0.0):
        if volume > 0.0:
            raise ValueError("Volume must be less than 0.0.")

        self.instrument = instrument(
            sample_rate=song.sample_rate, bit_depth=song.bit_depth
        )
        self.song = song
        self.volume = volume
        self.segment = AudioSegment.empty()

    def __len__(self) -> int:
        """Length of the track in milliseconds."""
        return len(self.segment)

    def add_note(
        self,
        interval: int,
        *,
        octave: int = 0,
        duration: type[NoteDuration_T] = QuarterNote,
    ) -> None:
        """Add a note to the track's timeline."""
        note = self.song.key.note(interval, octave)
        self._add_to_timeline(note, duration=duration)

    def add_chord(
        self,
        interval: int,
        *,
        octave: int = 0,
        duration: type[NoteDuration_T] = QuarterNote,
    ) -> None:
        """Add a chord to the track's timeline."""
        chord = self.song.key.chord(interval, octave)
        self._add_to_timeline(chord, duration=duration)

    def add_rest(self, *, duration: type[NoteDuration_T] = QuarterNote) -> None:
        """Add a rest to the track's timeline."""
        self._add_to_timeline(None, duration=duration)

    def _add_to_timeline(
        self, playable: Note | Chord | None, *, duration: type[NoteDuration_T]
    ) -> None:
        duration_ms = duration.to_millis(self.song.bpm)
        # Concatenating segments like this compounds rounding errors in note length,
        # but it's 10x faster than the alternative of calculating and overlaying notes
        # at correct positions. The total accumulated error with 32nd notes over 4
        # minutes is only ~100ms, so I think it's worth the speed.
        self.segment += self.instrument(
            playable, duration=duration_ms, volume=self.volume
        )

    def loop(self, n: int) -> None:
        """Loop the track n times."""
        self.segment *= n
