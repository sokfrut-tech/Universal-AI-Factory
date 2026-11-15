# AVTOY KOREA — continuation handoff (2026-11-15 19:24 UTC)

This is an additive checkpoint. Read the master handoff first:
`docs/AVTOY_KOREA_RUSSIAN_STANDBY_MASTER_HANDOFF_2026-11-15.md`.

## Current verified GitLab state

- Project: `sokfrut/avtoY-korea-auto`, ID `88934554`.
- Working branch: `deploy/russian-tuqo-static-2026-11-15`.
- Latest branch HEAD: `75a4d9f04539a2630d9a7efb2116776cfe4a81e2`.
- Commit: `docs(ydb): verify metadata auth deployment boundary`.
- Previous HEAD: `a3916cac63a81dd1c1e268dd2abdcd426221f619`.
- New document: `standby/docs/YDB_RUNTIME_AUTH_COMPATIBILITY_2026-11-15.md`.
- Commit URL: https://gitlab.com/avtoY-korea-auto/-/commit/75a4d9f04539a2630d9a7efb2116776cfe4a81e2
- Document URL: https://gitlab.com/avtoY-korea-auto/-/blob/deploy/russian-tuqo-static-2026-11-15/standby/docs/YDB_RUNTIME_AUTH_COMPATIBILITY_2026-11-15.md

## What was checked

Re-fetched the live branch and inspected:
- `standby/server.mjs`
- `standby/storage/ydb-request-store.mjs`
- `standby/storage/ydb-schema-v2.sql`
- `standby/storage/ydb-schema-v3-operator-security.sql`
- `standby/package.json`
- `standby/docs/YDB_LEAST_PRIVILEGE_RUNTIME_GRANTS_2026-11-15.md`
- `standby/docs/YDB_PROVIDER_SELECTION_2026-11-15.md`

Confirmed current server startup:
- Imports `Driver`, `query`, `MetadataCredentialsProvider`, and `createYdbRequestStore`.
- Creates Driver with `new MetadataCredentialsProvider()`.
- Awaits `driver.ready()` before building SQL store and schema probes.
- Production `INBOX_STORE=v2` requires externally managed schema; it performs read-only verification before serving.
- The runtime code already awaits driver readiness; no code change was necessary for that point.

## Authentication finding

Official YDB JS SDK documentation explicitly lists VM metadata auth for Yandex Cloud, and its metadata provider defaults to the standard metadata token endpoint and `Google` flavor. Yandex Cloud's official Node.js Managed YDB tutorial says a Cloud Function with an attached service account authenticates to YDB through metadata.

Therefore, `MetadataCredentialsProvider` is a valid candidate for an app running inside Yandex Cloud with an attached service account. It is not portable to an arbitrary third-party VPS: there, the link-local metadata endpoint will not provide a Yandex token. A non-Yandex host needs a separately reviewed service-account credential provider/secret injection strategy.

Sources:
- https://github.com/ydb-platform/ydb-js-sdk/blob/main/packages/auth/README.md
- https://github.com/ydb-platform/ydb-js-sdk/blob/main/packages/auth/src/metadata.ts
- https://yandex.cloud/ru/docs/tutorials/serverless/connect-from-cf-nodejs
- https://ydb.js.org/guide/core

## Verification boundary

- This was a documentation/source review only.
- No Node test suite was run for this documentation-only commit.
- Factory run 43751714424 (74/74) remains the latest selected-source regression evidence for the earlier code snapshot; it does not cover this documentation commit or prove live YDB.
- No GitLab CI success, no live Managed YDB connection, no metadata token test, no Russian ISP acceptance, no restore drill.
- No Yandex account, billing account, payment, DB, service account, Russian host, MAX bot/group, domain, DNS or production resource created.
- No MR merge or deployment.

## Next execution order

1. Perform exact DDL ↔ store-query audit: every table, column, type, index, transaction and bounded DELETE must match v2/v3 migrations.
2. Build a safe migration preflight that inspects existing `SHOW CREATE TABLE` definitions and refuses mismatches; do not rely on `IF NOT EXISTS` as schema validation.
3. Review effective ACLs/owner/inherited permissions and produce a non-mutating preflight for the runtime identity. Do not apply grants to a live DB before owner approval.
4. Confirm selected Yandex Serverless runtime metadata support before provisioning. Keep the app runtime inside Yandex Cloud if retaining the metadata provider.
5. Only after explicit approval: billing setup/resources, migration identity, YDB, Russian host, backup target, live integration and restore drill.
6. Test public access from at least two Russian networks without VPN. Keep Telegram/MAX/GitHub/Cloudflare optional adapters, never critical runtime dependencies.
7. No production merge/deploy or paid resource without explicit approval.

User preference: continue autonomously, do not wait for Claude/Gemini/GitLab Runner, do not ask the user to inspect GitLab manually, and only ask for a human action when unavoidable and clearly explained.
