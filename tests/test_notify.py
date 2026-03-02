from __future__ import annotations

import subprocess
from types import SimpleNamespace
from typing import Any

import pytest

from agentnotifier.notifier.base import (
    CompositeNotifier,
    NotificationError,
    NotificationLevel,
    Notifier,
    NotifierUnavailable,
)
from agentnotifier.notifier.linux import LinuxNotifier
from agentnotifier.notifier.macos import MacOSNotifier
from agentnotifier.notifier.windows import WindowsNotifier


def _completed(*, returncode: int, stderr: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=["cmd"],
        returncode=returncode,
        stdout="",
        stderr=stderr,
    )


def test_macos_notifier_prefers_terminal_notifier(monkeypatch) -> None:  # noqa: ANN001
    calls: list[list[str]] = []

    def fake_which(name: str) -> str | None:
        mapping = {
            "terminal-notifier": "/opt/homebrew/bin/terminal-notifier",
            "osascript": "/usr/bin/osascript",
        }
        return mapping.get(name)

    def fake_runner(args: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        del kwargs
        calls.append(args)
        return _completed(returncode=0)

    monkeypatch.setattr("agentnotifier.notifier.macos.shutil.which", fake_which)
    notifier = MacOSNotifier(runner=fake_runner)
    notifier.notifier("Title", "Message", NotificationLevel.INFO)
    assert calls == [[
        "/opt/homebrew/bin/terminal-notifier",
        "-title",
        "Title",
        "-message",
        "Message",
    ]]


def test_macos_notifier_falls_back_to_osascript(monkeypatch) -> None:  # noqa: ANN001
    calls: list[list[str]] = []

    def fake_which(name: str) -> str | None:
        mapping = {
            "terminal-notifier": "/opt/homebrew/bin/terminal-notifier",
            "osascript": "/usr/bin/osascript",
        }
        return mapping.get(name)

    def fake_runner(args: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        del kwargs
        calls.append(args)
        if args[0].endswith("terminal-notifier"):
            return _completed(returncode=1, stderr="tn failed")
        return _completed(returncode=0)

    monkeypatch.setattr("agentnotifier.notifier.macos.shutil.which", fake_which)
    notifier = MacOSNotifier(runner=fake_runner)
    notifier.notifier("Title", "Message", NotificationLevel.INFO)
    assert len(calls) == 2
    assert calls[0][0].endswith("terminal-notifier")
    assert calls[1][0] == "osascript"


def test_macos_osascript_fallback_flattens_newlines(monkeypatch) -> None:  # noqa: ANN001
    calls: list[list[str]] = []

    def fake_which(name: str) -> str | None:
        mapping = {
            "terminal-notifier": "/opt/homebrew/bin/terminal-notifier",
            "osascript": "/usr/bin/osascript",
        }
        return mapping.get(name)

    def fake_runner(args: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        del kwargs
        calls.append(args)
        if args[0].endswith("terminal-notifier"):
            return _completed(returncode=1, stderr="tn failed")
        return _completed(returncode=0)

    monkeypatch.setattr("agentnotifier.notifier.macos.shutil.which", fake_which)
    notifier = MacOSNotifier(runner=fake_runner)
    notifier.notifier("Title", "line1\nline2", NotificationLevel.INFO)

    assert len(calls) == 2
    assert calls[1][0] == "osascript"
    assert "line1 line2" in calls[1][2]
    assert "\n" not in calls[1][2]


def test_macos_notifier_requires_backend(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setattr("agentnotifier.notifier.macos.shutil.which", lambda _: None)
    notifier = MacOSNotifier()
    with pytest.raises(NotifierUnavailable):
        notifier.notifier("Title", "Message")


def test_windows_notifier_rejects_non_windows(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setattr("agentnotifier.notifier.windows.platform.system", lambda: "Darwin")
    notifier = WindowsNotifier()
    with pytest.raises(NotifierUnavailable):
        notifier.notifier("Title", "Message")


def test_windows_notifier_uses_powershell(monkeypatch) -> None:  # noqa: ANN001
    calls: list[list[str]] = []

    def fake_runner(args: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        del kwargs
        calls.append(args)
        return _completed(returncode=0)

    monkeypatch.setattr("agentnotifier.notifier.windows.platform.system", lambda: "Windows")
    notifier = WindowsNotifier(runner=fake_runner)
    notifier.notifier("Title", "Message")
    assert calls
    assert calls[0][0] == "powershell"


def test_windows_notifier_uses_win10toast_fallback(monkeypatch) -> None:  # noqa: ANN001
    def fake_runner(args: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        del args, kwargs
        return _completed(returncode=2)

    fake_module = SimpleNamespace(
        ToastNotifier=lambda: SimpleNamespace(show_toast=lambda *args, **kwargs: None)
    )

    monkeypatch.setattr("agentnotifier.notifier.windows.platform.system", lambda: "Windows")
    monkeypatch.setattr(
        "agentnotifier.notifier.windows.importlib.import_module",
        lambda _: fake_module,
    )
    notifier = WindowsNotifier(runner=fake_runner)
    notifier.notifier("Title", "Message")


def test_linux_notifier_uses_notify_send(monkeypatch) -> None:  # noqa: ANN001
    calls: list[list[str]] = []

    def fake_runner(args: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        del kwargs
        calls.append(args)
        return _completed(returncode=0)

    monkeypatch.setattr("agentnotifier.notifier.linux.platform.system", lambda: "Linux")
    monkeypatch.setattr(
        "agentnotifier.notifier.linux.shutil.which",
        lambda name: "/usr/bin/notify-send" if name == "notify-send" else None,
    )
    notifier = LinuxNotifier(runner=fake_runner)
    notifier.notifier("Title", "Message", NotificationLevel.FAILURE)

    assert calls == [[
        "/usr/bin/notify-send",
        "--app-name=agent-notifier",
        "--urgency=critical",
        "--expire-time=5000",
        "Title",
        "Message",
    ]]


def test_linux_notifier_requires_linux(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setattr("agentnotifier.notifier.linux.platform.system", lambda: "Darwin")
    notifier = LinuxNotifier()
    with pytest.raises(NotifierUnavailable):
        notifier.notifier("Title", "Message")


def test_linux_notifier_requires_notify_send(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setattr("agentnotifier.notifier.linux.platform.system", lambda: "Linux")
    monkeypatch.setattr("agentnotifier.notifier.linux.shutil.which", lambda _: None)
    notifier = LinuxNotifier()
    with pytest.raises(NotifierUnavailable):
        notifier.notifier("Title", "Message")


def test_composite_notifier_raises_when_all_children_fail() -> None:
    class FailingNotifier(Notifier):
        def notifier(  # type: ignore[override]
            self,
            title: str,
            message: str,
            level: NotificationLevel = NotificationLevel.INFO,
            metadata: dict[str, object] | None = None,
        ) -> None:
            del title, message, level, metadata
            raise NotificationError("no backend")

    notifier = CompositeNotifier([FailingNotifier(), FailingNotifier()])
    with pytest.raises(NotificationError):
        notifier.notifier("Title", "Message")
