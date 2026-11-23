# Jarvis AI research handoff — 2026-11-24

Status: research update committed to OGAM and opened as a draft PR. No production code, APK or device state changed.

## Canonical project
- Active implementation: `sokfrut-tech/OGAM` (GitHub).
- Separate GitLab project `sokfrut-tech/jarvis` was checked: only README.md, main branch and initial commit; not the active implementation.
- Target device: OPPO Find X6 Pro PGEM10 / Snapdragon 8 Gen 2 / Android 16 / ColorOS 16.0.5.

## OGAM state
- Draft PR #1 (implementation: storage/privacy, model library, prompt APIs, voice image generation, localization, APK workflow) remains open and unmerged.
- CI/build is still blocked by unavailable private `off-grid-ai/shared` and `off-grid-ai/mobile-pro` workspaces because `PRO_SUBMODULE_PAT` was empty in the recorded run. The later explicit-clock test fix had not yet been verified by a rerun in the PR description.
- No Gradle APK, installation or PGEM10 runtime validation is claimed.
- Draft PR #2 contains the Breeno/ColorOS research and clean-room implementation plan.

## New research
- Strongest architecture reference for small offline agents: LocalIntelligence (Apache-2.0); audit further before reuse.
- Nyral (MIT) is local-first for data/memory but uses user-supplied remote inference; not an offline LLM.
- PalmClaw (AGPL-3.0) offers useful sessions/skills/automation/permission ideas; architecture-only by default.
- Open Jarvis (MIT) has a broad Android feature checklist, but README claims require source/test/device verification.
- DroidClaw and self-hosted JARVIS need license/source maturity checks before reuse.
- Kimi: optional OpenAI-compatible cloud provider with streaming and tool calls; paid API, not offline core.
- Qwen: local small-model and speech candidates worth benchmark-only evaluation; do not switch production model without PGEM10 Russian-quality/RAM/thermal tests.
- Z.ai GLM-5.4: current announcement says weights are planned after safety hardening; treat as optional remote provider, not local runtime.
- Keep deterministic authorization between model proposals and Android tools; one physical microphone owner; no always-on/wake-word claims until real implementation and device validation.

## Canonical deliverables
- OGAM research branch: `research/jarvis-agent-ecosystem-2026-11-24`
- Commit: `f6950677afa44414669a7e1eaac890939a144f7d`
- Draft PR #3: https://github.com/sokfrut-tech/OGAM/pull/3
- Research document: https://github.com/sokfrut-tech/OGAM/blob/research/jarvis-agent-ecosystem-2026-11-24/research/agent-ecosystem/JARVIS_ANDROID_AGENT_ECOSYSTEM_RESEARCH_2026-11-24.md

## Next actions
1. Resolve private submodule access or establish a license-safe build route.
2. Re-run all CI gates, then Gradle arm64 APK build.
3. Install and verify Android assistant role/bridge on PGEM10.
4. Benchmark Russian KWS, streaming ASR and Russian TTS against the fixed corpus; no production model selection before measurements.
5. Implement/test deterministic action approval and permission gates.
6. Continue source-level audits of LocalIntelligence, Nyral and Open Jarvis; confirm licenses before any code reuse.

Research-only update. No PR merged.

## Step 1 memory audit — 2026-11-24
- Inspected OGAM's actual persistence and RAG sources on `feature/jarvis-step-2-storage-privacy`.
- Confirmed durable chat history: Zustand `local-llm-chat-storage`, chunked AsyncStorage and hydration-gated recovery; chat migration schema v2.
- Confirmed project/document RAG: SQLite `rag.db` membership, `documents.db` pages/chunks/vector BLOBs/FTS5, local llama.rn embeddings, cited retrieval and project-scoped guards.
- Confirmed no distinct curated long-term personal memory store was found. "Memory" modules/tests largely refer to model RAM residency.
- Security caveat: inspected code does not establish encryption-at-rest or biometric memory vault.
- Recommended additive `jarvis_memory.db` with typed facts/preferences/project decisions, explicit user confirmation, provenance, scope, confidence, expiry, conflict handling, inspect/edit/delete/export and local-only-by-default sync.
- Audit document: https://github.com/sokfrut-tech/OGAM/blob/research/jarvis-agent-ecosystem-2026-11-24/research/agent-ecosystem/JARVIS_STEP_1_MEMORY_AUDIT_2026-11-24.md
- Commit: `8ebb125938b02ce1927be965c7359bb89fbd3b8f`; recorded in draft PR #3 comment.
- No production code changed, no tests executed, no APK built, no device test performed.
- Next: complete memory schema threat model and acceptance criteria, then implement schema + migrations + repository tests as a separate PR/commit; do not proceed to scheduler until Step 1 gates are satisfied.


