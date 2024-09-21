"""Songs that arrange and render tracks."""

from __future__ import annotations

from pydub import AudioSegment
from pydub.playback import play

from .audio import normalized_overlay
from .key import Key
from .track import Track


class Song:
    def __init__(self, key: Key, bpm: int = 120, sample_rate: int = 11025):
        self.key = key
        self.bpm = bpm
        self.sample_rate = sample_rate
        self.tracks: list[Track] = []

    def __len__(self) -> int:
        """Length of the song in milliseconds."""
        return max([len(track) for track in self.tracks])

    def render(self) -> AudioSegment:
        unmuted_tracks = [track for track in self.tracks if not track.mute]
        solo_tracks = [track for track in self.tracks if track.solo]
        play_tracks = solo_tracks or unmuted_tracks

        return normalized_overlay([track.segment for track in play_tracks])

    def play(self):
        """Play the song."""
        play(self.render())

    def add_track(self, instrument, **kwargs) -> Track:
        """Create a new track with the given instrument."""
        track = Track(instrument, song=self, **kwargs)
        self.tracks.append(track)
        return track

    def loop(self, n: int) -> None:
        for track in self.tracks:
            track.loop(n)
