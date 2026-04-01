#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
MAKE_BIN="${CLAUDE_HOOK_MAKE_BIN:-make}"

# Read JSON payload from stdin
PAYLOAD=$(cat)
if [ -z "$PAYLOAD" ]; then
  exit 0
fi

FILE_PATH=$(echo "$PAYLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('file_path',''))" 2>/dev/null || true)
if [ -z "$FILE_PATH" ]; then
  exit 0
fi

# Convert absolute path to relative
REL_PATH="${FILE_PATH#"$PROJECT_DIR"/}"

# Reject path traversal
if [[ "$REL_PATH" == *".."* ]]; then
  exit 0
fi

cd "$PROJECT_DIR"
$MAKE_BIN claude-post-tool-use FILE="$REL_PATH" 2>/dev/null || true
