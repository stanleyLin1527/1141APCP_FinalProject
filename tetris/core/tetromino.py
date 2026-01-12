from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

from tetris.core.vec2 import Vec2
from tetris.core.pieces import PIECE_DEFS, PIECE_COLORS

@dataclass
class Tetromino:
    kind: str
    pos: Vec2
    rot: int = 0  # 0..3

    @property
    def color(self) -> Tuple[int, int, int]:
        return PIECE_COLORS[self.kind]

    def cells(self, pos: Vec2 | None = None, rot: int | None = None) -> List[Vec2]:
        p = self.pos if pos is None else pos
        r = self.rot if rot is None else (rot % 4)
        offsets = PIECE_DEFS[self.kind][r]
        return [p + (o.x, o.y) for o in offsets]

    def rotated(self, dir: int) -> int:
        return (self.rot + dir) % 4
