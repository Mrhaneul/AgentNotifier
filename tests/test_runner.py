import sys

from agentnotifier.core.runner import ProcessRunner
from agentnotifier.core.timefmt import format_duration


def test_process_runner_success() -> None:
    runner = ProcessRunner()
    result = runner.run(
        [
            sys.executable,
            "-c",
            "import time; print('start', flush=True); time.sleep(0.2); print('done', flush=True)",
        ],
        capture_output=True,
        tail_lines=5,
        tool_name="test-tool",
    )

    assert result.exit_code == 0
    assert result.duration_seconds >= 0.15
    assert result.output_tail[-1] == "done"


def test_process_runner_failure_exit_code() -> None:
    runner = ProcessRunner()
    result = runner.run(
        [
            sys.executable,
            "-c",
            "import sys, time; print('failing', flush=True); time.sleep(0.1); sys.exit(3)",
        ],
        capture_output=True,
        tail_lines=5,
    )

    assert result.exit_code == 3
    assert "failing" in result.output_tail


def test_duration_formatting() -> None:
    assert format_duration(0.25) == "0.25s"
    assert format_duration(5.0) == "5s"
    assert format_duration(61.2) == "1m 1s"
    assert format_duration(3661.0) == "1h 1m 1s"
