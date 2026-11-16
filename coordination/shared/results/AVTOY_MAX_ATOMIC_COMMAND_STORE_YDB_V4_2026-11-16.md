# AVTOY KOREA — atomic MAX receipt + command storage (YDB v4)

Date: 2026-11-16

## Source
- GitLab project: sokfrut/avtoY-korea-auto (88934554)
- Branch: deploy/russian-tuqo-static-2026-11-15
- Implementation commit: 4495bf4805488fc91329ce4bfb52c06bb1a7797b
- Hardening/fix commit: 7abe3e0428fa1f442b0f770fa7c53c712d3fe150
- Least-privilege documentation commit: efe28a1d040a9fa0b1bfaf394566925d4ee40303
- Final branch HEAD: efe28a1d040a9fa0b1bfaf394566925d4ee40303
- Commit URL: https://gitlab.com/sokfrut/avtoy-korea-auto/-/commit/efe28a1d040a9fa0b1bfaf394566925d4ee40303

## Implemented
- Added createYdbRequestStore().recordMaxWebhookEventAndCommand(event, command): serializable/idempotent YDB transaction inserts provider receipt and optional normalized command row together.
- Existing receipt causes duplicate return without second queue insert.
- Queue insert failure propagates out of the transaction; transaction rollback is expected to roll back receipt too, allowing MAX retry.
- Command payload is closed-schema validated: only action/operatorId/requestRef; actions help/status/retry; bounded operator ID and opaque reference; raw message text or extra fields are rejected.
- Event metadata validation allows callback updates with no attached message ID while requiring message_created ID.
- Added ensureMaxCommandSchema and explicit verifyMaxCommandSchema. Default verifySchema/startup behavior is intentionally unchanged until webhook/worker integration is approved.
- Added v4 DDL for standby_max_operator_commands, plus schema preflight, backup/restore inventory and least-privilege guidance.
- No queue indexes yet: the first schema is deliberately simple; add indexes only when a real YDB version/query plan is validated.

## Tests authored (not executed)
- Extended fake SQL adapter with transaction snapshots and rollback simulation.
- Added tests for atomic receipt+command write, duplicate replay, queue insert failure rollback and safe retry, malformed payload rejection, callback receipt-only path and explicit schema probe.
- Total test declarations in ydb-request-store.test.mjs: 30. This is a count of authored test cases, not a passing test result.

## Verification performed
- Re-read branch after all commits: exact HEAD efe28a1d040a9fa0b1bfaf394566925d4ee40303.
- Re-fetched store, test, v4 migration, schema preflight, least-privilege guide and backup runbook from GitLab; confirmed expected sections and files exist.
- Latest GitLab pipeline ID 3071898877 targets exact final HEAD, status failed, started_at=null; jobs API returned empty list. This is the known account/provider identity-verification blocker before jobs start. No Node tests, build or lint jobs ran.
- No live YDB engine test was run. Fake SQL tests are not proof of YQL compatibility, serializable conflict behavior or actual transaction rollback in Managed YDB.

## Safety boundary / not enabled
- Parser and MAX webhook are not wired together.
- No command worker, role revalidation at execution, request-reference lookup, audit-before-action, group reply outbox or customer reply exists yet.
- New v4 table is not required by default startup probes and has not been applied to a live database.
- No MAX bot/group, YDB resource, Russian hosting, secrets, deployment or production behavior was changed.

## Next gate
Run the focused Node test file and syntax check on a trusted runner, then test actual YDB v4 migration and concurrent duplicate webhook deliveries with a disposable Russian-region database. Only after that should the webhook call this atomic store method. Keep command execution disabled until worker authorization, audit and idempotent outbox are implemented.