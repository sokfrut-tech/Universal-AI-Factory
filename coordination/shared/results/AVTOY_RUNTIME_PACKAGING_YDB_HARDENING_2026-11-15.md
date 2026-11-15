# AVTOY KOREA — runtime packaging and YDB queue hardening (2026-11-15)

## Current source state
GitLab project: `sokfrut/avtoY-korea-auto` (88934554)
Branch: `deploy/russian-tuqo-static-2026-11-15`
Latest HEAD: `ae9fac940a73dd03460d4f65172c6eebe336d35a`
Commit: https://gitlab.com/sokfrut/avtoY-korea-auto/-/commit/ae9fac940a73dd03460d4f65172c6eebe336d35a

## Fixes committed in this continuation
1. `claimEnquiry`: lease end now derives from `Date.parse(nowIso)`, so both Date/ISO timestamp inputs and numeric clocks are handled consistently. Previously ISO string input produced an invalid lease end through `Number(now)`.
2. `completeDelivery`: rejects absent/empty required admin receipts, malformed receipt arrays/IDs, and invalid retry delay bounds. Prevents silently keeping a request in queued state forever when no required recipients are configured, and prevents negative/NaN retry delays.
3. Added tests for ISO timestamp lease arithmetic and invalid delivery/retry inputs.
4. Found and fixed a production container packaging defect: `server.mjs` imports `./channels/max-adapter.mjs` and `./security/operator-auth.mjs`, but Dockerfile previously copied only server/storage/public/scripts. Added explicit `COPY channels` and `COPY security`.
5. Added `standby/test/docker-image-contract.test.mjs`, included by the existing `test/*.test.mjs` glob and by `npm run check`.

## Verification
- Read back latest branch HEAD and all changed files after commits; expected code changes, tests, Docker COPY directives and package scripts are present.
- **No Node test suite, Docker build, or GitLab CI job was run in this continuation.** The project CI has previously been blocked before job creation by provider/account identity verification. Do not mark new tests as passed.
- No actual YDB database was provisioned or queried.

## YDB transaction semantics confirmed against official documentation
- `@ydbjs/query` `sql.begin({ isolation: 'serializableReadWrite', idempotent: true }, fn)` is the documented transaction helper. The SDK docs state that idempotent enables retries for conditionally retryable errors and that business logic must itself be idempotent.
- YDB Serializable mode uses optimistic concurrency; conflicting concurrent transactions may fail with `Transaction locks invalidated`. Therefore actual claim contention must be tested on real YDB; fake-SQL tests cannot prove this.
- The SDK docs explicitly say per-query `.idempotent(true)` is ignored inside `sql.begin`; transaction-level option is the relevant one.
Sources:
- https://ydb.js.org/ru/guide/query/transactions
- https://ydb.js.org/guide/query/options
- https://ydb.tech/docs/ru/concepts/transactions
- https://ydb.tech/docs/ru/dev/example-app/example-js

## Remaining blockers / risks
1. Root `standby/package.json` has semver ranges and there is no root `standby/package-lock.json` in the branch tree. Docker uses `npm install`, so dependency resolution is not reproducible. Generate/commit a lockfile using the real project environment, then use `npm ci` in Docker. Not done here.
2. Build and run the Docker image to prove module packaging and runtime startup.
3. Execute the full `npm test` and `npm run check` commands in a trusted runner; record exact counts.
4. Run two-worker concurrent lease claim, idempotency collision, MAX event dedupe and rate-limit tests against a disposable Managed YDB database.
5. Confirm the exact pinned @ydbjs/query/@ydbjs/core/@ydbjs/auth package versions and metadata auth behavior in the selected Yandex runtime.
6. Keep Russian no-VPN runtime as the deployment requirement; none has been provisioned. No account, billable service, server, database, domain, DNS, TLS, bot, webhook or payment was created.
7. No MR merge or production deployment.

## Next work
- Add reproducible dependency lock and container build verification.
- Review startup dependency health, shutdown/driver close, and fail-closed behavior for YDB.
- Then return to Russian hosting feasibility and the actual Russian network acceptance plan.
