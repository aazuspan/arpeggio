"""Parse Arpeggio source code into an AST."""

from dataclasses import dataclass

from lark import Lark, UnexpectedCharacters, UnexpectedToken

import arpeggio.arp_ast as ast


class ParsingError(Exception):
    """Errors occurred during parsing."""


@dataclass
class Position:
    line: int
    column: int


@dataclass
class Diagnostic:
    msg: str
    position: Position

    def __repr__(self):
        return f"{self.position.line}:{self.position.column}: {self.msg}"


class Parser:
    def __init__(self):
        self.diagnostics: list[Diagnostic] = []
        self.transformer = ast.get_transformer()
        self.parser = Lark.open_from_package(
            "arpeggio",
            "arpeggio.lark",
            start="song",
            parser="lalr",
            propagate_positions=True,
        )

    def _collect_error(self, e: UnexpectedToken | UnexpectedCharacters):
        if isinstance(e, UnexpectedToken):
            expected = ", ".join(e.accepts or e.expected)
            got = str(e.token)
            unexpected_type = "token"
        elif isinstance(e, UnexpectedCharacters):
            expected = ", ".join(e.allowed)
            got = str(e.char)
            unexpected_type = "character"

        msg = f"Unexpected {unexpected_type} {got!r}. Expected one of: {{{expected}}}"
        diagnostic = Diagnostic(msg, position=Position(e.line, e.column))
        self.diagnostics.append(diagnostic)
        return True

    def parse(self, source: str, wrap_errors: bool = False) -> ast.Song:
        """
        Parse an Arpeggio program and return the AST.

        On error, sets diagnostics and raises a ParsingError.
        """
        source += "\n"

        on_error = self._collect_error if wrap_errors else None
        self.tree = self.parser.parse(source, on_error=on_error)
        if self.diagnostics:
            raise ParsingError("\n".join([str(d) for d in self.diagnostics]))

        return self.transformer.transform(self.tree)
