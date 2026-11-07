# Jarvis Message Broker v2.5 — CI and integration report

Date: 2026-11-07
Branch: `feat/jarvis-broker-v2.5-integration`
Candidate: `coordination/bridge/candidates/broker_v2.5-proposed-NOT-RELEASE.ps1`

## Verified evidence

GitHub Actions run: https://github.com/sokfrut-tech/Universal-AI-Factory/actions/runs/42363845595

- Windows Server 2025 runner, Windows PowerShell 5.1.
- v2.4 compatibility checks passed.
- v2.5 candidate parser passed.
- v2.5 integration suite passed: **23 assertions**.
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
16. Processed-file reconciliation marks a task complete after a simulated crash between moving the file and saving Ledger.\n17. ACK with an invalid HMAC signature is rejected and retained in processing.\n18. Processed-file reconciliation repairs Ledger after a simulated crash between file move and Ledger save.\n19. ACK with invalid HMAC is rejected and retained in processing.\n20. ACK is rejected when the HMAC secret is missing.\n21. ACK with invalid HMAC is rejected and retained in processing.\n22. ACK is rejected when the HMAC secret is missing.\n23. ACK is rejected when the HMAC secret is shorter than 32 UTF-8 bytes.

## Changes in v2.5

- Parameterized base directory, run-once mode, bounded iteration mode, sleep interval, and mutex name for safe integration tests.
- Uses an OS Mutex acquired with `WaitOne`, rather than relying only on whether the named object was newly created.
- Writes Ledger to a same-directory temporary file and uses `File.Replace` for replacement with backup.
- Attempts backup recovery when primary Ledger JSON is corrupt, then restores the primary file.
- Quarantines duplicate task IDs rather than allowing a duplicate to overwrite the accepted task.
- Reconciles orphaned files already present in processing.
- Validates ACK sender/recipient routing against the original task before completion.\n- Requires HMAC-SHA256 signature over canonical `v1` ACK fields; secret is read only from process environment variable `JARVIS_ACK_HMAC_KEY`. Missing, weak (under 32 UTF-8 bytes), or invalid secret/signature fails closed.\n- Reconciles files already in `processed` with stale Ledger state after a crash between file move and Ledger save.
- Gemini transport remains deliberately disabled (`$geminiPanelEndpoint = $null`).

## Latest verified run\n\nGitHub Actions run: https://github.com/sokfrut-tech/Universal-AI-Factory/actions/runs/42364262177\n\nValidated broker/test commit: `950ddbc6b7efcbfe653e9d9a8455c7d52631de75`\n\nWorkflow source-guard revision: `0fca461327c0498827e457ca315f0d31449fbb43`\n\nThe latest run confirms 23 assertions, including valid signed ACK completion, rejection of invalid signatures, fail-closed behavior when the HMAC secret is missing or shorter than 32 UTF-8 bytes, route validation, and recovery after a simulated crash between file move and Ledger save. The v2.5 source guards also pass on the workflow revision containing the 32-byte minimum-key check. The same run also passed the workflow source guard requiring the HMAC function, process-environment secret lookup, and HMACSHA256 implementation.\n\n## Release status

**NOT RELEASE-APPROVED. Do not merge or deploy this candidate.**

Passing CI establishes the tested behaviors above, not full production readiness. Remaining gates:

1. CI uses an isolated test-only HMAC key. The missing-secret negative test passed. Before deployment, provision a high-entropy shared secret separately on every trusted participant, document rotation/revocation, and verify sender key identity. HMAC proves possession of the shared key, not a unique sender identity.
2. Add crash-injection tests for every file/ledger transition, especially a process crash after moving ACK/original files but before persisting the final Ledger state.
3. Expand idempotent reconciliation tests to cover ACK crash points (original moved, ACK moved, Ledger commit interrupted) and filename collisions.
4. Test simultaneous writers and filesystem failure modes beyond the single-instance mutex scenario.
5. Keep Gemini HTTP transport disabled until the separate authenticated transport integration is implemented and tested end-to-end.

## Operational boundary

This branch is a test candidate only. The v2.4 candidate remains unchanged. No production transport was enabled, no API key was added to source, and no release/deployment was performed.


## Protocol specification

The canonical signing payload, field mapping, secret requirements, and security limitations are documented in [ACK_HMAC_PROTOCOL_v1.md](ACK_HMAC_PROTOCOL_v1.md).
