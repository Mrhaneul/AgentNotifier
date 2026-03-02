"""Small bridge entrypoints for external hook integrations."""

from __future__ import annotations

import sys

from agentnotifier.cli import app


def _run_bridge(*, command: str, name: str, prog_name: str) -> None:
    """Dispatch a hook bridge command with consistent defaults."""
    app.main(
        args=[
            command,
            "--name",
            name,
            "--channel",
            "both",
            "--chime",
            "ping",
            *sys.argv[1:],
        ],
        prog_name=prog_name,
    )


def codex_hook_main() -> None:
    """Codex hook bridge with sensible defaults for end users."""
    _run_bridge(
        command="codex-hook",
        name="codex",
        prog_name="agent-notifier-codex-hook",
    )


def gemini_hook_main() -> None:
    """Gemini hook bridge with sensible defaults for end users."""
    _run_bridge(
        command="gemini-hook",
        name="gemini",
        prog_name="agent-notifier-gemini-hook",
    )


def claude_hook_main() -> None:
    """Claude hook bridge with sensible defaults for end users."""
    _run_bridge(
        command="claude-hook",
        name="claude-code",
        prog_name="agent-notifier-claude-hook",
    )
