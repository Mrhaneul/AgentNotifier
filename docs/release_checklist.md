# Release Checklist

Date: 2026-02-20

Use this checklist for a clean open-source release.

## 1. Repository Readiness

1. Ensure `.gitignore` excludes local artifacts (`.venv`, caches, logs, temp files).
2. Remove local-only files before commit (`.tmp_*`, `.pytest_cache`, `*.egg-info`, `__pycache__`).
3. Verify documentation does not contain machine-specific absolute paths.

## 2. Metadata

1. Update `pyproject.toml`:
   - `version`
   - `description`
   - `[project.urls]` (`Homepage`, `Repository`, `Issues`)
2. Keep `agentnotifier/__init__.py` `__version__` in sync with `pyproject.toml`.
3. Add release notes entry in `CHANGELOG.md`.

## 3. Quality Gates

Run all checks locally:

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest -q
python -m build
```

Optional package verification:

```bash
python -m pip install twine
twine check dist/*
```

## 4. Git + GitHub

Initialize and push (first time):

```bash
git init
git add .
git commit -m "chore: prepare initial open-source release"
git branch -M main
gh repo create <org-or-user>/agent-notifier --public --source=. --remote=origin --push
```

If remote already exists:

```bash
git add .
git commit -m "chore: release prep"
git push origin main
```

## 5. Tag + Release

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```

Create a GitHub release from `vX.Y.Z` and paste notes from `CHANGELOG.md`.

## 6. Post-Release Smoke Test

1. Install in a clean environment: `pipx install agent-notifier` (or from GitHub URL).
2. Run:
   - `agent-notifier test-notifier --channel console`
   - `agent-notifier run -- python -c "import time; time.sleep(1)"`
3. Verify task-level hooks using one of:
   - Gemini `AfterAgent`
   - Claude `Stop`/`SubagentStop`
   - Codex `notify` with `examples/codex_notifier_bridge.sh`
