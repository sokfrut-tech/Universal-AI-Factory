# Antigravity Mobile — Fallout reference asset handoff record

- Автор: ChatGPT / Factory Coordinator
- Дата: 2026-11-04
- Проект: Antigravity-Mobile
- Correlation IDs: ANTIGRAVITY-FALLOUT-ASSET-2026-11-04; ANTIGRAVITY-FALLOUT-REVIEW-2026-11-04

## Purpose of the folders

- `shared-assets/reference-images/` is the persistent, cross-project library for original reference images, logos, UI screenshots and design examples. Keep originals here.
- `shared-assets/reference-images/.transfer/` is a temporary technical bridge used only when an integration cannot transport binary image files directly. It may contain compressed JPEG/base64 transfer copies and should not be treated as the canonical source or as the app asset directory.
- Android implementation must copy the selected, verified reference into the Antigravity-Mobile app's own Android resource folder so it is packaged inside the APK. The runtime app must not depend on GitHub or the temporary bridge.

## Current image inventory

1. `shared-assets/reference-images/122.png` — user-provided image; expected candidate Fallout/UI reference. Its contents have not yet been visually verified in this session.
2. `shared-assets/reference-images/a1c26558cc356f59dcc775543ade83f1d306697dd1509f3fdeaf397333ee685e.png` — inspected via the temporary export bridge; it is the Antigravity Mobile launcher logo, not the Fallout background. Do not use it as the Fallout theme image.

## Temporary export findings

- Workflow `.github/workflows/export-reference-image.yml` on branch `tools/export-reference-image-2026-11-04` initially exported the hashed launcher-logo image to `.transfer/reference-image.jpg.b64`.
- Run `41807213839` uploaded an artifact but failed at publishing the text bridge because that destination already existed. The artifact is the launcher logo and is not the Fallout reference.
- The workflow was edited in commit `ba53b061427215f7194fb5766ad3d2f7aeab6ece` to select `122.png`, but that branch was based on a commit predating the upload of `122.png`. Run `41830100479` therefore failed with `FileNotFoundError: shared-assets/reference-images/122.png`.
- A fresh isolated branch `tools/export-fallout-reference-2026-11-04` was created from current main and contains a temporary exporter for `122.png`. No successful run/artifact is confirmed yet.

## Required next actions

- Gemini: visually inspect `122.png`, compare it to current UI, and propose/implement the actual Fallout theme in a separate Antigravity-Mobile feature branch and PR.
- Claude: independently review current PR #13 and the eventual implementation PR; do not treat dispatcher ACK as review completion.
- Android implementation: package the selected image locally in the APK, preserve app functionality, and add UI tests.
- QA/security: verify build, emulator tests, artifact provenance and security checks; real-device validation remains separate.
- Do not publish to Google Play. Do not merge the implementation PR without evidence and review.

## Exchange status

Task messages were created in Gemini and Claude inboxes under `coordination/`. The Claude inbox dispatcher produced only its automatic receipt; it does not prove Claude read or executed the task. Gemini has no substantive response for this new task yet. The provider dispatch endpoint in Antigravity-Mobile's Factory API remains intentionally disabled until a real provider adapter is implemented.
