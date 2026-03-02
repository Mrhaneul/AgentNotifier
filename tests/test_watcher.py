from agentnotifier.core.watcher import ProcessWatcher, pid_exists


def test_watcher_symbols_importable() -> None:
    assert callable(pid_exists)
    assert hasattr(ProcessWatcher, "wait_for_exit")
