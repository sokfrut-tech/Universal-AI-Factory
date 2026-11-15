# AVTOY KOREA — bounded retry batch and verification environment (2026-11-15)

## Source change
- GitLab project: `sokfrut/avtoY-korea-auto` (ID `88934554`)
- Branch: `deploy/russian-tuqo-static-2026-11-15`
- Commit: `31b0ac662712928e2455f196e36130d73e1db170`
- Parent: `2e491c5b7f3345a2d266b6105ac55de7a3cd8e4c`
- Commit URL: https://gitlab.com/sokfrut/avtoY-korea-auto/-/commit/31b0ac662712928e2455f196e36130d73e1db170

## Change
- Added `RETRY_BATCH_LIMIT = 3`.
- Added shared `DELIVERY_LEASE_MS = 120_000` and used it consistently for single-request and background retry claims.
- Background YDB retry worker now claims at most three requests per cycle rather than fifty.
- Added a regression test asserting the worker passes the bounded limit and lease duration to the durable store.
- Existing YDB store itself enforces the supplied limit and interleaves due requests with expired leases to avoid starvation.

## Timing review
The inspected app defaults are Telegram request timeout 15 seconds and MAX timeout 10 seconds. Telegram sends to configured admins in parallel; MAX failover is attempted after Telegram is incomplete. A single delivery therefore has a nominal upper request-time budget of 25 seconds. Three sequential claimed deliveries fit within 75 seconds, leaving 45 seconds before the common 120-second lease expires. This is a code/configuration review, not a live network timing measurement. Production must retain these timeout bounds; any increase requires revisiting batch size or lease duration.

## CI and local verification environment
- Push pipeline #551: https://gitlab.com/sokfrut/avtoY-korea-auto/-/pipelines/3071080694
- Pipeline failed before jobs: `started_at=null`, zero jobs. No test job ran; this is the previously observed account/provider identity-verification gate, not a test failure.
- Local runtime: Node.js 22.16.0, npm 10.9.2.
- Attempted `npm view @ydbjs/core@6.3.1`; registry DNS lookup failed with `EAI_AGAIN registry.npmjs.org`.
- npm cache contains no `@ydbjs` packages.
- Docker CLI is unavailable in this execution environment.
- No lockfile was fabricated; no Docker build or repository test suite is claimed.

## Verification limits
- The commit diff and live branch HEAD were read back from GitLab.
- The newly added regression test has not been run in the repository.
- Full `npm run check`, `npm test`, Docker build/start, real YDB, MAX API, Telegram API, and Russian-network acceptance tests remain outstanding.
- No production deployment, YDB instance, MAX bot/group, webhook, DNS/TLS, billing, or cloud resources were provisioned or changed.

## Next safe step
Use an approved trusted runner with authenticated read access to the private GitLab branch and npm registry access to install dependencies, generate a real lockfile, run the complete suite, and build/start the Docker image. Do not expose a runner token in logs or workflow output. Resolve the GitLab identity-verification block through the provider's normal account process; do not bypass it.
