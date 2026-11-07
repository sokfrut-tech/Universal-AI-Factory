#!/usr/bin/env bash
set -euo pipefail

REQUEST_FILE="${1:?usage: call-gemini-api.sh REQUEST.json RESPONSE.json}"
RESPONSE_FILE="${2:?usage: call-gemini-api.sh REQUEST.json RESPONSE.json}"
: "${GEMINI_API_KEY:?GEMINI_API_KEY secret is required}"

PRIMARY_MODEL="${GEMINI_MODEL:-gemini-3.1-pro-preview}"
FALLBACK_MODEL="${GEMINI_FALLBACK_MODEL:-gemini-3.8-flash}"
MAX_ATTEMPTS="${GEMINI_MAX_ATTEMPTS:-5}"
FALLBACK_AFTER="${GEMINI_FALLBACK_AFTER:-2}"
BASE_DELAY="${GEMINI_BASE_DELAY:-2}"
CURL_BIN="${CURL_BIN:-curl}"
SLEEP_BIN="${SLEEP_BIN:-sleep}"

if [[ ! "$MAX_ATTEMPTS" =~ ^[1-9][0-9]*$ || ! "$FALLBACK_AFTER" =~ ^[1-9][0-9]*$ || ! "$BASE_DELAY" =~ ^[1-9][0-9]*$ ]]; then
  echo "ERROR: retry configuration must contain positive integers." >&2
  exit 2
fi
if [[ "$PRIMARY_MODEL" == "$FALLBACK_MODEL" ]]; then
  echo "ERROR: primary and fallback Gemini models must be different." >&2
  exit 2
fi
if [[ ! -s "$REQUEST_FILE" ]]; then
  echo "ERROR: Gemini request file is missing or empty." >&2
  exit 2
fi

TRANSIENT_HTTP_RE='^(408|429|500|502|503|504)$'
SUCCESS=0

for ((attempt=1; attempt<=MAX_ATTEMPTS; attempt++)); do
  if (( attempt > FALLBACK_AFTER )); then
    CURRENT_MODEL="$FALLBACK_MODEL"
  else
    CURRENT_MODEL="$PRIMARY_MODEL"
  fi

  echo "Gemini API attempt $attempt/$MAX_ATTEMPTS using model $CURRENT_MODEL"
  URL="https://generativelanguage.googleapis.com/v1beta/models/$CURRENT_MODEL:generateContent"
  : > "$RESPONSE_FILE"

  set +e
  HTTP_STATUS=$("$CURL_BIN" --silent --show-error --connect-timeout 15 --max-time 75 \
    --write-out '%{http_code}' --output "$RESPONSE_FILE" \
    "$URL" \
    --header "x-goog-api-key: $GEMINI_API_KEY" \
    --header 'content-type: application/json' \
    --data-binary "@$REQUEST_FILE")
  CURL_EXIT=$?
  set -e

  if (( CURL_EXIT == 0 )) && [[ "$HTTP_STATUS" == "200" ]]; then
    echo "Gemini API returned HTTP 200 from $CURRENT_MODEL"
    SUCCESS=1
    break
  fi

  if [[ "$HTTP_STATUS" =~ $TRANSIENT_HTTP_RE ]] || { (( CURL_EXIT != 0 )) && [[ "$HTTP_STATUS" == "000" ]]; }; then
    echo "Temporary Gemini API failure: HTTP ${HTTP_STATUS:-000}, curl exit $CURL_EXIT"
    if [[ -s "$RESPONSE_FILE" ]] && jq -e . "$RESPONSE_FILE" >/dev/null 2>&1; then
      # Deliberately omit provider error messages and response bodies from logs.
      jq -c 'if .error then {error:{code:.error.code,status:.error.status}} else {diagnostic:"response contained no structured error metadata"} end' "$RESPONSE_FILE" 2>/dev/null || true
    else
      echo "No structured error metadata available."
    fi

    if (( attempt == MAX_ATTEMPTS )); then
      echo "ERROR: Gemini retry budget exhausted." >&2
      exit 22
    fi

    EXPONENT=$((attempt - 1))
    DELAY=$((BASE_DELAY * (2 ** EXPONENT) + RANDOM % 4))
    echo "Retrying after ${DELAY}s (exponential backoff with jitter)."
    "$SLEEP_BIN" "$DELAY"
    continue
  fi

  echo "FATAL: non-retryable Gemini failure: HTTP ${HTTP_STATUS:-000}, curl exit $CURL_EXIT" >&2
  if [[ -s "$RESPONSE_FILE" ]] && jq -e . "$RESPONSE_FILE" >/dev/null 2>&1; then
    jq -c 'if .error then {error:{code:.error.code,status:.error.status}} else {diagnostic:"no structured error metadata"} end' "$RESPONSE_FILE" 2>/dev/null || true
  fi
  exit 22
done

(( SUCCESS == 1 )) || { echo "ERROR: Gemini request did not succeed." >&2; exit 22; }
