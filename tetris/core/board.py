from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Tuple

from tetris.core.vec2 import Vec2
from tetris.core.tetromino import Tetromino

Color = Tuple[int, int, int]

@dataclass
class Board:
    cols: int = 10
    rows: int = 20

    def __post_init__(self) -> None:
        self._grid: List[List[Optional[Color]]] = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    @property
    def grid(self) -> List[List[Optional[Color]]]:
        return self._grid

    def inside(self, cell: Vec2) -> bool:
        return 0 <= cell.x < self.cols and 0 <= cell.y < self.rows

    def empty_at(self, cell: Vec2) -> bool:
        return self._grid[cell.y][cell.x] is None

    def can_place(self, piece: Tetromino, pos: Vec2 | None = None, rot: int | None = None) -> bool:
        for c in piece.cells(pos=pos, rot=rot):
            if not self.inside(c):
                return False
            if not self.empty_at(c):
                return False
        return True

    def lock(self, piece: Tetromino) -> None:
        for c in piece.cells():
            if self.inside(c):
                self._grid[c.y][c.x] = piece.color

    def clear_lines(self) -> int:
        new_grid: List[List[Optional[Color]]] = []
        cleared = 0
        for row in self._grid:
            if all(cell is not None for cell in row):
                cleared += 1
            else:
                new_grid.append(row)
        while len(new_grid) < self.rows:
            new_grid.insert(0, [None for _ in range(self.cols)])
        self._grid = new_grid
        return cleared
