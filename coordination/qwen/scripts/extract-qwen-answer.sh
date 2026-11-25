#!/usr/bin/env bash
set -euo pipefail

RESPONSE_FILE="${1:?usage: extract-qwen-answer.sh RESPONSE.json}"
if [[ ! -s "$RESPONSE_FILE" ]]; then
  echo "ERROR: Qwen response file is missing or empty." >&2
  exit 2
fi

ANSWER="$(jq -er '
  if .error then error("Qwen API returned an error object")
  elif (.choices[0].message.content | type) != "string" then error("assistant content is not a string")
  else (.choices[0].message.content | select(test("[^[:space:]]")))
  end
' "$RESPONSE_FILE" 2>/dev/null)" || {
  echo "ERROR: Qwen response contains no usable assistant text (API error, empty choice, or malformed JSON)." >&2
  jq -c '{id,model,error,choices:[.choices[]? | {finish_reason:.finish_reason}],usage}' "$RESPONSE_FILE" >&2 2>/dev/null || true
  exit 3
}
printf '%s\n' "$ANSWER"