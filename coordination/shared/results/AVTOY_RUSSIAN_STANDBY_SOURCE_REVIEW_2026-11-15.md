# AVTOY Russian standby mirror — independent source review

Date: 2026-11-15
Reviewed ref: `deploy/russian-tuqo-static-2026-11-15`
Reviewed commit: `2ab8c4751cad6b105e6936eb9f597afbbc47639a`
Project: `sokfrut/avtoY-korea-auto` (GitLab project 88934554)

## Scope inspected

- `standby/scripts/inventory-approved-media.mjs`
- `standby/scripts/mirror-approved-media.mjs`
- `standby/scripts/verify-public-parity.mjs`
- `standby/scripts/export-live-public-catalog.mjs`
- `standby/scripts/build-public-snapshot.mjs`
- `standby/scripts/media-order-eligibility.mjs`
- `standby/package.json`
- `standby/README.md`
- `standby/docs/GITLAB_PAGES_DEPLOYMENT_GATE_2026-11-15.md`
- Related inventory and parity tests.

## Confirmed design protections

1. Inventory is explicitly private, rejects output under `public/`, writes with mode 0600, and reports sanitized failure codes rather than Telegram token-bearing error text.
2. Mixed photo/video albums are marked ambiguous unless the explicit `mediaItems` source sequence is accompanied by `mediaOrderKnown === true`.
3. Mirror download stages a complete media generation, enforces byte limits and media-type checks, validates photo signatures/dimensions, preserves recognized video container extensions, and commits through a recovery journal. On a download failure it removes staging and refuses to publish a partial map.
4. Public snapshot builder refuses incomplete car media and approved review media; the parity verifier compares approved source IDs, sanitized text, exact media types and exact media order, and fails closed on excluded eligible source records.
5. Live export is restricted to the expected HTTPS Worker hostname, accepts only same-origin `/api/` media paths, stages downloads before replacing the media directory, and rolls back on snapshot/media publication failure.
6. Documentation explicitly states that no production export, DNS, Telegram webhook, Yandex resource creation, or paid resource activation is authorized.

## Findings / gates

- No source-level defect was confirmed in the reviewed ordering, privacy-path, media validation, or staged-publication logic.
- The reviewed GitLab Pages gate states CI is blocked before jobs start by account identity verification. This is an infrastructure restriction, not a test failure. Do not evade it.
- The reviewed scripts and tests were inspected as source, but this review did not execute the GitLab branch test suite. The current GitLab branch has no demonstrated successful test-run evidence in the inspected material. Syntax/test execution and a real sanitized-export → mirror → parity → static-build run remain required before calling the Russian mirror ready.
- The live export path and approved-KV mirror path are alternative data acquisition paths; do not mix their inputs. The approved-KV route must run inventory, mirror, snapshot build, parity, manifest, and static build in that order.
- Real production media has not been exported or parity-checked. No claim is made that the backup catalogue currently contains the live approved catalogue.

## Release decision

**Not release-ready yet.** Keep GitLab Pages deployment manual and disabled until the full local test suite and a sanitized fixture end-to-end run pass. Then require owner approval for any real approved-data export or paid/cloud resource activation. No production services were changed during this review.

## Execution independence

This review was performed by the primary ChatGPT coordinator. No Claude/Gemini review was received or required. It is a self-review, not an independent third-party audit.
