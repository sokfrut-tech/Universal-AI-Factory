# Gemini Direct API Worker — repair report

Date: 2026-11-07  
Status: **PATCH READY FOR REVIEW — NOT MERGED / NOT RELEASED**

## Scope

Repair the direct Gemini Developer API worker in `.github/workflows/real-ai-agent-execution.yml` and add deterministic regression coverage. This does not enable Message Broker transport.

## Findings

1. The worker is intentionally restricted to pushes on `main` and manual `workflow_dispatch` runs. Pushes to feature branches do not constitute a valid Gemini execution. The earlier failed feature-branch runs therefore do not prove that Gemini API authentication or generation failed.
2. The push-task resolver computed a fallback revision range for an empty/zero `github.event.before`, but the subsequent `git diff` ignored that range and used the empty/zero SHA directly.
3. The API call allowed two retries with a 240-second per-attempt deadline while the whole job timeout was only eight minutes. The timeout budget was internally inconsistent.
4. The response parser assumed `candidates[0].content.parts[].text` existed. API error objects, safety blocks, empty candidates, and malformed JSON were not classified clearly.
5. A direct manual dispatch has not yet been evidenced in this repair cycle. No API key value was read, printed, or changed.

## Changes in this branch

- Added `coordination/gemini/scripts/resolve-task.sh`: explicit event handling, parent-aware empty/zero-before handling, exactly-one-task enforcement, path allow-list, and file existence validation.
- Added `coordination/gemini/scripts/extract-answer.sh`: validates Gemini API response structure and rejects API errors, safety blocks, malformed JSON, and empty text.
- Updated worker workflow:
  - main-only guard;
  - task resolver helper;
  - 12-minute job / 8-minute API step budget;
  - bounded curl retries for transient network/HTTP conditions with curl's exponential backoff (no retry-all-errors);
  - report commit rebases on latest main before push.
- Added `.github/workflows/gemini-runner-tests.yml` and `coordination/gemini/tests/test-runner.sh`.

## Verification evidence

- Local shell syntax checks: passed.
- Local regression suite: 7 assertions passed.
- GitHub Actions run **42366084720**: success, 7 assertions passed.
- Latest GitHub Actions run **42366132810**: success, 7 assertions passed.
- Latest tested source SHA: `aa6b8ac138e1e3d45c9226feaa179522a1845e9d`.
- Draft PR: [#22](https://github.com/sokfrut-tech/Universal-AI-Factory/pull/22).

## Remaining acceptance gate

The CI suite proves local task resolution and response parsing, not a live call to Gemini. A manual `workflow_dispatch` on `main` with the exact task path must still be run after this patch is reviewed and merged by the repository owner. Confirm the API response, report commit, and logs before calling the integration live.

**Release freeze remains in force. Gemini transport remains disabled.**
