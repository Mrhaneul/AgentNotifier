# Contributing

Thanks for contributing to `agent-notifier`.

## Setup

```bash
python -m pip install -e ".[dev]"
```

## Local checks

```bash
ruff check .
pytest -q
```

## Pull requests

- Keep changes focused and small.
- Add or update tests for behavior changes.
- Update `CHANGELOG.md` for user-visible changes.
- Ensure CI passes on macOS and Windows.

## Commit style

Use clear, imperative commit messages. See `docs/commit_plan.md` for a suggested sequence.
