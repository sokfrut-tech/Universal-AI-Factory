# AVTOY KOREA — START HERE (new-chat entrypoint)

**Updated:** 2026-11-15  
For every new ChatGPT conversation about AVTOY KOREA, read these files in order before asking the user to repeat project context.

1. [Master handoff — complete project state and execution plan](https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/docs/AVTOY_KOREA_RUSSIAN_STANDBY_MASTER_HANDOFF_2026-11-15.md)
2. [Official Russian hosting verification addendum](https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_RUSSIAN_HOSTING_VERIFICATION_ADDENDUM_2026-11-15.md)
3. [GitVerse / SourceCraft signup clarification](https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_GITVERSE_SOURCECRAFT_SIGNUP_UPDATE_2026-11-15.md)


- [SourceCraft compatibility audit (repo/PR source evidence)](https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_SOURCECRAFT_COMPATIBILITY_AUDIT_2026-11-15.md)

- [Static mirror pipeline source review and test gaps](https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STATIC_MIRROR_PIPELINE_SOURCE_REVIEW_2026-11-15.md)

- [Static frontend + Object Storage integration blocker](https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STATIC_OBJECT_STORAGE_INTEGRATION_BLOCKER_2026-11-15.md)

## Current next actions

- **New continuation point (2026-11-15):** outbound MAX failover code is now in GitLab branch `deploy/russian-tuqo-static-2026-11-15`, latest known commit `79a7d8cc60b320ae884cf70735b8533cfdef7587`. Read `standby/docs/RUSSIA_AUTONOMOUS_BOT_ARCHITECTURE.md`.
- Factory regression run for the isolated standby source snapshot: https://github.com/sokfrut-tech/Universal-AI-Factory/actions/runs/43692987243 . Review its result/report before further changes.
- Next: if tests pass, add the actual MAX webhook receiver using documented `X-Max-Bot-Api-Secret` validation only after Russian HTTPS backend/domain are provisioned; then continue Russian host + durable admin panel work.

- First try SourceCraft with the user's own Yandex ID; no Russian helper has been shown to be necessary.
- Inspect the AVTOY frontend for Service Worker, custom-domain and API CORS dependencies before choosing SourceCraft.
- Check SpaceWeb again later; its free 1 GB plan currently shows sold out, despite phone-only identity being documented.
- Check Beget signup with user's own phone; foreign-number acceptance is unknown.
- Cloud.ru standard registration is described as phone+email or Sber ID; try user's own number first if proceeding. Stop before card binding or payment.
- Cloud.ru remains the strongest media bucket candidate with a documented permanent free tier (15 GB plus monthly operations/egress allowance), but services require positive balance and minimum individual top-up is 100 ₽.
- Do not recruit a person in Russia unless a real provider signup step blocks the user's own credentials and the chosen technical option truly needs that step.
- No payment, card binding, account creation, live data export, DNS update or production deployment without explicit user approval.

## Working policy
ChatGPT remains the default executor and does not wait for external agents or GitLab CI. Use Factory runners where possible. Save each meaningful state change and exact evidence back to Universal-AI-Factory. Never claim a copied test harness is a full branch test. Keep primary production unchanged.


## Latest verified continuation point — 2026-11-15
- GitLab branch `deploy/russian-tuqo-static-2026-11-15`, latest known commit `32bbfa30613a3740dce5a6924ba0205652cb3473`.
- MAX outbound failover is implemented in standby code; 31/31 isolated regression tests passed: https://github.com/sokfrut-tech/Universal-AI-Factory/actions/runs/43693100303
- Read latest GitLab source `standby/docs/RUSSIA_AUTONOMOUS_BOT_ARCHITECTURE.md` and report `coordination/shared/results/AVTOY_STANDBY_TESTS_43693100303.md`.
- Next: independent code review; then implement a MAX webhook receiver only with documented `X-Max-Bot-Api-Secret` validation after the Russian HTTPS backend/domain exists. Continue provisioning Russian API/database/admin panel separately. Do not merge or deploy production without explicit user approval.



