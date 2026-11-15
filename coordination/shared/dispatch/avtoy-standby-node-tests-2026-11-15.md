# AVTOY standby test dispatch

This marker asks Universal-AI-Factory to run the AVTOY Russian standby test snapshot.

Target branch: `sokfrut-tech/avtoy-korea-auto:factory/max-failover-test-2026-11-15`

Scope: `standby/server.mjs`, MAX adapter, and the standby HTTP server regression tests.

This is isolated test execution only. It does not merge the GitLab branch or deploy production.

Second dispatch: include YDB request-store source and regression tests.

Third dispatch: verify concurrency-safe report persistence and capture TAP counts.

Fourth dispatch: test authenticated MAX operator webhook receiver, YDB event deduplication and regression suite.

Fifth dispatch: rerun after fixing the YDB fake event map assertion; include latest MAX webhook validation.

Sixth dispatch: verify the mobile operator inbox panel, route security and latest MAX webhook receiver snapshot.

Seventh dispatch: verify final mobile phone/SMS actions and operator panel source checks.

Eighth dispatch: test MAX sender allowlist and callback actor identity handling.

Ninth dispatch: verify bounded MAX webhook event retention using explicit cutoff timestamps, batch limit validation (1–500), and regression that preserves all events at or after the cutoff. Test snapshot source commit: `f0aadd82318865c92481a6c5b86ed48999ae955c`.

Tenth dispatch: test the new strict per-operator bearer-auth parser and role permission matrix (viewer/operator/supervisor/owner), including disabled/unknown credentials, duplicate config, and fail-closed parsing. Target snapshot now includes `standby/security/operator-auth.mjs` and its test suite.

Eleventh dispatch: verify HTTP integration of per-operator credentials and RBAC, YDB durable audit writes, audit-failure fail-closed behavior, and production rejection of the legacy shared token. Snapshot includes updated server, YDB store/tests, and server route tests.

Twelfth dispatch: verify supervisor retry authorization with durable audit recorded before queue processing; validate YDB audit event primary-key declaration and strict target identifier allowlist.

Thirteenth dispatch: verify legacy shared-token access is permitted only under explicit `NODE_ENV=test|development`; an unset or production environment must fail closed even when `STANDBY_ADMIN_TOKEN` is present.

Fourteenth dispatch: verify role-protected `/ops/audit` endpoint, supervisor-only audit listing, durable audit append-before-read ordering, and YDB audit-list decoding/limit behavior.

Fifteenth dispatch: test the role-aware mobile operator panel, including operator identity/role display, retry visibility based on `notifications:retry`, and supervisor/owner audit button calling `/ops/audit`; verify safe text rendering and no browser storage.

Sixteenth dispatch: verify denied-auth and forbidden-role audit records, ensure bearer secrets are never included, and confirm the per-process throttle returns 429 after 10 failed operator attempts in a 10-minute window.

Seventeenth dispatch: verify legacy shared admin token is accepted only when `NODE_ENV=test`; development, unset and production environments must all reject it.

Eleventh dispatch: run the updated standby snapshot with `assertDurableAdminRuntime` and its regression tests. Startup must refuse configured per-operator administration or MAX webhook when the durable YDB request store is absent; per-operator mode must also require the durable audit schema capability. Snapshot target branch `factory/max-failover-test-2026-11-15`, server commit `e1a28ebd2bc1c32f4d0c15111cb1d35ac0731e3c`, server-test commit `12710a83d18d12f0770ca51c7a40fd2297baedc`, YDB-test commit `2043f6973173afcfcf74f931c935c12c2e38cabc`.

Twelfth dispatch: verify shared cross-instance auth throttling via YDB. The store now persists only SHA-256 digests of source IPs, counts failures in a 10-minute window inside serializable transactions, rejects after 10 attempts, and exposes bounded stale-bucket cleanup. The server uses this store when available and fails closed if the shared limiter errors; in-memory fallback is only for isolated tests. Snapshot commits: server `7b6d37ef4b94b5263d1b75586368c1141ef0c218`, YDB store `532881a6132c193226e418b6ad75cd1f4d57c2b0`, YDB tests `c6cde8eec8062b3c03d4ff59f8b0f25421076d79`, HTTP tests `5540095f501554fc09504056ed36610fc11e4799`.

Thirteenth dispatch: rerun the shared YDB auth rate limiter suite after correcting the fake SQL adapter to model the literal initial `failures = 1` in the first UPSERT. The previous run 43749160893 had 67/68 tests pass; the only failure was the fake adapter storing `undefined` for the literal constant, not an observed production YDB failure. Updated test commit `458d8f27984b643d067d09f10e17b89aebc43a1a`.

