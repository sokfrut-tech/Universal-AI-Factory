# Static review: Message Broker v2.4 candidate
Date: 2026-11-07
Status: **NOT APPROVED FOR RELEASE OR EXECUTION**

## Artifacts
- Candidate: `coordination/bridge/candidates/broker_v2.4-proposed-NOT-RELEASE.ps1`
- Smoke tests: `coordination/bridge/tests/Run-BrokerTests.ps1`
- CI: `.github/workflows/bridge-powershell-validation.yml`

## Verified in CI
- Windows PowerShell 5.1 parser: PASS.
- Minimal backup-ledger smoke test: PASS.
- Static source guard for duplicate task_id branch: PASS.
- Disabled transport / real HTTP call source guards: PASS.
- GitHub Actions run: https://github.com/sokfrut-tech/Universal-AI-Factory/actions/runs/42350560052

The scripts are stored with a UTF-8 BOM. This is required for Windows PowerShell 5.1 to correctly parse Cyrillic text in UTF-8 files; without the BOM, the runner decoded the file as an ANSI code page and treated byte sequences as smart quote characters, producing misleading unmatched-brace errors.

## Scope limits of the tests
The green run is **not** a full functional test of the broker:
- The broker itself was parsed, not executed; its main loop is infinite and transport remains disabled.
- Ledger test is a smoke test of the backup-file selection/conversion pattern, not an invocation of the broker's actual Load-Ledger function.
- Duplicate handling is checked by source guards only; two real duplicate files are not imported in an integration test.
- Mutex contention, abandoned mutex behavior, filesystem collisions, crash recovery, ACK spoofing, and HTTP integration were not exercised.

## Blocking engineering findings

1. **Corrupt primary Ledger does not fall back to backup.** If `ledger.json` exists but is malformed, `Load-Ledger` selects it, logs the parse error, and returns an empty hashtable. It never tries `ledger.bak.json`. A later save can overwrite state.
2. **Fail-open behavior remains.** If no valid ledger is loaded, the function returns `@{}` rather than stopping and preserving evidence.
3. **Duplicate task files are stranded.** The file is moved into shared `processing` before duplicate detection. When task_id already exists, the duplicate file is left there without quarantine or reconciliation.
4. **Destination collisions can overwrite files.** `Move-Item -Force` is used with a shared processing directory and other destinations. Same-named files from different outboxes can collide.
5. **ACK validation is insufficient.** Only the existence of `ack_task_id` is checked. Sender, recipient, message type, correlation, original task state, and duplicate/late ACK behavior are not validated.
6. **Malformed ACK envelope can throw.** The processing path calls `$parsed.Meta.ContainsKey(...)` without first checking `$parsed.Valid`.
7. **ACK state/file transition is not crash-safe.** Files are moved and in-memory state is changed before a durable ledger update; a crash can desynchronize disk state.
8. **No restart reconciliation.** There is no recovery scan for queued/in-flight/completed entries against the actual files in each directory.
9. **No filesystem bootstrap/validation.** Required outbox, processing, errors, processed, inbox, and log directories are not created or validated before use.
10. **Mutex behavior is only statically reviewed.** The candidate checks the `createdNew` flag but does not perform an explicit `WaitOne`/abandoned-mutex recovery protocol. Runtime contention and permissions for the Global namespace were not tested.
11. **Transport remains disabled.** `$geminiPanelEndpoint = $null`; no local panel endpoint has been discovered or contacted. The script is not yet a working Jarvis↔Gemini bridge.
12. **HTTP logging overstates status.** It logs literal `HTTP 200` regardless of the actual response, and it does not validate a model-completion payload.
13. **No real bidirectional transport.** There is no demonstrated reverse Gemini→Jarvis delivery path.

## Required next work before release
- Make Ledger loading validate primary, then backup; if both invalid, stop without overwriting either.
- Add schema/version validation and durable atomic persistence.
- Use collision-safe generated filenames and quarantine duplicate task files.
- Validate a typed ACK envelope and make ACK transitions idempotent and state-gated.
- Add startup reconciliation and crash-safe transition journaling.
- Add real behavioral tests for concurrent start, duplicate files, corrupt primary/backup combinations, spoofed/late ACK, collisions, interrupted writes, and recovery.
- Discover and validate the local Gemini panel API separately before enabling transport.
- Do not execute on the user's PC or release based on parser-only CI.

## Decision
**v2.4 is a parser-clean candidate, not a release candidate. Release remains blocked.**
