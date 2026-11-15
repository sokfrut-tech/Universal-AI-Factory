# AVTOY KOREA — Russian standby mirror master handoff

**Last consolidated:** 2026-11-15  
**Owner:** user  
**Coordinator:** ChatGPT (agent-independent by default)  
**Primary project:** [sokfrut-tech/avtoy-korea-auto](https://github.com/sokfrut-tech/avtoy-korea-auto)  
**Factory of record:** [sokfrut-tech/Universal-AI-Factory](https://github.com/sokfrut-tech/Universal-AI-Factory)

> This is the startup brief for every new chat about AVTOY KOREA / Russian mirror. Read this before asking the user to repeat context. Recheck live repository/provider state before acting; historical notes are not live verification.

## 1. User goal and non-negotiable constraints

Build a reliable Russian-accessible standby copy of the AVTOY KOREA public website/catalog, including approved cars, reviews, photos and videos, with HTTPS and a maintainable update path.

- The existing primary website, Cloudflare Worker, KV, DNS, Telegram webhook and production data must remain untouched unless the user explicitly authorizes a specific production action.
- No paid resource, balance top-up, domain purchase, subscription or automatic billing without explicit approval.
- Prefer free tiers and Russian-hosted infrastructure where practical.
- Do not publish private customer/admin details, Telegram identifiers, tokens, secrets, private inquiries, moderation data or internal inventory.
- Public Git repositories/hosting may contain only a deliberately sanitized public snapshot. Never put credentials or private source data in a public repository.
- Do not bypass identity checks, provider restrictions, regional controls, or use another person's identity. A helper in Russia may assist with legitimate registration/payment only under the provider's rules; never request their passwords or share project secrets.
- User works mainly from Android and wants exact, short, actionable instructions only when a human action is truly required.
- Do not wait for Claude/Gemini or GitLab Runner. ChatGPT is the primary implementer/coordinator. External agents are optional. Label coordinator self-review honestly; never call it independent review.
- Do not claim success without exact commit/run/test evidence.

## 2. Current primary AVTOY media work

### Ordered-media PR #78

- Repository: `sokfrut-tech/avtoy-korea-auto`
- PR: [#78 — ordered media sequence](https://github.com/sokfrut-tech/avtoy-korea-auto/pull/78)
- Branch: `fix/ordered-media-sequence-main-2026-11-15`
- Exact head at last confirmed run: `e5924ad5b13cd19c752deb0c06086b7644002343`
- Status at last known check: open, Draft, not merged.
- Factory runner exact-head run [43688682757](https://github.com/sokfrut-tech/Universal-AI-Factory/actions/runs/43688682757) passed syntax checks and **152 tests, 0 failures**.
- Report: [AVTOY_NODE_TESTS_43688682757.md](https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_NODE_TESTS_43688682757.md)
- Self-review report: [AVTOY_PR78_SELF_REVIEW_2026-11-15.md](https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_PR78_SELF_REVIEW_2026-11-15.md)

What the PR addressed:
1. Preserve backwards compatibility for legacy video review URLs while retaining typed `mediaItems`.
2. Preserve source ordering for mixed Telegram photo/video/document albums.
3. Exercise larger albums (including 14 photos), source message IDs, API/frontend order and canonical mixed-media fixtures.
4. Correct tests to distinguish initial import preview from the later full moderation submission; production logic was not weakened to make tests pass.

Private AVTOY GitHub Actions on this head failed before jobs started: `runner_id: 0`, empty runner name, no steps/logs, very short runs. This is a runner allocation failure, not evidence of test failure and not proof of exhausted minutes. The public Factory runner was used instead. Do not claim a definitive cause unless new evidence appears.

**Next PR #78 actions:** re-fetch PR/head/status; inspect latest diff; rerun Factory test workflow if head changed; finish safe source review; do not merge or deploy without user approval. Live Telegram → moderation → public Worker E2E remains unverified.

## 3. Russian standby mirror — GitLab implementation state

GitLab project: [sokfrut/avtoY-korea-auto](https://gitlab.com/avtoY-korea-auto) (project ID `88934554`)  
MR: [!76](https://gitlab.com/avtoY-korea-auto/-/merge_requests/76)

Relevant branches:
- `research/russia-migration-assessment-2026-11-14`
- `research/russian-zero-cost-hosting-2026-11-15`
- `deploy/russian-static-mirror-2026-11-15`
- `deploy/russian-tuqo-static-2026-11-15`

Latest known deployment-branch correction:
- Commit: `e3ccc7eb8fa8225a522cf771f0e172b356d2679b`
- [Commit link](https://gitlab.com/avtoY-korea-auto/-/commit/e3ccc7eb)
- The media-order gate now normalizes `type`, `mediaType`, `is_video`, and image documents with JPEG/PNG/WebP/GIF MIME types. Mixed photo/video albums require `mediaOrderKnown === true`; unknown/unproven order fails closed.
- Added tests for image documents mixed with video, JPEG/PNG, compatibility fields, homogeneous albums, explicitly proven mixed albums and legacy unknown-order mixed albums.

GitLab CI incident:
- The user reported seeing an identity-verification requirement when attempting to run CI, and said verification had already been completed.
- On 2026-11-15 pipeline `3069961646` failed before jobs appeared; Jobs API returned no jobs, no start time/duration and no YAML error. This does **not** mean the tests failed; it also does not establish the exact root cause.
- Do not ask the user to repeat identity verification without fresh evidence and a concrete provider prompt.
- The source correction has **not yet been executed in Node** at the last confirmed checkpoint. Do not mark it tested.
- A previous report claimed a follow-up report was written; verify the file exists before relying on it.

Mirror safety architecture reviewed:
- Private inventory rejects output under `public/`, uses restrictive file permissions, and sanitizes failure codes.
- Mixed photo/video albums are marked ambiguous unless explicit `mediaItems` order proof exists.
- Media mirroring stages a complete generation, checks byte limits/types, validates image signatures/dimensions, preserves video extensions, uses a recovery journal and refuses partial publication on failure.
- Snapshot builder refuses incomplete car media and approved-review media.
- Parity verifier checks approved source IDs, sanitized text, media types and exact order, failing closed on missing eligible records.
- Live export is restricted to the expected HTTPS Worker origin, stages downloads before replacing media, and rolls back on failure.
- These are source-review findings, not a completed end-to-end production test.

Important remaining test gaps at last inspection:
- No confirmed dedicated tests for the full live-export and mirror orchestration scripts.
- Need run helper test and full `cd standby && npm run check && npm test` on the exact GitLab commit.
- Need sanitized fixture E2E: inventory → mirror (mocked Telegram) → snapshot build → parity → manifest → static build.
- Never export live approved production data or deploy Pages before tests pass and the user approves.

Reports:
- [Source review](https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_RUSSIAN_STANDBY_SOURCE_REVIEW_2026-11-15.md)
- [Media-order follow-up](https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_RUSSIAN_STANDBY_FOLLOWUP_2026-11-15.md) — verify its latest contents/commit before relying on it.

## 4. Hosting and identity research — decision record (2026-11-15)

The user explicitly wants us to check whether there is a **free Russian option that requires verification only**, before asking a person in Russia or spending 100 ₽. Do not skip this question or jump straight to Cloud.ru.

### Candidates discussed

| Provider | Historical finding from research | Suitability / unresolved checks |
|---|---|---|
| **Cloud.ru Evolution Object Storage** | Strongest media-storage candidate discussed: advertised free allowance was 15 GB storage, 1 million read operations, 100,000 write operations and up to 10 TB monthly outbound traffic. A minimum 100 ₽ balance top-up for an individual was discussed. | Best candidate for a larger media bucket, but not yet confirmed whether current registration can be completed by the user, whether payment/balance is mandatory, whether card/Sber ID/Russian phone is required, and whether all listed limits remain current. 100 ₽ is a proposed initial balance, **not** a verified monthly price or guaranteed total cost. Check billing, overage rates and auto-top-up before use. |
| **Yandex Cloud Object Storage** | A free allowance of about 1 GB was discussed; a billing account/payment card may be needed, including a small temporary card verification charge. | Potential fallback, but 1 GB is likely too small for the video catalog. Verify current free-tier and identity/payment rules. |
| **Tuqo** | Free tier around 150 MB discussed. | Too small for the intended photo/video mirror; do not treat as primary media hosting. |
| **Selectel** | A time-limited free S3 promotion was discussed; minimum balance around 200 ₽ was reported. | Not a durable zero-payment solution unless current terms differ. Recheck before considering. |
| **SourceCraft Sites** | Candidate for free static frontend hosting with HTTPS. Public-repository/source-publication constraint was discussed. | May host sanitized static site only; confirm actual current availability, limits, domain, deploy/update path and whether private repo support exists. Never expose private project repo. |
| **GitVerse Pages** | Candidate for free static frontend. Historical notes: Free tier, up to 500 MB artifact, public repo, GigaID with SMS/email. Germany was not in the listed supported foreign-number set seen during research. | Confirm current signup/phone verification and Pages limits. Do not assume user cannot register until testing the actual official flow. Public artifact must contain sanitized static output only. |
| **Uplio** | A 1 GB free storage offer was discussed, registration via email/Yandex ID, public links. | S3/CDN/API compatibility and direct media delivery are unverified. Experimental fallback only. |
| **HostiMan** | Free hosting around 1 GB and SSL discussed; signup reportedly requested a photo of identity document with site. | Avoid unless independently confirmed necessary and user explicitly accepts privacy tradeoff. Not preferred. |

### Key decision

**Do not yet recruit a person in Russia.** First verify free options that need identity verification only and can be legitimately registered by the user. If a provider requires a Russian phone/identity/payment instrument that the user cannot provide, or if Cloud.ru is the only technically viable storage choice and requires a Russian payment step, then find a trusted person in Russia to assist lawfully with their own account/authorized arrangement. Never use false identity or share account credentials.

The earlier idea was to ask a friend in Russia to help with the Cloud.ru minimum 100 ₽ top-up if needed. This remains a contingency, not a final choice. The user did not authorize any payment or paid resource activation.

### Architecture to test

Preferred low-cost split architecture:
1. Free static host for frontend (SourceCraft Sites or GitVerse Pages) if it passes signup and technical checks.
2. Separate object storage for photos/videos (Cloud.ru first candidate if necessary and affordable).
3. Generate a sanitized static snapshot from approved public catalog only.
4. Keep private Worker/bot/admin inquiry flow separate; the static mirror must not leak private contact or moderation data.
5. Use HTTPS and test from Russian ISP/mobile networks, not just from Germany or a VPN.
6. A static host is not a substitute for a media bucket; evaluate total size, egress, cache, hotlink/rate limits, file-size limits and update automation.

## 5. Other hosting context

- Main AppDeploy site `avtoy-korea-e55k1k`: do not touch.
- Backup AppDeploy `avtoy-korea-dp92f8`: [https://avtoy-korea-dp92f8.v2.appdeploy.ai/](https://avtoy-korea-dp92f8.v2.appdeploy.ai/); previously ready as a backup frontend but not autonomous, because it calls the primary Worker and showed frontend/API errors. Do not claim it is a standalone Russian mirror.
- No Russian mirror has been deployed; no approved live catalog has been exported.
- No Cloud.ru bucket, Yandex bucket, Pages site, Russian domain or paid resource is confirmed created.
- Cloud.ru 100 ₽ idea came from earlier discussion; the user mentioned asking friends in Russia. No helper has been confirmed.

## 6. Immediate execution plan (ordered)

### P0 — Resume without asking user to repeat context
1. Recheck this brief, latest GitHub Factory main, AVTOY PR #78, GitLab MR !76 and all relevant branches/heads.
2. Verify both Factory reports above exist and fetch their contents; correct any stale or missing report.
3. Confirm the exact GitLab standby branch SHA and fetch the current helper/test/package files.
4. Create a small Factory Node 22 harness containing the exact helper and test source bytes from GitLab commit `e3ccc7eb...`, plus SHA-256 hashes and provenance. Run `node --check` and `node --test` on Factory public runner. State clearly this validates copied exact files, not the entire GitLab branch.
5. If that passes, build a broader test harness for the full standby scripts and/or arrange a safe exact-source test bundle. Do not pretend a copied subset is the whole project test suite.
6. Add focused mocked-fetch tests for live-export/mirror/parity orchestration where coverage is missing. Run all tests on a public Factory runner.

### P1 — Resolve free registration-only hosting first
7. Verify current official docs and signup/identity/payment requirements for SourceCraft Sites, GitVerse Pages, Uplio, Cloud.ru Evolution and Yandex Cloud. Distinguish: email/SMS verification, identity verification, bank card, payment-account creation, mandatory balance and actual charge.
8. Prefer a free static frontend that the user can register for themselves without a Russian intermediary, if it meets technical requirements.
9. Separately select a media-storage provider based on actual free capacity, egress and API support. Do not assume 15 GB is sufficient until catalog size is inventoried.
10. Only if an unavoidable Russian phone/payment/identity requirement blocks the chosen provider, tell the user exactly what the helper in Russia would need to do and why. No vague request to “find someone” before that.

### P2 — Sanitized mirror validation
11. Create synthetic fixtures only; verify all privacy filters and source ordering.
12. Verify full media integrity, no duplicates/missing assets, exact mixed album order, MIME/extension, manifest hashes, snapshot/parity and rollback.
13. Test mirror accessibility from Russian networks/mobile providers without VPN when possible. Do not promise bypass of ISP blocking; only test legitimate availability and provider reachability.
14. Prepare deployment plan and cost forecast. Do not create paid infrastructure, export live production data, change DNS or deploy until user explicitly approves.

### P3 — Release
15. Require clean exact-head tests, security/privacy review, parity proof and rollback procedure.
16. Present the user a concise release approval request with exact target, changes, costs (including overage and auto-renewal), and rollback.
17. Only after explicit approval, perform the authorized deployment step. Keep primary service unchanged.

## 7. Startup checklist for every new chat

- [ ] Read this file first.
- [ ] Read [docs/MASTER_PROJECT_INDEX.md](https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/docs/MASTER_PROJECT_INDEX.md).
- [ ] Recheck live PR #78, GitLab MR !76, exact branch SHAs and latest CI; do not trust historical status blindly.
- [ ] Check whether the Factory helper harness and follow-up report have since been added.
- [ ] Continue at the first incomplete P0 step above; do not ask the user to restate decisions.
- [ ] Keep all new decisions, exact commits, test run URLs, provider terms and remaining blockers updated in this brief and the Factory index.

## 8. User-facing summary

## 9. Progress update — MAX outbound failover (2026-11-15)
GitLab feature branch `deploy/russian-tuqo-static-2026-11-15` has advanced to `79a7d8cc60b320ae884cf70735b8533cfdef7587`.
- Added MAX operator sender `standby/channels/max-adapter.mjs` with fixed official API origin, Authorization header, one configured operator group destination, timeout/retry classification, and privacy-safe message text.
- Integrated Telegram-first / MAX-fallback delivery in standby server. The durable request is complete if Telegram delivered to all configured admins OR MAX operator group accepted the notification. If both channels fail, it remains queued.
- Added regression tests for MAX success fallback, both channels failing, and stable YDB operator receipt. Corrected escaped regex parsing in Telegram admin IDs.
- Updated bot architecture doc with the current implementation and official MAX webhook secret header contract.
- Factory runner is executing isolated server + MAX test files at https://github.com/sokfrut-tech/Universal-AI-Factory/actions/runs/43692987243 . Do not claim full tests until it completes and the report is reviewed.
- GitLab MR !76 remains unmerged; GitLab pipeline still has the identity-verification blocker. No production deployment, MAX registration, domain, Russian host or paid resources have been created.


The user wants the Russian standby mirror completed quickly, but safely and without unnecessary spending. The key unresolved question is not simply “which host is best”; it is whether a viable Russian static host/media store can be used for free with verification only. Investigate that first. Cloud.ru with a possible 100 ₽ initial balance is the leading media-storage fallback, not a decision to spend. A person in Russia is a contingency only if the chosen provider's legitimate signup/payment rules make their help necessary.


## 10. Verified MAX failover implementation — 2026-11-15
- Latest GitLab feature branch commit: `32bbfa30613a3740dce5a6924ba0205652cb3473`.
- MAX sender adapter: `standby/channels/max-adapter.mjs`; fixed official API host, Authorization header, configured operator chat only, bounded plain-text notification, no customer PII.
- Standby delivery is Telegram-first with MAX fallback. Completion is recorded when all configured Telegram admins receive it OR the configured MAX operator group accepts the notification. If both fail, the durable request remains queued.
- YDB completion uses a stable `operators` receipt; regression coverage added.
- Factory run **43693100303** passed **31/31 tests**, 0 failed, on Node.js 22, including syntax checks, MAX adapter tests, standby server tests and YDB request-store tests. Durable report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43693100303.md
- Test execution used an isolated snapshot branch `factory/max-failover-test-2026-11-15` at `f83526794bccc3235284ac5d4c686ea48aeb53e2`. This is not a GitLab pipeline, not full repository-wide CI, and not production E2E.
- GitLab CI remains blocked by account identity verification. MR !76 remains unmerged.
- MAX webhook is not implemented yet; official secret header is documented as `X-Max-Bot-Api-Secret`. Do not enable webhook before Russian HTTPS endpoint and durable event storage exist.
- No production changes, account registration, bot creation, payment, DNS or deployment performed.


## GitLab branch/MR mapping correction — 2026-11-15
MR !76 actually targets source branch `research/russia-migration-assessment-2026-11-14` at `2fe182560e35175bb1438fded60bcc1d5a74ff91`; it is not the current working branch. Its pipeline status does not describe the MAX work. The current feature branch `deploy/russian-tuqo-static-2026-11-15` is at `32bbfa30613a3740dce5a6924ba0205652cb3473` and currently has no associated MR. Do not conflate MR !76 with the MAX implementation; its test evidence is Factory run `43693100303` (31/31 on selected-source snapshot).


## Latest source checkpoint
Latest GitLab feature branch HEAD is `61900daacb638d9211ecc206acaaa3d026991c02`. The MAX outbound notification/failover slice is tested 31/31 in Factory run `43693103183`. This does **not** mean MAX is operational: no bot/group, inbound webhook, Russian runtime, or operator web panel has been provisioned. MR !76 is a separate older research branch; current feature branch has no MR yet.


## 11. MAX inbound webhook + operator inbox MVP — 2026-11-15
Latest GitLab feature branch HEAD: `ce1792b743612c343be9570d3a8c31d7731f7398`.
- Authenticated MAX webhook route `POST /api/max/webhook` verifies `X-Max-Bot-Api-Secret`, exact configured operator group, supported message/callback types, bounded body and durable persistence before HTTP 200.
- YDB stores SHA-256 deduplicated event metadata only; no raw message body/text.
- `/ops` mobile operator inbox panel lists requests, refreshes, retries queued notifications, and offers tel/SMS actions for phone-only contacts. Admin token remains in tab memory and is not persisted.
- Factory selected-snapshot run `43693667994`: 41/41 tests passed, 0 failed, Node 22. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43693667994.md
- This is not full-repository CI, GitLab CI, production, or live MAX E2E. No bot/group or Russian hosting provisioned.
- Current limits: event receipt only, no command execution, per-operator authentication/allowlist, retention policy, customer reply sending or message history. Panel is an inbox MVP.
- Next gates: sender allowlist and individual operator roles/audit; retention; customer channel mapping/reply adapters; Russian HTTPS:443 + YDB provision; only then real MAX webhook subscription.


## 12. MAX operator sender allowlist
Latest GitLab branch HEAD: `206cce5e8d6cb8ae602d6e0a11ff57dd72c4dae8`. `MAX_OPERATOR_USER_IDS` is now mandatory; only allowlisted users in the configured private group can produce accepted message/callback receipts. Callback actor is taken from `callback.user.user_id`. Factory run `43693780039` passed 43/43 selected tests. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43693780039.md. Still no actual MAX bot/group or Russian runtime; webhook must remain unsubscribed until HTTPS:443 and durable YDB exist.


## 13. Bounded MAX webhook event retention (2026-11-15 18:34 UTC)
- GitLab branch `deploy/russian-tuqo-static-2026-11-15`: commit `22fcd4dabf8e1242d6abb9f4a0468af4d1de0708` adds `pruneMaxWebhookEvents({ before, limit })` to the YDB request store; docs follow in `f43c6865fcf67ac0da36ee12c346468e4360d281`.
- Cleanup requires an explicit valid cutoff and a batch size 1–500; only `received_at < cutoff` is eligible. YQL deletes selected primary keys using `DELETE FROM ... ON SELECT ... LIMIT`. No automatic schedule or implicit retention duration is configured.
- Factory run **43747461090** passed **45/45**, 0 failed, Node.js 22. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43747461090.md
- Exact selected-source snapshot branch `factory/max-failover-test-2026-11-15` HEAD: `f0aadd82318865c92481a6c5b86ed48999ae955c`. This is selected-file regression testing only, not GitLab CI, full repository CI, live YDB, MAX E2E or production.
- Latest GitLab branch HEAD after documentation: `f43c6865fcf67ac0da36ee12c346468e4360d281`. No MR, merge, or deployment. MAX bot/group and Russian runtime remain unprovisioned.
- Next: individual operator authentication/roles and audit design; then customer channel mapping/reply adapters. Do not enable MAX commands or subscribe webhook before Russian HTTPS:443 + YDB and verified operator accounts exist.


## 14. Per-operator auth primitives (2026-11-15 18:36 UTC)
- GitLab branch HEAD: `4ff95a79f48b4dbcbe8073ef5f449da5d03d406e`.
- Added `standby/security/operator-auth.mjs` and tests: strict `STANDBY_OPERATORS_JSON` parsing, independent SHA-256 bearer-token identities, constant-time digest comparison, disabled/unknown credential rejection, and viewer/operator/supervisor/owner permission matrix.
- Factory run **43747665597** passed **51/51**, 0 failed. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43747665597.md
- Snapshot HEAD `4bc657537730199b0713015a03db7d1cae49fe54`; selected-source suite only.
- Important boundary: auth helper is not yet wired into `/ops/inbox` or `/ops/retry`; HTTP panel still uses shared MVP token. Do not expose publicly. Durable YDB audit table/store and fail-closed route integration are next; no production deployment.


## 15. Per-operator RBAC + YDB audit wired into HTTP routes (2026-11-15 18:40 UTC)
- GitLab branch HEAD: `f19f21b2481e95269eaa4572031a1b948fed0f45`.
- `/ops/inbox` now requires `inbox:read`; `/ops/retry` requires `notifications:retry`. Operators are individually identified by SHA-256 bearer-token digest in strict `STANDBY_OPERATORS_JSON`; constant-time comparison; disabled/unknown credentials denied.
- YDB store creates `standby_operator_audit_events` and records minimal allowlisted audit events before inbox access or retry work. If audit write fails, protected route returns 503 before proceeding. Audit metadata excludes customer PII; target IDs are restricted.
- Legacy shared token is accepted only with explicit `NODE_ENV=test` or `development`; unset/production fails closed.
- Factory run **43748005666** passed **58/58**, 0 failed. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43748005666.md
- Snapshot HEAD `86ec8fe442fdae187ae068fef9b83f7c1cedf11b`; selected-file tests only, not GitLab CI, live YDB, multi-instance or production E2E.
- Remaining: audit read endpoint, denied-auth audit/rate limiting, live YDB DDL validation, secure production token provisioning, multi-instance tests, panel operator identity/role UX. Keep `/ops` off public production until these gates pass.


## 16. Role-protected audit read endpoint (2026-11-15 18:41 UTC)
- GitLab branch HEAD: `97d3cec66a6e281321d981abd730dca53cb696ff`.
- Added `GET /ops/audit`, restricted to `audit:read` (supervisor/owner). It writes an `audit.read` event before listing recent audit records. YDB listing returns only event/operator/action/target/outcome and sanitized metadata fields.
- Factory run **43748164089** passed **60/60**, 0 failed. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43748164089.md
- Snapshot HEAD `feea43f5d3c5e266295dc64eeb032c82bce9e7fa`; selected-file tests only, not live YDB or production E2E.
- Remaining: failed-auth audit, distributed rate limiting, mobile panel audit view, live YDB DDL/query validation, production operator credential provisioning, multi-instance testing. No Russian runtime/YDB instance or MAX bot/group exists; no merge/deploy.


## 17. Role-aware mobile audit panel (2026-11-15 18:43 UTC)
- GitLab branch HEAD after docs: `ac1ca3b744a6900ee7927e3f8ab410547f716550`.
- `/ops` now displays operator ID/role, hides retry unless `notifications:retry`, shows audit control only for `audit:read`, and renders audit entries via `textContent`. Token remains in tab memory; no browser storage.
- Factory run **43748317816** passed **61/61**, 0 failed. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43748317816.md
- Snapshot HEAD `70f3c94cc624fe1f46d52cd5dd5ae7af72958b26`; selected-source tests only.
- Remaining: failed-auth audit, distributed rate limiting, credential rotation workflow, live YDB validation, multi-instance and Russian network acceptance. No Russian runtime/YDB or MAX bot/group; no merge/deploy.


## 18. Failed-auth audit and throttling (2026-11-15 18:45 UTC)
- GitLab branch HEAD after docs: `c40894a262a115f966edbbbc9a55333c771b8ee8`.
- Unknown credentials and forbidden role actions create privacy-safe `auth.denied` / `auth.forbidden` audit events. Tokens, Authorization headers and customer PII are not logged.
- Per-process throttle: 10 failed attempts/IP/10 minutes, then HTTP 429. Forwarded IP is trusted only with `TRUST_PROXY=true`. Denial remains denial if audit write fails.
- Production caveat: in-memory throttle is not shared across instances; distributed rate limiting at Russian edge/reverse proxy is mandatory before multi-instance production.
- Factory run **43748471412** passed **62/62**, 0 failed. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43748471412.md
- Snapshot HEAD `6a2d0c2b6c36010a5e586410e33a87758d4487fb`; selected-source suite only.
- No Russian host/YDB or MAX bot/group provisioned; no MR/merge/deployment. Next: review audit/security edge cases, then Russian runtime provisioning feasibility and live YDB integration.


## 19. Strict test-only legacy credential gate (2026-11-15 18:47 UTC)
- GitLab branch HEAD after docs: `4e5589c917c3f432f945f7c9afbb3e755dfb339f`.
- Shared `STANDBY_ADMIN_TOKEN` is now accepted only with explicit `NODE_ENV=test`; development, unset and production all deny it. Production requires per-operator `STANDBY_OPERATORS_JSON` plus YDB audit.
- Factory run **43748653690** passed **63/63**, 0 failed. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43748653690.md
- Snapshot HEAD `fd4a27c4a851eec9c4030860e13719f7534a26db`; selected-source suite only.
- Remaining: distributed rate limiting, live YDB DDL/query verification, secure operator credential provisioning/rotation, multi-instance tests, Russian no-VPN acceptance. No Russian host/YDB or MAX bot/group provisioned; no MR/merge/deploy.


## 15. Durable admin startup gate verified (2026-11-15 18:50 UTC)
- Latest GitLab branch HEAD observed: `252306bed729c85eb47b210ff9368a960dea300a` (`deploy/russian-tuqo-static-2026-11-15`).
- Added `assertDurableAdminRuntime`: if per-operator administration or MAX webhook is configured, startup requires the durable YDB request store; per-operator administration additionally requires the audit-schema capability. Startup creates the audit table before listening. This prevents a configured admin panel/webhook from silently running with ephemeral/local storage.
- Factory run **43748987700** passed **64/64**, 0 failed. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43748987700.md
- Exact selected-source snapshot commit: `2043f6973173afcfcf74f931c935c12e2c38cabc`. This is selected-file regression testing only; GitLab CI still blocked by provider identity verification; no live YDB/MAX/Russian host E2E.
- Current `/ops` route auth and audit are now wired to per-operator config and durable audit store in the feature branch; legacy shared token is accepted only in explicit `NODE_ENV=test` fixtures. Still not production-ready: no live YDB permission/append-only enforcement, no rate limit persistence across instances, no actual operators provisioned, no Russian runtime, no MAX bot/group.
- Next: test and tighten production data-store permissions, multi-instance rate limiting, audit retention/backups, and verify panel privacy/no-store headers; then customer identity/reply-channel adapters. No MR merge or deployment.


## 16. Shared YDB authentication throttling (2026-11-15 18:54 UTC)
- GitLab branch HEAD `5c5805ad8f7ec249e2034975a6c3ca1533148bf8`.
- Added YDB table `standby_operator_auth_rate_limits`: SHA-256 digest of source IP only, serializable 10-minute failure counter, block after 10 failed attempts; if shared limiter fails, authentication denial path fails closed. Added bounded stale-bucket cleanup method (max 500 rows) with no automatic schedule.
- First Factory run `43749160893` exposed a fake-SQL test adapter issue: it did not model the literal initial counter `1`, resulting in 67/68. Production YQL uses literal `1`; test adapter corrected to default the omitted parameter to 1.
- Rerun **43749293947** passed **68/68**, 0 failed. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43749293947.md
- Exact selected-source snapshot commit `458d8f27984b643d067d09f10e17b89aebc43a1a`; selected tests only, not live YDB concurrency or GitLab CI.
- Next: verify YDB DDL/YQL against a real Russian YDB instance, establish a scheduled but bounded cleanup policy and backup/restore, then review database roles/permissions. No server provisioned or data deployed.


## 17. Bounded operator audit retention (2026-11-15 18:55 UTC)
- GitLab branch HEAD `9ffabe82130b4526135a8685ba9f3e71b57a94d7`.
- Added `pruneOperatorAuditEvents({ before, limit })`: explicit UTC cutoff, exclusive comparison, max 500 primary keys per invocation. No public endpoint, implicit retention period or scheduler.
- Factory run **43749431381** passed **69/69**, 0 failed. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43749431381.md
- Exact snapshot commit `b6c37e23ee1e83c7bfc533a8867918ee8a2371bc`; selected-source tests only, no live YDB execution.
- Next: review no-store/cache/security headers and backup/restore procedure; verify YDB DDL/DELETE/transactions against a real Russian instance before any deployment. Retention duration requires explicit legal/business approval.


## 18. Operator panel cache hardening (2026-11-15 18:57 UTC)
- GitLab branch HEAD `a2b9669940e9ffbc02717b92337006c19508c175`.
- `/ops` HTML now sends `Cache-Control: no-store, max-age=0`, `Cross-Origin-Resource-Policy: same-origin`, `Permissions-Policy` denying camera/microphone/location, plus existing `nosniff`, frame denial and CSP. JSON API responses already use no-store.
- Factory run **43749661826** passed **70/70**, 0 failed. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43749661826.md
- Snapshot commit `e098866b64f8867767bfadd959068fe06eeb63ed`; selected-file suite only.
- Previous run 43749560660 failed because test fixture did not create `ops.html` (404); fixture corrected and rerun passed. No production failure observed.
- Next: YDB live integration, DB role separation, backup/restore and a controlled retention maintenance plan. Russian runtime remains unprovisioned; no deployment.


## 19. YDB backup/restore runbook (2026-11-15 18:58 UTC)
- GitLab branch HEAD `2206b15426ed2e56f907db78c929992719d9d04d`.
- Added `standby/docs/YDB_BACKUP_RESTORE_RUNBOOK_2026-11-15.md`: inventory of request/idempotency/MAX/audit/rate-limit tables, Russian-only off-cluster destination requirement, proposed retention (not approved), YDB CLI backup/restore options, documented limitations, and mandatory isolated restore drill/RPO/RTO evidence.
- Official YDB docs reviewed: database dump/restore, tools dump/restore, S3 export/import. Current YDB docs warn that database restore does not restore column-table data or secrets; current standby schema uses row tables.
- No actual backup was created; no Russian YDB or backup target exists. Recoverability must not be claimed until a clean restore drill passes.
- 70/70 code tests remain the latest run; run 43749661826 report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43749661826.md


## 20. Complete YDB runtime gate + provider decision (2026-11-15 19:02 UTC)
- GitLab branch HEAD `18251cea75bf34adf077cf331849da73d58d7332`.
- Code fix commit `fdcd94c4`: production startup now requires the complete durable request lifecycle (`createEnquiry`, `getEnquiry`, `claimEnquiry`, `claimDueEnquiries`, `listPrivateEnquiries`, `completeDelivery`), durable MAX receipt recording when MAX is configured, and operator audit/rate-limit/read/write capabilities when individual operators are configured. This prevents a partial mock/adapter from passing startup while customer enquiries fall back to local JSON.
- Factory run **43750064228** passed **70/70**, 0 failed. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43750064228.md
- Exact selected-source snapshot commit `b0c24bb817b570a1ffe22d16a01aa8b70c382a97`; selected files only, not GitLab CI or live YDB.
- Provider selection: documented Yandex Managed YDB Serverless in Russia / `ru-central1` as preferred candidate. Official free tier lists 1m RU, 1 GB stored data, and two recent full automatic backups per month; usage beyond the tier is billed. This is not guaranteed zero-cost. Storage cap and billing alerts must be configured.
- Provider selection doc: `standby/docs/YDB_PROVIDER_SELECTION_2026-11-15.md`. Official source says managed YDB is distributed across three `ru-central1` availability zones. User account eligibility (+49 phone/payment acceptance) remains unverified; no account, card, payment, DB or service account created.
- Next: when user is ready, test their own Yandex ID/billing onboarding without paying or enabling billable resources; if successful, provision only Serverless in ru-central1 with strict caps and least privilege. Then live YDB DDL/transactions, Russia ISP checks and restore drill.


## 21. YDB schema/runtime privilege separation (2026-11-15 19:06 UTC)
- GitLab branch HEAD `73d213031c0605e6a8f8d5465fd79325a4feee71`.
- Production `INBOX_STORE=v2` now requires `YDB_SCHEMA_MANAGED_EXTERNALLY=true`. With this mode, runtime skips all `CREATE TABLE` DDL and performs read-only startup probes for required tables and both queue indexes. Missing schema/index causes startup failure.
- Added `standby/storage/ydb-schema-v3-operator-security.sql` for MAX webhook receipts, operator audit events and shared auth rate limits. Apply schema v2 then v3 with a separate migration identity; runtime identity should not receive CREATE/ALTER/DROP permissions. Documented in README, provider selection and backup runbook.
- Factory run **43750579755** passed **72/72**, 0 failed. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43750579755.md
- Exact selected-source snapshot commit `8fbe54ec54d44510733dfeda4f83132bc31f17f8`; selected files only, not GitLab CI or live YDB. Earlier runs 43750286136 and 43750452377 failed on stale test fixtures (fake SQL call shape and partial mock missing new capability); corrected and rerun 72/72. No production failure observed.
- YDB provider candidate remains Yandex Managed YDB Serverless in Russia / `ru-central1`, not provisioned. Free tier limits and billing guardrails documented. No Yandex account, payment or resource created.
- Next: independent review of YQL/DDL against official syntax, then user-owned Yandex Cloud onboarding only when ready, without payment; live YDB + Russian ISP + restore drill remain gates.


## 22. Production durable-storage fail-closed + least privilege (2026-11-15 19:18 UTC)
- GitLab branch HEAD `04d1cc0eed5de79c87bd9415eb508e8ae6bf5acb`.
- Critical guard added: `assertProductionRequestStore` makes production refuse startup unless `INBOX_STORE=v2`, `YDB_CONNECTION_STRING` is configured and a connected YDB request store exposes schema verification plus the full durable enquiry lifecycle. Production can no longer silently accept customer enquiries into local JSON when v2 is omitted.
- Runtime DDL nullability aligned with reviewed v3 migration; duplicate exported object property removed. Production schema remains externally managed, no DDL at runtime.
- Added `standby/docs/YDB_LEAST_PRIVILEGE_RUNTIME_GRANTS_2026-11-15.md`: separate owner, migration and runtime identities; per-table `SELECT ROW`, `UPDATE ROW`, `ERASE ROW` + database `CONNECT`; no broad ydb.editor/USE/INSERT/ALL for runtime; check inherited ACLs and owner status. This is a reviewed template, not applied.
- README now documents production storage fail-closed gate.
- Factory run **43751714424** passed **74/74**, 0 failed. Report: https://github.com/sokfrut-tech/Universal-AI-Factory/blob/main/coordination/shared/results/AVTOY_STANDBY_TESTS_43751714424.md
- Exact selected-source snapshot commit `5361ed131fe40808e581a60337272eacc27b4678`; selected files only, not GitLab CI or live YDB. Previous failure 43751609705 was a missing test import, fixed before 74/74.
- Official YDB docs confirm `VIEW IndexName` for secondary index reads, `DELETE FROM ... ON SELECT` for bounded deletion, granular `SELECT ROW`/`UPDATE ROW`/`ERASE ROW` and database `CONNECT`. See least-privilege doc.
- Provider update: free tier applies at payment-account level across all attached clouds/orgs; YDB allowance 1m RU, 1 GB/month storage and two recent full backups; overage billed. Source: https://yandex.cloud/ru/docs/billing/concepts/serverless-free-tier . Serverless default storage cap 50 GB; configure a lower cap after measuring and before traffic.
- No account/payment/database/resource provisioned. No real YDB test, Russian ISP test, restore drill or production deployment. No MR merge.
