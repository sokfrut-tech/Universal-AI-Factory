# AVTOY KOREA handoff — 2026-11-15 19:27 UTC

## Current working state

- GitLab project: `sokfrut/avtoY-korea-auto` (project ID `88934554`)
- Active branch: `deploy/russian-tuqo-static-2026-11-15`
- Current HEAD: `8521068a624d3538a35a5d5ce75b552a6b8c0693`
- Latest commit: `docs(ydb): add read-only schema preflight gate`
- Branch URL: https://gitlab.com/sokfrut/avtoY-korea-auto/-/tree/deploy/russian-tuqo-static-2026-11-15

## Work completed in this continuation

Added:
`standby/docs/YDB_SCHEMA_PREFLIGHT_2026-11-15.md`

Purpose:
- Defines a read-only pre-production schema inspection gate using YDB `SHOW CREATE TABLE`.
- Enumerates all six required v2/v3 row tables.
- Records both required queue indexes and their key/COVER columns.
- Requires review of types, nullability, primary-key order, indexes, table kind/settings.
- Explicitly blocks production startup on any mismatch.
- Separates schema inspection from the runtime-identity ACL preflight.

Evidence:
- GitLab commit: https://gitlab.com/sokfrut/avtoY-korea-auto/-/commit/8521068a624d3538a35a5d5ce75b552a6b8c0693
- YDB official SHOW CREATE docs: https://ydb.tech/docs/ru/yql/reference/syntax/show_create
- YDB official CREATE TABLE docs: https://ydb.tech/docs/ru/yql/reference/syntax/create_table/

## Newly confirmed gap

Current `createYdbRequestStore().verifySchema()` checks SELECT access to the required tables and runs explicit reads through `idx_due_queue` and `idx_expired_lease`. It does NOT compare full schema, column types/nullability, primary-key order, index COVER columns, or unexpected settings.

The existing `storage/ydb-request-store.test.mjs` uses fake SQL. It tests adapter/query construction, not YQL parsing, actual YDB transactions, managed service IAM, or index execution.

No live YDB database has been provisioned or inspected. The preflight doc is a procedure, not a successful live check.

## Next actions

1. Add a test-backed schema contract check for the checked-in v2/v3 migration DDL versus the adapter's required table/column/index contract. Keep it explicitly static; do not call it live YDB validation.
2. If feasible, add a read-only executable preflight that runs `SHOW CREATE TABLE` against a real connection and compares canonical schema signatures; avoid brittle regex-only comparison until the SDK result shape and YDB's normalized DDL are tested.
3. Review all SQL statements in `ydb-request-store.mjs` against migration DDL, especially transaction semantics and the two indexed queue queries.
4. Perform a separate effective-ACL preflight: runtime must not own schema objects and must have no inherited CREATE/ALTER/DROP or broad schema privileges.
5. Do not provision YDB, spend money, create accounts, deploy, merge, or start production without explicit user approval.
6. Keep the runtime autonomous in Russia; no production dependency on Cloudflare/GitHub/GitLab/Telegram.

## Existing constraints

- No real YDB, Russian host, domain, DNS, TLS, MAX bot/group, webhook subscription, payment or production data exists yet.
- GitLab CI previously failed before job creation due account identity verification; this is not a code test failure.
- Existing MR !76 is a separate research branch. Do not merge it.
- MAX bot creation still requires verified RF-resident organization/IP/self-employed profile; do not bypass.
- User expects autonomous progress and concise Russian reports; ask only for actions that require the user's account/approval.
