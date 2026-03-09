from __future__ import annotations


class MetricsRegistry:
    def __init__(self) -> None:
        self.request_count = 0

    def increment(self) -> None:
        self.request_count += 1
