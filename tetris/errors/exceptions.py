class TetrisError(Exception):
    """Base class for Tetris-related exceptions."""

class ConfigError(TetrisError):
    """Configuration issue (missing/invalid settings)."""

class SaveFileError(TetrisError):
    """Failure to read/write save file."""

class CorruptedDataError(TetrisError):
    """Corrupted or invalid game data."""

class InvalidMoveError(TetrisError):
    """Invalid move attempted in the game (e.g., out-of-bounds)."""
