class TetrisError(Exception):
    """Base exception class for the project."""

class ConfigError(TetrisError):
    """Configuration file format or field is invalid."""

class SaveFileError(TetrisError):
    """File read/write failure (IO/permission/path issues)."""

class CorruptedDataError(TetrisError):
    """Data file content is corrupted or cannot be parsed."""

class InvalidMoveError(TetrisError):
    """Invalid move (collision or out of bounds)."""
