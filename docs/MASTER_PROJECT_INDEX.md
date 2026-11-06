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
