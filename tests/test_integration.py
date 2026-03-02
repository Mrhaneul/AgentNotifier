from __future__ import annotations

from agentnotifier.core.notifications import notifier_run_completion, notifier_watch_completion


def test_notification_helpers_importable() -> None:
    assert callable(notifier_run_completion)
    assert callable(notifier_watch_completion)
