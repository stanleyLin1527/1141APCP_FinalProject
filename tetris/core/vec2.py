from __future__ import annotations
from dataclasses import dataclass
from typing import Iterator, Tuple, Union

NumberPair = Union[Tuple[int, int], "Vec2"]

@dataclass(frozen=True, slots=True)
class Vec2:
    x: int
    y: int

    # 運算子重載：座標加法/減法
    def __add__(self, other: NumberPair) -> "Vec2":
        ox, oy = other if isinstance(other, tuple) else (other.x, other.y)
        return Vec2(self.x + int(ox), self.y + int(oy))

    def __sub__(self, other: NumberPair) -> "Vec2":
        ox, oy = other if isinstance(other, tuple) else (other.x, other.y)
        return Vec2(self.x - int(ox), self.y - int(oy))

    def __iter__(self) -> Iterator[int]:
        # 讓你可以寫：x, y = vec
        yield self.x
        yield self.y
