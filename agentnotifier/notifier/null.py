"""Null notifier used in tests."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from agentnotifier.notifier.base import NotificationLevel, Notifier


@dataclass(slots=True)
class SentNotification:
    title: str
    message: str
    level: NotificationLevel
    metadata: Mapping[str, Any] | None


class NullNotifier(Notifier):
    """Captures notifications without sending them anywhere."""

    def __init__(self) -> None:
        self.notifications: list[SentNotification] = []

    def notifier(
        self,
        title: str,
        message: str,
        level: NotificationLevel = NotificationLevel.INFO,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        self.notifications.append(
            SentNotification(title=title, message=message, level=level, metadata=metadata)
        )
