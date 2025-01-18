from pathlib import Path

import pytest

import arpeggio
from arpeggio.exceptions import ConfigError

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


@pytest.mark.parametrize("source", ["", "~ comment"])
def test_interpret_empty_songs(source):
    """An empty program should interpret as silence."""
    parser = arpeggio.parser.Parser()
    ast = parser.parse(source)
    song = arpeggio.interpreter.interpret(ast)

    assert ast.config == {}
    assert ast.tracks == []
    assert not song.render()


def test_interpret_empty_track():
    """An empty track should interpret as silence."""
    empty_track = "track\n@instrument sine\nend"
    nonempty_track = "track\n| 1 2 3 4\nend"
    source = "\n".join([nonempty_track, empty_track])

    parser = arpeggio.parser.Parser()
    ast = parser.parse(source)
    song = arpeggio.interpreter.interpret(ast)
    assert song.render()


def test_invalid_config_errors():
    """Test that invalid configurations raises errors."""
    parser = arpeggio.parser.Parser()

    parsed = parser.parse("@key 120")
    with pytest.raises(ConfigError, match="Invalid @key"):
        arpeggio.interpreter.interpret(parsed)

    parsed = parser.parse("@fadsf")
    with pytest.raises(ConfigError, match="Unrecognized configuration @fadsf"):
        arpeggio.interpreter.interpret(parsed)

    parsed = parser.parse("track\n@instrument cowbell\nend")
    with pytest.raises(ConfigError, match="Invalid @instrument"):
        arpeggio.interpreter.interpret(parsed)

    parsed = parser.parse("track\n@stuff\nend")
    with pytest.raises(ConfigError, match="Unrecognized configuration @stuff"):
        arpeggio.interpreter.interpret(parsed)
