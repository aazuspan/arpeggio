"""Tracks that arrange and render individual sounds."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydub import AudioSegment

from .instrument import Instrument
from .note import Chord, Duration, Note

if TYPE_CHECKING:
    from .song import Song


class Track:
    def __init__(
        self,
        instrument: type[Instrument],
        song: Song,
        volume: float = 0.0,
        pan: float = 0.0,
        octave: int = 0,
        chords: bool = False,
        mute: bool = False,
        solo: bool = False,
    ):
        if volume > 0.0:
            raise ValueError("Volume must be less than 0.0.")

        self.instrument = instrument(sample_rate=song.sample_rate)
        self.song = song
        self.volume = volume
        self.pan = pan
        self.octave = octave
        self.chords = chords
        self.mute = mute
        self.solo = solo
        self.segment: AudioSegment = AudioSegment.empty()

    def __len__(self) -> int:
        """Length of the track in milliseconds."""
        return len(self.segment)

    def play(
        self,
        interval: int,
        *,
        duration: Duration,
        octave: int = 0,
    ) -> Note | Chord:
        """Add a note or chord to the track's timeline."""
        playable: Note | Chord
        if self.chords:
            playable = self.song.key.chord(interval, octave + self.octave)
        else:
            playable = self.song.key.note(interval, octave + self.octave)

        self._add_to_timeline(playable, duration=duration)
        return playable

    def rest(self, *, duration: Duration) -> None:
        """Add a rest to the track's timeline."""
        self._add_to_timeline(None, duration=duration)

    def _add_to_timeline(
        self, playable: Note | Chord | None, *, duration: Duration
    ) -> None:
        duration_ms = duration.to_millis(self.song.bpm)
        # Concatenating segments like this compounds rounding errors in note length,
        # but it's 10x faster than the alternative of calculating and overlaying notes
        # at correct positions. The total accumulated error with 32nd notes over 4
        # minutes is only ~100ms, so I think it's worth the speed.
        self.segment += self.instrument(
            playable, duration=duration_ms, volume=self.volume
        ).pan(self.pan)

    def loop(self, n: int) -> None:
        """Loop the track n times."""
        self.segment *= n
