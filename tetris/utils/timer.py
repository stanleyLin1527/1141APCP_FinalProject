from __future__ import annotations

class DropTimer:
    """用毫秒計時的簡易計時器，用於控制自動下落節奏。"""
    def __init__(self, interval_ms: int):
        self.interval_ms = max(1, int(interval_ms))
        self.acc_ms = 0

    def set_interval(self, interval_ms: int) -> None:
        self.interval_ms = max(100, int(interval_ms))

    def tick(self, dt_ms: int) -> bool:
        """累積 dt_ms；若達到 interval 回傳 True（應下落一次）。"""
        self.acc_ms += int(dt_ms)
        if self.acc_ms >= self.interval_ms:
            self.acc_ms %= self.interval_ms
            return True
        return False
