"""Songs that arrange and render tracks."""

from __future__ import annotations

from pydub import AudioSegment
from pydub.playback import play

from .key import Key
from .track import Track


class Song:
    def __init__(
        self, key: Key, bpm: int = 120, sample_rate: int = 11025, bit_depth: int = 8
    ):
        self.key = key
        self.bpm = bpm
        self.sample_rate = sample_rate
        self.bit_depth = bit_depth
        self.tracks: list[Track] = []

    def __len__(self) -> int:
        """Length of the song in milliseconds."""
        return max([len(track) for track in self.tracks])

    def render(self) -> AudioSegment:
        segment = AudioSegment.silent(len(self))

        for track in self.tracks:
            segment = segment.overlay(track.segment)

        return segment

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