Fourteenth dispatch: verify bounded operator audit retention. The store now deletes audit records only before an explicit cutoff, in batches capped at 500; tests verify fresh-event preservation and invalid cutoff/limit rejection. No automatic retention period or cleanup scheduler is enabled. Snapshot YDB store commit `9aa5662ff27669f6b744fd5e6e21a51cc7d0d8d5`, test commit `b6c37e23ee1e83c7bfc533a8867918ee8a2371bc`.

Fifteenth dispatch: verify the private `/ops` HTML response is `Cache-Control: no-store, max-age=0`, with same-origin resource policy and existing nosniff protection. This keeps the operator login surface out of browser/shared caches; API responses already use no-store. Snapshot server commit `3de549ca739100ec4419eb5303fb5389b2af17c9`, test commit `2a65df5bc62345c5c88ac51eef0e0add529a03f5`.

Sixteenth dispatch: rerun operator-page cache header test after correcting its test fixture to create `public/ops.html` before requesting `/ops`. The previous run 43749560660 had 68 other tests and this one fixture setup failure (404 because fixture omitted ops.html); production route implementation was not implicated. Updated test commit `e098866b64f8867767bfadd959068fe06eeb63ed`.

Seventeenth dispatch: regression-check stricter production startup gate. `assertDurableAdminRuntime` now requires the full durable enquiry lifecycle (`createEnquiry`, `getEnquiry`, claim/claimDue, private listing, completion); MAX requires idempotent durable receipt recording; individual operators require durable audit schema, failed-auth limiter, audit read/write and inbox listing. This closes a gap where a partial adapter could pass startup while leaving requests in local JSON. GitLab source commit `fdcd94c4c9fb9dd8fd24068044651fee32a13a66`; snapshot commits server `67e445e9966a8c333b4356f6c7960ddb68984ff8`, test `b0c24bb817b570a1ffe22d16a01aa8b70c382a97`.

Eighteenth dispatch: verify separation of YDB schema migrations from production runtime credentials. Added `schemaManagedExternally` mode, read-only startup probes for all required tables and both queue indexes, and production startup requirement `YDB_SCHEMA_MANAGED_EXTERNALLY=true`. Added `standby/storage/ydb-schema-v3-operator-security.sql` for MAX receipts, operator audit and shared auth rate limits; apply v2 then v3 with a separate migration identity. Production app identity must not need DDL rights. GitLab source code commit `70ec196a70f7fab2027512025e4a48615d73afeb`; schema migration commit follows on branch. Snapshot commits: server `5feff3f649c16e9e8b10e8b0a3d8b1556cdb8ebd`, request store `4b62b29595e16b19dbf8414ab262d482af9c5281`, request-store tests `e18e03702ba8d345389035c7285c1ecd8b6daba1`, server tests `10e96368c32c8f6753bb928f8c4e1f20d6b4f17e`.

Nineteenth dispatch: rerun after correcting the schema-verification test harness to inspect its recorded SQL strings (the fake records strings, not `{query}` objects). External schema mode now skips runtime DDL, verifies required tables and both due/expired-lease indexes with read-only SELECTs, and production refuses implicit schema creation. Source branch includes migration v3 and README/runbook/provider docs for separate migration identity. Final selected snapshot commits: server `421c18fe85d4f8086d38f859a7136b4a96195c0e`, store `caf55c31c7b94c4e7c4ae7cb68bbbaeeecd3db0d`, store tests `2ccaca17b5a23df33d2f0ba1aed677876f05d5d9`, server tests `5bb7105ff87fa77d7fb3717c849eb7c6c28cbe43`.

Twentieth dispatch: final fixture correction for schema-separation tests. The first external-schema test failure came from reading `call.query` while fakeSql records raw strings; the second test had the same stale property access. The startup-gate assertion also needed its partial mock to include the new required `verifySchema` capability so the assertion reaches the intended missing-enquiry-capabilities branch. Corrected both test files. Snapshot commits store test `635e14308d7f3245cb3c18d19946f98e654a559a`, server test `8fbe54ec54d44510733dfeda4f83132bc31f17f8`.

Twenty-first dispatch: production storage must never fall back to local JSON. Added `assertProductionRequestStore`: when `NODE_ENV=production`, startup now requires `INBOX_STORE=v2`, a configured YDB connection and the complete durable enquiry lifecycle/schema-verification interface; otherwise it fails before serving requests. This closes a serious gap where the request handler could accept enquiries into local JSON if v2 was omitted. Also aligned dev helper DDL nullability with v3 migration and removed duplicate object export. Source commit `c93e10547dc4d7fb359e03576b6a4081ada93c0c`, follow-up DDL alignment commit follows. Snapshot commits: server `0c456156f3c589c999e214ae56d82e861b2c899b`, server tests `8fde1317116b6b34dd266dbcbed8bf6a38ed402a`, YDB store `481010fed52719d3bb9e738f5ba5e05600ef8ce7`, store tests `25f713b97dddfe4965eff5495ccb64edce881c6a`.
