from __future__ import annotations
import random
from typing import Dict, List, Tuple

from tetris.core.vec2 import Vec2

PIECE_DEFS: Dict[str, List[List[Vec2]]] = {
    "I": [
        [Vec2(-1, 0), Vec2(0, 0), Vec2(1, 0), Vec2(2, 0)],
        [Vec2(1, -1), Vec2(1, 0), Vec2(1, 1), Vec2(1, 2)],
        [Vec2(-1, 1), Vec2(0, 1), Vec2(1, 1), Vec2(2, 1)],
        [Vec2(0, -1), Vec2(0, 0), Vec2(0, 1), Vec2(0, 2)],
    ],
    "O": [
        [Vec2(0, 0), Vec2(1, 0), Vec2(0, 1), Vec2(1, 1)],
        [Vec2(0, 0), Vec2(1, 0), Vec2(0, 1), Vec2(1, 1)],
        [Vec2(0, 0), Vec2(1, 0), Vec2(0, 1), Vec2(1, 1)],
        [Vec2(0, 0), Vec2(1, 0), Vec2(0, 1), Vec2(1, 1)],
    ],
    "T": [
        [Vec2(-1, 0), Vec2(0, 0), Vec2(1, 0), Vec2(0, 1)],
        [Vec2(0, -1), Vec2(0, 0), Vec2(0, 1), Vec2(1, 0)],
        [Vec2(-1, 0), Vec2(0, 0), Vec2(1, 0), Vec2(0, -1)],
        [Vec2(0, -1), Vec2(0, 0), Vec2(0, 1), Vec2(-1, 0)],
    ],
    "S": [
        [Vec2(0, 0), Vec2(1, 0), Vec2(-1, 1), Vec2(0, 1)],
        [Vec2(0, -1), Vec2(0, 0), Vec2(1, 0), Vec2(1, 1)],
        [Vec2(0, 0), Vec2(1, 0), Vec2(-1, 1), Vec2(0, 1)],
        [Vec2(0, -1), Vec2(0, 0), Vec2(1, 0), Vec2(1, 1)],
    ],
    "Z": [
        [Vec2(-1, 0), Vec2(0, 0), Vec2(0, 1), Vec2(1, 1)],
        [Vec2(1, -1), Vec2(0, 0), Vec2(1, 0), Vec2(0, 1)],
        [Vec2(-1, 0), Vec2(0, 0), Vec2(0, 1), Vec2(1, 1)],
        [Vec2(1, -1), Vec2(0, 0), Vec2(1, 0), Vec2(0, 1)],
    ],
    "J": [
        [Vec2(-1, 0), Vec2(0, 0), Vec2(1, 0), Vec2(-1, 1)],
        [Vec2(0, -1), Vec2(0, 0), Vec2(0, 1), Vec2(1, 1)],
        [Vec2(-1, 0), Vec2(0, 0), Vec2(1, 0), Vec2(1, -1)],
        [Vec2(0, -1), Vec2(0, 0), Vec2(0, 1), Vec2(-1, -1)],
    ],
    "L": [
        [Vec2(-1, 0), Vec2(0, 0), Vec2(1, 0), Vec2(1, 1)],
        [Vec2(0, -1), Vec2(0, 0), Vec2(0, 1), Vec2(1, -1)],
        [Vec2(-1, 0), Vec2(0, 0), Vec2(1, 0), Vec2(-1, -1)],
        [Vec2(0, -1), Vec2(0, 0), Vec2(0, 1), Vec2(-1, 1)],
    ],
}

PIECE_COLORS: Dict[str, Tuple[int, int, int]] = {
    "I": (0, 255, 255),
    "O": (255, 255, 0),
    "T": (160, 0, 240),
    "S": (0, 255, 0),
    "Z": (255, 0, 0),
    "J": (0, 0, 255),
    "L": (255, 140, 0),
}

ALL_KINDS = list(PIECE_DEFS.keys())

def random_bag(rng: random.Random) -> List[str]:
    """7-bag: Shuffle IOTSZJL and return them in order."""
    bag = ALL_KINDS[:]
    rng.shuffle(bag)
    return bag
