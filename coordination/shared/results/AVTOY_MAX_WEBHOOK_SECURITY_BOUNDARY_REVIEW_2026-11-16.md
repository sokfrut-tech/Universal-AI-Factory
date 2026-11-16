# AVTOY KOREA — MAX webhook security boundary review (2026-11-16)

## Result
Read-only review of the current MAX webhook, parser, operator mapping, adapter, tests, and v4 DDL. Added a durable review note.

- GitLab commit: 3c2ad922a5af67316341b03fbec4a152ec9303b2
- Commit: https://gitlab.com/sokfrut/avtoY-korea-auto/-/commit/3c2ad922a5af67316341b03fbec4a152ec9303b2
- Review file: standby/docs/MAX_WEBHOOK_SECURITY_BOUNDARY_REVIEW_2026-11-16.md

## Key findings
- MAX webhook is intentionally receipt-only; it does not call the command parser or operator mapping helper.
- Numeric MAX_OPERATOR_USER_IDS is only an outer allowlist, not proof of an enabled operator identity/role.
- Message text is not read or persisted; callbacks are receipt-only and actor identity comes from callback.user.
- Parser and mapping helper are separate tested modules, not integrated.
- This is a partial security boundary by design, not command-ready. Do not wire parser/queue until current enabled operator mapping, action role checks, transaction rollback, and route-level tests are ready.
- Event digest delimiter '\\0' is a future hardening point; no exploitable collision was established. Prefer length-prefixed canonical encoding plus collision test before any change.

## Verification
Source inspection only. No Node tests executed. No live MAX/YDB. CI remains blocked before runner startup by provider identity verification. No production changes, deployment, or bot/group creation.

## Next gate
After a trusted Node runner and disposable Russian-region YDB are available: implement feature-flagged parser + mapping + role-gated atomic enqueue, add route integration tests, and prove duplicate concurrency/rollback in real YDB. Keep command execution disabled until worker, execution-time role recheck, audit-before-action, and durable response outbox are complete.
