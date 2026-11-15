# AVTOY KOREA — explicit MAX operator identity mapping

Date: 2026-11-15
GitLab project: `sokfrut/avtoY-korea-auto` (88934554)
Branch: `deploy/russian-tuqo-static-2026-11-15`
Commit: `7ea725630618e4a06fe3224b7973fefb47959c8f`
Parent: `f63e8971e6eaf059b561c1220217eda7cbfc320f`

## Change

Added two isolated files:
- `standby/security/max-operator-mapping.mjs`
- `standby/security/max-operator-mapping.test.mjs`

The parser accepts an explicit JSON mapping of MAX numeric user IDs to existing operator IDs. It enforces 1–100 mappings, numeric MAX IDs, the existing operator ID format, and unique MAX IDs and operator IDs.

The resolver looks up the operator in the current authoritative `STANDBY_OPERATORS_JSON` parsed config every time. It returns only the operator ID and current role, and returns null for unknown, removed, disabled, malformed, or unsupported-role identities. It does not copy roles, token hashes, or enabled state into the mapping. A role downgrade therefore takes effect immediately when the current operator config is reloaded.

## Deliberate limits

- This is a pure helper and tests only. It is NOT wired into the MAX webhook yet.
- Existing `MAX_OPERATOR_USER_IDS` allowlist remains the active ingress gate and behavior is unchanged.
- No MAX commands are parsed or executed.
- No bot, group, webhook, YDB, schema migration, role grant, hosting, or production deployment was created.
- Mapping must not be treated as authentication by itself; webhook secret, exact private group, outer allowlist, current enabled operator lookup, role authorization, and durable audit remain required.
- One-to-one mapping is enforced to prevent ambiguous/shared MAX identities.

## Test coverage added (not executed)

Six Node test cases cover:
1. enabled user resolution to current operator and role;
2. unknown, malformed, removed, and disabled identity denial;
3. immediate role change from current operator config;
4. missing, malformed, empty, and >100 mapping configuration;
5. malformed IDs and duplicate MAX/operator IDs;
6. immutable mapping records with no copied role/credential fields.

These are added tests only. No local test runner was available in the connector workflow, and GitLab CI did not execute jobs.

## Verification

- GitLab branch re-read confirms exact HEAD `7ea725630618e4a06fe3224b7973fefb47959c8f`.
- Both new files were fetched back from the branch; module exports `resolveMaxOperator`; test file contains six test cases.
- Pipeline #555, ID `3071141988`, exact SHA `7ea72563...`: failed with `started_at=null`; jobs API returned an empty list. No test/build ran. This is the known account/provider identity-verification pre-job blocker, not a source test failure and not a pass.

## Next

1. Add the pure strict command parser and parser tests; still do not execute commands.
2. Then integrate mapping into webhook validation only after an explicit migration/compatibility plan for `MAX_OPERATOR_USER_IDS`; ensure unknown/disabled mapped users are denied.
3. Only then add atomic event-receipt + normalized command queue persistence and bounded worker.
4. Keep reply-center work separate until encryption/key management and customer-channel mapping are designed and approved.
