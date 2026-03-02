"""PID watcher implementation."""

from __future__ import annotations

import os
import platform
import subprocess
import time
from datetime import datetime, timezone

from agentnotifier.core.result import WatchResult


def pid_exists(pid: int) -> bool:
    """Return True if a process with ``pid`` appears to exist."""

    if pid <= 0:
        return False

    if platform.system() == "Windows":
        return _pid_exists_windows(pid)

    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError as exc:
        # Windows uses winerror 87 for invalid PID.
        if platform.system() == "Windows" and getattr(exc, "winerror", None) == 87:
            return False
        return False
    return True


def _pid_exists_windows(pid: int) -> bool:
    script = (
        f"$p=Get-Process -Id {pid} -ErrorAction SilentlyContinue; "
        "if ($p) { exit 0 } else { exit 1 }"
    )
    try:
        completed = subprocess.run(
            ["powershell", "-NoProfile", "-Command", script],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return False
    return completed.returncode == 0


class ProcessWatcher:
    """Waits for an existing PID to exit."""

    def __init__(self, poll_interval: float = 1.0, max_interval: float = 5.0, backoff: float = 1.2):
        if poll_interval <= 0:
            raise ValueError("poll_interval must be > 0")
        self.poll_interval = poll_interval
        self.max_interval = max_interval
        self.backoff = backoff

    def wait_for_exit(self, pid: int) -> WatchResult:
        if pid <= 0:
            raise ValueError("pid must be positive")

        started_at = datetime.now(timezone.utc)
        started_monotonic = time.monotonic()

        if not pid_exists(pid):
            now = datetime.now(timezone.utc)
            return WatchResult(
                pid=pid,
                duration_seconds=0.0,
                exit_code=None,
                started_at=started_at,
                ended_at=now,
                already_exited=True,
            )

        interval = self.poll_interval
        can_waitpid = platform.system() != "Windows"

        while True:
            if can_waitpid:
                try:
                    waited_pid, status = os.waitpid(pid, os.WNOHANG)
                except ChildProcessError:
                    can_waitpid = False
                except OSError:
                    can_waitpid = False
                else:
                    if waited_pid == pid:
                        exit_code = os.waitstatus_to_exitcode(status)
                        now = datetime.now(timezone.utc)
                        return WatchResult(
                            pid=pid,
                            duration_seconds=time.monotonic() - started_monotonic,
                            exit_code=exit_code,
                            started_at=started_at,
                            ended_at=now,
                            already_exited=False,
                        )

            if not pid_exists(pid):
                now = datetime.now(timezone.utc)
                return WatchResult(
                    pid=pid,
                    duration_seconds=time.monotonic() - started_monotonic,
                    exit_code=None,
                    started_at=started_at,
                    ended_at=now,
                    already_exited=False,
                )

            time.sleep(interval)
            interval = min(self.max_interval, interval * self.backoff)
