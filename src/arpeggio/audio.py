import numpy as np
from pydub import AudioSegment
from pydub.utils import get_min_max_value


def normalized_overlay(segments: list[AudioSegment]) -> AudioSegment:
    """
    Overlay multiple audio segments, normalizing as needed to prevent clipping.

    This avoids clipping that otherwise occurs with AudioSegment.overlay. The output
    segment will have the same duration as the longest input segment.
    """
    max_segment_length = int(
        max([len(segment._data) / segment.sample_width for segment in segments])
    )
    # Use int to prevent overflow
    output = np.zeros(max_segment_length, dtype=int)

    for segment in segments:
        segment_array = np.array(segment.get_array_of_samples())
        output[: len(segment_array)] += segment_array

    min_val, max_val = get_min_max_value(16)

    if output.max() > max_val or output.min() < min_val:
        output = np.interp(output, (output.min(), output.max()), (min_val, max_val))

    return segments[0]._spawn(output.astype(np.int16).tobytes())
