from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from tetris.core.board import Board
from tetris.core.tetromino import Tetromino

class RendererBase(ABC):
    @abstractmethod
    def begin_frame(self) -> None: ...
    @abstractmethod
    def end_frame(self) -> None: ...

    @abstractmethod
    def poll_events(self) -> List[Any]: ...
    @abstractmethod
    def tick(self) -> int: ...

    @abstractmethod
    def draw_menu(self, player_name: str, hint: str, highscores: List[Dict[str, Any]]) -> None: ...

    @abstractmethod
    def draw_game(
        self,
        board: Board,
        active: Tetromino,
        ghost_cells: List[Tuple[int, int]] | None,
        next_kinds: List[str],
        hold_kind: Optional[str],
        score: int,
        level: int,
        total_lines: int,
        paused: bool,
    ) -> None: ...

    @abstractmethod
    def draw_game_over(self, score: int, level: int, total_lines: int, highscores: List[Dict[str, Any]]) -> None: ...

    @abstractmethod
    def shutdown(self) -> None: ...
