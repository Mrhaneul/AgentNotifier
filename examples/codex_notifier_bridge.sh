#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH='' cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${AGENT_NOTIFIER_PROJECT_ROOT:-$(cd -- "$SCRIPT_DIR/.." && pwd)}"
AGENT_NOTIFIER_CODEX_HOOK_BIN="${AGENT_NOTIFIER_CODEX_HOOK_BIN:-$(command -v agent-notifier-codex-hook || true)}"
AGENT_NOTIFIER_BIN="${AGENT_NOTIFIER_BIN:-$(command -v agent-notifier || true)}"
LOG_TARGET="/dev/null"

if [[ -z "$AGENT_NOTIFIER_CODEX_HOOK_BIN" ]]; then
  for candidate in \
    "$HOME/.local/bin/agent-notifier-codex-hook" \
    "$HOME/miniconda3/bin/agent-notifier-codex-hook" \
    "$HOME/anaconda3/bin/agent-notifier-codex-hook"; do
    if [[ -x "$candidate" ]]; then
      AGENT_NOTIFIER_CODEX_HOOK_BIN="$candidate"
      break
    fi
  done
fi

if [[ -z "$AGENT_NOTIFIER_BIN" ]]; then
  for candidate in \
    "$HOME/.local/bin/agent-notifier" \
    "$HOME/miniconda3/bin/agent-notifier" \
    "$HOME/anaconda3/bin/agent-notifier"; do
    if [[ -x "$candidate" ]]; then
      AGENT_NOTIFIER_BIN="$candidate"
      break
    fi
  done
fi

if [[ -z "${AGENT_NOTIFIER_PYTHON:-}" ]]; then
  if [[ -x "$PROJECT_ROOT/.venv/bin/python" ]]; then
    AGENT_NOTIFIER_PYTHON="$PROJECT_ROOT/.venv/bin/python"
  elif command -v python3 >/dev/null 2>&1; then
    AGENT_NOTIFIER_PYTHON="$(command -v python3)"
  else
    AGENT_NOTIFIER_PYTHON="$(command -v python)"
  fi
fi

if [[ "${AGENT_NOTIFIER_DEBUG:-0}" == "1" ]]; then
  LOG_DIR="${AGENT_NOTIFIER_CODEX_LOG_DIR:-$HOME/.agentnotifier/logs}"
  LOG_FILE="${AGENT_NOTIFIER_CODEX_LOG:-$LOG_DIR/codex_notifier.log}"
  if mkdir -p "$LOG_DIR" >/dev/null 2>&1; then
    if touch "$LOG_FILE" >/dev/null 2>&1; then
      LOG_TARGET="$LOG_FILE"
    fi
    {
      printf -- '--- %s ---\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
      printf 'bridge=%s\n' "$0"
      printf 'hook_bin=%s\n' "${AGENT_NOTIFIER_CODEX_HOOK_BIN:-<none>}"
      printf 'notify_bin=%s\n' "${AGENT_NOTIFIER_BIN:-<none>}"
      printf 'python_bin=%s\n' "${AGENT_NOTIFIER_PYTHON:-<auto>}"
      printf 'argc=%s\n' "$#"
      index=1
      for arg in "$@"; do
        printf 'arg%d=%s\n' "$index" "$arg"
        index=$((index + 1))
      done
    } >>"$LOG_TARGET" 2>/dev/null || true
  fi
fi

if [[ -n "$AGENT_NOTIFIER_CODEX_HOOK_BIN" ]]; then
  if [[ "${AGENT_NOTIFIER_DEBUG:-0}" == "1" ]]; then
    "$AGENT_NOTIFIER_CODEX_HOOK_BIN" "$@" >>"$LOG_TARGET" 2>&1
    EXIT_CODE="$?"
    printf 'exit=%s\n' "$EXIT_CODE" >>"$LOG_TARGET" 2>/dev/null || true
    exit "$EXIT_CODE"
  fi
  exec "$AGENT_NOTIFIER_CODEX_HOOK_BIN" "$@"
fi

if [[ -n "$AGENT_NOTIFIER_BIN" ]]; then
  if [[ "${AGENT_NOTIFIER_DEBUG:-0}" == "1" ]]; then
    "$AGENT_NOTIFIER_BIN" codex-hook \
      --name codex \
      --channel both \
      --chime ping \
      --verbose \
      "$@" >>"$LOG_TARGET" 2>&1
    EXIT_CODE="$?"
    printf 'exit=%s\n' "$EXIT_CODE" >>"$LOG_TARGET" 2>/dev/null || true
    exit "$EXIT_CODE"
  fi
  exec "$AGENT_NOTIFIER_BIN" codex-hook \
    --name codex \
    --channel both \
    --chime ping \
    "$@"
fi

if [[ "${AGENT_NOTIFIER_DEBUG:-0}" == "1" ]]; then
  env PYTHONPATH="$PROJECT_ROOT${PYTHONPATH:+:$PYTHONPATH}" \
    "$AGENT_NOTIFIER_PYTHON" -m agentnotifier.cli codex-hook \
    --name codex \
    --channel both \
    --chime ping \
    --verbose \
    "$@" >>"$LOG_TARGET" 2>&1
  EXIT_CODE="$?"
  printf 'exit=%s\n' "$EXIT_CODE" >>"$LOG_TARGET" 2>/dev/null || true
  exit "$EXIT_CODE"
fi

exec env PYTHONPATH="$PROJECT_ROOT${PYTHONPATH:+:$PYTHONPATH}" \
  "$AGENT_NOTIFIER_PYTHON" -m agentnotifier.cli codex-hook \
  --name codex \
  --channel both \
  --chime ping \
  "$@"
