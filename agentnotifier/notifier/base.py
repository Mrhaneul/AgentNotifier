"""Notification interface and common types."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Mapping
from enum import Enum
from typing import Any


class NotificationLevel(str, Enum):
    INFO = "info"
    SUCCESS = "success"
    FAILURE = "failure"


class NotifierUnavailable(RuntimeError):
    """Raised when a notifier backend is unavailable on this machine."""


class NotificationError(RuntimeError):
    """Raised when notification dispatch fails unexpectedly."""


class Notifier(ABC):
    """Interface for all notification channels."""

    @abstractmethod
    def notifier(
        self,
        title: str,
        message: str,
        level: NotificationLevel = NotificationLevel.INFO,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        raise NotImplementedError


class CompositeNotifier(Notifier):
    """Dispatches a notification to multiple notifiers."""

    def __init__(self, notifiers: Iterable[Notifier]):
        self._notifiers = list(notifiers)

    def notifier(
        self,
        title: str,
        message: str,
        level: NotificationLevel = NotificationLevel.INFO,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        errors: list[Exception] = []
        delivered = False
        for notifier in self._notifiers:
            try:
                notifier.notifier(title=title, message=message, level=level, metadata=metadata)
            except Exception as exc:
                errors.append(exc)
            else:
                delivered = True

        if not delivered and errors:
            raise NotificationError(
                "; ".join(str(err) for err in errors if str(err)) or "all notifiers failed"
            )