## GitLab branch mapping correction
MR !76 is an older research branch (`research/russia-migration-assessment-2026-11-14`), not the current working branch. Current MAX feature branch `deploy/russian-tuqo-static-2026-11-15` at `32bbfa30613a3740dce5a6924ba0205652cb3473` has no MR yet. Do not use MR !76 pipeline status as evidence for the MAX code.


## Latest source SHA and remaining work
Latest GitLab branch HEAD: `61900daacb638d9211ecc206acaaa3d026991c02`. MAX outbound sender/failover tests: 31/31 passed in run https://github.com/sokfrut-tech/Universal-AI-Factory/actions/runs/43693103183. Still unprovisioned: MAX bot/group, inbound webhook, Russian hosting/runtime, persistent webhook event storage, operator web panel. Current feature branch has no MR; MR !76 is a separate older research branch.


## Latest continuation point — 2026-11-15
- Current GitLab branch: `deploy/russian-tuqo-static-2026-11-15`, HEAD `ce1792b743612c343be9570d3a8c31d7731f7398`.
- MAX inbound webhook + YDB idempotent metadata receipt implemented; `/ops` mobile operator inbox MVP added (list/refresh/retry/tel/SMS).
- Factory run **43693667994** passed **41/41** selected tests: https://github.com/sokfrut-tech/Universal-AI-Factory/actions/runs/43693667994
- Read `standby/docs/RUSSIA_AUTONOMOUS_BOT_ARCHITECTURE.md` and the latest report.
- Not production-ready: no Russian HTTPS host/YDB instance, no actual MAX bot/group/webhook subscription, no operator sender allowlist or automated client replies. No merge/deploy performed.


## Current source checkpoint — 2026-11-15
Latest GitLab branch HEAD: `206cce5e8d6cb8ae602d6e0a11ff57dd72c4dae8`. MAX sender allowlist and callback actor checks added. Factory selected-snapshot test run 43693780039: **43/43 passed**. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43693780039.md. Continue from `standby/docs/RUSSIA_AUTONOMOUS_BOT_ARCHITECTURE.md`; do not claim MAX operational until bot/group and Russian HTTPS/YDB are provisioned.


## Newest continuation checkpoint — 2026-11-15 18:34 UTC
The newest checkpoint supersedes older status notes above.
- GitLab feature branch: `deploy/russian-tuqo-static-2026-11-15`, latest HEAD `f43c6865fcf67ac0da36ee12c346468e4360d281`.
- Added bounded MAX webhook receipt retention: `pruneMaxWebhookEvents({ before, limit })`; explicit cutoff, max 500 keys per call, exclusive cutoff, no automatic scheduler/retention period.
- Factory run **43747461090**: **45/45 passed**, 0 failed. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43747461090.md
- Exact selected-file snapshot branch HEAD: `f0aadd82318865c92481a6c5b86ed48999ae955c`. Not GitLab CI, full-repository CI, live YDB or production E2E.
- No Russian host/YDB, MAX bot/group, webhook subscription, MR, merge or production deployment exists. Keep webhook unsubscribed.
- Next engineering slice: individual operator accounts/roles/audit; then customer channel mapping and reply adapters. Russian autonomous runtime remains the primary product requirement.


## Newest continuation checkpoint — 2026-11-15 18:36 UTC
Supersedes older status notes above.
- GitLab branch `deploy/russian-tuqo-static-2026-11-15`, HEAD `4ff95a79f48b4dbcbe8073ef5f449da5d03d406e`.
- Added strict per-operator auth primitives and role matrix in `standby/security/operator-auth.mjs`; tests cover distinct identities, disabled/unknown credentials, malformed/duplicate config and role permissions.
- Factory run **43747665597** passed **51/51**. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43747665597.md
- Exact test snapshot HEAD `4bc657537730199b0713015a03db7d1cae49fe54`. Selected files only, not GitLab CI or production E2E.
- Auth primitives are not yet wired to HTTP routes; `/ops` still uses shared MVP token. Next: YDB audit store and fail-closed route auth integration. Keep panel off public production.
- Russian runtime, YDB instance, MAX bot/group and webhook remain unprovisioned. No merge/deploy.


