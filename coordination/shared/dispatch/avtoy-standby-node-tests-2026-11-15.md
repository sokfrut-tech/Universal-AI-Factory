# AVTOY standby test dispatch

This marker asks Universal-AI-Factory to run the AVTOY Russian standby test snapshot.

Target branch: `sokfrut-tech/avtoy-korea-auto:factory/max-failover-test-2026-11-15`

Scope: `standby/server.mjs`, MAX adapter, and the standby HTTP server regression tests.

This is isolated test execution only. It does not merge the GitLab branch or deploy production.

Second dispatch: include YDB request-store source and regression tests.

Third dispatch: verify concurrency-safe report persistence and capture TAP counts.

Fourth dispatch: test authenticated MAX operator webhook receiver, YDB event deduplication and regression suite.
