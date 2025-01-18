class SourceError(Exception):
    """An error associated with source code."""

    def __init__(self, message: str, meta):
        super().__init__(message)
        self.message = message
        self.meta = meta

    def __str__(self):
        # TODO: Report the filename of the parsed program
        return f"line {self.meta.line}, column {self.meta.column}: {self.message}"


class ConfigError(SourceError):
    """An error raised by invalid configuration."""


class ParserError(SourceError):
    """An syntax error that prevents parsing."""
