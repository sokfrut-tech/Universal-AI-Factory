#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
RESOLVER="$ROOT/coordination/gemini/scripts/resolve-task.sh"
EXTRACTOR="$ROOT/coordination/gemini/scripts/extract-answer.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

pass=0
fail() { echo "FAIL: $1" >&2; exit 1; }
assert_eq() { [[ "$1" == "$2" ]] || fail "$3 (expected '$2', got '$1')"; pass=$((pass + 1)); }
assert_fails() { if "$@" >/dev/null 2>&1; then fail "$1 unexpectedly succeeded"; fi; pass=$((pass + 1)); }

# Use an isolated git repository to prove both ordinary and first-commit diff paths.
git -C "$TMP" init -q
git -C "$TMP" config user.name test
git -C "$TMP" config user.email test@example.invalid
mkdir -p "$TMP/coordination/gemini/dispatch"
echo base > "$TMP/README.md"
git -C "$TMP" add .
git -C "$TMP" commit -qm base
BASE="$(git -C "$TMP" rev-parse HEAD)"
echo task > "$TMP/coordination/gemini/dispatch/task-1.md"
git -C "$TMP" add .
git -C "$TMP" commit -qm task
HEAD_SHA="$(git -C "$TMP" rev-parse HEAD)"
ACTUAL="$(cd "$TMP" && "$RESOLVER" push "$BASE" "$HEAD_SHA" "")"
assert_eq "$ACTUAL" "coordination/gemini/dispatch/task-1.md" "push event resolves exactly one task"

ACTUAL="$(cd "$TMP" && "$RESOLVER" workflow_dispatch "" "$HEAD_SHA" "coordination/gemini/dispatch/task-1.md")"
assert_eq "$ACTUAL" "coordination/gemini/dispatch/task-1.md" "manual dispatch accepts exact task path"
assert_fails bash -c "cd '$TMP' && '$RESOLVER' workflow_dispatch '' '$HEAD_SHA' '../secrets.md'"
ACTUAL="$(cd "$TMP" && "$RESOLVER" push "0000000000000000000000000000000000000000" "$HEAD_SHA" "")"; assert_eq "$ACTUAL" "coordination/gemini/dispatch/task-1.md" "zero-before push resolves task using parent-aware diff"

printf '%s\n' '{"candidates":[{"content":{"parts":[{"text":"Gemini diagnosis"}]}}]}' > "$TMP/ok.json"
ACTUAL="$("$EXTRACTOR" "$TMP/ok.json")"
assert_eq "$ACTUAL" "Gemini diagnosis" "extractor returns candidate text"
printf '%s\n' '{"candidates":[{"content":{"parts":[{"text":"  "}]}}]}' > "$TMP/empty.json"
assert_fails "$EXTRACTOR" "$TMP/empty.json"
printf '%s\n' '{"error":{"code":400,"message":"invalid model"}}' > "$TMP/error.json"
assert_fails "$EXTRACTOR" "$TMP/error.json"
echo "Gemini runner regression tests: $pass assertions passed."
