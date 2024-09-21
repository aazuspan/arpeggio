class Mode(list[int]):
    def semitones_to(self, interval: int, octave: int = 0) -> int:
        """Return the number of semitones from the tonic to the note at an interval."""
        if interval < 1 or interval > len(self):
            raise ValueError(f"Interval must be in range [1, {len(self)}].")

        # Intervals are one-indexed
        return sum(self[: interval - 1]) + 12 * octave


modes = {
    "Ionian": Mode([2, 2, 1, 2, 2, 2, 1]),
    "Major": Mode([2, 2, 1, 2, 2, 2, 1]),
    "Aeolian": Mode([2, 1, 2, 2, 1, 2, 2]),
    "Minor": Mode([2, 1, 2, 2, 1, 2, 2]),
    "Dorian": Mode([2, 1, 2, 2, 2, 1, 2]),
    "Phrygian": Mode([1, 2, 2, 2, 1, 2, 2]),
    "Lydian": Mode([2, 2, 2, 1, 2, 2, 1]),
    "Mixolydian": Mode([2, 2, 1, 2, 2, 1, 2]),
    "Locrian": Mode([1, 2, 2, 1, 2, 2, 2]),
    "HarmonicMinor": Mode([2, 1, 2, 2, 1, 3, 1]),
    "MelodicMinor": Mode([2, 1, 2, 2, 2, 2, 1]),
}


def get_mode(name: str) -> Mode:
    """Return the mode with the given name."""
    return {k.lower(): v for k, v in modes.items()}[name.lower()]
