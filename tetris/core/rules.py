from __future__ import annotations

def score_for_lines(lines: int, level: int) -> int:
    base = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}.get(lines, 0)
    return base * (level + 1)

def level_for_total_lines(total_lines: int) -> int:
    return total_lines // 10

def drop_interval_ms(level: int) -> int:
    return max(100, 1000 - level * 75)
