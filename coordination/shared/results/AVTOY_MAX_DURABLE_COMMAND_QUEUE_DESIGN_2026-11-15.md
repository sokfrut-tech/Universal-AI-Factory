# AVTOY KOREA — MAX durable command queue design

Date: 2026-11-15

## GitLab source
- Project: sokfrut/avtoY-korea-auto (88934554)
- Branch: deploy/russian-tuqo-static-2026-11-15
- Commit: 070190dbd3d6d0a84249f7f24f3e2918642e3cc9
- Parent: 60548a93e829628072ad1173302d8a17f6937256
- URL: https://gitlab.com/sokfrut/avtoY-korea-auto/-/commit/070190dbd3d6d0a84249f7f24f3e2918642e3cc9
- Added: standby/docs/MAX_DURABLE_COMMAND_QUEUE_DESIGN_2026-11-15.md

## Work completed
Inspected current webhook, YDB request store, operator mapping/parser, schema preflight, least-privilege grants, and existing command/reply design. Authored a design for the next durable command layer:
- strict event-to-command normalization with no raw message text persistence;
- mapping MAX user IDs to current enabled operator identities, with role rechecked at execution;
- proposed v4 command table keyed by provider event digest;
- one serializable transaction for webhook receipt + normalized command, so queue failure rolls back receipt and produces HTTP 503;
- bounded worker leases, exact-one opaque request-reference resolution, audit-before-action, idempotent retry, PII-free group responses;
- schema/grants/preflight/backup/retention and test/release gates.

## Scope
Documentation only. No parser/webhook wiring, no new YDB table/migration, no worker, no command execution, no group response, no MAX bot/group, no live YDB, no hosting, and no deployment. Existing runtime behavior remains unchanged.

## Verification
- Re-read branch HEAD after commit: exact SHA 070190dbd3d6d0a84249f7f24f3e2918642e3cc9.
- Re-fetched the new design document from the branch and verified the atomic transaction and failure/replay sections.
- GitLab pipeline ID 3071210045, exact SHA 070190dbd3d6d0a84249f7f24f3e2918642e3cc9: failed before startup (started_at=null); jobs API returned empty list. The account/provider identity-verification blocker remains. No CI tests/build ran; do not treat this as code test result.
- No live YDB/MAX or Russian-network acceptance performed.

## Next implementation gate
Before wiring parser into webhook, implement and test the YDB store method and v4 schema in isolation: atomic receipt+command persistence, rollback on command insert failure, duplicate replay, and concurrency behavior. Then wire the webhook. Keep command worker and retry execution disabled until audit-before-action and role revalidation are implemented and independently verified.