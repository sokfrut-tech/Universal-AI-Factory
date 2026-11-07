# Review: submitted Gemini Message Broker v2.2
Date: 2026-11-07
Status: REJECTED — NOT SAFE TO EXECUTE

## Blocking findings

1. **Simulated HTTP success remains.** The Invoke-RestMethod call is commented out, but when an endpoint is configured the script sets $statusCode = 200 and transitions to WAITING_ACK. This is a fabricated transport acceptance, not a real HTTP response.
2. **Ledger corruption fails open.** Load-Ledger catches parse errors and returns an empty hashtable. The next Save-Ledger can overwrite the only durable task state. It must fail closed and preserve the damaged file for recovery.
3. **Duplicate task ID handling is incomplete.** The duplicate source file is moved into the shared processing directory before the ledger check; it is then not safely reconciled, and the same filename can collide.
4. **Shared processing namespace.** Both outboxes use the original filename in one processing directory. Equal names can overwrite one another due to Move-Item -Force.
5. **ACK validation is not sufficient.** It checks only whether ack_task_id exists. It does not validate from/to identity, original task state, response type, or duplicate/late ACK semantics.
6. **No reverse delivery implementation.** The script only sends tasks whose Target is gemini; Target=jarvis messages are not delivered by an independent transport or durable inbox consumer.
7. **No true restart recovery.** It does not reconcile ledger entries against processing files or safely restore in-flight work.
8. **No backoff.** Retry timing is absent; the state loop polls every three seconds.
9. **YAML parser is not a YAML parser.** The regex does not robustly parse escaped quotes, colons, empty fields, duplicate keys, or validate required fields and allowed values.
10. **No single-writer lock.** Two instances can race on ledger and file moves.
11. **Atomicity is overstated.** Out-File then Move-Item -Force is not a complete crash-safe replacement strategy on Windows; no backup/recovery protocol is present.
12. **Missing path/bootstrap validation.** Required folders and ledger/log parent paths are not created or checked before writes.

## Positive change
The recursive PSCustomObject-to-hashtable conversion is compatible in principle with Windows PowerShell 5.1 and avoids the PS7-only -AsHashtable switch.

## Required next revision
- Remove simulated status code entirely. With no verified transport: remain TRANSPORT_NOT_CONFIGURED.
- Use separate internal filenames/namespaces per source and task.
- Fail closed on ledger corruption and preserve a backup.
- Add single-instance locking and restart reconciliation.
- Validate envelope and ACK sender/recipient/correlation.
- Implement both directions as durable file-queue routing, and keep HTTP adapter disabled until endpoint discovery.
- Add self-tests executable on Windows PowerShell 5.1, and report actual runtime test evidence separately from static review.

This review is static; no Windows PowerShell 5.1 runtime was available in this environment. No script was executed on the user's computer.
