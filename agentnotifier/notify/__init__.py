"""Notification backends and abstractions."""

from agentnotifier.notifier.base import (
    CompositeNotifier,
    NotificationLevel,
    Notifier,
    NotifierUnavailable,
)
from agentnotifier.notify.linux import LinuxNotifier
from agentnotifier.notify.macos import MacOSNotifier
from agentnotifier.notify.windows import WindowsNotifier

__all__ = [
    "Notifier",
    "NotificationLevel",
    "NotifierUnavailable",
    "CompositeNotifier",
    "LinuxNotifier",
    "MacOSNotifier",
    "WindowsNotifier",
]
