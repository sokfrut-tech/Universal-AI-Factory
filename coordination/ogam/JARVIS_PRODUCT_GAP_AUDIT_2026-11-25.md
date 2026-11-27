# Jarvis product gap audit — 2026-11-25

## Executive finding

The APK published as `Jarvis-OGAM-arm64-release.apk` is **not yet a distinct, finished Jarvis AI assistant**. It is an ARM64 Android build of the upstream Off Grid AI application forked into `sokfrut-tech/OGAM`, with Jarvis-related implementation work layered onto that codebase. The user's objection that the downloaded app does not yet represent the intended Jarvis product is valid.

## Verified repository facts

- Repository: https://github.com/sokfrut-tech/OGAM
- Repository metadata identifies it as a fork of `off-grid-ai/OGAM`.
- The current README still brands the app as **Off Grid AI**, calls it an on-device AI suite, and documents a Pro tier; it does not present a finished Jarvis product.
- Current package manifest: `name=offgrid-mobile`, `version=0.0.125`; Android application ID in the inspected release workflow/package evidence is `ai.offgridmobile`.
- The published APK release tag is `jarvis-ogam-arm64-2026-11-25`; its release notes pin source commit `750bae3f01ca32c3471c90d95d0367f512737814` and SHA-256 `85130f7b765787d501a480cdbf8aafcc869b710c3653ddb783b4cf1a43685981`.
- That release proves a signed standalone APK was built and published. It does **not** prove Jarvis product identity, local model provisioning, end-to-end Russian voice, assistant-role operation, or successful runtime on OPPO PGEM10.

## Current Jarvis-related work — do not overstate

Open draft PRs in OGAM show an incremental memory implementation chain:
- PR #4: M1 isolated memory database foundation.
- PR #7: M2 secret guard, conflicts, tombstones, confirmation UI and Android probe.
- PR #8: M3 management and M4 deterministic prompt retrieval.
- PR #9: M5 security/resilience hardening, adversarial tests and a separate native probe app.

These are draft, stacked implementation changes. PR #9 is based on PR #8, not directly on main. They are not evidence that the complete Jarvis assistant is already integrated into the distributable app. The separate draft PR #1 is storage/privacy and Android permission bridge work. OGAM PR #2/#3 are research/architecture work. Keep the separate `sokfrut-tech/Gemeni` project isolated.

## Product acceptance definition

Do not call a release "Jarvis AI" until the following are demonstrated on the actual target phone (OPPO Find X6 Pro PGEM10, Snapdragon 8 Gen 2, Android 16 / ColorOS):

1. **Identity and onboarding** — the app is clearly branded Jarvis; the first-run flow explains offline/online modes, model setup, microphone permissions and privacy.
2. **A real brain** — at least one compatible local model can be downloaded/imported, integrity-checked, loaded, selected and used for a Russian conversation; no fake/demo response path.
3. **Russian voice loop** — microphone capture → VAD/ASR → model response → TTS playback works repeatedly, with cancellation, permission denial and interruption handled.
4. **Persistent memory** — the M1–M5 memory chain is reviewed, integrated in dependency order, tested and exposed to the user with inspect/edit/delete controls; no silent model writes.
5. **Phone actions** — a small, explicit allowlist of Android actions works through deterministic typed tools, with visible confirmation for sensitive actions and postcondition verification.
6. **Background/assistant integration** — foreground/background lifecycle, audio focus, Android assistant role and ColorOS restrictions are tested; do not claim always-on wake word without measured battery and OEM tests.
7. **Reliability and privacy** — offline smoke test, network-disabled test, crash/recovery, storage/migration, permission and prompt-injection tests pass. No secrets or personal data in logs.
8. **Release evidence** — exact commit, reproducible build, checksum, test report, APK install/launch evidence and a user-verified PGEM10 acceptance result are attached to the release.

## Ordered implementation plan

### Phase A — establish a clean product baseline
- Freeze and label the current APK as an experimental Off Grid AI-derived engineering build, not the finished Jarvis product.
- Inspect OGAM PR #1–#9 and their exact-head checks; resolve the stacked PR dependency chain in order. Do not merge a downstream PR before its base is integrated and verified.
- Inspect actual app entry points, navigation, model registry/download/load flow, voice service, permissions and Android manifest. Separate existing upstream capabilities from Jarvis additions.

### Phase B — build the minimum real Jarvis vertical slice
- Add Jarvis identity/onboarding without removing upstream attribution or violating upstream license obligations.
- Deliver one end-to-end Russian text session with a real local model and visible model status.
- Add push-to-talk Russian speech input and speech output as a bounded, foreground-first flow. Defer always-on wake word.
- Integrate memory only after the M1–M5 chain is reviewed and CI/native SQLite gates pass.
- Add only 2–3 safe phone actions with typed schemas, explicit confirmation and postcondition checks.

### Phase C — device and release acceptance
- Build a new APK from the integrated branch, not from an unrelated or stale commit.
- Test installation, launch, model load, offline Russian chat, speech loop, memory persistence and approved actions on PGEM10.
- Publish as a clearly named Jarvis alpha only after those checks; state limitations and checksum.

## Immediate blockers / unknowns

- No evidence in the reviewed release record that a local model was bundled or successfully provisioned and loaded on PGEM10.
- No verified end-to-end Russian ASR + LLM + TTS loop on the target device.
- No verified Android assistant-role activation or ColorOS background behavior.
- No physical-device acceptance result.
- The memory PR chain remains draft and stacked; exact-head CI/native probe results must be read before integration.

## Evidence labels

- **Verified:** repository is a fork of Off Grid AI; current README and package identity remain Off Grid; standalone APK release asset exists with pinned source commit and checksum; PR #4/#7/#8/#9 are open draft PRs.
- **Implemented, not accepted as product:** Jarvis-related memory modules and probes are present in draft branches.
- **Unverified:** complete Jarvis UX, local model runtime on PGEM10, Russian speech loop, assistant role, safe phone actions and real-world battery/thermal behavior.
- **Not done in this audit:** no source code, workflows, secrets, deployments, PR merges or device state changed.

## Handoff

Next executor should start by reviewing exact-head checks and diffs for PR #4, #7, #8 and #9 in dependency order, then inspect the app's actual model and voice entry points. The goal is a demonstrable vertical slice, not another documentation-only APK rename.
