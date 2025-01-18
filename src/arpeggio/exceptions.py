class SourceError(Exception):
    """An error associated with source code."""

    def __init__(self, message: str, meta):
        super().__init__(message)
        self.message = message
        self.meta = meta

    def __str__(self):
        loc = f"{self.meta.filename}, line {self.meta.line}, column {self.meta.column}"
        return f"{loc}: {self.message}"


class ConfigError(SourceError):
    """An error raised by invalid configuration."""


class ParserError(SourceError):
    """An syntax error that prevents parsing."""
