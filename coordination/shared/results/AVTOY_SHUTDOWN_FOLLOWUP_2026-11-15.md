# AVTOY KOREA — shutdown race correction (2026-11-15)

## Current source
- GitLab project: `sokfrut/avtoY-korea-auto` (88934554)
- Branch: `deploy/russian-tuqo-static-2026-11-15`
- Latest verified HEAD: `10ce21465f1b08e0aebf01f0b5b62af201c65666`
- Commit: https://gitlab.com/sokfrut/avtoY-korea-auto/-/commit/10ce21465f1b08e0aebf01f0b5b62af201c65666

## Additional defect found and fixed
The first graceful-shutdown implementation checked `server.listening` after the deadline. Node changes this flag when `server.close()` begins, not only when all active requests have drained. Therefore, after a forced close the code could close YDB before the HTTP close callback completed. Corrected by always awaiting the `server.close()` callback after the deadline has forced remaining connections closed.

A second hardening change ensures the YDB driver is still closed if HTTP shutdown fails, while preserving and rethrowing the shutdown error. Shutdown remains idempotent and stops the retry timer. Added/updated tests:
- idempotent shutdown and HTTP-before-YDB ordering;
- forced close waits for the HTTP close callback before YDB;
- invalid deadline rejected;
- YDB driver is closed even when HTTP shutdown reports an error.

## Verification
- Copied the exact current `createGracefulShutdown` helper and its four committed test scenarios into an isolated temporary Node test harness and executed with Node v22.16.0 / npm 10.9.2.
- Result: 4 tests passed, 0 failed.
- This is **isolated helper-level verification**, not a full repository test run and not a live HTTP/YDB integration test.
- Read back current server helper and test file from GitLab after commits.
- Latest pipeline #547 for the latest SHA failed immediately at 19:50:00 UTC; `started_at=null`, no jobs, and list-pipeline-jobs returned 0. This is a pre-job pipeline failure, not evidence of Node tests failing. Pipeline: https://gitlab.com/sokfrut/avtoY-korea-auto/-/pipelines/3071063638

## Remaining blockers
- No `standby/package-lock.json`, npm shrinkwrap, pnpm lock or yarn lock in the branch tree. Docker still uses `npm install --omit=dev`; image dependency resolution is not reproducible.
- No full `npm run check`, `npm test`, Docker build/start, live YDB driver close, or end-to-end request drain executed.
- CI pipeline still fails before jobs start; previous project context records provider/account identity verification as the known block. No bypass attempted.
- No Russian production infrastructure, database, domain/DNS/TLS, MAX bot/group, webhook or deployment provisioned.

## Next
1. Obtain a trusted Node/npm build environment with dependency registry access, generate a genuine lockfile, review it and switch Docker to `npm ci --omit=dev`.
2. Run the entire repository check/test suite and Docker build on the exact branch SHA.
3. Run an integration test with real HTTP keep-alive and in-flight requests; validate YDB driver closure against a disposable test database.
4. Keep Russian runtime isolation requirements as the production acceptance gate.
