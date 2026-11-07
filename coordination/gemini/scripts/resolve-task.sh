#!/usr/bin/env bash
set -euo pipefail

EVENT_NAME="${1:-}"
EVENT_BEFORE="${2:-}"
EVENT_SHA="${3:-}"
INPUT_TASK="${4:-}"

if [[ "$EVENT_NAME" == "workflow_dispatch" ]]; then
  TASK="$INPUT_TASK"
elif [[ "$EVENT_NAME" == "push" ]]; then
  if [[ -z "$EVENT_SHA" ]]; then
    echo "ERROR: push event SHA is missing." >&2
    exit 2
  fi
  if [[ -z "$EVENT_BEFORE" || "$EVENT_BEFORE" == "0000000000000000000000000000000000000000" ]]; then
    mapfile -t TASKS < <(git diff-tree --root --no-commit-id --name-only --diff-filter=AM -r "$EVENT_SHA" -- 'coordination/gemini/dispatch/*.md')
  else
    mapfile -t TASKS < <(git diff --name-only --diff-filter=AM "$EVENT_BEFORE" "$EVENT_SHA" -- 'coordination/gemini/dispatch/*.md')
  fi
  if [[ "${#TASKS[@]}" -ne 1 ]]; then
    echo "ERROR: expected exactly one added/modified Gemini task; found ${#TASKS[@]}." >&2
    exit 3
  fi
  TASK="${TASKS[0]}"
else
  echo "ERROR: unsupported event '$EVENT_NAME'." >&2
  exit 4
fi

if [[ ! "$TASK" =~ ^coordination/gemini/dispatch/[A-Za-z0-9._-]+\.md$ ]]; then
  echo "ERROR: invalid Gemini task path." >&2
  exit 5
fi
if [[ ! -f "$TASK" ]]; then
  echo "ERROR: Gemini task file does not exist: $TASK" >&2
  exit 6
fi
printf '%s\n' "$TASK"
