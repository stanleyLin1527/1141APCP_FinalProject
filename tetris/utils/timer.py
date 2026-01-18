from __future__ import annotations

class DropTimer:
    """Simple timer in milliseconds for controlling automatic drop rhythm."""
    def __init__(self, interval_ms: int):
        self.interval_ms = max(1, int(interval_ms))
        self.acc_ms = 0

    def set_interval(self, interval_ms: int) -> None:
        self.interval_ms = max(100, int(interval_ms))

    def tick(self, dt_ms: int) -> bool:
        """Accumulates dt_ms; returns True when interval is reached (should drop once)."""
        self.acc_ms += int(dt_ms)
        if self.acc_ms >= self.interval_ms:
            self.acc_ms %= self.interval_ms
            return True
        return False
