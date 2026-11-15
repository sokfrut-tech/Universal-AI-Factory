# AVTOY KOREA — lease/retry regression coverage (2026-11-15)

## Change
Branch: `deploy/russian-tuqo-static-2026-11-15`
Latest branch HEAD: `9eb9dbdcc61c5cde8cbdcce659eb8d98470969c5`

Updated:
`standby/storage/ydb-request-store.test.mjs`

Added focused cases:
1. Expired lease is reclaimed with a fresh lease token; completion by the previous worker is rejected; the new lease holder can complete.
2. Partial admin delivery remains queued, preserves already-delivered admin receipts, schedules the configured retry delay, rejects early claim, and becomes claimable at the retry time.
3. An idempotency key whose seven-day record has expired creates a new request and replaces the digest mapping rather than returning the old request.

## Verification status
The tests have been added but **have not yet been executed** in this continuation. The fake SQL adapter does not model YDB transaction conflicts or concurrent serializable execution. Do not describe these cases as passed.

Existing previous focused evidence remains 4/4 schema contract checks (separate test file) in the prior report. No full repo test suite or GitLab CI result is claimed.

## Review observations / limits
- `claimEnquiry` does the read/eligibility check/update inside a serializable read-write transaction, which is the intended guard against two workers claiming the same lease. This must be validated with actual YDB concurrent transactions.
- `claimDueEnquiries` discovers candidates outside transactions and then individually claims each candidate transactionally. Duplicate candidate discovery is expected to be filtered by the transactional claim; it can cause extra reads but should not cause duplicate ownership if YDB serializable conflict behavior matches the SDK contract.
- `completeDelivery` validates the current lease token before updating, preventing a stale worker from overwriting a newer lease.
- No live YDB, Managed YDB IAM, YQL parser, transaction conflict, or end-to-end MAX/Telegram notification test was run.
- No production resource, data, payment, account, DNS, or deployment was changed.

## Next
1. Run the complete Node test suite through an available trusted runner; report exact command and counts.
2. Verify concurrent claim behavior on a disposable YDB database once provisioned with explicit approval.
3. Verify the @ydbjs/query transaction options and retry/conflict semantics against the pinned SDK version.
4. Continue effective ACL preflight and production startup fail-closed validation.
