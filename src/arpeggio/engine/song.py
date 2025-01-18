"""Songs that arrange and render tracks."""

from __future__ import annotations

from pydantic import Field, PositiveInt, field_validator
from pydantic_core import PydanticCustomError
from pydub import AudioSegment
from pydub.playback import play

from arpeggio.engine.audio import normalized_overlay
from arpeggio.engine.key import Key
from arpeggio.engine.track import Track
from arpeggio.validation import ValidatedConfig


class Song(ValidatedConfig):
    """The base component of a parsed program."""

    key: Key = Field(default="C_major", validate_default=True)
    """The musical key."""

    bpm: PositiveInt = 120
    """Tempo in beats per minute."""

    sample_rate: PositiveInt = 11_025
    """The sampling rate of rendered audio."""

    tracks: list[Track] = Field(default_factory=list)
    """The tracks that comprise the song."""

    loop: PositiveInt = 1
    """The number of times to loop the song."""

    @field_validator("key", mode="before")
    def validate_key(cls, v: str):
        try:
            return Key.from_name(v)
        except Exception:
            raise PydanticCustomError(
                "invalid_key",
                "Key should be in the form `tonic_mode`. Got `{key_name}`.",
                dict(key_name=v),
            ) from None

    def __len__(self) -> int:
        """Length of the song in milliseconds."""
        return max([len(track) for track in self.tracks])

    def render(self) -> AudioSegment:
        unmuted_tracks = [track for track in self.tracks if not track.mute]
        solo_tracks = [track for track in self.tracks if track.solo]
        tracks = solo_tracks or unmuted_tracks

        rendered = normalized_overlay([track.render() for track in tracks])
        if self.loop > 1:
            rendered *= self.loop

        return rendered

    def play(self):
        """Play the song."""
        play(self.render())
