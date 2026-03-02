"""Result types for process run and process watch operations."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(slots=True)
class RunResult:
    """Outcome for a wrapped command execution."""

    command: list[str]
    exit_code: int
    duration_seconds: float
    output_tail: list[str] = field(default_factory=list)
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    ended_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    tool_name: str | None = None

    @property
    def succeeded(self) -> bool:
        return self.exit_code == 0


@dataclass(slots=True)
class WatchResult:
    """Outcome for monitoring a PID until it exits."""

    pid: int
    duration_seconds: float
    exit_code: int | None
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    ended_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    already_exited: bool = False

    @property
    def exited(self) -> bool:
        return True

    @property
    def succeeded(self) -> bool | None:
        if self.exit_code is None:
            return None
        return self.exit_code == 0
