"""Instruments for synthesizing signals from notes and chords."""

import random
from abc import ABC

from pydub import AudioSegment
from pydub.generators import Sawtooth as SawtoothGenerator
from pydub.generators import SignalGenerator
from pydub.generators import Sine as SineGenerator
from pydub.generators import Square as SquareGenerator
from pydub.generators import Triangle as TriangleGenerator
from pydub.generators import WhiteNoise as WhiteNoiseGenerator

from .audio import normalized_overlay
from .note import Chord, Note

# Initialize the RNG to generate reproducible noise
random.seed(42)


class Instrument(ABC):
    """An instrument converts notes and chords to playable audio segments."""

    gen: type[SignalGenerator]

    def __init__(self, sample_rate: int):
        self.sample_rate = sample_rate
        self.bit_depth = 16

    def __call__(
        self, playable: Note | Chord | None, duration: float, volume: float = 0.0
    ) -> AudioSegment:
        if playable is None:
            return self._play_rest(duration)
        if isinstance(playable, float):
            return self._play_note(playable, duration, volume=volume)
        if isinstance(playable, Chord):
            return self._play_chord(playable, duration, volume=volume)

        raise TypeError(f"Invalid playable type: {type(playable)}")

    def _play_note(
        self, note: Note, duration: float, volume: float = 0.0
    ) -> AudioSegment:
        return self.gen(
            note, sample_rate=self.sample_rate, bit_depth=self.bit_depth
        ).to_audio_segment(duration, volume=volume)

    def _play_chord(
        self, chord: Chord, duration: float, volume: float = 0.0
    ) -> AudioSegment:
        segments = [self._play_note(note, duration, volume=volume) for note in chord]
        return normalized_overlay(segments)

    def _play_rest(self, duration: float) -> AudioSegment:
        return AudioSegment.silent(duration)


class Sine(Instrument):
    gen = SineGenerator


class Square(Instrument):
    gen = SquareGenerator


class Sawtooth(Instrument):
    gen = SawtoothGenerator


class Triangle(Instrument):
    gen = TriangleGenerator


class Noise(Instrument):
    gen = WhiteNoiseGenerator

    def _play_note(
        self, note: Note, duration: float, volume: float = 0.0
    ) -> AudioSegment:
        # WhiteNoiseGenerator doesn't support frequency
        return self.gen(
            sample_rate=self.sample_rate, bit_depth=self.bit_depth
        ).to_audio_segment(duration, volume=volume)


instruments = {
    "sine": Sine,
    "triangle": Triangle,
    "square": Square,
    "sawtooth": Sawtooth,
    "noise": Noise,
}


def get_instrument(name: str) -> type[Instrument]:
    return {k.lower(): v for k, v in instruments.items()}[name.lower()]
