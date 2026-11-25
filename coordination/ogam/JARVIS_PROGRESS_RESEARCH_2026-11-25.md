# Jarvis AI — progress and technology research (2026-11-25)

Status: evidence-based continuation note. Documentation only in this commit; no Jarvis application source, model weights, APK, secrets, or device state changed by this report.

## Executive summary

There are two distinct Jarvis code lines and they must not be conflated:

1. **Primary Android Jarvis agent:** `sokfrut-tech/Gemeni`.
2. **OGAM / Off Grid AI Jarvis fork:** `sokfrut-tech/OGAM`, currently the more active standalone/offline Android implementation branch.

The Universal AI Factory is actively recording and validating work, but it is not yet a fully autonomous multi-provider factory. The factory's latest main commit is `c773c02cf938d769185e8edd2ae7b50fb9d0d102` (2026-11-25). Current research and implementation are being tracked through factory coordination notes and PRs.

## Verified new implementation — OGAM PR #1

PR: https://github.com/sokfrut-tech/OGAM/pull/1  
Branch: `feature/jarvis-step-2-storage-privacy`  
Head: `750bae3f01ca32c3471c90d95d0367f512737814`  
State: OPEN / DRAFT / UNMERGED.

### What is present in source

- Privacy-first fork: PostHog analytics startup/transport disabled; no telemetry by default.
- SAF-first file selection and typed Android storage permission wrapper; reuse existing native permission API rather than duplicating it.
- Local model scanner/library for GGUF, LiteRT, Whisper, mmproj, MNN/QNN and related artifacts; split/unsupported packs are not falsely presented as importable.
- llama.rn raw-prompt and assistant-prefix prefill paths with prompt logging redaction.
- Voice-assisted image-generation screen with editable positive/negative prompts and explicit enhancement preview.
- Russian/English localization and device-locale-based ASR defaults for new profiles; previously saved language preference is preserved.
- Validated task-plan/DAG lifecycle, pause/resume/retry/cancel guards, persisted run state, typed tool-skill contracts and approval rules.
- Russian model-evaluation harness: six candidate profiles, 14 fixed scenarios and JSONL validation/scoring. It does not download or run models and does not select a production model automatically.
- Existing OGAM registries and permission APIs are reused; no parallel duplicate registry or permission module was introduced.

### Exact-head CI and APK evidence

At PR head `750bae3f01ca32c3471c90d95d0367f512737814`:

- External dependency audit: success on push and pull request.
- CI run: https://github.com/sokfrut-tech/OGAM/actions/runs/45625995963
  - changed-inputs, lint/actionlint, TypeScript, dependency architecture, all 8 Jest shards, coverage and Android tests passed.
  - Roll-up CI is marked failure because the iOS test job was auto-cancelled after waiting 15 minutes for an unavailable macOS runner. The final gate also recorded a native test result as `abandoned`; do not call the entire CI run green.
- Standalone ARM64 release APK build: https://github.com/sokfrut-tech/OGAM/actions/runs/45625998930 — success.
- Artifact: https://github.com/sokfrut-tech/OGAM/actions/runs/45625998930/artifacts/15031006793
- APK: `Jarvis-OGAM-arm64-release.apk`, 221,395,787 bytes.
- SHA-256: `85130f7b765787d501a480cdbf8aafcc869b710c3653ddb783b4cf1a43685981`.
- Package inspection verified `ai.offgridmobile`, version `0.0.125`, target SDK 36, bundled Hermes JS, QNN/Hexagon assets, 57 ARM64 native libraries and `JarvisVoiceInteractionService`.
- The build uses the standalone open-core path without `PRO_SUBMODULE_PAT`; Pro-gated functionality remains dormant through `proStub.js`.
- This proves build/package/signature inspection, not successful installation, assistant-role activation, voice quality, thermals or runtime behavior on the OPPO Find X6 Pro PGEM10.

## Other Jarvis implementation track — Gemeni

