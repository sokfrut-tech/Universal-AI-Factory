# AVTOY KOREA — MAX command queue reconciliation (2026-11-16)

## Result
Reviewed current GitLab branch `deploy/russian-tuqo-static-2026-11-15`. Added a durable handoff note that supersedes the stale implementation-status paragraph in the earlier MAX queue design.

- New GitLab commit: `71e87b1e882055799463b618f3766bf215732b4f`
- File: `standby/docs/MAX_COMMAND_QUEUE_IMPLEMENTATION_RECONCILIATION_2026-11-16.md`
- Commit URL: https://gitlab.com/sokfrut/avtoY-korea-auto/-/commit/71e87b1e882055799463b618f3766bf215732b4f

## Findings
- Atomic receipt + optional normalized command persistence method exists, but webhook parsing/enqueue is not wired.
- The committed v4 table is intentionally minimal (event digest, command ID, operator ID, action, request ref, received time, status). Worker lease fields and indexes in the earlier design proposal are NOT part of v4.
- Legacy receipt-only events will remain duplicates and will not be backfilled into commands on provider replay. This is a deliberate anti-replay safety boundary.
- The fake SQL adapter rollback test does not prove real YDB rollback/concurrency. Its transaction callbacks are not serialized.
- No command worker, execution-time role recheck, exact-one request resolver, audit-before-action, or durable command response outbox exists. Keep command execution disabled.

## CI evidence
GitLab pipeline 3071898877 targets prior HEAD efe28a1d040a9fa0b1bfaf394566925d4ee40303; it failed before runner startup (`started_at=null`) and returned an empty jobs list. It is not evidence of test failure or success. The new documentation commit has no pipeline result yet.

## Not done / not claimed
No Node tests executed, no trusted runner, no live YDB migration or concurrency test, no MAX bot/group, no hosting, no deployment, and no production activation.

## Next gates
Trusted Node 22 runner; run check/focused/full tests on exact SHA; disposable Russian-region YDB v4 migration and concurrent duplicate/rollback test; validate least-privilege grants; implement worker/authorization/audit/outbox before wiring webhook; full independent CI and Russian-network acceptance before activation.
