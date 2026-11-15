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
