"""Notification payload construction and dispatch helpers."""

from __future__ import annotations

from collections.abc import Iterable

from agentnotifier.core.result import RunResult, WatchResult
from agentnotifier.core.timefmt import format_duration
from agentnotifier.notifier.base import NotificationLevel, Notifier

MAX_TITLE_LENGTH = 120
MAX_BODY_LENGTH = 700


def _truncate(value: str, limit: int) -> str:
    if len(value) <= limit:
        return value
    if limit <= 3:
        return value[:limit]
    return f"{value[: limit - 3]}..."


def build_title(
    *,
    exit_code: int | None,
    tool_name: str | None,
    title_override: str | None,
    default_tool_name: str,
) -> str:
    if title_override:
        return _truncate(title_override, MAX_TITLE_LENGTH)

    if exit_code is None:
        status = "Done"
    else:
        status = "Done" if exit_code == 0 else "Failed"
    label = tool_name or default_tool_name
    return _truncate(f"[{label}] {status}", MAX_TITLE_LENGTH)


def build_body(
    *,
    duration_seconds: float,
    exit_code: int | None,
    output_tail: Iterable[str] | None = None,
) -> str:
    lines: list[str] = [
        f"Duration: {format_duration(duration_seconds)}",
        f"Exit code: {exit_code if exit_code is not None else 'unknown'}",
    ]

    tail = list(output_tail or [])
    if tail:
        lines.append("Tail:")
        lines.extend(tail)

    return _truncate("\n".join(lines), MAX_BODY_LENGTH)


def notifier_run_completion(
    notifier: Notifier,
    result: RunResult,
    *,
    tool_name: str | None,
    title_override: str | None,
    default_tool_name: str,
) -> tuple[str, str, NotificationLevel]:
    title = build_title(
        exit_code=result.exit_code,
        tool_name=tool_name or result.tool_name,
        title_override=title_override,
        default_tool_name=default_tool_name,
    )
    body = build_body(
        duration_seconds=result.duration_seconds,
        exit_code=result.exit_code,
        output_tail=result.output_tail,
    )
    level = NotificationLevel.SUCCESS if result.exit_code == 0 else NotificationLevel.FAILURE
    notifier.notifier(
        title=title,
        message=body,
        level=level,
        metadata={
            "command": result.command,
            "duration_seconds": result.duration_seconds,
            "exit_code": result.exit_code,
        },
    )
    return title, body, level


def notifier_watch_completion(
    notifier: Notifier,
    result: WatchResult,
    *,
    tool_name: str | None,
    title_override: str | None,
    default_tool_name: str,
) -> tuple[str, str, NotificationLevel]:
    title = build_title(
        exit_code=result.exit_code,
        tool_name=tool_name,
        title_override=title_override,
        default_tool_name=default_tool_name,
    )
    body = build_body(
        duration_seconds=result.duration_seconds,
        exit_code=result.exit_code,
        output_tail=[f"PID: {result.pid}", f"Already exited: {result.already_exited}"],
    )
    level = NotificationLevel.INFO
    if result.exit_code is not None:
        level = NotificationLevel.SUCCESS if result.exit_code == 0 else NotificationLevel.FAILURE

    notifier.notifier(
        title=title,
        message=body,
        level=level,
        metadata={
            "pid": result.pid,
            "duration_seconds": result.duration_seconds,
            "exit_code": result.exit_code,
            "already_exited": result.already_exited,
        },
    )
    return title, body, level
