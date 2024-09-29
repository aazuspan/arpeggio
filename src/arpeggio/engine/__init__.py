"""
The audio engine that powers arpeggio's music generation.
"""

from arpeggio.engine import note
from arpeggio.engine.instrument import Instrument, get_instrument
from arpeggio.engine.key import Key, get_mode
from arpeggio.engine.note import Note
from arpeggio.engine.song import Song
from arpeggio.engine.track import Track

__all__ = [
    "Song",
    "Track",
    "Key",
    "Instrument",
    "Note",
    "get_mode",
    "get_instrument",
    "note",
]
