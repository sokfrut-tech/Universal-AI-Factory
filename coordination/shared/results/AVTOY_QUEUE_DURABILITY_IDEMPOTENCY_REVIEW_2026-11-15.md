# AVTOY KOREA — queue durability and idempotency review
Date: 2026-11-15
Source project: `sokfrut/avtoY-korea-auto` (GitLab project 88934554)
Branch: `deploy/russian-tuqo-static-2026-11-15`
Reviewed HEAD: `31b0ac662712928e2455f196e36130d73e1db170`

## Scope and evidence
Read the live branch files:
- `standby/server.mjs`
- `standby/storage/ydb-request-store.mjs`
- `standby/channels/max-adapter.mjs`
- `standby/test/server.test.mjs`
- `standby/storage/ydb-request-store.test.mjs`

This is a source review only. No repository tests, live YDB, Telegram/MAX API, deployment, or Russian-network checks were run.

## Findings

### 1. Enquiry persistence and idempotency
- `createEnquiry` stores the enquiry and the SHA-256 digest of the supplied idempotency key in one explicit Serializable read-write transaction.
- A still-valid digest resolves to the existing enquiry; the digest table entry is replaced when its seven-day TTL has expired.
- The external notification call occurs after the persistence transaction, so provider latency does not hold a database transaction open.
- Concurrent same-key requests depend on YDB Serializable conflict detection/retry and the primary-key uniqueness of the digest row. This needs a real YDB concurrency test; mock tests cannot prove SDK retry semantics.

### 2. Claiming and lease transitions
- Individual claims are short Serializable transactions and update status to `sending` with a fresh lease token and expiry.
- Batch discovery reads due queued rows and expired sending rows separately, interleaves both sets, de-duplicates IDs, then claims each row individually. This prevents an always-full due queue from starving expired leases in the selection order.
- A claim lost to another worker is skipped; the claim token protects completion from a later worker that has already reclaimed the row.
- The query/discovery phase is not one atomic snapshot with all claims. That is acceptable because each claim rechecks eligibility transactionally, but contention and pagination behavior still need live YDB tests.

### 3. Delivery acknowledgement is at-least-once, not exactly-once
- Provider HTTP sends happen outside the YDB transaction. The database only records receipts after the external provider reports success.
- If a provider accepts a message and the process crashes before `completeDelivery` commits, the lease eventually expires and the notification may be sent again. Neither the Telegram `sendMessage` path nor the MAX adapter supplies an application-level idempotency key.
- Therefore duplicate operator notifications are possible after crash/timeout ambiguity. This must be documented as at-least-once delivery; do not claim exactly-once delivery.
- Per-admin Telegram receipts are retained across attempts. MAX currently acts as a group-level fallback and returns the stable logical receipt `operators` after successful send.

### 4. Retry worker and leases
- Retry batch limit is 3 and lease duration is 120 seconds. Current configured timeouts are Telegram 15 seconds and MAX 10 seconds; nominal worst-case sequential delivery budget is 75 seconds for three items, leaving 45 seconds before lease expiry, subject to runtime overhead.
- The retry worker processes claims sequentially. A thrown unexpected error during one item's `deliver` or `completeDelivery` aborts the loop; later already-claimed items remain in `sending` until their leases expire. Network errors in the current Telegram/MAX adapters are normally converted to failed results, so this is a defensive-path concern rather than evidence of a routine failure.
- A DB acknowledgement failure after provider success also leaves the lease for expiry and can cause a duplicate send, consistent with at-least-once semantics.
- No overlapping timer cycles are started in one process; shutdown waits for the active retry cycle before closing YDB.

### 5. MAX webhook deduplication
- The handler authenticates the secret, restricts the configured private group and allowlisted sender, then hashes the complete serialized update. Raw webhook content is not persisted.
- `recordMaxWebhookEvent` checks the digest and inserts the receipt in one Serializable transaction; the digest is the primary key. Duplicate retries return HTTP 200 only after the stored event is confirmed.
- Hashing the complete JSON means semantically identical updates with different JSON property ordering or changed non-semantic fields may produce different digests. Provider retries normally replay the same payload, but this assumption should be verified against MAX's webhook retry contract and documented. A canonical event identity based on update type/chat/message/callback identifiers would be more robust if those identifiers are stable and present.

## Recommended next changes (not applied)
1. Add per-item failure isolation to the YDB retry loop so an unexpected exception for one claim does not prevent later claims in the same batch from being processed. If the DB completion call itself fails, preserve the lease-expiry recovery behavior and record a structured operational error without pretending the item was acknowledged.
2. Add focused tests for thrown provider-adapter errors, completion-store errors, mixed success/failure in a three-item batch, and stale lease-token completion after another worker reclaims a request.
3. Add explicit docs/tests describing at-least-once delivery and the unavoidable send-success/DB-ack crash window.
4. Test concurrent same-key enquiry creation, concurrent claim attempts, expired lease recovery, and webhook duplicate delivery against a real YDB test database.
5. Decide and document a MAX webhook canonical identity only after confirming which update identifiers MAX guarantees stable across retries.

## External evidence
YDB's official transaction documentation states that Serializable transactions provide serializable execution and competing transactions can fail with `Transaction locks invalidated`; SDK retry behavior and the exact deployed SDK version must be verified in integration tests: https://ydb.tech/docs/ru/concepts/transactions

## Status
No source changes were made in this review. No CI success is claimed. The last known GitLab pipeline blocker remains account/provider identity verification before jobs start. No production resources or external bots were created.
