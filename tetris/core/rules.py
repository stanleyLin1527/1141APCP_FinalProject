from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tetris.core.board import Board
    from tetris.core.tetromino import Tetromino
    from tetris.core.vec2 import Vec2

def score_for_lines(lines: int, level: int, is_tspin: bool = False, is_tspin_mini: bool = False) -> int:
    """Calculate line clear score, including T-spin bonuses"""
    if is_tspin and not is_tspin_mini:
        # T-Spin bonus
        base = {0: 400, 1: 800, 2: 1200, 3: 1600}.get(lines, 0)
    elif is_tspin_mini:
        # Mini T-Spin bonus
        base = {0: 100, 1: 200, 2: 400}.get(lines, 0)
    else:
        # Normal line clear
        base = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}.get(lines, 0)
    return base * (level + 1)

def level_for_total_lines(total_lines: int) -> int:
    return total_lines // 10

def drop_interval_ms(level: int) -> int:
    return max(100, 1000 - level * 75)

def check_tspin(board: "Board", piece: "Tetromino", last_action_was_rotate: bool) -> tuple[bool, bool]:
    """
    Check if a T-spin occurred.
    Returns: (is_tspin, is_mini)
    
    T-spin conditions:
    1. Piece must be T-type
    2. Last action must be a rotation
    3. Check the four corner positions of T piece
    """
    if piece.kind != "T" or not last_action_was_rotate:
        return False, False
    
    # Four corner positions of T piece (relative to center)
    # Check different corners based on rotation state
    corners = [
        piece.pos + (-1, -1),  # Top-left
        piece.pos + (1, -1),   # Top-right
        piece.pos + (-1, 1),   # Bottom-left
        piece.pos + (1, 1),    # Bottom-right
    ]
    
    # Count how many corners are occupied or out of bounds
    filled_corners = 0
    for corner in corners:
        if not board.inside(corner) or not board.empty_at(corner):
            filled_corners += 1
    
    # T-spin: at least 3 corners are occupied
    if filled_corners >= 3:
        # Check if it's a mini T-spin
        # Determine based on rotation direction and corner checks
        rot = piece.rot
        
        # Check the two key front corners
        if rot == 0:  # T facing up
            front_corners = [corners[0], corners[1]]  # Top two corners
        elif rot == 1:  # T facing right
            front_corners = [corners[1], corners[3]]  # Right two corners
        elif rot == 2:  # T facing down
            front_corners = [corners[2], corners[3]]  # Bottom two corners
        else:  # rot == 3, T facing left
            front_corners = [corners[0], corners[2]]  # Left two corners
        
        # Check if front corners are both filled
        front_filled = sum(1 for c in front_corners if not board.inside(c) or not board.empty_at(c))
        
        is_mini = front_filled < 2
        return True, is_mini
    
    return False, False
