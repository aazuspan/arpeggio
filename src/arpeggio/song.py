"""Songs that arrange and render tracks."""

from __future__ import annotations

from dataclasses import dataclass, field

from pydub import AudioSegment
from pydub.playback import play

from .audio import normalized_overlay
from .instrument import Instrument
from .key import Key
from .track import Track


@dataclass
class Song:
    key: Key
    bpm: int = 120
    sample_rate: int = 11_025
    tracks: list[Track] = field(default_factory=list)
    loop: int = 1

    def __len__(self) -> int:
        """Length of the song in milliseconds."""
        return max([len(track) for track in self.tracks])

    def render(self) -> AudioSegment:
        unmuted_tracks = [track for track in self.tracks if not track.mute]
        solo_tracks = [track for track in self.tracks if track.solo]
        tracks = solo_tracks or unmuted_tracks

        if self.loop > 1:
            return normalized_overlay([track.render() * self.loop for track in tracks])

        return normalized_overlay([track.render() for track in tracks])

    def play(self):
        """Play the song."""
        play(self.render())

    def add_track(self, instrument: type[Instrument], **kwargs) -> Track:
        """Create a new track with the given instrument."""
        track = Track(
            instrument=instrument(sample_rate=self.sample_rate), song=self, **kwargs
        )
        self.tracks.append(track)
        return track
