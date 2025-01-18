"""Tracks that arrange and render individual sounds."""

from __future__ import annotations

from functools import cached_property

from pydantic import (
    Field,
    NonNegativeInt,
    NonPositiveFloat,
    PositiveInt,
    PrivateAttr,
    field_validator,
)
from pydantic_core import PydanticCustomError
from pydub import AudioSegment

from arpeggio.engine import Key
from arpeggio.engine.instrument import Instrument, get_instrument
from arpeggio.engine.note import Chord, Duration, Note
from arpeggio.validation import ValidatedConfig


class Track(ValidatedConfig):
    """A track that arranges and renders individual sounds."""

    instrument_type: type[Instrument] = Field(
        default="sine", alias="instrument", validate_default=True
    )
    """The type of instrument generator."""

    volume: NonPositiveFloat = 0.0
    """The volume of the track, in decibels between -infinity and 0."""

    pan: float = Field(0.0, ge=-1.0, le=1.0)
    """The stereo panning of the track, between -1 (left) and 1 (right)."""

    octave: int = 0
    """An octave offset to apply to all notes and chords."""

    chords: bool = False
    """If true, play chords instead of single notes."""

    staccato: bool = False
    """If true, notes are held for half their duration."""

    mute: bool = False
    """If true, mute the track when rendering the song."""

    solo: bool = False
    """If true, only play this track when rendering the song."""

    loop: PositiveInt = 1
    """The number of times to loop the track."""

    offset: NonNegativeInt = 0
    """The number of 16th notes to delay this track's start."""

    sample_rate: PositiveInt
    """The sample rate of the song."""

    key: Key
    """The key of the song."""

    bpm: PositiveInt
    """The tempo of the song in beats per minute."""

    _segment: AudioSegment = PrivateAttr(default_factory=AudioSegment.empty)

    @field_validator("instrument_type", mode="before")
    def validate_instrument(cls, v: str):
        try:
            return get_instrument(v)
        except Exception:
            raise PydanticCustomError(
                "invalid_instrument",
                "Instrument `{instrument_name}` not found.",
                dict(instrument_name=v),
            ) from None

    @cached_property
    def instrument(self) -> Instrument:
        return self.instrument_type(sample_rate=self.sample_rate)

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
            playable = self.key.chord(interval, octave + self.octave)
        else:
            playable = self.key.note(interval, octave + self.octave)

        if self.staccato:
            self._add_to_timeline(playable, duration=duration / 2)
            self.rest(duration=duration / 2)
        else:
            self._add_to_timeline(playable, duration=duration)

        return playable

    def rest(self, *, duration: Duration) -> None:
        """Add a rest to the track's timeline."""
        self._add_to_timeline(None, duration=duration)

    def _add_to_timeline(
        self, playable: Note | Chord | None, *, duration: Duration
    ) -> None:
        duration_ms = duration.to_millis(self.bpm)
        # Concatenating segments like this compounds rounding errors in note length,
        # but it's 10x faster than the alternative of calculating and overlaying notes
        # at correct positions. The total accumulated error with 32nd notes over 4
        # minutes is only ~100ms, so I think it's worth the speed.
        self._segment += self.instrument(
            playable, duration=duration_ms, volume=self.volume
        ).pan(self.pan)

    def render(self) -> AudioSegment:
        """Render the track to an audio segment."""
        segment = self._segment * self.loop if self.loop > 1 else self._segment

        if self.offset > 0:
            # Add silence to the beginning of the track
            offset_ms = Duration(self.offset, 16).to_millis(self.bpm)
            offset_segment = self.instrument(None, duration=offset_ms)
            segment = offset_segment + segment

        return segment
