"""Tracks that arrange and render individual sounds."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pydub import AudioSegment

from arpeggio.engine.instrument import Instrument
from arpeggio.engine.note import Chord, Duration, Note

if TYPE_CHECKING:
    from .song import Song


@dataclass
class Track:
    """A track that arranges and renders individual sounds."""

    instrument: Instrument
    song: Song
    _segment: AudioSegment = field(default_factory=AudioSegment.empty)

    volume: float = 0.0
    """The volume of the track, in decibels between -infinity and 0."""

    pan: float = 0.0
    """The stereo panning of the track, between -1 (left) and 1 (right)."""

    octave: int = 0
    """An octave offset to apply to all notes and chords."""

    chords: bool = False
    """If true, play chords instead of single notes."""

    mute: bool = False
    """If true, mute the track when rendering the song."""

    solo: bool = False
    """If true, only play this track when rendering the song."""

    loop: int = 1
    """The number of times to loop the track."""

    def __post_init__(self):
        if self.volume > 0.0:
            raise ValueError("Volume must be less than 0.0.")

        if not -1 <= self.pan <= 1:
            raise ValueError("Pan must be between -1 and 1.")

        if self.loop < 1:
            raise ValueError("Loop must be greater than 0.")

    def __len__(self) -> int:
        """Length of the track in milliseconds."""
        return len(self._segment)

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
        self._segment += self.instrument(
            playable, duration=duration_ms, volume=self.volume
        ).pan(self.pan)

    def render(self) -> AudioSegment:
        """Render the track to an audio segment."""
        if self.loop > 1:
            return self._segment * self.loop

        return self._segment
