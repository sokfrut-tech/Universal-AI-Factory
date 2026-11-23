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
