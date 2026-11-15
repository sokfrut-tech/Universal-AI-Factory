# AVTOY KOREA — MAX operator command and reply-center design handoff

Date: 2026-11-15
GitLab project: `sokfrut/avtoY-korea-auto` (88934554)
Branch: `deploy/russian-tuqo-static-2026-11-15`
Commit: `f63e8971e6eaf059b561c1220217eda7cbfc320f`
Parent: `6577bc8e3be1c0410f2c9712b07a19eab7e8a7de`

## Work completed

Rechecked branch before editing: branch was at 6577bc8e. Inspected current `standby/server.mjs`, `standby/security/operator-auth.mjs`, `standby/public/ops.html`, and `standby/storage/ydb-request-store.mjs`.

Confirmed current state:
- MAX webhook accepts only `message_created` and `message_callback` from the configured private group and numeric user allowlist.
- It records an idempotent stable event receipt, then returns 200. It does not parse or execute operator commands.
- Current role-based operator permissions are enforced for the web panel; MAX numeric allowlist is not yet mapped to those operator roles.
- `/ops` supports inbox read, audit read, and retry of due notifications. There is no customer reply center or customer conversation history.
- Customer contact phone alone is not a provider chat identity and cannot safely be used as one.

Created and read-back verified:
`standby/docs/MAX_OPERATOR_COMMANDS_AND_REPLY_CENTER_DESIGN_2026-11-15.md`

Design includes:
- strict command grammar: `/help`, `/status <shortRequestRef>`, `/retry <shortRequestRef>`;
- MAX numeric user ID -> enabled operator identity/role mapping;
- privacy-safe group responses, no customer PII or raw command logging;
- atomic YDB transaction for provider event receipt + normalized command queue item;
- worker leases, duplicate suppression, audit-before-action, re-check role at execution;
- customer replies only through authenticated panel and durable outbound outbox;
- encryption/key management required before storing customer message bodies;
- migration, RBAC, recovery, tests, CI and Russian-network acceptance gates.

No source runtime behavior was changed. No MAX bot/group/token/subscription, YDB resource, migration/grant, hosting, domain, or production deployment was created.

## Verification

- GitLab commit created successfully: `f63e8971e6eaf059b561c1220217eda7cbfc320f`.
- Branch re-read confirms exact HEAD `f63e8971e6eaf059b561c1220217eda7cbfc320f`.
- New design document re-read; 8,655 characters and key security invariant present.
- Pipeline #554, ID `3071140081`, exact SHA f63e8971: status failed, `started_at=null`, jobs API returned zero jobs. This is a pre-job account/provider verification blocker; no tests/build ran. Do not report this as a source-code test failure or pass.
- No full test suite, live MAX/YDB, production, or Russian-network test was run.

## Next implementation sequence

1. Add an explicit MAX user-ID-to-operator mapping, with compatibility validation and role re-check against current enabled operator config.
2. Add pure strict command parser and tests only; no execution path yet.
3. Add normalized command queue and atomic receipt+queue persistence with schema/preflight/least-privilege updates.
4. Add bounded command worker with leases, audit-before-action, privacy-safe responses and duplicate/replay tests.
5. Build reply center separately after encryption/key-management, customer-route mapping, outbox and provider delivery contracts are approved.
6. Require fresh full CI and independent test evidence before enabling or deploying.

## Official MAX references checked 2026-11-15

- Commands: https://dev.max.ru/docs-api/use-cases/chatbot-commands
- Event notifications/webhook: https://dev.max.ru/docs-api/use-cases/event-notifications/
- Update schema: https://dev.max.ru/docs-api/objects/Update
- Send message: https://dev.max.ru/docs-api/methods/POST/messages
- API overview: https://dev.max.ru/docs-api
