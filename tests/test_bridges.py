from __future__ import annotations

from collections.abc import Callable
from typing import Any

from agentnotifier.bridges import claude_hook_main, codex_hook_main, gemini_hook_main


def _capture_bridge_invocation(
    monkeypatch: Any,  # noqa: ANN401
    argv: list[str],
    bridge_main: Callable[[], None],
) -> dict[str, object]:
    captured: dict[str, object] = {}

    def fake_main(*, args, prog_name):  # type: ignore[no-untyped-def]
        captured["args"] = args
        captured["prog_name"] = prog_name

    monkeypatch.setattr("agentnotifier.bridges.app.main", fake_main)
    monkeypatch.setattr("agentnotifier.bridges.sys.argv", argv)

    bridge_main()
    return captured


def test_codex_hook_main_passes_expected_default_args(monkeypatch) -> None:  # noqa: ANN001
    captured = _capture_bridge_invocation(
        monkeypatch,
        ["agent-notifier-codex-hook", "type=agent-turn-complete", "turn-id=t-1"],
        codex_hook_main,
    )

    assert captured["prog_name"] == "agent-notifier-codex-hook"
    assert captured["args"] == [
        "codex-hook",
        "--name",
        "codex",
        "--channel",
        "both",
        "--chime",
        "ping",
        "type=agent-turn-complete",
        "turn-id=t-1",
    ]


def test_gemini_hook_main_passes_expected_default_args(monkeypatch) -> None:  # noqa: ANN001
    captured = _capture_bridge_invocation(
        monkeypatch,
        ["agent-notifier-gemini-hook", "--max-prompt-chars", "200"],
        gemini_hook_main,
    )

    assert captured["prog_name"] == "agent-notifier-gemini-hook"
    assert captured["args"] == [
        "gemini-hook",
        "--name",
        "gemini",
        "--channel",
        "both",
        "--chime",
        "ping",
        "--max-prompt-chars",
        "200",
    ]


def test_claude_hook_main_passes_expected_default_args(monkeypatch) -> None:  # noqa: ANN001
    captured = _capture_bridge_invocation(
        monkeypatch,
        ["agent-notifier-claude-hook", "--event", "SubagentStop"],
        claude_hook_main,
    )

    assert captured["prog_name"] == "agent-notifier-claude-hook"
    assert captured["args"] == [
        "claude-hook",
        "--name",
        "claude-code",
        "--channel",
        "both",
        "--chime",
        "ping",
        "--event",
        "SubagentStop",
    ]
