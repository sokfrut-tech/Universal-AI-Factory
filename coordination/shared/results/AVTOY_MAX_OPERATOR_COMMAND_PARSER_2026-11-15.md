# AVTOY KOREA — MAX operator command parser

Date: 2026-11-15

## Source commit

- Repository: `sokfrut/avtoY-korea-auto`
- Branch: `deploy/russian-tuqo-static-2026-11-15`
- Commit: `60548a93e829628072ad1173302d8a17f6937256`
- Parent: `7ea725630618e4a06fe3224b7973fefb47959c8f`
- Commit URL: https://gitlab.com/sokfrut/avtoY-korea-auto/-/commit/60548a93e829628072ad1173302d8a17f6937256

## Changes

Created:
- `standby/security/max-operator-command.mjs`
- `standby/security/max-operator-command.test.mjs`
- `standby/docs/MAX_OPERATOR_COMMAND_PARSER_2026-11-15.md`

The parser accepts only `/help`, `/status <ref>`, and `/retry <ref>`; command names are case-insensitive. References are 6–24 ASCII characters from letters, digits, underscore, and hyphen. Harmless ASCII spaces are accepted. It rejects malformed/extra arguments, mentions, markup, controls, newlines, non-ASCII lookalikes, unknown commands, non-string input, and inputs over 64 characters. It returns only a frozen normalized action/reference record or null.

## Scope and security

Parser-only. Not wired into webhook; no command queue, request lookup, role authorization, execution, group replies, customer messaging, or production behavior change. Existing ingress allowlist remains unchanged. No MAX bot/group/webhook, YDB, hosting, or deployment created.

## Verification

- Branch HEAD re-read after commit: exact SHA `60548a93e829628072ad1173302d8a17f6937256`.
- Parser and test files fetched from GitLab at the branch and confirmed present.
- Test file contains the intended command, malformed-input, Unicode/control, and immutable-output cases.
- Tests have NOT been executed.
- GitLab pipeline #557? Actual pipeline ID: `3071146214`, URL https://gitlab.com/sokfrut/avtoY-korea-auto/-/pipelines/3071146214, exact SHA `60548a93e829628072ad1173302d8a17f6937256`: status failed, `started_at=null`, jobs API returned an empty list. This is the same pre-job identity-verification blocker; no CI jobs ran, so it is neither a test failure nor a pass.
- Full repository tests/build, live MAX/YDB, and Russian-network acceptance remain unverified.

## Next safe step

Add isolated tests for the parser on a trusted runner when available, then design the durable command queue transaction separately. Do not connect parser to webhook or execute `/retry` until event receipt + command enqueue are atomic, current role is rechecked, and audit-before-action is enforced.
