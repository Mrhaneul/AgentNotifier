"""Linux desktop notification backend."""

from __future__ import annotations

import platform
import shutil
import subprocess
from collections.abc import Callable, Mapping
from typing import Any

from agentnotifier.notifier.base import (
    NotificationError,
    NotificationLevel,
    Notifier,
    NotifierUnavailable,
)

RunCallable = Callable[..., subprocess.CompletedProcess[str]]


class LinuxNotifier(Notifier):
    """Send notifications via `notify-send` on Linux."""

    def __init__(self, runner: RunCallable = subprocess.run) -> None:
        self._runner = runner

    def notifier(
        self,
        title: str,
        message: str,
        level: NotificationLevel = NotificationLevel.INFO,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        del metadata
        if platform.system() != "Linux":
            raise NotifierUnavailable("Linux notifier is only available on Linux")

        executable = shutil.which("notify-send")
        if executable is None:
            raise NotifierUnavailable("notify-send is not available on this system")

        urgency = _urgency_for_level(level)
        completed = self._runner(
            [
                executable,
                "--app-name=agent-notifier",
                f"--urgency={urgency}",
                "--expire-time=5000",
                title,
                message,
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            stderr = completed.stderr.strip()
            raise NotificationError(
                f"notify-send failed with code {completed.returncode}: {stderr}"
            )


def _urgency_for_level(level: NotificationLevel) -> str:
    if level == NotificationLevel.FAILURE:
        return "critical"
    if level == NotificationLevel.SUCCESS:
        return "normal"
    return "low"

