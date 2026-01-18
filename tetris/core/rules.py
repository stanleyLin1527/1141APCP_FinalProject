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
    檢測是否為 T-spin
    返回: (is_tspin, is_mini)
    
    T-spin 條件:
    1. 方塊必須是 T 型
    2. 最後一個動作必須是旋轉
    3. 檢查 T 方塊的四個角落位置
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
    
    # T-spin: 至少3個角落被佔據
    if filled_corners >= 3:
        # 檢查是否為 mini T-spin
        # 根據旋轉方向和角落檢查判斷
        rot = piece.rot
        
        # 檢查關鍵的兩個前角
        if rot == 0:  # T 朝上
            front_corners = [corners[0], corners[1]]  # 上方兩個角
        elif rot == 1:  # T 朝右
            front_corners = [corners[1], corners[3]]  # 右方兩個角
        elif rot == 2:  # T 朝下
            front_corners = [corners[2], corners[3]]  # 下方兩個角
        else:  # rot == 3, T 朝左
            front_corners = [corners[0], corners[2]]  # 左方兩個角
        
        # 檢查前角是否都被填充
        front_filled = sum(1 for c in front_corners if not board.inside(c) or not board.empty_at(c))
        
        is_mini = front_filled < 2
        return True, is_mini
    
    return False, False
