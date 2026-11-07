#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
RESOLVER="$ROOT/coordination/gemini/scripts/resolve-task.sh"
EXTRACTOR="$ROOT/coordination/gemini/scripts/extract-answer.sh"
API_CALLER="$ROOT/coordination/gemini/scripts/call-gemini-api.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

pass=0
fail() { echo "FAIL: $1" >&2; exit 1; }
assert_eq() { [[ "$1" == "$2" ]] || fail "$3 (expected '$2', got '$1')"; pass=$((pass + 1)); }
assert_fails() { if "$@" >/dev/null 2>&1; then fail "$1 unexpectedly succeeded"; fi; pass=$((pass + 1)); }
assert_contains() { [[ "$1" == *"$2"* ]] || fail "$3 (missing '$2')"; pass=$((pass + 1)); }

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
ACTUAL="$(cd "$TMP" && bash "$RESOLVER" push "$BASE" "$HEAD_SHA" "")"
assert_eq "$ACTUAL" "coordination/gemini/dispatch/task-1.md" "push event resolves exactly one task"

ACTUAL="$(cd "$TMP" && bash "$RESOLVER" workflow_dispatch "" "$HEAD_SHA" "coordination/gemini/dispatch/task-1.md")"
assert_eq "$ACTUAL" "coordination/gemini/dispatch/task-1.md" "manual dispatch accepts exact task path"
assert_fails bash -c "cd '$TMP' && bash '$RESOLVER' workflow_dispatch '' '$HEAD_SHA' '../secrets.md'"
ACTUAL="$(cd "$TMP" && bash "$RESOLVER" push "0000000000000000000000000000000000000000" "$HEAD_SHA" "")"
assert_eq "$ACTUAL" "coordination/gemini/dispatch/task-1.md" "zero-before push resolves task using parent-aware diff"

printf '%s\\n' '{"candidates":[{"content":{"parts":[{"text":"Gemini diagnosis"}]}}]}' > "$TMP/ok.json"
ACTUAL="$(bash "$EXTRACTOR" "$TMP/ok.json")"
assert_eq "$ACTUAL" "Gemini diagnosis" "extractor returns candidate text"
printf '%s\\n' '{"candidates":[{"content":{"parts":[{"text":"  "}]}}]}' > "$TMP/empty.json"
assert_fails bash "$EXTRACTOR" "$TMP/empty.json"
printf '%s\\n' '{"error":{"code":400,"message":"invalid model"}}' > "$TMP/error.json"
assert_fails bash "$EXTRACTOR" "$TMP/error.json"

# Deterministic curl/sleep shims exercise retry, fallback, diagnostics, and secret hygiene.
mkdir -p "$TMP/bin"
cat > "$TMP/bin/fake-curl" <<'FAKE_CURL'
#!/usr/bin/env bash
set -euo pipefail
out=""
url=""
while (($#)); do
  case "$1" in
    --output) out="$2"; shift 2 ;;
    --write-out) shift 2 ;;
    --header|--data-binary|--connect-timeout|--max-time) shift 2 ;;
    https://*) url="$1"; shift ;;
    *) shift ;;
  esac
done
n=0
[[ -f "$FAKE_CURL_COUNT" ]] && n="$(cat "$FAKE_CURL_COUNT")"
n=$((n + 1))
printf '%s' "$n" > "$FAKE_CURL_COUNT"
printf '%s\\n' "$url" >> "$FAKE_CURL_URLS"
status="$(sed -n "${n}p" "$FAKE_CURL_STATUSES")"
if [[ -z "$status" ]]; then status=503; fi
if [[ "$status" == "200" ]]; then
  printf '%s' '{"candidates":[{"content":{"parts":[{"text":"OK"}]}}]}' > "$out"
else
  printf '%s' "{\\"error\\":{\\"code\\":$status,\\"status\\":\\"UNAVAILABLE\\",\\"message\\":\\"diagnostic contains $FAKE_SECRET_SENTINEL\\"}}" > "$out"
