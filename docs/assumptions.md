# Assumptions

Date: 2026-02-20

1. `agent-notifier run` accepts commands as argument lists after `--` and does not accept a single shell string. This avoids shell-injection ambiguity and matches the security requirement.
2. In `watch --pid` mode, exit codes are only guaranteed when the watched PID is a child process that can be reaped (for example in tests on POSIX). For arbitrary existing PIDs, exit code may be unavailable and is reported as `unknown`.
3. Default channel is `desktop` with automatic fallback to console when the desktop backend is unavailable.
4. Windows desktop notifications use BurntToast when installed; fallback is optional `win10toast`.
5. Linux desktop notifications use `notify-send` when available, with console fallback when unavailable.
6. CLI implementation uses Click (instead of Typer) to satisfy the Typer-or-Click requirement while keeping dependencies minimal and broadly available.
7. Tool names are auto-detected when `--name` is not provided: `run` uses the wrapped command and `watch` uses best-effort PID process-name lookup.
8. Process-exit shell integration is intentionally not part of this project direction; the focus is task-level notifications via tool-native hooks.
9. Team process defaults to Scrum-style cadence for execution tracking: daily standups on weekdays, weekly refinement, and biweekly planning/review-retro.
10. Standup default start time is assumed to be 09:00 local timezone unless explicitly changed.
11. Direction changes are captured by updating `docs/project_charter.md`, `docs/assumptions.md`, and `docs/commit_plan.md` together to prevent drift.
12. Task-level notifications for interactive sessions are implemented through tool-native hooks where available: Gemini (`AfterAgent`), Claude (`Stop`/`SubagentStop`), and Codex (`notifier` -> `agent-turn-complete` payload).
13. `--quiet-when-focused` currently detects focus on macOS by checking the frontmost application via `osascript`; other platforms default to notifiering.
14. `--chime ping` uses native best-effort sound playback (macOS `afplay`, Windows PowerShell beep, terminal bell fallback).
15. Pure interactive `ollama run` currently has no native task-finished hook; `ollama-hook` support assumes JSON/JSONL output (`--format json`) or upstream integration through Codex/Claude launchers.
16. Project repository is hosted at `https://github.com/Kipung/AgentNotifier`; package metadata URLs reference this repository.
