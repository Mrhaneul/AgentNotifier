"""Notification backends and abstractions."""

from agentnotifier.notifier.base import (
    CompositeNotifier,
    NotificationLevel,
    Notifier,
    NotifierUnavailable,
)
from agentnotifier.notifier.linux import LinuxNotifier
from agentnotifier.notifier.macos import MacOSNotifier
from agentnotifier.notifier.windows import WindowsNotifier

__all__ = [
    "Notifier",
    "NotificationLevel",
    "NotifierUnavailable",
    "CompositeNotifier",
    "LinuxNotifier",
    "MacOSNotifier",
    "WindowsNotifier",
]
