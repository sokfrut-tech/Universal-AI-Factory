#!/usr/bin/env bash
set -euo pipefail

REQUEST_FILE="${1:?usage: call-qwen-api.sh REQUEST.json RESPONSE.json}"
RESPONSE_FILE="${2:?usage: call-qwen-api.sh REQUEST.json RESPONSE.json}"
: "${QWEN_API_KEY:?QWEN_API_KEY secret is required}"
: "${QWEN_BASE_URL:?QWEN_BASE_URL repository variable is required}"

BASE_URL="${QWEN_BASE_URL%/}"
MODEL="${QWEN_MODEL:-qwen4-max}"

if [[ ! "$BASE_URL" =~ ^https://[A-Za-z0-9.-]+(:[0-9]+)?(/[A-Za-z0-9._~-]+)*/v1$ ]]; then
  echo "ERROR: QWEN_BASE_URL must be an HTTPS API base URL ending in /v1." >&2
  exit 2
fi
if [[ ! "$MODEL" =~ ^[A-Za-z0-9._/-]+$ ]]; then
  echo "ERROR: QWEN_MODEL contains unsupported characters." >&2
  exit 2
fi
if [[ ! -s "$REQUEST_FILE" ]]; then
  echo "ERROR: Qwen request file is missing or empty." >&2
  exit 2
fi

URL="${BASE_URL}/chat/completions"
TRANSIENT_HTTP_RE="^(408|429|500|502|503|504)$"
MAX_ATTEMPTS=3
SUCCESS=0
mkdir -p "$(dirname "$RESPONSE_FILE")"

for ((attempt=1; attempt<=MAX_ATTEMPTS; attempt++)); do
  : > "$RESPONSE_FILE"
  echo "Qwen API attempt ${attempt}/${MAX_ATTEMPTS}; configured model: ${MODEL}"
  set +e
  HTTP_STATUS="$(curl --silent --show-error --connect-timeout 15 --max-time 180 \
    --write-out '%{http_code}' --output "$RESPONSE_FILE" \
    "$URL" \
    --header "Authorization: Bearer ${QWEN_API_KEY}" \
    --header 'content-type: application/json' \
    --data-binary "@${REQUEST_FILE}")"
  CURL_EXIT=$?
  set -e

  if (( CURL_EXIT == 0 )) && [[ "$HTTP_STATUS" == "200" ]]; then
    echo "Qwen API returned HTTP 200."
    SUCCESS=1
    break
  fi

  if [[ "$HTTP_STATUS" =~ $TRANSIENT_HTTP_RE ]] || { (( CURL_EXIT != 0 )) && [[ "${HTTP_STATUS:-000}" == "000" ]]; }; then
    echo "Transient Qwen API failure: HTTP ${HTTP_STATUS:-000}, curl exit ${CURL_EXIT}."
    if (( attempt == MAX_ATTEMPTS )); then
      echo "ERROR: Qwen retry budget exhausted." >&2
      exit 22
    fi
    DELAY=$((attempt * 3))
    echo "Retrying once the bounded ${DELAY}s backoff expires."
    sleep "$DELAY"
    continue
  fi

  echo "FATAL: non-retryable Qwen API failure: HTTP ${HTTP_STATUS:-000}, curl exit ${CURL_EXIT}." >&2
  if [[ -s "$RESPONSE_FILE" ]] && jq -e . "$RESPONSE_FILE" >/dev/null 2>&1; then
    jq -c 'if .error then {error:{code:.error.code,type:.error.type}} else {diagnostic:"provider returned a non-success response"} end' "$RESPONSE_FILE" 2>/dev/null || true
  fi
  exit 22
done

(( SUCCESS == 1 )) || { echo "ERROR: Qwen API request did not succeed." >&2; exit 22; }

jq -e '.choices[0].message.content | select(type == "string" and test("[^[:space:]]"))' "$RESPONSE_FILE" >/dev/null 2>&1 || {
  echo "ERROR: Qwen API returned HTTP 200 but no substantive assistant text." >&2
  jq -c '{id,model,error,choices:[.choices[]? | {finish_reason:.finish_reason}] ,usage}' "$RESPONSE_FILE" 2>/dev/null || true
  exit 23
}