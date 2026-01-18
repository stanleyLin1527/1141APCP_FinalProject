from __future__ import annotations
from dataclasses import dataclass
from typing import Iterator, Tuple, Union

NumberPair = Union[Tuple[int, int], "Vec2"]

@dataclass(frozen=True, slots=True)
class Vec2:
    x: int
    y: int

    # Operator overloading: coordinate addition/subtraction
    def __add__(self, other: NumberPair) -> "Vec2":
        ox, oy = other if isinstance(other, tuple) else (other.x, other.y)
        return Vec2(self.x + int(ox), self.y + int(oy))

    def __sub__(self, other: NumberPair) -> "Vec2":
        ox, oy = other if isinstance(other, tuple) else (other.x, other.y)
        return Vec2(self.x - int(ox), self.y - int(oy))

    def __iter__(self) -> Iterator[int]:
        # Allows you to write: x, y = vec
        yield self.x
        yield self.y
