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
