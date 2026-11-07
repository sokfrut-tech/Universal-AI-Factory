# Static review: submitted Gemini Message Broker v2.3
Date: 2026-11-07
Status: REJECTED — NOT SAFE TO RELEASE OR EXECUTE

## Scope and evidence
Reviewed the exact v2.3 source supplied in the conversation. The candidate is preserved separately in `coordination/bridge/candidates/broker_v2.3-proposed-NOT-RELEASE.ps1`.
This is a static source review. No PowerShell process was run on the user's PC and no local endpoint at 127.0.0.1:8320 was contacted.

## Blocking findings

1. **Ledger still fails open.** If the primary ledger is corrupt and the backup is missing/corrupt, `Load-Ledger` returns an empty hashtable. A later save can overwrite the only surviving state. It must throw/stop and preserve both files for manual recovery.
2. **Backup is not validated.** The code chooses the primary whenever it exists; if primary parsing fails it does not try the backup. The claimed automatic backup recovery therefore does not work for the most important case.
3. **No SHA-256 duplicate detection.** The candidate contains no hash calculation or stored hash comparison. `OriginalName` is also not stored. The description of this feature is not implemented.
4. **Duplicate task IDs strand files.** The duplicate file is already moved to shared `processing`; on a duplicate ID it is left there and is not safely quarantined or reconciled.
5. **Filename collisions can overwrite data.** Both source outboxes share one processing namespace, and `Move-Item -Force` is used for processing, errors, and inbox/processed destinations.
6. **ACK validation is inadequate.** Only existence of `ack_task_id` is checked. Sender, recipient, message type, correlation, original task state, and duplicate/late ACK handling are not validated.
7. **ACK processing is not transaction-safe.** Files are moved and task state mutated before the ledger is durably saved. A crash between these operations can leave state and files inconsistent. A malformed envelope can also reach `$parsed.Meta.ContainsKey` without a robust validity guard.
8. **No single-instance lock.** Multiple broker instances can concurrently import, move, and overwrite files or ledger state.
9. **No restart reconciliation.** There is no deterministic recovery of QUEUED/IN_FLIGHT/WAITING_ACK entries against inbox, processing, processed, and errors folders.
10. **No real reverse transport.** The script has one outbound HTTP path to Gemini only. There is no confirmed panel API and no durable bidirectional Jarvis↔Gemini transport.
11. **Transport success is overstated.** `Invoke-RestMethod` is real now, which is an improvement, but the log hardcodes the text “HTTP 200” instead of reporting the actual response/status. A successful HTTP response only proves endpoint acceptance, not model completion or task completion.
12. **Retry behavior is unsafe/incomplete.** There is no delay/backoff, retry schedule or persisted next-attempt time. The loop may retry every three seconds after failures.
13. **Envelope parsing/validation is not YAML-compliant.** The regex parser accepts partial metadata, does not reject duplicate keys or validate required fields, allowed sender/recipient values, ACK type, or escaped content.
14. **Filesystem bootstrap and error handling are missing.** Required directories are not created/validated; missing paths and failed moves/writes can produce non-terminating errors and inconsistent state.
15. **Ledger serialization/replacement remains weak.** Backup copy and temp-file move are not a complete durable transaction protocol; there is no schema/version validation, checksum, fsync strategy, or recovery journal.

## Positive changes
- No fabricated `$statusCode = 200` remains.
- A real `Invoke-RestMethod` call is present, but the endpoint is still null/disabled by default.
- A backup path and copy step were introduced.
- The PowerShell 5.1-compatible recursive PSCustomObject conversion remains.

## Required before a release candidate
- Fail closed when both primary and backup ledgers cannot be parsed/validated; try the backup after primary failure.
- Add schema/version validation and preserve corrupt files without overwriting them.
- Implement content-hash duplicate detection and collision-safe generated internal filenames.
- Make ACKs typed, identity-checked, correlated, idempotent, and state-gated.
- Add exclusive process lock and crash/restart reconciliation.
- Make file moves and ledger updates recoverable and ordered.
- Add bounded retry with persisted backoff.
- Validate all paths and create required directories safely.
- Add Windows PowerShell 5.1 runtime tests on a Windows runner, including corrupt-primary/valid-backup, both-corrupt fail-closed, duplicate IDs/content, collisions, spoofed/late ACKs, interrupted transitions, concurrent start, and disabled transport.

## Verification status
- Static review: completed.
- Windows PowerShell 5.1 parser/runtime tests: not yet run.
- Functional queue/ACK/recovery tests: not run.
- Local Gemini panel API discovery/integration: not run.
- Release decision: BLOCKED.

## CI evidence update (2026-11-07)
- First Windows PowerShell 5.1 parser run: FAILED. GitHub Actions run [42349737698](https://github.com/sokfrut-tech/Universal-AI-Factory/actions/runs/42349737698) found a syntax error in the interpolated string `"Ошибка отправки $key: ..."` (`InvalidVariableReferenceWithDrive`), followed by a parser cascade error.
- The candidate was minimally corrected to use `${key}` in that message. This fixes the reported parser defect only; it does not resolve the architectural blockers above.
- A fresh Windows PowerShell 5.1 validation run [42349771804](https://github.com/sokfrut-tech/Universal-AI-Factory/actions/runs/42349771804) was started against the corrected commit. At report update time it was still in progress; no green result is claimed.
- The CI workflow currently checks PowerShell 5.1 parsing and source-level transport guards only. It does not yet run behavioral queue, recovery, locking, ACK, or HTTP integration tests.
