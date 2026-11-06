# Universal AI Factory — Master Project Index
Updated: 2026-11-06

Purpose: the single entry point for resuming active projects without relying on chat history. Repository state is the durable source of truth.

## Global operating rules
1. ChatGPT is the default coordinator and implementer. Continue independently when external agents are unavailable.
2. Gemini is a quota-limited escalation expert only: use for a genuine blocker, difficult architecture choice, or independent high-risk review. Do not trigger on routine inbox pushes. Batch questions; keep retries low.
3. Claude API is optional. Missing ANTHROPIC_API_KEY must not block other work.
4. An agent plan is not an implementation. Require a patch/commit and test evidence. Empty ACK files are not deliverables.
5. Prefer free, local and offline-first solutions. No paid APIs or unexpected spending without explicit approval.
6. Before merge/deploy inspect the diff, run tests/build/security checks and verify the exact result. Failed required checks must block deployment.
7. Ask the user only for decisions, credentials, device actions or other steps that cannot safely be done by the agent. User mainly works from Android phone.
8. Maintain a cross-project technology radar: research useful tools, algorithms and implementation mechanics; adopt only after license, security, compatibility and test review. Research is not integration.

## Jarvis AI source audit
- Primary repository: [sokfrut-tech/Gemeni](https://github.com/sokfrut-tech/Gemeni).
- Repository-wide audit and cross-language source inventory: [docs/REPOSITORY_WIDE_AI_AUDIT_2026-11-06.md](https://github.com/sokfrut-tech/Gemeni/blob/main/docs/REPOSITORY_WIDE_AI_AUDIT_2026-11-06.md).
- Jarvis is an AI agent, not only a voice assistant. Preserve reasoning, planning, memory, perception, tool use, controlled learning and evidence-based execution as core product requirements.

## Cross-project technology radar
- Research snapshot and adoption gates: [docs/TECHNOLOGY_RADAR_AI_TOOLS_2026-11-06.md](TECHNOLOGY_RADAR_AI_TOOLS_2026-11-06.md).
- Reusable patterns: typed tools/skills, bounded agent loop, action verification, controlled memory, local-first fallbacks, safety confirmations, device E2E evidence and model provenance.

## Project index

| Project | Repository | Handoff | First resume step |
|---|---|---|---|
| Factory | sokfrut-tech/Universal-AI-Factory | docs/FACTORY_CONTINUATION_BRIEF.md | Audit dispatcher, workflows and a real end-to-end task |
| StampCleaner / Neon Club | sokfrut-tech/stamp-cleaner | https://github.com/sokfrut-tech/stamp-cleaner/blob/main/docs/PROJECT_HANDOFF_2026-11-06.md | Inspect PR #4/source; validate cleaning pipeline and dancer animation |
| Jarvis AI (primary) | sokfrut-tech/Gemeni | https://github.com/sokfrut-tech/Gemeni/blob/main/docs/REPOSITORY_WIDE_AI_AUDIT_2026-11-06.md | Review [PR #78 safe runtime integration](https://github.com/sokfrut-tech/Gemeni/pull/78), then implement [Phase B local reasoning runtime](https://github.com/sokfrut-tech/Gemeni/blob/integration/jarvis-safe-agent-runtime-2026-11-06/docs/agents/BRIEF_LOCAL_REASONING_RUNTIME_PHASE_B_2026-11-06.md) after CI/device gates |
| RussSearchOPPO (voice/translation baseline) | sokfrut-tech/RussSearchOPPO | https://github.com/sokfrut-tech/RussSearchOPPO/blob/main/docs/PROJECT_HANDOFF_2026-11-06.md | Preserve Vosk, translation and ColorOS modules for Jarvis reuse |
| Antigravity Mobile | sokfrut-tech/Antigravity-Mobile | https://github.com/sokfrut-tech/Antigravity-Mobile/blob/main/docs/PROJECT_HANDOFF_2026-11-06.md | Inspect APK/source/API; connect UI to real factory state |
| AVTOY KOREA | sokfrut-tech/avtoy-korea-auto | https://github.com/sokfrut-tech/avtoy-korea-auto/blob/main/docs/PROJECT_HANDOFF_2026-11-06.md | Recheck PR #55/Worker; verify private inquiries and Telegram media |
| Forest 4G | No dedicated repository confirmed | This document, below | Confirm measurements and create/confirm dedicated repo before implementation |

## Forest 4G connectivity — planning brief
Goal: reliable 4G deep in a forest, prioritizing reception margin and weather resilience over lowest price. A temporary shelter setup should later be portable to a future forest home. 5G is not required.

Known context: bands B3, B38, B31 (450 MHz), B20 and B7 have been discussed. Existing VARIUS Forester MIMO 2x2 antenna is installed but connection is unstable during weather changes.

Requirements:
- Confirm operator bands, signal measurements and router/modem support at the actual installation point.
- B31/450 MHz is a key requirement; verify chipset, firmware and operator compatibility, not just marketing claims.
- External MIMO antenna, appropriate connectors/cable-loss budget, weatherproof mounting, safe grounding/lightning protection.
- Keep vulnerable modem/router electronics protected indoors, not exposed on the mast.
- Consider dual-SIM/operator failover only after checking coverage and device support.
- Compare Russian-market/Ozon and KROKS options; verify specifications and availability.
- Prefer a compact kit transferable from temporary shelter to future home.

Next step: record operator/SIM, per-band RSRP/RSRQ/SINR, antenna model/cable and candidate datasheets. No purchase recommendation until B31 and environmental suitability are verified.

## Jarvis AI — 2026-11-06 live handoff
- Integration branch: sokfrut-tech/Gemeni / integration/jarvis-safe-agent-runtime-2026-11-06.
- Draft PR #78: https://github.com/sokfrut-tech/Gemeni/pull/78 — active ASR transcript now routes through the provider contract, strict proposal validator and Android tool gateway; dialer actions require explicit approval.
- Honest capability boundary: current local provider is deterministic command parsing, not a neural LLM. Real on-device inference is Phase B; brief is linked in the project row above.
- PR #60 truncates three handoff documents; PR #78 restores them from current main. Do not merge #58–#63 blindly.
- CI/security/emulator checks are still running; refresh exact-head results before merge. No APK release or OPPO runtime acceptance is claimed.
- Auto-repair workflow no longer pushes artifacts directly to main; repair evidence is retained as an artifact to avoid non-fast-forward races.

## Resume protocol
1. Open this index and the project handoff.
2. Recheck default branch, open PRs, latest commits, Actions, releases and deployment. Historical statuses below are leads, not live truth.
3. Read linked architecture, QA and decision documents; prefer newest source-backed evidence.
4. Inspect source before describing implemented functionality.
5. Start with the first unchecked P0 item. Make a small change and run targeted then full relevant checks.
6. Record commit SHA, exact tests/results, artifact URL and remaining risks.
7. Use status labels: Verified (checked now), Historical (must recheck), Planned, Implemented-unverified, Blocked (with evidence and next action).

## Jarvis AI — local inference runtime decision (2026-11-06)
- Preferred first neural runtime spike: llama.cpp through an app-owned JNI adapter, pinned to upstream commit 954de248ac6907dd05dc19f0f511ab18f2807a54.
- The current Arm AI Chat wrapper is not drop-in compatible: its library declares minSdk 33; generic llama.cpp Android NDK guide example uses API 28. API24 compatibility remains unproven.
- MLC LLM is deferred to a physical-device Adreno GPU experiment; ONNX Runtime Android package availability alone does not prove generative LLM support.
- Jarvis source has no real local neural inference yet. The prompt-echo placeholder was removed and a regression test added.
- Technical decision: https://github.com/sokfrut-tech/Gemeni/blob/integration/jarvis-safe-agent-runtime-2026-11-06/docs/engineering/2026-11-06-local-inference-runtime-decision.md
- Phase B brief: https://github.com/sokfrut-tech/Gemeni/blob/integration/jarvis-safe-agent-runtime-2026-11-06/docs/agents/BRIEF_LOCAL_REASONING_RUNTIME_PHASE_B_2026-11-06.md
- Safe runtime PR #78: https://github.com/sokfrut-tech/Gemeni/pull/78

### Jarvis model shortlist update — Qwen3.5 (2026-11-06)
- Official Qwen3.5-0.8B is Apache-2.0; official ggml-org GGUF Q4_0 candidate is 563 MB, pinned revision 4c11520cef475dd40ed72ec4a1e68b26721bd769, SHA-256 57d1997790d1744fba5b40a7317df71ea5e2acee28c47e78f0cce39c0703f8cf. Use for initial runtime bring-up only, not as a quality promise.
- Qwen3.5-2B instruction model is Apache-2.0. bartowski Q4_K_M conversion is around 1.40 GB and is the primary quality/size candidate; pin exact conversion revision and SHA-256 before download/installation because it is third-party.
- Full evidence and gates: https://github.com/sokfrut-tech/Gemeni/blob/integration/jarvis-safe-agent-runtime-2026-11-06/docs/engineering/2026-11-06-local-inference-runtime-decision.md
- No model has been integrated into the APK or benchmarked on the OPPO device yet.

## Jarvis complete assistant capability roadmap — 2026-11-06
- Design PR #81: https://github.com/sokfrut-tech/Gemeni/pull/81 (draft, documentation only; not an implementation claim).
- Full capability design: https://github.com/sokfrut-tech/Gemeni/blob/feature/jarvis-phone-control-foundation-2026-11-06/docs/engineering/2026-11-06-phone-control-design.md
- Explicit product scope now includes: intelligent planner and tasks; calendar read/write; reminders, timers and alarm clock; web search and safe browser surfing; local music; internet radio; media controls; Russian voice interaction; local-first reasoning and controlled memory; maps/navigation; weather/news/utilities; and phone/system control.
- Multi-step execution must be bounded, cancellable and tool-by-tool policy checked. The assistant must verify postconditions and never claim success from a launched screen or unverified request.
- Calendar writes, messages, sensitive settings and external side effects require user review/approval. Browser automation must not handle credentials, purchases or destructive submissions without explicit review. No DRM/paywall/access-control circumvention.
- Core should remain free and offline-first. Internet-only services are clearly labeled; online model fallback is optional and opt-in.
- Platform source audit: minSdk=29, targetSdk=35 on current main; Android 7/API24 is not currently supported. Accessibility service is empty and its broad XML scope must be narrowed before implementation.
- PR #78 CI run #42277569386: secret scanning and CodeQL succeeded; emulator smoke test was still in progress at the latest check. Recheck before any merge.
- Next: finish the active emulator CI diagnosis, then implement small tested vertical slices in dependency order: typed tool/capability contracts -> local planner/reminders/alarms -> calendar -> media/radio -> web assistant -> broader integrations and local neural reasoning.


### Jarvis strict privacy and on-device learning — mandatory invariant
- Intelligence growth must happen locally: user-approved memory, corrections, task outcomes, local skill/rule refinement and (only if feasible) on-device model adaptation.
- Be honest about learning type: updating memory/retrieval/rules is not the same as training model weights. Any local weight update must be versioned, regression-tested and rollback-capable.
- Default network egress from private context is forbidden: no telemetry, analytics, crash uploads, conversation/memory sync, training-data uploads or background content transmission.
- Web search/radio are permitted network functions, but send only the minimum query/URL explicitly requested. Never append private memory, contacts, calendar, messages, files or notification contents to network requests automatically.
- Cloud model fallback is OFF by default. If later offered, it must be per-request, show the exact data leaving the device and require explicit user confirmation. A model/agent cannot enable it autonomously.
- Audit manifests, SDKs, dependencies, endpoints and background workers; automated tests must prove local memory/learning/inference do not make outbound calls.
- User controls: inspect, correct, reset and delete local memory/learning data; backups only by explicit user action and protected locally.
- Full privacy contract and acceptance gates: https://github.com/sokfrut-tech/Gemeni/blob/feature/jarvis-phone-control-foundation-2026-11-06/docs/engineering/2026-11-06-phone-control-design.md


### Jarvis local learning implementation slice — 2026-11-06
- Draft stacked PR #82: https://github.com/sokfrut-tech/Gemeni/pull/82 (base is runtime PR #78; do not merge independently or before dependency reconciliation).
- Adds app-private, bounded correction memory with explicit opt-in disabled by default, exact normalized retrieval, correction replacement, size caps and clear operation.
- Adds unit tests for default-off, opt-in, normalization, replacement, disabling, deletion, invalid inputs and bounded retention.
- Manifest now disables Android backup and device transfer, with explicit data-extraction exclusions, to prevent silent backup/migration of app data.
- This is memory/retrieval learning only, NOT neural model-weight training; it is not yet integrated into the assistant reasoning loop or settings UI.
- CI has not yet reported a run for PR #82 at the time of this entry. Build, tests, manifest validation and network-egress review remain pending.


### Jarvis Creative & Development Studio — 2026-11-06
- Product direction: evolve Jarvis into a phone-first, local-first AI creative/development studio, with Qwen as the primary reasoning/coding core and specialist local models/runtimes for vision, image generation, ASR/TTS and audio.
- Full brief: `sokfrut-tech/Gemeni/docs/engineering/2026-11-06-jarvis-creative-development-studio.md` on PR #81 branch; PR #81 remains documentation-only.
- Target capabilities: project/code reading and editing, Python workspace and sandboxed execution, Android project generation and local APK builds, playable games, image understanding and actual image generation/editing, poetry/writing and specialist audio tools.
- Core privacy invariant: no telemetry, prompts, source code, images, audio, memory or project files leave the phone in local mode. Any online search/generation/build is explicit per task and discloses exact data first.
- Qwen is not treated as a universal image/audio generator: separate specialist models and runtimes are required. Local diffusion, Python native wheels, Android SDK/Gradle and game-engine support must be benchmarked on the OPPO Find X6 Pro before capability claims.
- Delivery sequence: device/runtime benchmark -> local Python/code vertical slice -> on-device APK factory -> image/creative studio -> playable game factory -> local learning integration.
- This is an approved product brief, not shipped functionality. No capability is marked implemented until an end-to-end on-device test proves it.


### Jarvis local runtime assessment — OPPO Find X6 Pro — 2026-11-06
- Runtime assessment: `sokfrut-tech/Gemeni/docs/engineering/2026-11-06-jarvis-local-runtime-assessment-oppo-find-x6-pro.md` on PR #81 documentation branch.
- Candidate stack: llama.cpp Android/GGUF as portable Qwen baseline; Qualcomm GenieX/QAIRT as an optional Snapdragon 8 Gen 2 acceleration path; Qwen3-VL as a separate vision-language path; Chaquopy 17.2 as the embedded Python candidate; dedicated SD1.5/QNN path for first local image-generation benchmark.
- Official/runtime docs reviewed: llama.cpp Android guide, Qwen3.5 repository, Qualcomm GenieX/QAIRT Android support, Chaquopy 17.2 Android setup. Chaquopy docs state minSdk 24 and arm64-v8a support; current Jarvis app minSdk 29 is compatible in principle, but Gradle/runtime integration still needs build verification.
- Important hardware caveat: Snapdragon 8 Gen 2 appears in Qualcomm's supported-device matrix (Hexagon V73), and SD1.5 NPU is a plausible local image-generation target. SDXL/newer DiT/video pipelines are not assumed supported on this generation.
- APK building directly on-device remains a separate feasibility spike: embedded Python does not provide Android SDK/Gradle. No source upload or cloud build fallback without explicit per-task consent.
- No runtime is claimed integrated or benchmarked on the physical OPPO. Next proof: device identity/resource probe, Qwen small-model inference smoke test, isolated offline Python execution, and independent SD1.5 local generation benchmark.


### Jarvis device capability probe — PR #83 — 2026-11-06
- Draft PR: https://github.com/sokfrut-tech/Gemeni/pull/83
- Branch: `feature/jarvis-device-capability-probe-2026-11-06`, based on runtime integration branch used by PR #78.
- Adds local-only Android device probe for manufacturer/model/hardware/SoC, API, ABIs, RAM, app heap cap, free app storage, low-memory and thermal status.
- Adds conservative model runtime budget selector and deterministic threshold unit tests.
- No network, analytics, telemetry or user-content access in this component.
- Latest head `4b3c67a98cd1e704e4dd26a5e33b4cd2049cfd3f`; preflight tiering was refined to use system-available RAM rather than Java heap (native inference memory is not Java heap). PR currently reports mergeability unknown/false; no CI run was returned yet, so tests/build remain unverified.
- This is the first executable foundation for measuring the target OPPO rather than guessing which Qwen/model tier it can handle. UI integration and physical-device measurement remain next.


### Jarvis CI checkpoint — 2026-11-06 19:43 UTC
- PR #78 run #93: latest job snapshot — secret scan and CodeQL succeeded; debug APK build completed; emulator smoke tests still in progress. The prior attempt failed during ADB split-APK installation before any test executed; the retry has progressed past APK build and is now at the emulator test step. No emulator result yet.
- PR #82 run #98: secret scan succeeded; CodeQL job completed Kotlin build, full debug APK build, APK verification/hash and upload steps; emulator smoke tests are in progress. CodeQL analysis is queued after emulator. No full CI conclusion yet.
- PR #83 run #103: secret scan succeeded; CodeQL job completed Kotlin build, full debug APK build, APK verification/hash and upload steps; emulator smoke tests are in progress. CodeQL analysis is queued after emulator. No full CI conclusion yet.
- Rechecked latest jobs on 2026-11-06: PR #78 emulator job 128112867371 in progress; PR #82 emulator job 128107922074 in progress; PR #83 emulator job 128112530329 in progress. Do not mark any PR fully green or merge stacked PRs #82/#83 before PR #78 dependency chain is reconciled.


### Jarvis Python Studio isolated-runtime spike — 2026-11-06
- Added design brief to PR #81 branch: https://github.com/sokfrut-tech/Gemeni/blob/feature/jarvis-phone-control-foundation-2026-11-06/docs/engineering/2026-11-06-jarvis-python-studio-isolated-runtime-spike.md
- Defines a phone-first offline Python workspace (project browser/editor, bounded runner, tests, export) and a strict privacy/security contract.
- Chaquopy embedded in the main app process is explicitly **not** accepted as a sandbox for user scripts.
- Preferred feasibility experiment: Chaquopy inside an Android `isolatedProcess` service with a distinct UID, no app permissions, no network, and only bounded Binder/pipe file-descriptor exchange. Compatibility is unproven and must be demonstrated before exposing Run.
- If isolatedProcess cannot host the runtime safely, stop and evaluate a separate worker APK/UID; do not silently run untrusted scripts in Jarvis's main process.
- P0 acceptance requires proof of UID/permission isolation, no network egress, bounded resources, cancellation, path-traversal resistance, no access to Jarvis memory/model files/credentials/tool gateway, and physical OPPO validation.
- This is a design brief only; no Python runtime or editor is yet integrated.


### Jarvis isolated Python worker proof — PR #84 — 2026-11-06
- Draft PR: https://github.com/sokfrut-tech/Gemeni/pull/84
- Branch: `spike/jarvis-isolated-python-worker-2026-11-06`, based on safe runtime PR #78.
- Adds a non-exported Android `isolatedProcess` probe service and instrumentation test. The test asks the service for its process UID and checks whether INTERNET and RECORD_AUDIO permissions are present.
- This is an OS-level identity/permission proof only. No Python interpreter, script execution, project file access, UI or user-facing Run action is included.
- Head SHA: `e0449c98bfa3199e75614d954f63d06f210527d1`.
- Factory Security Baseline run #105 / id `42282624776` was queued at 2026-11-06 19:46 UTC. No result yet.
- Acceptance: prove a distinct UID and no inherited permissions on emulator, then validate on the OPPO. Passing this test does not prove Chaquopy compatibility or full sandboxing.
- Keep PR draft and do not integrate Python until this proof plus separate file-transfer, resource-quota, cancellation and no-egress tests pass.


### Jarvis CI refresh — 2026-11-06 19:47 UTC
- PR #78 run #93: CodeQL and Secret Scanning succeeded; emulator job 128112867371 remains in progress.
- PR #82 run #98: Secret Scanning succeeded; CodeQL job 128107922074 remains in progress (the job is currently at emulator tests before its CodeQL analyze step).
- PR #83 run #103: Secret Scanning succeeded; CodeQL job 128112530329 remains in progress (emulator tests before CodeQL analyze).
- PR #81 run #104: Secret Scanning succeeded; CodeQL job 128114750087 remains in progress.
- PR #84 run #105: Secret Scanning succeeded; CodeQL job 128115243996 remains in progress.
- No new PR has full green CI. Keep all dependent implementation PRs in draft until the required checks complete and code/test evidence is reviewed.


### Jarvis explicit model-download consent fix — PR #85 — 2026-11-06
- Draft PR: https://github.com/sokfrut-tech/Gemeni/pull/85
- Branch: `fix/jarvis-explicit-model-download-consent-2026-11-06`, based on safe runtime PR #78.
- Code review found a privacy-contract violation: microphone startup called `ensureRussianAsr()`, which silently downloaded the Russian ASR model from Hugging Face on first use.
- Changed the normal `prepare()` path to verify/load only an already-installed model; no download is performed there.
- Added a separate user-consent dialog. Only after tapping **Разрешить загрузку** does the app fetch model files. Dialog states that the host receives connection metadata (including IP), while voice, messages, local files and memory are not included in model-file requests.
- Model readiness hash checks are moved off the UI thread.
- PR head SHA: `5599925801e07aee4a81e7d7f8e803dda06dad58` (latest at index update). Run #106 / id `42283105816` started on an earlier head; newer commits may trigger a follow-up run.
- Validation remains pending. Add automated coverage for no network before consent and test the accept/decline/error/busy UI paths. The app still has INTERNET permission; all other network call sites require a separate egress audit.

### CI checkpoint — 2026-11-06 19:51 UTC
- PR #81 run #104: CodeQL and Secret Scanning both completed successfully. Documentation-only PR; no emulator test job.
- PR #78 run #93: CodeQL and Secret Scanning succeeded; Android emulator smoke test still in progress.
- PR #82 run #98: Secret Scanning succeeded; CodeQL job still in progress.
- PR #83 run #103: Secret Scanning succeeded; CodeQL job still in progress.
- PR #84 run #105: Secret Scanning succeeded; CodeQL job still in progress.
- PR #85 run #106: workflow in progress on initial head `7a7c30c1fb3de8185ebd9263ecb252613f91b48d`; latest code has since advanced to `5599925801e07aee4a81e7d7f8e803dda06dad58`.
- PR #81's successful checks do not validate any Android runtime code. Do not describe any app feature as release-ready based on these checks.


### PR #82 emulator/CI diagnosis — 2026-11-06 19:52 UTC
- PR #82 run #98 CodeQL job 128107922074 ended **failure** after Kotlin build, debug APK build, APK verification/hash and artifact upload all passed.
- The failing step was **Android emulator smoke tests**: emulator never reached boot-completed state and the runner reported `Timeout waiting for emulator to boot` at 19:51:22 UTC. No app assertion was reached. CodeQL analyze was skipped because the job's build/test dependency failed; this is an infrastructure/emulator boot failure, not a CodeQL finding.
- Do not weaken tests or mark PR #82 green. Next diagnostic: capture emulator startup configuration, boot logs and runner resource state; consider a bounded retry only after preserving diagnostics.
- PR #81 run #104: CodeQL and Secret Scanning succeeded.
- PR #78 run #93: CodeQL and Secret Scanning succeeded; emulator smoke remains in progress.
- PR #83 run #103: Secret Scanning succeeded; CodeQL/emulator pipeline still in progress.
- PR #84 run #105: Secret Scanning succeeded; CodeQL/emulator pipeline still in progress.
- PR #85 run #108: Secret Scanning succeeded; CodeQL/emulator pipeline still in progress on latest head `5599925801e07aee4a81e7d7f8e803dda06dad58`.


### CI architecture repair — PR #86 — 2026-11-06
- Draft PR: https://github.com/sokfrut-tech/Gemeni/pull/86
- Branch: `ci/jarvis-independent-emulator-codeql-2026-11-06`, base `integration/jarvis-safe-agent-runtime-2026-11-06`.
- Workflow change: CodeQL compile/build/analyze is now independent from Android emulator instrumentation. Emulator tests run in their own job with bounded 20-minute step / 35-minute job, fresh AVD, headless boot options and always-uploaded test results.
- Rationale: PR #82 run #98 built and verified APK, but the emulator never booted; this caused CodeQL analysis to be skipped/failed as a downstream dependency. Separating jobs ensures static analysis still completes if emulator infrastructure fails.
- Head SHA: `ec62c07116428de700631cb4ea842fe4fdd9a096`.
- CI run #109 / id `42283835061` was queued when recorded. No validation result yet; keep draft until exact-head jobs finish.
- No emulator assertions were removed or relaxed.

### Latest Jarvis CI state — 2026-11-06 19:55 UTC
- PR #81 run #104: full workflow success (documentation branch).
- PR #78 run #93: CodeQL and Secret Scanning succeeded; Android emulator job remains in progress.
- PR #82 run #98: Secret Scanning succeeded; CodeQL job failed because emulator startup timed out before tests began. Kotlin compile, APK build, verification and artifact upload had passed. No test assertions ran.
- PR #83 run #103: Secret Scanning succeeded; CodeQL job is still blocked/running at emulator step after Kotlin compile, APK build, verification and upload passed.
- PR #84 run #105: Secret Scanning succeeded; CodeQL job still running at emulator step after compile/build/verification/upload passed.
- PR #85 run #108: Secret Scanning succeeded; CodeQL job still running at emulator step after compile/build/verification/upload passed.
- PR #86 run #109: queued; it is intended to prevent emulator startup from blocking CodeQL in future workflow runs.
- Do not mark any Android runtime PR fully green based only on APK build. Keep draft until independent CodeQL and emulator results are available and reviewed.


### PR #86 first execution evidence — 2026-11-06 19:56 UTC
- Run #109 / id `42283835061` started on exact head `ec62c07116428de700631cb4ea842fe4fdd9a096`.
- Secret scanning completed successfully.
- CodeQL static-analysis job and Android emulator instrumentation job are both running as separate parallel jobs. This confirms the workflow graph no longer serializes CodeQL behind emulator startup.
- Emulator job has completed checkout, JDK and Android SDK setup; SDK/NDK installation is in progress.
- CodeQL job has completed checkout/JDK/Gradle setup; Android SDK setup is in progress.
- No compile, CodeQL or emulator conclusion yet.


### Jarvis expanded capability brief — PR #87 — 2026-11-06
- Draft PR: https://github.com/sokfrut-tech/Gemeni/pull/87
- Branch: `feature/jarvis-multimodal-research-memory-media-2026-11-06`, based on phone-control foundation branch.
- Brief: `docs/engineering/2026-11-06-jarvis-music-research-memory-workspace-video-brief.md`.
- Added first-class requirements inspired by:
  - Suno: original music generation, lyrics, waveform editing, stems, remix/cover workflows, reusable local sound profiles and audio export.
  - Perplexity: opt-in web research, multi-step Deep Research, source-grounded citations, contradiction checking, local file analysis and report export.
  - Superpower: project folders, global search, conversation maps, saved prompts/chains, task queue, notes/highlights, references, gallery and export.
  - Breeno Memory / Alice My Memory: user-confirmed local notes, tasks, reminders, project-scoped memory, provenance, inspect/edit/delete/export.
  - Alice AI: Russian-first multimodal task assistance and safe task agents.
  - Video studio: import, metadata, multi-track timeline, trim/split, subtitles, transcription, scene/keyframe analysis, smart rough-cut, audio tracks, text/image-to-video and real MP4 export.
- Privacy invariants: offline/local by default; no silent cloud/API calls; explicit per-task consent for any outbound query/media; no private project, prompt, memory, audio or video upload by default.
- The brief is documentation/planning only. None of these new features is represented as already implemented. Each requires a real end-to-end test and target-phone resource benchmark.
- Commit: `89528dde66724b86602ddcf74be81811ef779ce8`.


### Jarvis P1 local memory implementation slice — 2026-11-06
- Added to PR #87: https://github.com/sokfrut-tech/Gemeni/pull/87
- New implementation file: `app/src/main/java/com/jarvis/breeno/assistant/memory/JarvisMemoryRepository.kt`.
- New instrumentation tests: `app/src/androidTest/java/com/jarvis/breeno/assistant/JarvisMemoryRepositoryTest.kt`.
- Provides app-private, local-only explicit-save memory records with kinds NOTE/PREFERENCE/FACT/PROJECT/TASK/REMINDER; project scopes; timestamps; list/filter; case-insensitive literal search; edit/delete/clear-scope operations; bounded entry/text sizes (500 entries, 4,000 chars each).
- Save/update/delete APIs are deliberately named `*AfterUserConfirmation`; caller must show the exact content/action and obtain user confirmation before invoking. No implicit conversation capture, background recording, semantic embedding or network code is present.
- Persistence uses a dedicated SharedPreferences file and Gson. No encryption-at-rest claim; existing PR #82 backup-exclusion changes remain a separate stacked branch and are not automatically included in PR #87's base.
- Commit 1: `55779a8ae7072c860bc8793fcc851eae54adfc3d`; tests commit: `aaa0f20a39ab869eff7806559b398acfc932a127`.
- Verification pending: PR #87 run #111 was queued after the test commit. No build/test result has been claimed yet.
- Not yet integrated into UI, assistant planner, semantic recall, reminder notifications or encrypted storage. This is a tested-intent design slice pending CI and must not be presented as a complete memory feature.

### CI repair PR #86 update — 2026-11-06
- Run #109 / id `42283835061`: Secret Scanning passed; CodeQL static analysis passed on exact head `ec62c07116428de700631cb4ea842fe4fdd9a096`; Android emulator instrumentation job remained in progress at last check.
- This demonstrates the CodeQL/emulator jobs now complete independently. Emulator result remains outstanding.


### Jarvis memory privacy hardening — PR #87 update — 2026-11-06
- Added `android:allowBackup="false"`, `android:fullBackupContent="false"`, and `android:dataExtractionRules="@xml/data_extraction_rules"` to the application manifest.
- Added `app/src/main/res/xml/data_extraction_rules.xml` excluding app-private data from cloud backup and device transfer.
- Added instrumentation assertion that `ApplicationInfo.FLAG_ALLOW_BACKUP` is unset.
- Rationale: SharedPreferences are app-private, but Android backup/transfer defaults must not be treated as "local-only". This hardening is required before the memory module can be considered private by default.
- Latest PR #87 head: `d11334adae0f5f859e04da5a08e9ee9fcf8e3465`; run #115 / id `42285178637` was pending at the time of this update. Earlier exact-head runs were cancelled by newer commits; no green result yet.
- Memory remains a repository-only slice: no UI confirmation dialog, planner integration, semantic recall, encryption-at-rest or reminder scheduling has been implemented yet.

### Video feasibility research note — target device constraint
- Public Android on-device generation projects indicate support is model/chip-specific, not a generic Android capability. Nightmare Mobile's README search result lists SD 1.5 on Snapdragon 888+, but more advanced diffusion/video models on Snapdragon 8 Gen 3 / 8 Elite classes; it does not establish WAN/video generation on Snapdragon 8 Gen 2.
- Qualcomm's public GenieX Android example currently documents Snapdragon 8 Elite / Elite Gen 5 prerequisites; it is not proof of support for the user's Find X6 Pro.
- Therefore Jarvis should first deliver offline conventional editing (MediaCodec/MediaExtractor/MediaMuxer or a validated editing library), transcription, subtitles, thumbnails and MP4 export on the actual OPPO. Text/image-to-video remains a separate feasibility spike; no promise of local generative video on 8 Gen 2.
- Sources reviewed: https://github.com/AbrahamPaulJ/nightmare-mobile and https://qualcomm.github.io/qidk/blogs/geniex_android.html


### Jarvis memory UI vertical slice — PR #88 — 2026-11-06
- Draft PR: https://github.com/sokfrut-tech/Gemeni/pull/88
- Branch: `feature/jarvis-memory-ui-consent-2026-11-06`, based on PR #87 head `d11334adae0f5f859e04da5a08e9ee9fcf8e3465`.
- Added `JarvisMemoryActivity.kt`: a local memory screen reachable from Jarvis home; project scope, memory type, explicit save/update confirmation, search, edit and delete confirmation.
- All repository I/O is dispatched to `Dispatchers.IO`; no network, automatic capture or cloud sync.
- Added UI instrumentation test `JarvisMemoryConsentUiTest.kt` verifying the repository remains empty until the user taps the explicit confirmation button, then stores the approved text.
- Commits on PR #88 head `5a2cc189ea70efc238e75b64dde1d0f35560c4a7`.
- CI run #116 / id `42285376790`: Secret Scanning passed; CodeQL job was still setting up Gradle at last check. Build and instrumentation test results are not available yet. Keep draft.
- PR #87 run #115 / id `42285178637`: Secret Scanning passed; CodeQL build job in progress. PR #87 exact-head code still requires verification.
- PR #86 run #109 / id `42283835061`: CodeQL and Secret Scanning passed; emulator instrumentation remained in progress. Workflow independence is proven, but emulator test result remains pending.

### Video editor implementation decision
- Prefer AndroidX Jetpack Media3 Transformer as first candidate for offline trimming, transcoding, resizing, rotation, track removal, effects and MP4 export; it is an Android-native API and supports hardware codecs where available.
- MP4 edit-list trim optimization can be fast but has a privacy/compatibility caveat: removed samples may remain in the file and be hidden by edit-list metadata. For any "permanently remove this segment" operation, use a verified re-encode/export path rather than relying on edit lists.
- Multi-clip compositions, preview and advanced timeline features require additional implementation and target-device tests. Start with import -> metadata -> trim -> MP4 export -> playback/hash validation on the OPPO.
- Official docs: https://developer.android.com/media/media3/transformer/transformations and https://developer.android.com/media/media3/transformer


### Verified Jarvis memory PRs — 2026-11-06
- PR #87 exact head `d11334adae0f5f859e04da5a08e9ee9fcf8e3465`, run #115 / `42285178637`: Secret Scanning SUCCESS; CodeQL SUCCESS. CodeQL workflow built Kotlin sources and full debug APK, verified/hash-uploaded APK, and completed static analysis. This does not prove runtime behavior on a physical OPPO.
- PR #88 exact head `5a2cc189ea70efc238e75b64dde1d0f35560c4a7`, run #116 / `42285376790`: Secret Scanning SUCCESS; CodeQL SUCCESS; Kotlin source build, full debug APK build, APK verification/hash/upload and CodeQL analysis completed. This workflow does not run Android instrumentation tests; the new UI consent instrumentation test remains unexecuted in this run.
- Both PRs remain open/draft and are not merged.

### Jarvis offline video editor — PR #89 — 2026-11-06
- Draft PR: https://github.com/sokfrut-tech/Gemeni/pull/89
- Branch: `feature/jarvis-offline-video-editor-2026-11-06`, based on PR #88 branch.
- Adds Media3 Transformer 1.11.1 stable; system video picker; local duration inspection; start/end trim sliders; a validated trim window with 500 ms minimum; new MP4 export to app cache then MediaStore Movies/Jarvis; cancellation; share-sheet handoff; Jarvis home shortcut.
- Original media is read-only and never uploaded. Export is a new file. This is a trim/export MVP, not a multitrack editor or AI video generator.
- Added `VideoTrimRangeTest` boundary unit tests and PR-specific workflow `.github/workflows/jarvis-video-ci.yml` to run unit tests and assemble/verify the APK for relevant pull requests.
- Latest PR #89 head: `427e8805f5ef1db1a7693f8aee7d776382c3f687`.
- CI run #1 / id `42286126486` was in progress at last check, still setting up Android SDK. Factory Security Baseline run #118 was pending; prior run #117 on the preceding head was still in progress. No compile/test pass is claimed yet.
- Physical OPPO codec support, performance, file-picker permissions and export playback remain untested.
- Official Media3 docs confirm 1.11.1 stable and Transformer dependencies: https://developer.android.com/jetpack/androidx/releases/media3 and https://developer.android.com/media/media3/transformer/getting-started


### Jarvis video editor preview + cancellation hardening — PR #89 update — 2026-11-06
- Added Media3 ExoPlayer + UI 1.11.1 (same aligned version as Transformer) for an embedded local playback preview.
- Added player lifecycle cleanup on screen disposal; selected media is prepared locally and is not sent to a service.
- Export cancellation now tracks and deletes the temporary MP4 file.
- Latest PR #89 head: `4ea4393effde1d2d9b7ddbb0377e047b2b92f495`.
- Latest exact-head Jarvis Video CI run #6 / id `42286439605` was queued; Factory Security Baseline run #123 / id `42286439956` was in progress. Earlier runs were cancelled by subsequent commits; no result yet.
- PR #87 run #115 and PR #88 run #116 both completed successfully (Secret Scanning + CodeQL, including Kotlin build and debug APK build). PR #88 UI instrumentation test was added but was not executed by that CodeQL workflow.
- PR #89 remains draft; no merge and no claim of device validation.


### Qwen advanced scientific and engineering knowledge scope — PR #90 — 2026-11-06
- Draft PR: https://github.com/sokfrut-tech/Gemeni/pull/90
- Branch: `feature/qwen-advanced-knowledge-domains-2026-11-06`, based on the Jarvis video-editor development branch.
- Brief: `docs/QWEN_ADVANCED_KNOWLEDGE_AND_EXPERT_SYSTEM_BRIEF_2026-11-06.md`.
- Covers physics, mathematics, chemistry, medicine, energy, astronomy, astrology as a separate non-empirical/cultural module, psychology, radio/radioelectronics, radio stations, antennas, modems/routers, LTE/Wi-Fi, mesh/MANET, robotics, programming, computer science, cybernetics, neural networks, neuroanalytics, geography, cartography, navigation, construction, gardening, probability/lotteries and calculations.
- Defines local-first knowledge packs, provenance/versioning, opt-in web research/downloads, local RAG, Python/calculation/simulation tools, answer verification, test suites and phased acceptance criteria.
- Explicit safeguards: evidence-based medical framing, local radio regulations, chemical/energy safety, authorized cybersecurity, engineering safety, non-predictive treatment of lotteries, and clear distinction between astronomy and astrology.
- PR #90 is documentation/requirements only; it does not establish that all subjects are already installed in Qwen or that model weights have been trained.
- Head SHA: `faec77e4ba59c6b3b4f4c26a085d532fbac0da83`. PR remains draft and is not merged.


#### Qwen domain catalog added to PR #90
- Added machine-readable `app/src/main/assets/knowledge/domain_catalog.json` (Russian, schema v1) with 21 domain groups, topic lists, local-only/network-consent policy, source-provenance fields and answer-quality requirements.
- Catalog explicitly labels astrology as a non-empirical cultural system and lottery outcomes as not reliably predictable; medicine and neuroanalytics have safety profiles.
- Latest PR #90 head: `b8bc463ee66b1ef810cb6aa00d1a53e962fde3e1`; PR remains draft and unmerged. Catalog is metadata only, not a downloaded knowledge corpus or implemented RAG.

### Qwen local domain-catalog loader — PR #90 update — 2026-11-06
- Added `KnowledgeDomainCatalog.kt`: typed domain metadata, strict schema/policy validation, and an Android asset repository that reads only bundled `knowledge/domain_catalog.json`. It contains no HTTP client, downloader, sync, or background task.
- Exposed the bundled catalog lazily from `JarvisCore.knowledgeCatalog`; this is metadata discovery only, not factual retrieval, RAG, model training, or a claim that Qwen already knows every listed subject.
- Added `KnowledgeDomainCatalogParserTest.kt` for valid parsing, duplicate IDs, non-local storage, forbidden implicit training, background network policy, and unknown-domain lookup.
- PR #90 head after this implementation: `c2a0c8a2b39220b920fe388282fa8f8abc634dda` (verify against GitHub before merge).
- Earlier exact-head CodeQL run `42286946665` failed because inherited Media3 1.11.1 dependencies require compileSdk 36 while the project is on compileSdk 35 / AGP 8.7.3. Secret scanning passed. Failure was a build-toolchain/dependency mismatch, not a finding in the Qwen catalog.
- Compatibility correction: pinned all Media3 artifacts to 1.5.1 on PR #89 branch (commit `666d981d563e1522799df571fb40ecc4ed8ac45d`) and PR #90 branch (commit `b7954bd497fce7e2ce44025d3ae08b81fa67e703`). Official Media3 release notes identify 1.5.1 as a stable release; fresh CI runs were queued/in progress at last check. Do not mark fixed until exact-head build and unit tests pass.
- Current PR #89 branch also needs a fresh compile/build/test after the downgrade; physical OPPO playback/export remains unverified.
- Keep both PRs draft/unmerged until CI passes, inspect resulting APK, and validate on device. No network sync or training on user data was introduced.
