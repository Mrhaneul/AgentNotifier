"""Windows toast notifier backend."""

from __future__ import annotations

import importlib
import platform
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


class WindowsNotifier(Notifier):
    """Send notifications on Windows via PowerShell + BurntToast, then win10toast fallback."""

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
        if platform.system() != "Windows":
            raise NotifierUnavailable("Windows notifier is only available on Windows")

        if self._notifier_with_powershell(title, message):
            return
        if self._notifier_with_win10toast(title, message):
            return

        raise NotifierUnavailable(
            "No Windows desktop notification backend available. "
            "Install BurntToast PowerShell module or win10toast Python package."
        )

    def _notifier_with_powershell(self, title: str, message: str) -> bool:
        ps_title = _escape_powershell_single_quoted(title)
        ps_message = _escape_powershell_single_quoted(message)

        script = "\n".join(
            [
                "$ErrorActionPreference = 'Stop'",
                "if (Get-Module -ListAvailable -Name BurntToast) {",
                "  Import-Module BurntToast | Out-Null",
                f"  New-BurntToastNotification -Text @('{ps_title}', '{ps_message}') | Out-Null",
                "  exit 0",
                "}",
                "exit 2",
            ]
        )

        try:
            completed = self._runner(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-Command",
                    script,
                ],
                check=False,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError:
            return False

        if completed.returncode == 0:
            return True
        if completed.returncode == 2:
            return False

        error_text = completed.stderr.strip()
        raise NotificationError(
            f"PowerShell notifier failed with code {completed.returncode}: {error_text}"
        )

    @staticmethod
    def _notifier_with_win10toast(title: str, message: str) -> bool:
        try:
            module = importlib.import_module("win10toast")
        except ImportError:
            return False

        try:
            toaster = module.ToastNotifier()
            toaster.show_toast(title, message, duration=5, threaded=False)
        except Exception:
            return False
        return True


def _escape_powershell_single_quoted(value: str) -> str:
    return value.replace("'", "''")
