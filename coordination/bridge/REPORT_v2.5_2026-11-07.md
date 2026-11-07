# Jarvis Message Broker v2.5 — CI and integration report

Date: 2026-11-07
Branch: `feat/jarvis-broker-v2.5-integration`
Candidate: `coordination/bridge/candidates/broker_v2.5-proposed-NOT-RELEASE.ps1`

## Verified evidence

GitHub Actions run: https://github.com/sokfrut-tech/Universal-AI-Factory/actions/runs/42363845595

- Windows Server 2025 runner, Windows PowerShell 5.1.
- v2.4 compatibility checks passed.
- v2.5 candidate parser passed.
- v2.5 integration suite passed: **16 assertions**.
- Disabled-transport source guard passed.

The 16 assertions cover:
1. PowerShell 5.1 parser accepts the v2.5 broker.
2. PowerShell 5.1 parser accepts the integration test script.
3. Duplicate task ID produces one Ledger record.
4. Duplicate task ID is quarantined.
5. Original task remains in processing.
6. Gemini transport remains disabled.
7. Validly routed ACK marks the original task completed.
8. ACK record is marked completed.
9. Original task file moves to processed.
10. ACK file moves to processed.
11. ACK with mismatched sender cannot complete the original task.
12. Mismatched ACK remains in processing for investigation.
13. Orphaned processing file is reconstructed into Ledger.
14. Corrupt primary Ledger is restored from valid backup.
15. Second concurrent broker process is rejected by the OS Mutex.
16. Mutex owner exits cleanly and releases the Mutex.

## Changes in v2.5

- Parameterized base directory, run-once mode, bounded iteration mode, sleep interval, and mutex name for safe integration tests.
- Uses an OS Mutex acquired with `WaitOne`, rather than relying only on whether the named object was newly created.
- Writes Ledger to a same-directory temporary file and uses `File.Replace` for replacement with backup.
- Attempts backup recovery when primary Ledger JSON is corrupt, then restores the primary file.
- Quarantines duplicate task IDs rather than allowing a duplicate to overwrite the accepted task.
- Reconciles orphaned files already present in processing.
- Validates ACK sender/recipient routing against the original task before completion.
- Gemini transport remains deliberately disabled (`$geminiPanelEndpoint = $null`).

## Release status

**NOT RELEASE-APPROVED. Do not merge or deploy this candidate.**

Passing CI establishes the tested behaviors above, not full production readiness. Remaining gates:

1. ACK routing metadata is not cryptographic authentication. Add a signed/HMAC ACK contract and secret handling before trusting ACKs across an untrusted boundary.
2. Add crash-injection tests for every file/ledger transition, especially a process crash after moving ACK/original files but before persisting the final Ledger state.
3. Add idempotent reconciliation for files already in `processed` when the Ledger write was interrupted.
4. Test simultaneous writers and filesystem failure modes beyond the single-instance mutex scenario.
5. Keep Gemini HTTP transport disabled until the separate authenticated transport integration is implemented and tested end-to-end.

## Operational boundary

This branch is a test candidate only. The v2.4 candidate remains unchanged. No production transport was enabled, no API key was added to source, and no release/deployment was performed.
