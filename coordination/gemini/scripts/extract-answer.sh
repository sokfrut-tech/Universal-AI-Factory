#!/usr/bin/env bash
set -euo pipefail
RESPONSE_FILE="${1:?usage: extract-answer.sh RESPONSE.json}"
if [[ ! -s "$RESPONSE_FILE" ]]; then
  echo "ERROR: Gemini response file is missing or empty." >&2
  exit 2
fi
ANSWER="$(jq -er '
  if .error then error("Gemini API returned an error object")
  elif .promptFeedback.blockReason then error("Gemini blocked the prompt")
  else ([.candidates[]?.content.parts[]?.text // empty] | join("\n") | select(test("[^[:space:]]")))
  end
' "$RESPONSE_FILE" 2>/dev/null)" || {
  echo "ERROR: Gemini response contains no usable text (API error, safety block, empty candidate, or malformed JSON)." >&2
  jq -c '{error, promptFeedback, candidates:[.candidates[]? | {finishReason, safetyRatings}]}' "$RESPONSE_FILE" >&2 2>/dev/null || true
  exit 3
}
printf '%s\n' "$ANSWER"
