from pathlib import Path

_EXAMPLE_PATHS = (Path(__file__).parent / "examples").rglob("*.arp")
EXAMPLE_SONGS = {path.stem: path.read_text() for path in _EXAMPLE_PATHS}