## Step 1 memory design — 2026-11-24
- Added design-only specification to OGAM research branch: `research/agent-ecosystem/JARVIS_STEP_1_MEMORY_DESIGN_2026-11-24.md`.
- Commit: `73329111c618c1010f517966f728a82a0715439c`.
- Defines typed `jarvis_memory.db` schema, constraints, indexes, migration rules, tombstones, lifecycle API, explicit confirmation, provenance and scope isolation.
- Defines privacy threat model for app-private data, Android Keystore/encryption options, backup/restore, local-only sync policy, prompt injection, logging, export and deletion limits.
- Adds 28 acceptance tests plus PGEM10 device acceptance checklist.
- Important caveat: SQLCipher/Keystore encryption is a design requirement to evaluate, not an existing verified capability. JSON1 and SQLite runtime capabilities must be checked before adopting the proposed DDL.
- No production source files changed; no tests executed; no APK built; no device test performed.
- Next: review design against OGAM's actual DB/migration abstractions and target SQLite runtime, then implement M1 only (schema + migrations + repository tests) in a separate implementation branch/PR. Keep model writes, UI and retrieval out of M1. Do not start scheduler until Step 1 gates pass.


## OGAM SQLite compatibility review — 2026-11-24
- Reviewed `feature/jarvis-step-2-storage-privacy` source: `@op-engineering/op-sqlite` is locked to 15.2.5; current stores use `open({ name })` + `executeSync`.
- No shared versioned migration framework was found in inspected stores. Documents use a local BEGIN/COMMIT/ROLLBACK helper; RAG performs additive ad-hoc column migrations.
- `react-native-keychain` 10.0.0 is present in package-lock, but this is not proof that memory encryption/key wrapping is implemented.
- Android manifest currently has `android:allowBackup="false"`; preserve it, but validate OEM transfer/reinstall/export behavior on device.
- JSON1/native SQLite compile options are not proven. Updated memory design to require TypeScript JSON validation first and to omit `json_valid()` CHECK until verified.
- Design update commit: `f05b6eab9ca6e1f2ecb90e4a67333db96c907ce5`.
- Created isolated M1 branch `feature/jarvis-step-1-memory-m1-2026-11-24` from the existing storage/privacy implementation branch. Intended scope: memory DB schema/migration + typed repository + tests only; no model writes, UI, retrieval or scheduler.
- Still no tests, APK or PGEM10 runtime probe have been executed. Do not report them as passed.


## M1 implementation started — 2026-11-24
- Created isolated branch: `sokfrut-tech/OGAM:feature/jarvis-step-1-memory-m1-2026-11-24`, based on `feature/jarvis-step-2-storage-privacy`.
- Draft PR #4: https://github.com/sokfrut-tech/OGAM/pull/4
- Added `src/services/jarvisMemory/types.ts`, `schema.ts`, `database.ts`, `repository.ts`.
- Added tests: `__tests__/unit/services/jarvisMemory/schema.test.ts`, `database.test.ts`, `repositoryValidation.test.ts`.
- Migration uses separate `jarvis_memory.db`, transaction `BEGIN IMMEDIATE/COMMIT/ROLLBACK`, version metadata, future-schema refusal and no JSON1 dependency. Repository validates JSON serialization/16 KiB, scope invariants, expiry and confidence; proposal starts as proposed/local_only and confirmation is a separate method.
- No model extraction, prompt retrieval, UI, deletion/export UI, sync or encryption added.
- Compare against base reports 8 commits ahead / 0 behind and 7 files changed (526 additions at PR creation).
- GitHub Actions query for this branch currently returns zero workflow runs; tests have not been executed locally or in CI. No APK or device tests.
- Next gate: inspect the M1 diff for API/type issues, obtain focused Jest + TypeScript CI execution, then run native SQLite capability probes (SQLite version, JSON1, foreign keys and rollback). Do not merge or proceed to M2 until those gates pass.


