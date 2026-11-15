# AVTOY KOREA — retry batch fault isolation — 2026-11-15

## Scope
Harden the YDB-backed background retry loop so one claimed enquiry cannot abort processing of the remaining claimed batch.

## Source change
Repository: `sokfrut/avtoY-korea-auto` (GitLab project ID `88934554`)
Branch: `deploy/russian-tuqo-static-2026-11-15`
Commit: `ec4b9c4b485e7dc8e900e7b946222fadbe7cb8fd`
Parent: `31b0ac662712928e2455f196e36130d73e1db170`
Commit URL: https://gitlab.com/sokfrut/avtoY-korea-auto/-/commit/ec4b9c4b485e7dc8e900e7b946222fadbe7cb8fd

Changed:
- `standby/server.mjs`: wrap each claimed item in its own error boundary; after a failed delivery/ack path, retry the durable completion write using the same known delivery receipts; if that also fails, leave the lease untouched so the normal expired-lease scan can reclaim it; continue processing later items.
- `standby/test/server.test.mjs`: add regression test where first item's initial YDB acknowledgement throws, its retry succeeds, and the second claimed item is still processed.

## Review
- The batch remains bounded at 3 claims and 120,000 ms lease.
- The recovery acknowledgement uses the same lease token; it cannot complete a row after a newer worker has replaced that token.
- If both acknowledgement attempts fail, no local state pretends the item was completed; the lease-expiry path remains responsible for recovery.
- External send followed by an unrecorded DB acknowledgement can still produce duplicate notifications after lease recovery. Delivery remains at-least-once, not exactly-once.
- The test is committed but has NOT been executed in the repository CI or a local full test suite in this environment.

## CI evidence
GitLab pipeline #552, ID `3071134470`, was created for this exact commit and failed before starting:
- `started_at = null`
- zero jobs returned by the pipeline jobs API
- therefore no test/build job ran and this is not a code-test failure or a passing result.
The known account/provider identity-verification gate still prevents GitLab jobs from starting. Do not attempt to bypass it.

Pipeline: https://gitlab.com/sokfrut/avtoY-korea-auto/-/pipelines/3071134470

## Operational boundaries
No merge, production deploy, MAX bot/group/webhook, YDB instance, Russian hosting, domain, DNS/TLS, billing, or external notification action was performed.