## Newest continuation checkpoint — 2026-11-15 18:40 UTC
Supersedes older status notes above.
- GitLab branch `deploy/russian-tuqo-static-2026-11-15`, HEAD `f19f21b2481e95269eaa4572031a1b948fed0f45`.
- Per-operator auth is now wired to `/ops/inbox` and `/ops/retry`; roles enforced server-side. YDB audit event is written before protected reads/retries; audit failure blocks the action. Shared token works only under explicit test/development environment.
- Factory run **43748005666**: **58/58 passed**. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43748005666.md
- Snapshot HEAD `86ec8fe442fdae187ae068fef9b83f7c1cedf11b`; selected files only, not live YDB/production E2E.
- Remaining auth work: audit read endpoint, failed-auth audit/rate limits, live YDB validation, secure production operator digests and multi-instance checks. `/ops` is not ready for public exposure.
- No Russian runtime/YDB instance, MAX bot/group, webhook subscription, MR, merge or deployment.


## Newest continuation checkpoint — 2026-11-15 18:41 UTC
Supersedes older status notes above.
- GitLab branch `deploy/russian-tuqo-static-2026-11-15`, HEAD `97d3cec66a6e281321d981abd730dca53cb696ff`.
- Added role-protected `GET /ops/audit` for supervisor/owner; durable audit event is written before listing. The endpoint returns sanitized audit fields only.
- Factory run **43748164089**: **60/60 passed**. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43748164089.md
- Snapshot HEAD `feea43f5d3c5e266295dc64eeb032c82bce9e7fa`; selected-file suite only.
- Remaining: failed-auth audit/rate limiting, audit view in mobile panel, live YDB validation, production credential provisioning and multi-instance tests. No Russian runtime/YDB, MAX bot/group or deployment.


## Newest continuation checkpoint — 2026-11-15 18:43 UTC
Supersedes older status notes above.
- GitLab branch `deploy/russian-tuqo-static-2026-11-15`, HEAD `ac1ca3b744a6900ee7927e3f8ab410547f716550`.
- Mobile `/ops` now displays operator identity/role, hides retry for non-supervisors, and exposes audit only to supervisor/owner. Server-side permission checks remain authoritative.
- Factory run **43748317816**: **61/61 passed**. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43748317816.md
- Snapshot HEAD `70f3c94cc624fe1f46d52cd5dd5ae7af72958b26`; selected-file suite only.
- Remaining: denied-auth audit/rate limiting, credential rotation, live YDB/multi-instance validation and Russian no-VPN acceptance. No Russian host/YDB or MAX bot/group.


## Newest continuation checkpoint — 2026-11-15 18:45 UTC
Supersedes older status notes above.
- GitLab branch `deploy/russian-tuqo-static-2026-11-15`, HEAD `c40894a262a115f966edbbbc9a55333c771b8ee8`.
- Denied/forbidden operator attempts are audited without credentials; local throttle is 10 failures/IP/10 minutes then 429. This is per-process only; distributed Russian edge rate limiting is still required for production.
- Factory run **43748471412**: **62/62 passed**. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43748471412.md
- Snapshot HEAD `6a2d0c2b6c36010a5e586410e33a87758d4487fb`; selected-file suite only.
- Live YDB, multi-instance rate limiting, Russian no-VPN acceptance, hosting and MAX registration remain unverified/unprovisioned.


## Newest continuation checkpoint — 2026-11-15 18:47 UTC
Supersedes older status notes above.
- GitLab branch `deploy/russian-tuqo-static-2026-11-15`, HEAD `4e5589c917c3f432f945f7c9afbb3e755dfb339f`.
- Shared admin token fallback is test-only (`NODE_ENV=test`); development/unset/production deny. Production needs individual operator hashes and YDB audit.
- Factory run **43748653690**: **63/63 passed**. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43748653690.md
- Snapshot HEAD `fd4a27c4a851eec9c4030860e13719f7534a26db`; selected-file tests only.
- Still no Russian host/YDB, MAX bot/group, live integration or production. Multi-instance/distributed rate limit and no-VPN acceptance remain required.