- Open PR #148: https://github.com/sokfrut-tech/Gemeni/pull/148
- Title describes llama.cpp + Qwen2.5 offline brain, Russian Piper voice, interactive orb, SaveVideo and Control Center.
- PR remains open and its last update is 2026-11-21. Its description lists added JVM tests, but this report does not claim the PR's exact-head CI, APK or physical-device acceptance.
- Do not merge or combine PR #148 with OGAM PR #1 blindly. They are separate repositories/branches and have different baselines.

## What has been researched by source inspection ("подсматривание")

The 2026-11-24 research handoff records source-level reconnaissance and clean-room adoption candidates:

- LocalIntelligence (Apache-2.0): small local-agent architecture; further audit before reuse.
- Nyral (MIT): local-first memory/data patterns, but remote inference supplied by the user; not an offline model.
- PalmClaw (AGPL-3.0): session, skill, automation and permission concepts; architecture reference only unless license implications are accepted.
- Open Jarvis (MIT): Android feature checklist, typed action plans, task-scoped memory and postcondition verification ideas; identified weaknesses in prompt-injection detection and autonomous action safety.
- DroidClaw and other self-hosted Jarvis implementations: source maturity and license audit still required.
- Giga Agent / GigaChain (MIT): subagents, tools/MCP, durable tasks, RAG, scheduler, connectors and sandbox patterns.
- OpenMAIC (MIT root; package-specific licenses vary): durable sessions, leases, replayable events, validated tools and steering.
- sherpa-onnx (Apache-2.0) and Vosk (Apache-2.0): local Android speech/VAD/KWS/ASR candidates to benchmark.
- Impeccable (Apache-2.0): design critique/adaptation ideas; do not copy unsafe unattended apply hooks.
- MiniMind (Apache-2.0): training/distillation research, not a ready production phone model.
- Breeno/ColorOS: a separate OGAM draft research PR documents structural analysis of 26 local APKs and clean-room parity targets. Full JADX method-level audit and device-runtime validation remain outstanding.

Rule: inspect source, license, build/tests and behavior; extract product/architecture ideas and implement independently. Do not copy proprietary source/assets or treat README claims as proof.

## New technology radar — OpenAI (official sources checked 2026-11-25)

1. **Responses API Multi-agent (beta):** root agent can spawn, message, follow up, wait for and interrupt subagents; focused independent work can run in parallel. The documentation recommends a default maximum of three concurrent subagent turns. WebSocket mode supports incremental tool-result injection for long-running workflows.
   - https://developers.openai.com/api/docs/guides/responses-multi-agent
2. **Agents API (public beta):** managed agent harness with durable sessions, context compaction/recovery, tools/MCP, sandbox selection and subagent coordination.
   - https://openai.com/index/introducing-the-agents-api/
3. **Computer use in Agents API:** changelog records computer-use support added 2026-09-29, with browser access approvals and sign-in controlled by the application.
   - https://developers.openai.com/api/docs/changelog

Jarvis/Factory adoption decision:
- Use the architecture pattern, not a paid cloud dependency in the offline Android core.
- Factory can split a large task into bounded roles: researcher, implementer, test engineer, independent reviewer. Each must return evidence, not only a narrative.
- Keep one coordinator and a shared append-only task ledger; independent workstreams get isolated branches/workspaces to avoid shared-file races.
- Persist run/session IDs, correlation IDs, checkpoint, tool calls, artifact links and exact commit/test evidence.
- Make cloud multi-agent execution optional and explicit; local Jarvis remains usable without it.

## New technology radar — Qwen (official sources checked 2026-11-25)

1. **Qwen4-Max (2026-11-16):** 2.4T total backbone parameters, 71B activated per token, native vision and 1M-token context; Qwen describes long-running agents, staged Live Delivery and stronger tool-oriented work. It is available via QwenCloud. The announcement says smaller Qwen4 models are coming open source, but does not provide a confirmed public small-model download in that announcement.
   - https://qwen.ai/blog?id=qwen4-max
