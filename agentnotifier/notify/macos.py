"""macOS Notification Center notifier backend."""

from __future__ import annotations

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


class MacOSNotifier(Notifier):
    """Send notifications through terminal-notifier or osascript on macOS."""

    def __init__(self, runner: RunCallable = subprocess.run) -> None:
        self._runner = runner

    def notifier(
        self,
        title: str,
        message: str,
        level: NotificationLevel = NotificationLevel.INFO,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        del level, metadata
        errors: list[str] = []

        terminal_notifier = shutil.which("terminal-notifier")
        if terminal_notifier is not None:
            try:
                self._run_terminal_notifier(
                    executable=terminal_notifier,
                    title=title,
                    message=message,
                )
                return
            except NotificationError as exc:
                errors.append(str(exc))

        if shutil.which("osascript") is not None:
            script = (
                f'display notification "{_escape_applescript(message)}" '
                f'with title "{_escape_applescript(title)}"'
            )
            try:
                self._run_osascript(script)
                return
            except NotificationError as exc:
                errors.append(str(exc))

        if errors:
            raise NotificationError("; ".join(errors))
        raise NotifierUnavailable("neither terminal-notifier nor osascript is available")

    def _run_terminal_notifier(self, *, executable: str, title: str, message: str) -> None:
        completed = self._runner(
            [executable, "-title", title, "-message", message],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            stderr = completed.stderr.strip()
            raise NotificationError(
                f"terminal-notifier failed with code {completed.returncode}: {stderr}"
            )

    def _run_osascript(self, script: str) -> None:
        completed = self._runner(
            ["osascript", "-e", script],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            stderr = completed.stderr.strip()
            raise NotificationError(f"osascript failed with code {completed.returncode}: {stderr}")


def _escape_applescript(value: str) -> str:
    escaped = value.replace("\\", "\\\\")
    escaped = escaped.replace('"', '\\"')
    return escaped