## Newest continuation checkpoint — 2026-11-15 18:50 UTC
Supersedes older status notes above.
- GitLab feature branch HEAD `252306bed729c85eb47b210ff9368a960dea300a`.
- `/ops` now uses per-operator credentials/RBAC and durable audit interfaces; startup gate refuses operator administration or MAX webhook without durable YDB request store, and refuses operator mode without audit schema support.
- Factory run **43748987700**: **64/64 passed**, 0 failed. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43748987700.md
- Snapshot commit `2043f6973173afcfcf74f931c935c12e2c38cabc`; selected files only, not GitLab CI/live YDB/production E2E.
- Remaining gates: enforce DB least privilege/append-only audit, persistent cross-instance auth rate limiting, audit retention/backups, verify admin no-store/privacy headers, provision actual Russian runtime/YDB/MAX only after eligibility/identity steps.
- No MAX bot/group, Russian server, domain, YDB instance, webhook subscription, MR merge or production deployment.


## Newest continuation checkpoint — 2026-11-15 18:54 UTC
Supersedes older status notes above.
- GitLab feature branch HEAD `5c5805ad8f7ec249e2034975a6c3ca1533148bf8`.
- Shared auth limiter implemented in YDB using SHA-256 source-IP digest, serializable 10-minute window, 10-failure threshold, fail-closed on store error, and bounded stale-row cleanup.
- Factory rerun **43749293947** passed **68/68**. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43749293947.md
- Snapshot commit `458d8f27984b643d067d09f10e17b89aebc43a1a`; selected-file tests only. Previous 67/68 run was a fake-SQL fixture bug and was corrected.
- Remaining gates: live YDB DDL/transaction verification, approved cleanup cadence, backup/restore, DB least privilege, Russian host and MAX registration. No live infrastructure, MR merge or deployment.


## Newest continuation checkpoint — 2026-11-15 18:55 UTC
Supersedes older status notes above.
- GitLab branch HEAD `9ffabe82130b4526135a8685ba9f3e71b57a94d7`.
- Added bounded audit deletion method requiring explicit cutoff, max batch 500, no automatic schedule.
- Factory run **43749431381**: **69/69 passed**, 0 failed. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43749431381.md
- Snapshot commit `b6c37e23ee1e83c7bfc533a8867918ee8a2371bc`; selected-file tests only.
- Next: cache/privacy header review, backup/restore, live YDB verification and owner-approved audit retention duration. No Russian runtime or production deployment.


## Newest continuation checkpoint — 2026-11-15 18:57 UTC
Supersedes older status notes above.
- GitLab branch HEAD `a2b9669940e9ffbc02717b92337006c19508c175`.
- `/ops` now explicitly non-cacheable and has same-origin resource policy, restrictive permissions policy, existing CSP/nosniff/frame protection.
- Factory run **43749661826**: **70/70 passed**, 0 failed. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43749661826.md
- Snapshot commit `e098866b64f8867767bfadd959068fe06eeb63ed`; selected-source tests only.
- Next: live YDB validation, DB least privilege, backup/restore and explicit retention maintenance. No Russian runtime or production deploy.


## Newest continuation checkpoint — 2026-11-15 18:58 UTC
Supersedes older status notes above.
- GitLab branch HEAD `2206b15426ed2e56f907db78c929992719d9d04d`.
- Added YDB backup/restore runbook at `standby/docs/YDB_BACKUP_RESTORE_RUNBOOK_2026-11-15.md`. It defines Russia-only off-cluster backup, table inventory, YDB CLI paths, documented limitations, restore-drill steps and RPO/RTO evidence.
- Latest code test run: **70/70 passed**, report https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43749661826.md
- No database, backup bucket, export, restore or production resource exists. No live restore drill. Next gate is Russian YDB provisioning, then live DDL/transactions and restore test.
