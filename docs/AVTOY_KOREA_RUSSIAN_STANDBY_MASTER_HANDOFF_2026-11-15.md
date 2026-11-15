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