## Ecosystem reconnaissance — 2026-11-24
- Added OGAM research report: `research/agent-ecosystem/JARVIS_RUSSIAN_AND_ADJACENT_AI_ECOSYSTEM_2026-11-24.md`.
- Commit: `56b667ff637bd5098df67dc76ef6afa7e5a5af46`.
- High-value references:
  - GitVerse/GigaCode docs: Plan/Build separation, read-only explore subagents, allow/ask/deny permissions, repository skills and MCP allowlists — apply to Factory agent contracts, not as embedded proprietary runtime.
  - ai-forever/giga_agent (MIT) + gigachain (MIT): subagents, tools/MCP, durable tasks, RAG, scheduler, connectors, sandbox and migration patterns. Study and extract narrow patterns; no unrestricted REPL in Android.
  - sherpa-onnx (Apache-2.0): top-priority offline Android ASR/KWS/VAD/TTS benchmark candidate.
  - alphacep/vosk-api (Apache-2.0): Russian offline ASR baseline/fallback candidate.
  - pbakaus/impeccable (Apache-2.0): Compose-aware design critique/audit/adapt and animation principles. Do not enable its live apply fallback or unattended hooks without reviewing; README describes a bypass-approval/sandbox fallback.
  - OpenMAIC (MIT root, some package-specific licenses): durable agent sessions, leases, replayable events, validated tools and steering; architectural reference only.
  - MiniMind (Apache-2.0): learning/training pipeline and tool-use/distillation research, not a production on-device model recommendation.
  - OpenCloud: hosted MCP/app builder; optional companion dashboard only, not Jarvis core.
  - Golos: Russian ASR corpus; dataset license must be checked before reuse. Silero model repo is CC BY-NC 4.0, so no commercial reuse without resolving rights.
- No third-party code copied, dependencies added, APKs built or models benchmarked.
- Next: finish Step 1 M1 first; then prepare PGEM10 Russian ASR/KWS/TTS benchmark Sherpa vs Vosk and manually audit Compose UI using Impeccable-derived criteria. Scheduler remains gated by Step 1.


## M1 code review follow-up — 2026-11-24
- Read the complete M1 source and test diff in draft PR #4. Found two API safety gaps and fixed them on the same feature branch:
  1. `repository.list()` previously allowed an omitted scope and could return records from global/project/conversation scopes together. It now requires an explicit scope; project/conversation listings require a non-empty scope ID, and global listing explicitly constrains `scope_id IS NULL`.
  2. `confirmProposal()` previously could confirm a proposal after its expiry time. Confirmation now includes a database-side `expires_at IS NULL OR expires_at > now` predicate and takes the approval timestamp from the repository clock, not a caller argument.
- Added `__tests__/unit/services/jarvisMemory/repositoryGuards.test.ts` covering explicit scope, project isolation, global isolation and expiry confirmation.
- Fix commit: `9646b7e744fa46a5a4051b79e9e2adb6290b8fee`.
- Guard-test commit: `67c896cf21cab6f4d0c0ba9118e6013770165252`.
- PR #4 current head: `67c896cf21cab6f4d0c0ba9118e6013770165252`; PR remains draft and unmerged.
- Verification: source review only. No Jest, TypeScript, ESLint, native SQLite, APK or device test has run. The new Jest tests are not evidence of passing until executed.
- CI trigger diagnosis confirmed: repository `.github/workflows/ci.yml` listens to PRs targeting `main` or `release/*`; PR #4 targets `feature/jarvis-step-2-storage-privacy`, so no PR workflow run is created. Do not retarget PR #4 directly to `main`: its base branch contains a large unrelated feature set (compare against main shows a broad diff). No workflow-dispatch action is available through the current GitHub connection.
- Next: arrange a clean, isolated validation path against `main` that contains only the M1 files, or obtain a supported workflow-dispatch/runner path; then run focused Jest + typecheck. After that, add a native SQLite probe for runtime version, JSON1, foreign-key enforcement and transaction rollback on the OPPO device. Keep M1 open and do not start M2/scheduler until gates pass.
