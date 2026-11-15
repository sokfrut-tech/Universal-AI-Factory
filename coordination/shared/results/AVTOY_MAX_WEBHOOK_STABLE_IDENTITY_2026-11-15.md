# AVTOY KOREA — MAX webhook stable event identity — 2026-11-15

## Source
GitLab project `sokfrut/avtoY-korea-auto` (88934554)
Branch `deploy/russian-tuqo-static-2026-11-15`
Commit `6577bc8e3be1c0410f2c9712b07a19eab7e8a7de`
Parent `ec4b9c4b485e7dc8e900e7b946222fadbe7cb8fd`
https://gitlab.com/sokfrut/avtoY-korea-auto/-/commit/6577bc8e3be1c0410f2c9712b07a19eab7e8a7de

## Finding
The previous webhook dedupe key hashed JSON.stringify(update). Semantically identical provider events could hash differently when JSON property order or irrelevant text fields changed. For callback updates, the implementation did not require the documented callback timestamp.

## Change
- `message_created`: dedupe SHA-256 now derives from event type + configured chat ID + MAX unique message ID (`message.body.mid`).
- `message_callback`: dedupe SHA-256 derives from event type + chat ID + original message ID (if present) + callback_id + callback timestamp + authorized clicking user ID.
- Reject malformed created-message events with no message ID.
- Reject callback events missing callback_id or a positive safe-integer callback timestamp.
- Do not hash raw JSON, message text, payload, names or other mutable/unnecessary fields.
- Existing YDB event table key remains the 64-character SHA-256 digest; no schema migration required.
- Added regression tests for reordered JSON / changed text dedupe and required callback timestamp; updated callback fixture to include provider-required timestamp.

## Official MAX API evidence
The official Update docs state that:
- MessageBody has a unique `mid` (message ID).
- Callback has `timestamp` (Unix milliseconds) and `callback_id`.
- Callback user identifies the user who clicked.
- Message recipient contains chat_id and chat_type.
Source: https://dev.max.ru/docs-api/objects/Update
Webhook docs recommend webhook for production and describe retries/unsubscribe behavior:
https://dev.max.ru/docs-api/methods/POST/subscriptions/

## Verification
- GitLab branch readback confirms HEAD exactly `6577bc8e3be1c0410f2c9712b07a19eab7e8a7de`.
- Pipeline #553, ID `3071138086`, matches this SHA but failed before starting: `started_at=null`, jobs API returned zero jobs. No CI test/build ran.
- Tests are committed but not claimed as executed.
- No live MAX API, bot, webhook subscription, YDB or Russian network test.

## Boundaries
No merge, production deployment, external bot/group creation, token handling, infrastructure, billing or data mutation.
