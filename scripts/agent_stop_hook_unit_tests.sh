#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
MAKE_BIN="${AGENT_STOP_HOOK_MAKE_BIN:-make}"
TARGET="${AGENT_STOP_HOOK_TARGET:-stop-hook-unit-tests}"
MAX_LINES="${AGENT_STOP_HOOK_MAX_LINES:-200}"

cd "$PROJECT_DIR"

OUTPUT=$($MAKE_BIN "$TARGET" 2>&1) || {
  echo "$OUTPUT" | tail -n "$MAX_LINES"
  exit 2
}
