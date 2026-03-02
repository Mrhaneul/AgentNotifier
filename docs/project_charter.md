# Project Charter

Date: 2026-02-20

## Purpose

Build and maintain `agent-notifier`, an open-source, cross-platform CLI utility that notifies users when long-running agentic workflows complete.

Primary targets:

- Codex app/CLI
- Claude Code app/CLI
- Gemini CLI
- Antigravity
- Any other process-based developer tool

## Product Goals

- Reliable completion notifications for wrapped and watched processes
- Strong cross-platform behavior (macOS, Windows, Linux)
- Secure command execution model (argument lists, no shell-string injection path by default)
- Clear documentation and contributor onboarding
- Proven correctness with automated tests and CI

## Current Stage

As of 2026-02-20, this repository is in **alpha hardening / open-source release-prep stage**:

- Package version: `0.1.1`
- Classifier: `Development Status :: 3 - Alpha`
- Core features implemented: `run`, `watch`, `test-notifier`, optional `tail`
- CI workflow present for macOS + Windows (Linux CI pending)

## Scope Boundary

In scope:

- Command wrapping (`run`)
- Existing PID attach/wait (`watch`)
- Platform desktop notification backends with fallback behavior
- Config via env vars and optional TOML
- Test coverage for core + integration behavior

Out of scope (current release):

- System tray support
- Advanced anti-spam/cooldown policies
- Rich remote channels (webhook/Slack) as production-default

## Definition of Done

Feature work is done when all are true:

1. Behavior is implemented and documented.
2. Unit/integration tests cover success and failure paths.
3. CI/lint/test checks pass in supported environments.
4. User-facing docs include examples and edge cases.
5. Changelog entry is added.

## Change Control

When product direction changes, update:

1. `docs/project_charter.md` (goal/scope change)
2. `docs/assumptions.md` (new assumptions and date)
3. `docs/commit_plan.md` (execution sequence)
4. `README.md` (user-facing behavior changes)

## Near-Term Priorities

1. Stabilize local test/developer setup parity with CI.
2. Harden Linux desktop notifier behavior in real desktop and headless sessions.
3. Prioritize one roadmap feature for next minor release (`0.2.x`).
