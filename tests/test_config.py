from __future__ import annotations

from pathlib import Path

from agentnotifier.config.config import load_config


def test_load_config_prefers_agent_notifier_env_vars(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setenv("AGENT_NOTIFIER_TITLE_PREFIX", "Ship")
    monkeypatch.setenv("AGENT_NOTIFIER_CHANNELS", "desktop,console")
    monkeypatch.setenv("AGENT_NOTIFIER_TAIL_LINES", "33")
    monkeypatch.setenv("AGENT_NOTIFIER_POLL_INTERVAL", "0.25")

    config = load_config(path=Path("/tmp/agentnotifier-missing-config.toml"))

    assert config.title_prefix == "Ship"
    assert config.channels == ["desktop", "console"]
    assert config.tail_lines == 33
    assert config.poll_interval == 0.25


def test_load_config_supports_legacy_agent_notify_env_vars(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setenv("AGENT_NOTIFY_TITLE_PREFIX", "Legacy")
    monkeypatch.setenv("AGENT_NOTIFY_CHANNELS", "console")
    monkeypatch.setenv("AGENT_NOTIFY_TAIL_LINES", "9")
    monkeypatch.setenv("AGENT_NOTIFY_POLL_INTERVAL", "2.5")

    config = load_config(path=Path("/tmp/agentnotifier-missing-config.toml"))

    assert config.title_prefix == "Legacy"
    assert config.channels == ["console"]
    assert config.tail_lines == 9
    assert config.poll_interval == 2.5
