# Suggested Commit Plan

1. `chore: scaffold agent-notifier package and project metadata`
   - Create package layout, `pyproject.toml`, and base modules.
2. `feat(run): implement wrapped command execution with macOS notifications`
   - Add `ProcessRunner`, output capture tail, time formatting, and `run` CLI command.
3. `test(run): add unit and integration coverage for runner and notifications`
   - Add tests for success/failure exit codes, duration formatting, tail behavior, and notifier payload.
4. `feat(watch): add PID watcher mode and notification wiring`
   - Add `ProcessWatcher` and `watch` CLI command.
5. `feat(windows): add Windows desktop notifier and test-notifier command`
   - Add PowerShell/BurntToast implementation with fallback.
6. `docs: add README, OSS governance docs, examples, and changelog`
   - Add usage docs, contributing, code of conduct, license, and release notes.
7. `ci: add macOS and Windows GitHub Actions workflow`
   - Run lint and tests on both platforms.
8. `chore: remove local-path assumptions and temp artifact leakage`
   - Make bridge scripts portable, clean up `.gitignore`, and remove machine-specific docs.
9. `chore(release): add release checklist and tag-build workflow`
   - Add GitHub tag workflow and release runbook for PyPI/GitHub release flow.