2. **Qwen3.8-Omni-Flash (2026-09-18):** multimodal text/image/audio/video model with 1M context, tool use and long-horizon audio/video workflows; Qwen also describes an open Qwen-Live Harness and Omni Skill Creator.
   - https://qwen.ai/blog?id=qwen3.8-omni-flash
3. **Qwen3.8-LiveTranslate (2026-09-18):** streaming speech translation, speaker separation, synchronized source/translation and long-context disambiguation; Russian is listed among supported input/output languages.
   - https://qwen.ai/blog?id=qwen3.8-livetranslate

Jarvis adoption decision:
- Qwen4-Max and Qwen3.8 Omni are cloud/API research candidates, not offline phone runtimes.
- Keep Qwen3.5-4B and other small local candidates in the benchmark manifest until a smaller open Qwen4 weight is actually released and licensed.
- Evaluate Qwen LiveTranslate for an optional network-connected interpreter mode only; compare latency, Russian accuracy, speaker attribution, API cost and privacy before integration.
- Do not route microphone audio or screen content to cloud without explicit user consent.
- No Qwen4-Max, Qwen3.8 API, or cloud LiveTranslate integration has been implemented in Jarvis by this report.

## Architecture decisions to carry forward

- Local-first core: Android app owns conversation, local model selection, local memory, voice pipeline and permissions.
- Replaceable inference providers: local llama.cpp/llama.rn baseline first; optional remote provider adapters are isolated behind explicit consent and policy.
- Deterministic tool broker: model proposes typed action → schema/capability validation → risk classification → user approval when required → execution → postcondition verification → event log.
- Single microphone owner and explicit capture lifecycle; no always-on/wake-word claim until real device testing.
- Add durable personal memory only as a separate, privacy-reviewed store with provenance, scope, expiry, conflict handling, inspect/edit/delete/export and encryption validation.
- Resource governor for Snapdragon 8 Gen 2: benchmark RAM, thermal state, battery, startup latency and model swap behavior before selecting default weights.
- Research and implementation stay separate: no production model switch based on vendor benchmarks alone.

## Next implementation sequence

1. **Close the APK-to-device evidence gap:** install artifact from run #2 on PGEM10; verify first launch, app navigation, model-library scan, role activation, permissions, offline airplane-mode behavior and crash-free restart. Record screenshots/logs and device/OS build. No user action is requested until a verified APK link and concise install steps are prepared.
2. **Repair CI truthfully:** inspect why native job reports `abandoned`, add/restore a supported runner path or make the required native check explicit; document iOS runner unavailability without masking it.
3. **Finish the speech runtime contract:** complete the standalone `@offgrid/speech` migration, tests and one-microphone-owner integration; then benchmark Russian VAD/KWS/streaming ASR/TTS with fixed audio corpus.
4. **Memory M1:** review the new `jarvis_memory.db` design and threat model, then implement schema/migrations/repository tests only after SQLCipher/Keystore/SQLite runtime capabilities are verified.
5. **Model benchmark:** pin exact model revisions, quantization and SHA-256; run the 14 Russian scenarios at least three times on PGEM10; score Russian quality, tool compliance, prompt-injection resistance, RAM, thermals and battery. Do not choose an uncensored model by label.
6. **Independent review:** request Qwen/Claude/Gemini review only through an explicit provider dispatch with correlated substantive report. An inbox ACK is not execution.
7. **Keep PRs separate:** OGAM PR #1 remains draft/unmerged; Gemeni PR #148 remains separate. Require exact-head checks and physical device gates before merge/release.

## Evidence and status labels

- **Verified:** GitHub Actions, commit, artifact and package-inspection facts listed above.
- **Implemented-unverified:** source changes that passed only partial checks or lack device/runtime acceptance.
- **Research-only:** vendor announcements and external repositories; not integrated.
- **Blocked/pending:** iOS runner, native abandoned job diagnosis, PGEM10 install/runtime, full speech benchmark, model weight hashes/licensing and memory encryption validation.

Last checked: 2026-11-25.
