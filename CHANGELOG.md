# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

- Linux desktop notification backend using `notify-send` with console fallback when unavailable.
- Cross-platform notifier backend tests for macOS, Windows, and Linux code paths.
- New packaged Codex bridge entrypoint: `agent-notifier-codex-hook`.
- New packaged Gemini and Claude bridge entrypoints:
  - `agent-notifier-gemini-hook`
  - `agent-notifier-claude-hook`
- New macOS bootstrap helper: `examples/setup_macos.sh` to automate local install, Codex/Gemini hook wiring, and Gemini trust setup.

### Changed

- Removed `shell-init` process-exit notification mode from the CLI.
- Removed shell hook generation internals/tests and aligned project docs to task-level notifications only.
- Updated Windows PID existence checks to avoid signal-based probing during watch mode.
- Gemini hook payload parsing now accepts both snake_case and camelCase keys (`hook_event_name`/`eventName`, etc.).
- macOS desktop backend now tries `terminal-notifier` before `osascript`.
- macOS `osascript` fallback now flattens newline/tab characters for safer payload rendering.
- `--channel both --verbose` now explicitly reports desktop backend failure even when console delivery succeeds.
- Config loader now supports documented `AGENT_NOTIFIER_*` env vars (with compatibility for legacy `AGENT_NOTIFY_*` names).
- README now includes a scenario matrix with verified Codex/macOS/iTerm diagnostics and fix paths.
- README now includes a verified zero-to-working macOS onboarding flow, explicit `terminal-notifier` guidance, and clarified Gemini trust-folder requirements.

## [0.1.1] - 2026-02-20

### Changed

- Reworked README onboarding flow with clearer mode selection, per-tool setup recipes, and troubleshooting guidance.
- Clarified task-level vs shell-exit notification behavior to reduce setup confusion.
- Added `.release-venv/` to `.gitignore` to keep local release environments out of commits.

## [0.1.0] - 2026-02-20

### Added

- Initial release of `agent-notifier`.
- `run` command to wrap long-running commands and notifier on completion.
- `watch` command to monitor an existing PID.
- `test-notifier` command for backend verification.
- Optional `tail` command for log pattern notification.
- macOS notifier using `osascript`.
- Windows notifier using PowerShell/BurntToast with `win10toast` fallback.
- Console and null notifier implementations.
- Unit and integration tests with mocked notifier coverage.
- GitHub Actions CI for macOS + Windows.


## [0.1.2] - 2026-03-02

