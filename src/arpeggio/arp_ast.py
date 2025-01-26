import sys
from dataclasses import dataclass

from lark import Transformer, ast_utils, v_args
from lark.tree import Meta


class Continue(ast_utils.Ast):
    """A marker to continue the previous note."""


class Rest(ast_utils.Ast):
    """A marker to rest for a note."""


@dataclass
class Interval(ast_utils.Ast):
    """A musical note or chord."""

    value: int
    octave: int = 0


@dataclass
class Config(ast_utils.Ast, ast_utils.WithMeta):
    """A configuration key and value."""

    meta: Meta
    key: str
    # Store as flag if no value is given
    value: float | int | str | bool = True


@dataclass
class Track(ast_utils.Ast):
    """A track with configuration and lines."""

    config: dict[str, Config]
    lines: list[list[Interval | Continue | Rest]]


@dataclass
class Song(ast_utils.Ast):
    """A song with configuration and tracks."""

    config: dict[str, Config]
    tracks: list[Track]


class _ToAst(Transformer):
    """Handler for other token types."""

    as_list = list

    @v_args(inline=True)
    def key(self, k):
        return k

    @v_args(inline=True)
    def value(self, v):
        return v

    @v_args(inline=True)
    def repeat(self, n):
        return int(n)

    @v_args(inline=True)
    def line(self, symbols, repeat=0):
        from fractions import Fraction

        if repeat:
            symbols *= repeat

        default_duration = Fraction(1, 16)
        # TODO: Refactor this
        symbol_durations: list[list[Interval | Continue | Rest | Fraction]] = []
        for s in symbols:
            if isinstance(s, Continue):
                if not symbol_durations:
                    raise ValueError("Cannot continue without a previous note.")
                symbol_durations[-1][1] += default_duration

            else:
                symbol_durations.append([s, default_duration])

        return symbol_durations

    def config_dict(self, configs: list[Config]) -> dict[str, Config]:
        config = {}
        for c in configs:
            config[c.key] = c

        return config

    def SIGNED_NUMBER(self, n) -> int | float:
        if "." in n:
            return float(n)
        return int(n)

    def OCTAVE(self, v):
        modifiers = {
            "_": -2,
            "-": -1,
            "+": 1,
            "*": 2,
        }
        return modifiers[v]

    INT = int
    WORD = NOTE_NAME = str


def get_transformer():
    return ast_utils.create_transformer(sys.modules[__name__], _ToAst())
