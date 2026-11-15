# AVTOY KOREA — Static mirror pipeline source review

**Date:** 2026-11-15  
**GitLab project:** `sokfrut/avtoY-korea-auto` (88934554)  
**Branch inspected:** `deploy/russian-tuqo-static-2026-11-15`  
**Latest branch commit recorded in handoff:** `e3ccc7eb8fa8225a522cf771f0e172b356d2679b`  
**Production:** no live export, object-storage upload, Pages deploy, DNS change, or payment performed.

## What the source currently does well

- `export-live-public-catalog.mjs` reads public `/api/cars` and `/api/reviews` from the exact approved Worker hostname over HTTPS.
- It accepts only same-origin `/api/` media paths, downloads media into a staging directory, enforces 25 MB per item and allowlists image/video MIME types.
- It writes the public snapshot to `data/public-snapshot.json`, stages media in `public/media`, and attempts rollback if publishing the media generation or snapshot fails.
- `mirror-approved-media.mjs` uses Telegram file IDs only in the private export step, keeps the private media map outside `public/` with mode 0600, deduplicates media, validates downloaded image signatures/dimensions, limits media bytes, and commits a full media generation through a transaction journal.
- `build-public-snapshot.mjs` rejects output inside `public/`, sanitizes text, requires local media-map URLs, rejects ambiguous mixed albums and fails rather than silently omitting incomplete approved media.
- `verify-public-parity.mjs` checks eligible approved IDs, sanitized text, media types and exact ordered media URLs; it rejects extra/missing records and public fields outside allowlists.

## Important integration observations

1. The live-export script currently downloads from the Cloudflare Worker API, so it is a one-time/controlled export pipeline; it is not a static site host itself.
2. The static builder consumes the sanitized snapshot plus local media and emits a separate `pages` tree. This is the likely frontend payload for SourceCraft/GitVerse, not the original private repo root.
3. SourceCraft/GitVerse static output must be built from a public-only artifact/repository. Never publish the private export, media map, Telegram identifiers, bot credentials, moderation records or source KV dump.
4. SourceCraft origin cannot directly call the existing Worker APIs as a drop-in replacement: the embedded AVTOY page uses relative same-origin API calls, while the inspected Worker has no CORS allow-origin/preflight support. A static snapshot should instead consume the prebuilt JSON and media URLs, or a separately reviewed API/CORS architecture.
5. Cloud.ru Object Storage remains the likely separate media origin. Before relying on it, test public-read policy, CORS, content-type preservation, range requests for video, cache headers, object naming, and exact free-tier/billing behavior. No bucket has been created.

## Test coverage gap / CI status

- The standby package's `check` script includes syntax checks for `export-live-public-catalog.mjs` and `mirror-approved-media.mjs`.
- The package test list includes tests for snapshot building, parity, media order eligibility, transactions, static catalog build, object-storage publishing and other helpers.
- The source review did not identify dedicated tests named `export-live-public-catalog.test.mjs` or `mirror-approved-media.test.mjs`. Their most safety-critical behavior is therefore not directly covered by a dedicated end-to-end mocked-fetch test at this point.
- GitLab pipeline previously failed before jobs were created; that is not evidence that tests passed or failed. The exact commit `e3ccc7eb` media-order fix remains unexecuted in GitLab CI.
- Next: build an isolated Node harness for the exact source bytes and add focused mocked-fetch/rollback tests for the live exporter and Telegram mirror script; run it on the working Factory GitHub runner. Clearly label copied-source tests as such, not as a full GitLab branch run.

## Next steps

1. Finish reviewing `build-static-catalog.mjs`, `verify-static-origin.mjs`, and object-storage publisher for path/CORS/range/cache behavior.
2. Add dedicated exporter and mirror tests (success, MIME rejection, size cap, incomplete album, failed download, rollback, no partial publication).
3. Run tests on Factory runner using exact source snapshots with commit/checksum provenance.
4. Produce a static-only prototype in a non-public local/staging path; verify sanitized output and media order.
5. Only after all gates pass, ask the user to choose SourceCraft/GitVerse and/or Cloud.ru registration. No account creation, card binding, balance top-up, public push, Pages deployment, or production changes without explicit approval.
