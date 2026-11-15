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

## Next recommended verification
Run the repository's actual shutdown tests and then the complete standby suite in a trusted Node/npm environment with the project dependencies installed. Separately exercise a real in-flight retry cycle against a disposable YDB instance before production approval.
