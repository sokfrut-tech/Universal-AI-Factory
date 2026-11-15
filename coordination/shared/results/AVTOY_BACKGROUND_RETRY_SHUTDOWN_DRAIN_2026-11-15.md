# AVTOY KOREA — background retry shutdown drain (2026-11-15)

## Change
- Project: `sokfrut/avtoY-korea-auto` (GitLab project ID `88934554`)
- Branch: `deploy/russian-tuqo-static-2026-11-15`
- Commit: `2e491c5b7f3345a2d266b6105ac55de7a3cd8e4c`
- Parent: `10ce21465f1b08e0aebf01f0b5b62af201c65666`
- Commit URL: https://gitlab.com/sokfrut/avtoY-korea-auto/-/commit/2e491c5b7f3345a2d266b6105ac55de7a3cd8e4c

## Defect addressed
The process previously cleared the retry interval and drained HTTP connections before closing YDB, but it did not wait for a retry cycle already started by the interval. A SIGTERM during a background delivery could therefore close the YDB driver while that retry was still using it.

## Implementation
- Track the active retry-cycle promise in the process entry point.
- Prevent overlapping timer-driven retry cycles while one is active.
- Pass a drain callback to `createGracefulShutdown`.
- Shutdown order is now: stop retry timer -> drain HTTP -> await active background retry cycle -> close YDB driver.
- Preserve the first shutdown error while still attempting the retry drain and driver close.
- Added two regression tests: shutdown blocks while an active retry promise remains unresolved, and driver closure still occurs when the drain callback fails.

## Verification performed
A standalone Node.js 22.16.0 harness executed the exact shutdown-helper control flow and the six shutdown scenarios:
- idempotent shutdown and HTTP-before-YDB ordering;
- forced connection close waits for the server close callback;
- grace deadline validation;
- YDB closes after HTTP close callback error;
- shutdown remains pending while a deliberately unresolved retry promise is active, then closes YDB only after that promise completes;
- YDB still closes if the retry drain reports an error.

Result: **6/6 passed** on the strengthened harness, including a deferred in-flight retry promise.

## CI status\nA push-triggered GitLab pipeline for the latest commit `2e491c5b` (pipeline #550) failed before any job started: `started_at=null`, zero jobs. The preceding commits also produced pre-job failures (#548 and #549). This is consistent with the existing provider/account identity-verification block and is not a test failure. No successful CI run is claimed.\n\n## Verification limits
- This was an isolated helper-level harness, not the repository's actual `node --test` suite.
- Full `npm run check`, full `npm test`, Docker build/start, real YDB concurrency/integration, and live HTTP+YDB shutdown were not run.
- GitLab CI did not execute any jobs for this change; pipeline #550 has zero jobs and no start timestamp. The account/provider identity-verification block remains unresolved.
- No production service, YDB instance, MAX bot/group, webhook, DNS/TLS, or cloud resource was provisioned or changed.

## Dependency-lock generation blocker\nThe GitHub repository `sokfrut-tech/avtoy-korea-auto` is private, and its `main` branch does not contain `standby/package.json` or `standby/package-lock.json`. Therefore its existing GitHub runner cannot safely generate a lockfile for the newer GitLab-only standby branch without first synchronizing source and arranging a secure private-source fetch. No workflow, token, or secret was added to attempt this. The local Node/npm environment still lacks the required YDB packages in its cache and has no registry network access.\n\n## Next recommended verification
Run the repository's actual shutdown tests and then the complete standby suite in a trusted Node/npm environment with the project dependencies installed. Separately exercise a real in-flight retry cycle against a disposable YDB instance before production approval.


# Follow-up: retry queue lease sizing (2026-11-15)

## New finding and fix
A second queue-lifecycle review found that `retryDue()` claimed up to 50 enquiries with a 120-second lease, then delivered them sequentially. Each item may consume up to 15 seconds for Telegram and then up to 10 seconds for MAX fallback. A 50-item serial batch could therefore outlive leases assigned to later items before their delivery starts.

- Follow-up commit: `31b0ac662712928e2455f196e36130d73e1db170`
- Commit URL: https://gitlab.com/sokfrut/avtoY-korea-auto/-/commit/31b0ac662712928e2455f196e36130d73e1db170
- Added named constants `RETRY_BATCH_LIMIT=3` and `DELIVERY_LEASE_MS=120000`.
- YDB retry worker now claims at most 3 records per serial cycle. Given the configured 15s Telegram and 10s MAX request timeouts, the nominal network budget is at most 75 seconds for three serial records, leaving approximately 45 seconds of the 120-second lease for storage and processing overhead.
- Direct one-record delivery uses the same named lease constant.
- Added a server test asserting the bounded claim limit and lease.

## Verification
- Branch head confirmed at `31b0ac662712928e2455f196e36130d73e1db170`.
- GitLab pipeline #551 failed before jobs: `started_at=null`, zero jobs. No test execution is claimed.
- The new repository test has not been run in the actual package test suite. Full `npm run check`, `npm test`, Docker build/start, and live YDB tests remain outstanding.
- The three-record limit is based on configured external HTTP timeouts; real YDB latency and end-to-end lease behavior still require integration testing.

## Current safety boundary
No production deployment, database provisioning, external bot, credentials, domain, DNS, TLS, or paid cloud resources were created or modified.
