from pathlib import Path

import pytest

import arpeggio

from .conftest import EXAMPLE_SONGS


@pytest.fixture(scope="session")
def original_datadir() -> Path:
    """Override the data directory used by pytest-regressions."""
    return Path(__file__).parent / "output"


@pytest.mark.parametrize("source", EXAMPLE_SONGS.values(), ids=EXAMPLE_SONGS.keys())
def test_interpret_example_songs(source: str, ndarrays_regression):
    parser = arpeggio.parser.Parser()
    ast = parser.parse(source)
    song = arpeggio.interpreter.interpret(ast)

    rendered = song.render()
    ndarrays_regression.check(
        {
            "rendered": rendered.get_array_of_samples(),
        }
    )
