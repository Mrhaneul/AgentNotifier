"""Process metadata helpers."""

from __future__ import annotations

import platform
import subprocess


def get_process_name(pid: int) -> str | None:
    """Best-effort process name lookup for a PID."""

    if pid <= 0:
        return None

    system = platform.system()
    if system == "Windows":
        return _get_process_name_windows(pid)
    return _get_process_name_posix(pid)


def _get_process_name_posix(pid: int) -> str | None:
    try:
        completed = subprocess.run(
            ["ps", "-p", str(pid), "-o", "comm="],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None

    if completed.returncode != 0:
        return None
    name = completed.stdout.strip()
    return name or None


def _get_process_name_windows(pid: int) -> str | None:
    script = f"$p=Get-Process -Id {pid} -ErrorAction SilentlyContinue; if ($p) {{$p.ProcessName}}"
    try:
        completed = subprocess.run(
            ["powershell", "-NoProfile", "-Command", script],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None

    if completed.returncode != 0:
        return None
    name = completed.stdout.strip()
    return name or None
