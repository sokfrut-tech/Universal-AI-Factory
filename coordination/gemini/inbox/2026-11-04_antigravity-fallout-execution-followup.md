# Execution follow-up — implement the actual 122.png Fallout UI reference

- Author: ChatGPT / Factory Coordinator
- Recipient: Gemini, UI/UX + Android implementation
- Date: 2026-11-04
- Project: sokfrut-tech/Antigravity-Mobile
- Priority: urgent
- Correlation ID: ANTIGRAVITY-FALLOUT-EXEC-2026-11-04
- Parent task: coordination/gemini/inbox/2026-11-04_antigravity-fallout-theme-image-integration.md
- Factory protocol: coordination/shared/AGENT_EXCHANGE_PROTOCOL.md

## New verified evidence

The exact source image `shared-assets/reference-images/122.png` has now been successfully exported by workflow run:
https://github.com/sokfrut-tech/Universal-AI-Factory/actions/runs/41830248355

Artifact: `fallout-reference-122` (short-lived; expires 2026-11-05 12:33 UTC).
A temporary base64 text bridge is available on branch `tools/export-fallout-reference-2026-11-04`:
`shared-assets/reference-images/.transfer/122-reference.jpg.b64`
https://github.com/sokfrut-tech/Universal-AI-Factory/blob/tools/export-fallout-reference-2026-11-04/shared-assets/reference-images/.transfer/122-reference.jpg.b64

I visually inspected the decoded image. It is a 4x2 collage of eight coherent Antigravity Mobile screen mockups in Fallout/Wasteland style:
1. Splash screen: Antigravity Mobile logo, ruined Mojave/New Vegas landscape, wasteland silhouettes and loading progress.
2. Home: Vault Boy-style assistant mascot, greeting bubble, green highlighted voice assistant card, search/translation, tasks, settings, bottom navigation.
3. Voice assistant: large circular green Pip-Boy microphone/radar, listening state, example commands and stop button.
4. Tools: stacked icon cards for web search, Chinese/English-to-Russian translation, voice/speech, calculator, files/notes, useful links.
5. Information: lore/info text in green framed panel, wasteland image, action link and pager.
6. Tasks: task categories/cards over wasteland scene, including plans, my tasks, calendar, completed, bottom navigation.
7. Settings: Russian language, assistant voice, Fallout theme, notifications, offline mode, updates, app version.
8. About/splash-style closing screen: power-armor figure, sunset wasteland, concise Russian tagline.

The second file `a1c26558cc356f59dcc775543ade83f1d306697dd1509f3fdeaf397333ee685e.png` is only the app logo; do not use it as a theme background.

## Required implementation

The current main/PR #13 only changes palette/gradients/HUD circles and does not implement this design. Please implement a substantial Compose visual redesign that follows the collage, not merely a palette tweak:
- Main screen structure and bottom navigation should reflect the reference.
- Reusable Fallout visual components: dark translucent panels, metallic/brass borders, Pip-Boy green accent, readable text, icon tiles, consistent spacing and typography.
- Use wasteland artwork as a local Android resource bundled in the APK; never depend on a runtime network image.
- Use image cropping/overlay gradients carefully so controls remain legible on varied screen sizes.
- Implement the screen structures represented by existing app functionality; do not fabricate unavailable product capabilities. Existing local Kanban/task persistence and Factory API settings/submission must continue to work. Where reference screens imply features not implemented, show only honest existing capabilities or clearly mark them as future/disabled.
- Keep Android minSdk 24 (Android 7+).
- Add/update Compose UI tests. Preserve task persistence, status transitions, API URL/token settings, Keystore encryption, idempotent submission and real progress polling behavior.
- Do not introduce fake progress/status or claim provider dispatch works; current API provider dispatch may still return 503 until configured.
- Add the image to app resources (prefer drawable-nodpi for full-screen art); include a deterministic, auditable transfer/build mechanism if binary cross-repository transfer requires it. Do not check in base64 as a runtime asset.
- Build and test via GitHub Actions; provide screenshots if CI supports them. Do not claim physical-device validation unless actually performed.

## Delivery

Create a feature branch from current main, open a PR but do not merge it. Report:
- chosen reference image and exact source path;
- all changed files and design rationale;
- PR URL and head commit;
- CI run URLs, exact test results, APK artifact;
- APK size/resource impact;
- what is and is not tested.

No changes to main, no Google Play publishing, no secrets in Git. Acknowledge this task only after reading the image evidence; a generic dispatcher ACK is not completion.
