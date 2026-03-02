from __future__ import annotations

import platform
import subprocess

import pytest

from agentnotifier.cli import (
    _build_desktop_notifier,
    _infer_tool_name_from_command,
    _infer_tool_name_from_pid,
)
from agentnotifier.core.procinfo import get_process_name
from agentnotifier.notifier.base import NotifierUnavailable
from agentnotifier.notifier.linux import LinuxNotifier
from agentnotifier.notifier.macos import MacOSNotifier
from agentnotifier.notifier.windows import WindowsNotifier


def test_infer_tool_name_from_simple_command() -> None:
    assert _infer_tool_name_from_command(("codex", "run", "task")) == "codex"


def test_infer_tool_name_from_path_and_exe_suffix() -> None:
    assert _infer_tool_name_from_command(("/usr/local/bin/gemini.exe", "--help")) == "gemini"


def test_infer_tool_name_from_python_module() -> None:
    assert _infer_tool_name_from_command(("python3", "-m", "claude_code", "ask")) == "claude_code"


def test_get_process_name_posix(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(  # noqa: ANN002, ANN003
            args=args, returncode=0, stdout="codex\n", stderr=""
        ),
    )
    assert get_process_name(12345) == "codex"


def test_get_process_name_windows(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(  # noqa: ANN002, ANN003
            args=args, returncode=0, stdout="Code\n", stderr=""
        ),
    )
    assert get_process_name(12345) == "Code"


def test_infer_tool_name_from_pid_falls_back_to_pid(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setattr("agentnotifier.cli.get_process_name", lambda pid: None)
    assert _infer_tool_name_from_pid(777) == "pid-777"


def test_build_desktop_notifier_macos(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setattr("agentnotifier.cli.platform.system", lambda: "Darwin")
    assert isinstance(_build_desktop_notifier(), MacOSNotifier)


def test_build_desktop_notifier_windows(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setattr("agentnotifier.cli.platform.system", lambda: "Windows")
    assert isinstance(_build_desktop_notifier(), WindowsNotifier)


def test_build_desktop_notifier_linux(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setattr("agentnotifier.cli.platform.system", lambda: "Linux")
    assert isinstance(_build_desktop_notifier(), LinuxNotifier)


def test_build_desktop_notifier_unsupported_platform(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setattr("agentnotifier.cli.platform.system", lambda: "Plan9")
    with pytest.raises(NotifierUnavailable):
        _build_desktop_notifier()
