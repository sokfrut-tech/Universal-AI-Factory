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
- Integration branch: `sokfrut-tech/Gemeni` / `integration/jarvis-safe-agent-runtime-2026-11-06`.
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
- Preferred first neural runtime spike: llama.cpp through an app-owned JNI adapter, pinned to upstream commit `954de248ac6907dd05dc19f0f511ab18f2807a54`.
- The current Arm AI Chat wrapper is not drop-in compatible: its library declares minSdk 33; generic llama.cpp Android NDK guide example uses API 28. API24 compatibility remains unproven.
- MLC LLM is deferred to a physical-device Adreno GPU experiment; ONNX Runtime Android package availability alone does not prove generative LLM support.
- Jarvis source has no real local neural inference yet. The prompt-echo placeholder was removed and a regression test added.
- Technical decision: https://github.com/sokfrut-tech/Gemeni/blob/integration/jarvis-safe-agent-runtime-2026-11-06/docs/engineering/2026-11-06-local-inference-runtime-decision.md
- Phase B brief: https://github.com/sokfrut-tech/Gemeni/blob/integration/jarvis-safe-agent-runtime-2026-11-06/docs/agents/BRIEF_LOCAL_REASONING_RUNTIME_PHASE_B_2026-11-06.md
- Safe runtime PR #78: https://github.com/sokfrut-tech/Gemeni/pull/78


### Jarvis model shortlist update — Qwen3.5 (2026-11-06)
- Official Qwen3.5-0.8B is Apache-2.0; official ggml-org GGUF Q4_0 candidate is 563 MB, pinned revision `4c11520cef475dd40ed72ec4a1e68b26721bd769`, SHA-256 `57d1997790d1744fba5b40a7317df71ea5e2acee28c47e78f0cce39c0703f8cf`. Use for initial runtime bring-up only, not as a quality promise.
- Qwen3.5-2B instruction model is Apache-2.0. bartowski Q4_K_M conversion is around 1.40 GB and is the primary quality/size candidate; pin exact conversion revision and SHA-256 before download/installation because it is third-party.
- Full evidence and gates: https://github.com/sokfrut-tech/Gemeni/blob/integration/jarvis-safe-agent-runtime-2026-11-06/docs/engineering/2026-11-06-local-inference-runtime-decision.md
- No model has been integrated into the APK or benchmarked on the OPPO device yet.


## Jarvis Phone Control — 2026-11-06
- New implementation issue: https://github.com/sokfrut-tech/Gemeni/issues/80
- Goal: manage OPPO/ColorOS phone functions and services through a typed, allowlisted Android gateway with explicit permission checks, approval for sensitive actions, cancellation, audit history and post-action state verification.
- First scope: read-only device diagnostics; audio/display/flashlight; app and settings launch; supported media/alarms/notification actions; connectivity via user-mediated system panels where direct toggles are restricted; approval-gated dial/SMS intents; user-defined automation scenes.
- Existing source gateway inspected on PR #78 branch: `AndroidJarvisToolRegistry.kt` currently supports app launch, web search, navigation, time and approval-gated dialer only. No full phone-control module is implemented yet.
- Platform boundary: Android 10+ ordinary apps cannot directly toggle Wi-Fi; Android 13+ ordinary apps cannot directly enable/disable Bluetooth. Implement supported system panels/intents and verify actual resulting state; never report fake success.
- CI run #42277569386 rechecked while updating this handoff: secret scanning and CodeQL passed; emulator smoke tests were still in progress after APK build passed. Do not commit to PR #78 branch until that run finishes, to avoid cancelling/restarting it.
- Next: finish PR #78 CI diagnosis; then implement Phone Control capability matrix and typed contracts in a separate focused change, with API-level and OPPO physical-device acceptance gates.

- Phone Control design baseline committed on `sokfrut-tech/Gemeni` branch `feature/jarvis-phone-control-foundation-2026-11-06` (commit `b0be2ca7406dc7a1906490f2ca9c8b26ad7623db`): https://github.com/sokfrut-tech/Gemeni/blob/feature/jarvis-phone-control-foundation-2026-11-06/docs/engineering/2026-11-06-phone-control-design.md. Design only; implementation not yet verified.

- Source audit for Phone Control design: Gemeni `app/build.gradle.kts` on main is verified at `minSdk=29`, `targetSdk=35` (not Android 7/API24); AccessibilityService config currently requests all event types and window-content access despite the service being empty. Narrow this privacy surface before implementation. Documented in PR #81.
