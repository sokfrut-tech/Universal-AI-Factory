# MAX outbound delivery acknowledgement review

Date: 2026-11-16
Reviewed branch HEAD: 3c2ad922a5af67316341b03fbec4a152ec9303b2

## Scope
Read-only review of `standby/channels/max-adapter.mjs`, its unit tests, the YDB delivery receipt logic in `standby/storage/ydb-request-store.mjs`, and the caller in `standby/server.mjs`. No runtime code or tests changed.

## Findings

### F1 — A 2xx response without a valid MAX message receipt is treated as delivered
Severity: High (P1/P2 boundary); confidence: high.

The adapter currently returns success for any `response.ok` unless parsed JSON has `success === false`. Therefore HTTP 200 with an empty object, malformed/unexpected JSON (the JSON parse catch returns `{}`), or a response without the documented message identity is accepted. The worker then writes the synthetic `max:<chatId>` marker as the `operators` receipt and completes the request. This can falsely mark an enquiry delivered when the sender has no evidence of a created MAX message.

Evidence:
- `standby/channels/max-adapter.mjs`: `response.json().catch(() => ({}))`; success condition `response.ok && !apiRejected`; receipt `max:<chatId>`.
- `standby/server.mjs`: MAX success adds `operators`; retry worker calls `completeDelivery(... requiredAdminIds:['operators'])`.
- `standby/storage/ydb-request-store.mjs`: request becomes `delivered` when required receipt is present.
- Existing adapter test returns a valid `message.body.mid` but does not assert malformed 200 / missing mid is rejected.

Smallest remediation direction: for POST /messages, require HTTP 200 plus a valid documented response object with non-empty `message.body.mid` (and, if available, verify returned recipient chat matches configured chat). Return a permanent/protocol error and do not acknowledge delivery when the body is malformed. Add route/worker regression tests proving malformed 200 leaves the request queued.

### F2 — Ambiguous network outcomes can create duplicate MAX notifications
Severity: Medium; confidence: high.

A timeout, connection reset, or lost response is classified retryable. MAX may already have accepted and created the message before the client loses the response. The next worker attempt sends the same notification again. The adapter currently discards the returned `message.body.mid` and returns only the constant `max:<chatId>`, so no provider receipt identity is retained to reconcile a prior attempt.

The official POST /messages documentation describes a created Message response containing a unique `body.mid`; it does not document a client-supplied idempotency key for this operation. Thus exactly-once delivery cannot be claimed from current code/API evidence. This is an at-least-once notification path with possible duplicates after ambiguous failures.

Smallest remediation direction: persist a stable per-enquiry delivery attempt/idempotency record before sending; after a successful response persist the actual MAX `mid`; expose duplicate-safe operator wording including the enquiry short ID; document the ambiguous timeout window. Do not claim exactly-once unless MAX documents and supports an idempotency mechanism or a safe reconciliation query is implemented.

## Confirmed positive properties
- MAX destination is fixed by server configuration; request payload cannot select another chat.
- Notification text excludes customer name, phone/contact and comment; it contains only short request reference and vehicle model.
- Token is sent in Authorization header and not included in returned error objects.
- Text length is bounded to 4000 characters.
- 429 and server/network failures are retryable; common permanent 4xx failures are not.

## Verification limits
Source inspection and comparison with current official MAX API documentation only. No Node tests executed, no live MAX request, no YDB transaction/worker test, and no production change. The branch's GitLab pipeline remains blocked before runner startup by provider identity verification; this is not a test failure and does not establish test success.

## Official MAX references
- POST /messages: https://dev.max.ru/docs-api/methods/POST/messages
- General API response semantics: https://dev.max.ru/docs-api

## Decision
Keep this path non-production until a trusted Node runner and disposable YDB environment are available. Before enabling MAX delivery in production, require strict response receipt validation and add failure-injection tests for malformed 200, timeout-after-acceptance, retry duplicate behavior, and durable acknowledgement failure.
