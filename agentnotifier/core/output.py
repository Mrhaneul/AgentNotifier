"""Output capture helpers."""

from __future__ import annotations

from collections import deque


class OutputRingBuffer:
    """Stores the last N output lines from a process."""

    def __init__(self, max_lines: int) -> None:
        if max_lines <= 0:
            raise ValueError("max_lines must be positive")
        self._lines: deque[str] = deque(maxlen=max_lines)

    def add_line(self, line: str) -> None:
        self._lines.append(line.rstrip("\n"))

    def tail(self) -> list[str]:
        return list(self._lines)