fi
printf '%s' "$status"
FAKE_CURL
cat > "$TMP/bin/fake-sleep" <<'FAKE_SLEEP'
#!/usr/bin/env bash
printf '%s\\n' "$1" >> "$FAKE_SLEEP_LOG"
FAKE_SLEEP
chmod +x "$TMP/bin/fake-curl" "$TMP/bin/fake-sleep"

printf '503\\n503\\n200\\n' > "$TMP/statuses-success"
: > "$TMP/urls-success"
: > "$TMP/sleeps-success"
export FAKE_CURL_STATUSES="$TMP/statuses-success" FAKE_CURL_COUNT="$TMP/count-success"
export FAKE_CURL_URLS="$TMP/urls-success" FAKE_SLEEP_LOG="$TMP/sleeps-success"
export FAKE_SECRET_SENTINEL="TEST_SECRET_MUST_NOT_LEAK"
export GEMINI_API_KEY="$FAKE_SECRET_SENTINEL"
export CURL_BIN="$TMP/bin/fake-curl" SLEEP_BIN="$TMP/bin/fake-sleep"
export GEMINI_MODEL="gemini-3.1-pro-preview" GEMINI_FALLBACK_MODEL="gemini-3.8-flash"
OUTPUT="$(bash "$API_CALLER" "$TMP/ok.json" "$TMP/api-response.json" 2>&1)"
assert_eq "$(cat "$FAKE_CURL_COUNT")" "3" "two 503s are retried before fallback succeeds"
assert_contains "$(cat "$FAKE_CURL_URLS")" "/models/gemini-3.1-pro-preview:" "primary model is used first"
assert_contains "$(tail -n 1 "$FAKE_CURL_URLS")" "/models/gemini-3.8-flash:" "fallback model is used after two failures"
assert_eq "$(wc -l < "$TMP/sleeps-success" | tr -d ' ')" "2" "backoff sleeps between transient failures"
assert_contains "$OUTPUT" '"code":503' "diagnostic captures HTTP error code"
if [[ "$OUTPUT" == *"$FAKE_SECRET_SENTINEL"* ]]; then fail "API secret leaked to stdout"; fi
pass=$((pass + 1))
assert_eq "$(bash "$EXTRACTOR" "$TMP/api-response.json")" "OK" "successful API response remains parseable"

printf '503\\n503\\n503\\n503\\n503\\n' > "$TMP/statuses-exhausted"
: > "$TMP/urls-exhausted"
: > "$TMP/sleeps-exhausted"
export FAKE_CURL_STATUSES="$TMP/statuses-exhausted" FAKE_CURL_COUNT="$TMP/count-exhausted"
export FAKE_CURL_URLS="$TMP/urls-exhausted" FAKE_SLEEP_LOG="$TMP/sleeps-exhausted"
if OUTPUT="$(bash "$API_CALLER" "$TMP/ok.json" "$TMP/api-response-exhausted.json" 2>&1)"; then
  fail "retry exhaustion unexpectedly succeeded"
else
  EXIT_CODE=$?
fi
assert_eq "$EXIT_CODE" "22" "retry exhaustion returns curl-compatible failure code"
assert_eq "$(cat "$FAKE_CURL_COUNT")" "5" "retry exhaustion performs five bounded attempts"
assert_eq "$(wc -l < "$TMP/sleeps-exhausted" | tr -d ' ')" "4" "no sleep occurs after final attempt"
if [[ "$OUTPUT" == *"$FAKE_SECRET_SENTINEL"* ]]; then fail "secret leaked in exhausted retry diagnostics"; fi
pass=$((pass + 1))

printf '400\\n' > "$TMP/statuses-fatal"
: > "$TMP/urls-fatal"
: > "$TMP/sleeps-fatal"
export FAKE_CURL_STATUSES="$TMP/statuses-fatal" FAKE_CURL_COUNT="$TMP/count-fatal"
export FAKE_CURL_URLS="$TMP/urls-fatal" FAKE_SLEEP_LOG="$TMP/sleeps-fatal"
assert_fails bash "$API_CALLER" "$TMP/ok.json" "$TMP/api-response-fatal.json"
assert_eq "$(cat "$FAKE_CURL_COUNT")" "1" "non-retryable HTTP 400 is not retried"

echo "Gemini runner regression tests: $pass assertions passed."
