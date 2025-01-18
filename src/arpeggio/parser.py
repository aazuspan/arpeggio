"""Parse Arpeggio source code into an AST."""

from lark import Lark, UnexpectedCharacters, UnexpectedToken
from lark.tree import Meta

import arpeggio.arp_ast as ast
from arpeggio.exceptions import ParserError


class Parser:
    def __init__(self):
        self.transformer = ast.get_transformer()
        self.parser = Lark.open_from_package(
            "arpeggio",
            "arpeggio.lark",
            start="song",
            parser="lalr",
            propagate_positions=True,
        )

    def parser_error(
        self, e: UnexpectedToken | UnexpectedCharacters, filename: str
    ) -> None:
        if isinstance(e, UnexpectedToken):
            got = str(e.token)
            unexpected_type = "token"
        elif isinstance(e, UnexpectedCharacters):
            got = str(e.char)
            unexpected_type = "character"

        msg = f"Unexpected {unexpected_type} {got!r}."
        meta = Meta()
        meta.line = e.line
        meta.column = e.column
        meta.filename = filename
        raise ParserError(msg, meta)

    def parse(self, source: str, filename: str = "<stdin>") -> ast.Song:
        """Parse an Arpeggio program and return the AST."""
        source += "\n"

        self.tree = self.parser.parse(
            source, on_error=lambda e: self.parser_error(e, filename)
        )
        return self.transformer.transform(self.tree)
