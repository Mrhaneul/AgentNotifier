"""Wrapped command runner."""

from __future__ import annotations

import subprocess
import sys
import time
from collections.abc import Sequence
from datetime import datetime, timezone

from agentnotifier.core.output import OutputRingBuffer
from agentnotifier.core.result import RunResult


class ProcessRunner:
    """Runs a process and returns structured execution metadata."""

    def run(
        self,
        command: Sequence[str],
        *,
        tool_name: str | None = None,
        capture_output: bool = True,
        tail_lines: int = 20,
    ) -> RunResult:
        command_list = [str(part) for part in command]
        if not command_list:
            raise ValueError("command must not be empty")

        started_at = datetime.now(timezone.utc)
        started_monotonic = time.monotonic()
        ring = OutputRingBuffer(max_lines=max(1, tail_lines))

        if capture_output:
            process = subprocess.Popen(
                command_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            assert process.stdout is not None

            try:
                for line in process.stdout:
                    sys.stdout.write(line)
                    sys.stdout.flush()
                    ring.add_line(line)
            except KeyboardInterrupt:
                process.terminate()
                process.wait(timeout=5)
                raise
            finally:
                process.stdout.close()

            exit_code = process.wait()
            output_tail = ring.tail()
        else:
            completed = subprocess.run(command_list, check=False)
            exit_code = completed.returncode
            output_tail = []

        ended_at = datetime.now(timezone.utc)
        duration_seconds = time.monotonic() - started_monotonic

        return RunResult(
            command=command_list,
            exit_code=exit_code,
            duration_seconds=duration_seconds,
            output_tail=output_tail,
            started_at=started_at,
            ended_at=ended_at,
            tool_name=tool_name,
        )
