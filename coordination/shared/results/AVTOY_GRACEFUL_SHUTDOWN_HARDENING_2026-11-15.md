# AVTOY KOREA — graceful shutdown hardening (2026-11-15)

## Scope
Repository: `sokfrut/avtoY-korea-auto` (GitLab project 88934554)  
Branch: `deploy/russian-tuqo-static-2026-11-15`  
Latest observed HEAD: `a735c6c145843746a3275c9ab103131d6a936e2e`  
Commit: https://gitlab.com/sokfrut/avtoY-korea-auto/-/commit/a735c6c145843746a3275c9ab103131d6a936e2e

## Implemented
- Added exported `createGracefulShutdown` in `standby/server.mjs`.
- Shutdown is idempotent: repeated SIGINT/SIGTERM handling shares one promise.
- Stops the retry interval, closes the HTTP listener, closes idle keep-alive connections, and gives active requests up to 10 seconds to finish.
- After the grace period, calls Node's `server.closeAllConnections()` to force-close remaining ordinary HTTP connections, then closes the YDB driver.
- YDB driver close happens after the HTTP drain/forced-close phase.
- SIGINT/SIGTERM now report shutdown failures and exit non-zero instead of always reporting success.
- Added `standby/test/shutdown.test.mjs` with cases for idempotency/order, forced close, and deadline validation.
- Added the new test to the `npm run check` syntax-check chain. The `npm test` wildcard already includes `test/*.test.mjs`.

## Verification evidence
- Read back the updated source, test, and package scripts from the target branch after commits.
- Confirmed the new test is referenced by the syntax-check script.
- GitLab commit status query for HEAD returned an empty status list: no fresh CI job result is available.
- No Node test, syntax-check command, Docker build, live HTTP drain test, or real YDB close test was executed in this continuation. The added tests are committed but **not yet proven passing**.
- YDB JS SDK documentation explicitly demonstrates closing the Driver with `await driver.close()`: https://github.com/ydb-platform/ydb-js-sdk/blob/main/packages/core/README.md and https://ydb.tech/docs/ru/dev/example-app/example-js

## Remaining build reproducibility blocker
- Repository tree inspection did not find `standby/package-lock.json`, `npm-shrinkwrap.json`, `pnpm-lock.yaml`, or `yarn.lock`.
- Dockerfile still runs `npm install --omit=dev`. Dependency ranges remain semver ranges, so image builds are not lockfile-reproducible.
- Did not fabricate a lockfile or dependency integrity hashes. A trusted Node/npm environment must run `npm install --package-lock-only` (or `npm install`), review the resulting lockfile, then switch Docker to `npm ci --omit=dev` and run tests/build.
- This must be completed before claiming a reproducible container build.

## Not performed
No GitLab CI identity-verification bypass, MR merge, deployment, YDB provisioning, schema migration, billing/payment, Russian hosting/domain/DNS/TLS setup, MAX bot/group creation, or webhook subscription. Production remains unprovisioned and unverified.

## Next actions
1. Generate and review a genuine npm lockfile in a trusted Node 22 environment; change Docker to `npm ci`.
2. Run `npm run check`, `npm test`, and a clean Docker build/start against this exact branch HEAD.
3. Verify shutdown with real keep-alive and in-flight HTTP requests; verify YDB driver closure against a test database.
4. Reconcile Russian deployment requirements separately; no foreign service is accepted as a Russian runtime dependency without network testing from two Russian operators.
