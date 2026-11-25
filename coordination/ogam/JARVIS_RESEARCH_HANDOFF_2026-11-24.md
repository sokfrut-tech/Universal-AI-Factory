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


## Isolated CI validation attempt — 2026-11-24
- To preserve PR #4's correct feature-branch base, created a temporary validation branch from `main`: `verify/jarvis-memory-m1-main-ci-2026-11-24`.
- Copied only the four M1 production files and four M1 Jest files (8 files total); no unrelated feature-branch commits or files were copied.
- Opened draft validation PR #5: https://github.com/sokfrut-tech/OGAM/pull/5
- Validation head commit: `efae5d3f269c890c0d088e36f7f2d9c0002cdd2e`.
- PR #5 is explicitly validation-only and must not be merged. Its only purpose is to trigger the existing main-target CI.
- Rechecked the commit workflow runs and combined commit statuses after PR creation: both returned zero runs/statuses. Thus CI has still not started; this is not a passing test result. The current GitHub connector exposes workflow-run reads/retries but no workflow-dispatch action, and its approved fetch endpoint rejected the workflow-list endpoint.
- Next: determine why the main-target PR event did not create a run (Actions disabled/repository event policy/connector delay), or use a supported runner path. Keep PR #4 and PR #5 unmerged. Do not claim Jest/typecheck success until there is a fresh run with successful jobs.


## GitLab CI fallback configured — 2026-11-24
- User requested GitLab CI as fallback executor when GitHub Actions cannot start.
- Located existing private GitLab project `sokfrut-tech/jarvis` (project ID `88675977`). Project metadata confirms `shared_runners_enabled=true`, `group_runners_enabled=true`, `jobs_enabled=true`; initially only README and one initial commit existed, no pipeline history.
- Created isolated branch `ci/jarvis-memory-m1-fallback-2026-11-24` with GitLab CI config and harness. No commits made to GitLab `main`.
- Branch URL: https://gitlab.com/sokfrut-tech/jarvis/-/tree/ci/jarvis-memory-m1-fallback-2026-11-24
- Added `.gitlab-ci.yml` with runner smoke stage and focused M1 validation stage. Added `.ci/run-jarvis-memory-m1.sh` which fetches only the public OGAM pinned commit `67c896cf21cab6f4d0c0ba9118e6013770165252`, copies four M1 source modules and four focused tests, sets up an isolated TypeScript/Jest harness, runs focused TypeScript + Jest, and probes the schema DDL/constraints/rollback using Node's bundled SQLite. No private submodule token/secrets required.
- Root GitLab README updated with purpose, source pin, safety boundaries and current state.
- GitLab CI create-pipeline API explicitly returned: `Identity verification is required in order to run CI jobs`. Push-triggered pipelines #1–#5 were also recorded as failed immediately with zero jobs and no started_at/duration. Thus no executor was assigned; this is not evidence of a product/test failure. Although shared runners are enabled, actual runner execution cannot be confirmed until GitLab identity verification is completed.
- Current branch head at setup review: `39f71fec6283c90bd056eca8f0acdc5e9695af1d`; README was updated after this head.
- GitLab pipeline config YAML syntax was independently parsed with Ruby Psych successfully. The job script itself has not been executed by a runner.
- Independent local SQL check: manually executed the M1 DDL from the PR against Node `node:sqlite` / SQLite 3.49.1. Foreign-key PRAGMA, JSON1, savepoint rollback and DDL CHECK constraints (scope, approval timestamp, expiry, confidence) passed. This is a Node SQLite result, **not** the exact Android op-sqlite 15.2.5 runtime and not a Jest/typecheck result.
- GitHub PR #5 was only a validation probe and produced no Actions workflow run/checks; close it as obsolete. Keep main implementation PR #4 open and draft.
- Remaining gates: GitLab account identity verification; then actual GitLab pipeline and logs (focused Jest, focused TS typecheck, Node SQLite schema test); then actual OPPO PGEM10 op-sqlite capability probe and Android app build/device checks. Do not advance to Jarvis scheduler M2 before memory acceptance gates pass.


### GitLab fallback follow-up
- Latest GitLab fallback branch head: `628cd56bafd594a291a5a6b7cb1e3a908da85bde`.
- README, CI YAML and focused harness script are committed to `sokfrut-tech/jarvis` branch `ci/jarvis-memory-m1-fallback-2026-11-24`.
- GitLab YAML syntax independently parsed successfully via Ruby Psych.
- Latest push pipeline #6: https://gitlab.com/sokfrut-tech/jarvis/-/pipelines/3106803480 — failed immediately, `started_at=null`, zero jobs; earlier push pipelines #1–#5 show the same pre-job failure.
- Manual pipeline create API continues to return the explicit identity-verification requirement. This is an account-level policy barrier before runner assignment, not evidence of no available runner. Shared and group runners are enabled in project metadata, but their execution capability remains untested.
- Once the account identity step is completed, trigger a pipeline on the fallback branch and inspect both jobs/logs. Do not merge fallback branch into GitLab main until a real run proves it works.


## Post-user-reported GitLab verification retry — 2026-11-24
- User reported "Готово" after being asked to complete GitLab identity verification.
- Immediately retried GitLab pipeline creation on `ci/jarvis-memory-m1-fallback-2026-11-24`; API still returned HTTP 400: `Identity verification is required in order to run CI jobs`.
- Fetched authenticated GitLab current user: ID 43704569, username `sokfrut`, active; `confirmed_at` exists (email/account confirmation) but that field does not establish completion of GitLab's separate identity-verification gate. `two_factor_enabled=false` is unrelated and not assumed to be the blocker.
- Project still reports shared runners, group runners and jobs enabled.
- Latest pipeline #7 (MR event) failed immediately with `started_at=null`, zero jobs: https://gitlab.com/sokfrut-tech/jarvis/-/pipelines/3106808057
- No runner has started. Do not claim that the reported identity verification has been recognized by the GitLab CI backend. Likely need the GitLab verification flow to be completed on the same account/session or reconnect/refresh the GitLab integration after the verification; ask user to confirm the exact GitLab verification screen completed and, if so, reconnect GitLab integration before another retry.


## External CI executor — CircleCI confirmed from prior records — 2026-11-24
- Corrected the fallback inventory using the user's prior setup record dated 2026-11-19: **CircleCI is the actually registered/connected external CI service**, not merely a suggested option.
- User explicitly reported registering/connecting CircleCI to GitLab for project `sokfrut-tech/russsearchoppo`.
- The CircleCI connection smoke test `say-hello-workflow` succeeded, confirming basic GitLab authorization/connection at that time.
- A `ferrite-dsp` workflow was also executed through CircleCI; GitLab showed associated statuses/repeated runs. The final Ferrite DSP validation was not confirmed because direct CircleCI job logs/session access were not available to the assistant.
- Existing CircleCI project config was recorded at `.circleci/config.yml` on branch `feat/ferrite-neon-vad-clean` in `sokfrut-tech/russsearchoppo`.
- Buildkite and Semaphore were only discussed; no registration/connection or execution evidence was found for them.
- **Important limitation:** the current assistant tool inventory does not expose a direct CircleCI connector/session. Historical registration and successful smoke test are evidence of prior setup, not proof that the current account authorization is still active or that this assistant can inspect/run CircleCI jobs now.
- Proposed next validation path for OGAM M1: inspect whether the existing CircleCI account can authorize the separate GitLab project `sokfrut-tech/jarvis` (project ID `88675977`) and run an isolated pipeline there, without changing OGAM PR #4 or merging the fallback branch. Reuse the existing tested integration only if its current access permits it; do not assume the prior authorization for `russsearchoppo` automatically covers `jarvis`.
- Preserve M1 gates: actual focused Jest + TypeScript job results, schema probe logs, then OPPO PGEM10 native `op-sqlite` capability probe. Do not proceed to M2 until these pass.


## CircleCI fallback preparation — 2026-11-24
- User confirmed continuing with the previously registered CircleCI account as the alternative runner for OGAM Jarvis M1.
- Confirmed there is no direct CircleCI connector/action in the current ChatGPT tool inventory and no CircleCI plugin was returned by plugin discovery. Do not claim CircleCI project access, pipeline execution or job-log access from this session.
- Current CircleCI documentation confirms CircleCI Cloud supports GitLab SaaS repositories. For GitLab SaaS, a separate CircleCI project/pipeline must be created/authorized for the target repository; prior access to `sokfrut-tech/russsearchoppo` does not automatically grant access to `sokfrut-tech/jarvis`.
- Added CircleCI config to the isolated GitLab fallback branch only: `.circleci/config.yml`, branch `ci/jarvis-memory-m1-fallback-2026-11-24`, commit `58f47e0da0e096f76a6d86e5054b0fa087a78b76`.
- Config uses `cimg/node:22.14`, checks Node/npm/Git, then runs the existing pinned M1 harness `.ci/run-jarvis-memory-m1.sh`. Workflow is branch-filtered to the isolated fallback branch. No secrets are required by the harness; it fetches public OGAM commit `67c896cf21cab6f4d0c0ba9118e6013770165252`.
- This is configuration preparation only. CircleCI has not yet been authorized for project `sokfrut-tech/jarvis`; no CircleCI pipeline/job has run, and no Jest/TypeScript/SQLite pass is claimed.
- Next user action: in CircleCI, select the existing CircleCI organization, create/set up a project using the GitLab SaaS integration, authorize the GitLab connection if requested, select repository `sokfrut-tech/jarvis`, choose branch `ci/jarvis-memory-m1-fallback-2026-11-24`, and configure `.circleci/config.yml` as the pipeline config. Save/setup the pipeline and trigger the branch. CircleCI docs: https://circleci.com/docs/guides/getting-started/create-project/ and https://circleci.com/docs/guides/integration/set-up-vcs-connections/.
- Keep GitLab `.gitlab-ci.yml` in place for now; do not remove or disable the previous fallback until CircleCI is proven to execute successfully. Do not merge either fallback branch or implementation PR #4. M1 remains gated on actual focused Jest + TypeScript + SQLite runner logs, followed by the OPPO PGEM10 native op-sqlite probe.



## User checkpoint — pause before further implementation — 2026-11-24
- User explicitly instructed: record the current state and, before doing more work, inspect the existing project/factory library because the prior setup and integration details should already be documented there.
- Reviewed the canonical factory records before proposing any new account, token, dependency or setup:
  - `docs/MASTER_PROJECT_INDEX.md`
  - `docs/FACTORY_CONTINUATION_BRIEF.md`
  - `docs/OPEN_SOURCE_GAP_RECOVERY_POLICY.md`
  - `coordination/shared/AGENT_EXCHANGE_PROTOCOL.md`
  - this OGAM handoff and the earlier Library recovery record `JARVIS_RECOVERY_HANDOFF_2026-11-08.md`.
- Global rule is mandatory: unavailable/private dependencies trigger search → inspect → compare → license-check → adapt/integrate → test → document. Do not stop at “need a token”; do not remove requested behavior, add fake stubs or claim success without evidence. Avoid unnecessary reliance on another party's private repo/account/secret.
- Confirmed today's GitHub Actions run `Jarvis Memory M1 Android Native Probe #1` was manually triggered on `main` commit `ccbe8d0` and failed in 15 seconds before build because workflow requires secret `PRO_SUBMODULE_PAT` for private `off-grid-ai/mobile-pro` and `off-grid-ai/shared`. No artifact was produced. Node 20 deprecation was only a warning, not the failure cause.
- User clarified `sokfrut-tech` is their own GitHub account and `off-grid-ai` is not theirs. Do not ask the user to create an account/token in `off-grid-ai`, and do not request or expose any token in chat.
- Important already-documented alternative: this handoff records an isolated GitLab fallback branch `ci/jarvis-memory-m1-fallback-2026-11-24` in `sokfrut-tech/jarvis`, with a pinned harness that fetches only public OGAM M1 source commit `67c896cf21cab6f4d0c0ba9118e6013770165252`, copies the four M1 production modules and four tests, and runs focused TypeScript/Jest plus Node SQLite schema checks without private submodule credentials. CircleCI config was also prepared on that branch at commit `58f47e0da0e096f76a6d86e5054b0fa087a78b76`; CircleCI was previously registered/connected for `sokfrut-tech/russsearchoppo`, but current authorization for `sokfrut-tech/jarvis` and actual CircleCI execution were not verified. GitLab runner attempts were blocked before jobs by identity-verification policy.
- Current OGAM implementation checkpoint remains: M1 branch `feature/jarvis-step-1-memory-m1-2026-11-24`, PR #4 draft/open/unmerged; latest branch head recorded in chat as `a267478a8bf6b290e71b3d86992852b0b192a58f`; main workflow commit `ccbe8d086618d1ffaa7f4656d2e91b3a9fcf15d8`. The native Android APK was not built; OPPO PGEM10 probe has not run. Earlier focused CircleCI success only covered baseline commit `bc68c7ca8a27d20fae9ce913e606fd076d12f726`, not the latest head.
- M1 source is implemented (typed memory schema/database/repository, explicit confirmation, scope isolation, expiry guard and focused tests). Do not merge PR #4 or begin M2 until exact-head tests and native Android/device acceptance pass.
- Before any further changes, inspect the existing fallback harness and its dependency inventory, then inspect OGAM's actual workflow/action/package manifests to determine whether Android native validation can be separated from the unrelated private workspace. Prefer the already-recorded CircleCI/GitLab fallback route if it can be made to run. Do not ask the user to create a new token until existing factory records and available owned integrations have been exhausted.
- Status: checkpoint recorded; no OGAM source/workflow changed by this checkpoint update.


## 2026-11-24 continuation — fallback harness audit

- Audited owned GitLab project `sokfrut-tech/jarvis` (project ID `88675977`), branch `ci/jarvis-memory-m1-fallback-2026-11-24`.
- Confirmed the harness previously pinned OGAM source to stale commit `67c896cf21cab6f4d0c0ba9118e6013770165252`, not the current reviewed M1 head `a267478a8bf6b290e71b3d86992852b0b192a58f`.
- Updated `.ci/run-jarvis-memory-m1.sh` to pin the latter immutable SHA. Verified the committed file now contains that exact SHA.
- Updated `.circleci/config.yml` runtime from `cimg/node:22.14` to `cimg/node:26.0`, aligning with the GitLab `node:26-bookworm` harness and its bundled `node:sqlite` probe. Verified the committed config.
- The focused harness still tests TypeScript/Jest with a resolver stub for `@op-engineering/op-sqlite`, plus Node's bundled SQLite DDL/constraint/savepoint probe. It is NOT an Android APK build and NOT an OPPO native op-sqlite runtime test.
- GitLab latest pipeline `3108084086` (commit `0d3ba3ebb73bdfe7a7f6e68ebb7567e22906cab5`) failed immediately; `started_at=null`, `finished_at` equals creation time, and pipeline jobs endpoint reports zero jobs. Thus no harness test ran. This is consistent with the earlier runner identity-verification gate; do not report as test failure or success.
- GitLab project metadata confirms shared runners enabled, but that does not bypass the account-level identity gate.
- CircleCI configuration exists in the branch, but no CircleCI integration/API is exposed in connected tools, so project registration/authorization and run status cannot be verified from this session. Do not tell user a CircleCI run happened.
- OGAM PR #4 remains unmerged; M2 remains blocked pending focused CI and real Android/OPPO native acceptance.


## 2026-11-24 continuation — CircleCI access boundary

- Rechecked available connected tool integrations: no CircleCI API/connector actions are exposed in this session. Therefore cannot inspect CircleCI project registration, authorization, pipeline history, or trigger a CircleCI run; do not claim that CircleCI is connected or tested.
- GitLab project `sokfrut-tech/jarvis` branch head is `0d3ba3ebb73bdfe7a7f6e68ebb7567e22906cab5`. This commit includes the two intended updates: focused harness pin to OGAM M1 `a267478a8bf6b290e71b3d86992852b0b192a58f` and CircleCI Node image `cimg/node:26.0`.
- The latest GitLab pipeline for this branch (`3108084086`) is failed with `started_at=null`, immediate finish, and zero jobs. No test command ran. Existing CircleCI config is present but its remote execution status is unknown.
- OGAM Android workflow was inspected. It explicitly requires private `off-grid-ai/mobile-pro` and `off-grid-ai/shared` packages to run the complete app build; the setup action skips those checkouts only when token is empty, but then the complete TypeScript/app build cannot be assumed to pass because file dependencies and test imports reference the private sibling workspace. Do not remove this requirement or represent a focused test as APK build.
- Attempted to create a separate secret-free GitHub Actions focused-validation branch in OGAM from M1 head. Branch `ci/jarvis-memory-m1-github-2026-11-24` was created, but GitHub file creation returned HTTP 422 (missing sha) and no workflow/script was committed. Treat branch as an empty branch at the M1 base; no CI was triggered. This is not a deliverable and must be revisited carefully or cleaned up when branch-delete capability is available.
- Next safe route: either obtain actual CircleCI integration/authorization through the user's existing CircleCI project UI (without asking for any foreign token), or implement focused GitHub Actions via Git Data API (blob/tree/commit/ref) with fresh tree/ref inspection. Preserve separate gates: focused TS/Jest/Node SQLite ≠ full Android APK ≠ OPPO native SQLite acceptance.


## 2026-11-24 continuation — focused GitHub Actions M1 validation succeeded

- Recovered the previously empty OGAM validation branch `ci/jarvis-memory-m1-github-2026-11-24` and inspected its exact ref/head before writing.
- Used Git Data API (blob → tree → commit → ref with expected-head lease) to commit two files:
  - `.ci/run-jarvis-memory-m1.sh` — isolated harness based on the reviewed M1 source and all four focused test files; pin updated to immutable M1 head `a267478a8bf6b290e71b3d86992852b0b192a58f`.
  - `.github/workflows/jarvis-memory-m1-focused.yml` — secret-free push + manual-dispatch workflow, Node.js 26, runs the focused harness only.
- Commit: `e5ee7a40f3e9f3c29fb0dd28d140346b496b88a7`.
- Verified both committed files by fetching them from the branch; the branch ref advanced successfully from parent `a267478a8bf6b290e71b3d86992852b0b192a58f`.
- GitHub Actions automatically started on push: run #1, ID `45382511098`, URL https://github.com/sokfrut-tech/OGAM/actions/runs/45382511098.
- Run completed successfully at 2026-11-24 11:16:04Z. Job `focused-validation` ID `138404881465` concluded `success`; all setup, checkout, Node 26 and focused-validation steps completed successfully. This proves the isolated script exited 0 for the pinned M1 source. Run duration for the focused command was approximately 12 seconds.
- Scope of this green run: focused M1 TypeScript type-check, four focused Jest suites, production schema compilation, Node 26 `node:sqlite` schema/migration DDL + CHECK constraint + savepoint rollback probe. The harness deliberately uses a resolver stub for `@op-engineering/op-sqlite` because Jest mocks the native module. This is NOT a full React Native/Android APK build and NOT an OPPO device/native `op-sqlite` runtime probe.
- This is a material gate passed for M1 source-level validation at the exact reviewed M1 head. PR #4 remains draft/open/unmerged. Do not start M2 yet: Android arm64 APK build and real PGEM10 native SQLite/device acceptance remain outstanding.
- Next: obtain the actual CI log text for the passing job if accessible, then solve the separate Android build/private-workspace dependency route without requesting credentials for the foreign `off-grid-ai` account. Keep all gates explicitly separated.


## 2026-11-24 continuation — isolated Android ARM64 OP-SQLite APK built successfully

- Created a separate validation branch in the user's own repository `sokfrut-tech/OGAM`: `ci/jarvis-memory-m1-op-sqlite-device-probe-2026-11-24`, based on the exact M1 source head `a267478a8bf6b290e71b3d86992852b0b192a58f`.
- Added a standalone React Native 0.83.1 Android app under `validation/android-native-probe/`, depending only on public packages and exact `@op-engineering/op-sqlite` 15.2.5. It copies the actual M1 `types/schema/database/repository` modules plus existing `generateId` and `logger` source from the OGAM checkout at build time. It does not check out or stub any `off-grid-ai` private packages.
- The probe app executes the actual production M1 database/repository on OP-SQLite: open `jarvis_memory.db`, migrate schema v1, read SQLite version, optional JSON1 check, enable and verify foreign keys, create/read/JSON round-trip a proposal, explicitly confirm it, list it by global scope, reject a second proposal, test savepoint rollback, and verify a real SQLite CHECK constraint rejects an invalid kind. The app displays PASS/FAIL and diagnostic details on-device.
- Added `.ci/prepare-jarvis-memory-m1-native-probe.sh` and `.github/workflows/jarvis-memory-m1-op-sqlite-probe.yml`. Workflow installs only public dependencies, verifies OP-SQLite Android autolinking, builds a release APK for `arm64-v8a`, verifies ARM64 native libraries in the APK, calculates SHA-256, and uploads APK + checksum + generated npm lockfile as an artifact.
- Initial workflow attempts exposed a GitHub Action SDK input parsing issue (semicolon-separated packages were passed as one package; then setup-android default attempted removed `tools`). Fixed by configuring `setup-android` with `packages: platform-tools` and invoking `sdkmanager` with each required package as a separate quoted argument. These failed runs stopped before npm install/build and are not build failures.
- Final run succeeded: GitHub Actions run `45384391834`, job `138411432821`, URL https://github.com/sokfrut-tech/OGAM/actions/runs/45384391834. Build command `gradle --no-daemon assembleRelease -PreactNativeArchitectures=arm64-v8a` completed `BUILD SUCCESSFUL` in 5m53s. OP-SQLite autolinking passed. APK contains `lib/arm64-v8a/libop-sqlite.so` (1,803,256 bytes), proving the actual native OP-SQLite ARM64 library was packaged. APK size 18 MB.
- APK SHA-256: `c501bb207d53820442184e2fd511e6313943cb1a5296ae6f1b06578d26c1ef68`.
- Artifact: `Jarvis-M1-OPSQLite-Native-Probe-APK`, artifact ID `14916215878`, archive size 9,644,612 bytes, not expired at checkpoint time. It contains `app-release.apk`, `.sha256`, and generated `package-lock.json`. User can download from the run page's Artifacts section.
- Final workflow branch head at the successful run: `1e42474b5b8e351b9e736bb13ccafbee6f396d36`. Subsequent changes are not needed for this successful run. Do not merge the validation branch into production automatically.
- Important remaining gate: the APK has been compiled and contains the native module, but it has NOT yet been installed/launched on the user's OPPO Find X6 Pro (PGEM10). The on-device PASS/FAIL screen must be run on that phone; only then can M1 native device acceptance be claimed. Build success alone does not prove runtime success.
- PR #4 (M1 production implementation) remains draft/open/unmerged. M2 remains blocked until the user/device acceptance result is observed. The standalone probe is deliberately separate from the full OGAM APK build and does not require foreign `off-grid-ai` credentials.

- Opened draft PR #6 in OGAM, targeting the M1 feature branch (not main): https://github.com/sokfrut-tech/OGAM/pull/6. It remains draft/open/unmerged pending installation and runtime acceptance on PGEM10.


## 2026-11-24 continuation — investigate probe APK launch failure

- User reported that the installed Jarvis M1 Probe APK did not launch on OPPO PGEM10. No live device screen/logcat was available in this chat, so the exact phone-side crash cause is not yet known.
- Inspected the complete changed-file list and the actual PR #6 launcher configuration:
  - AndroidManifest.xml declares android.intent.action.MAIN + android.intent.category.LAUNCHER for .MainActivity, label "Jarvis M1 Probe". Android creates the app-drawer launcher entry automatically; no shortcut-creation permission or special shortcut API is used by this APK.
  - MainActivity.kt registers React Native component JarvisM1Probe, matching app.json and index.js.
  - App.tsx automatically runs the native SQLite probe in useEffect on startup. Therefore a startup crash may occur before the screen renders, during React Native bootstrap or OP-SQLite initialization; source inspection alone cannot identify the exact cause.
- Added an emulator runtime diagnostic stage to .github/workflows/jarvis-memory-m1-op-sqlite-probe.yml on the existing PR #6 branch:
  - Commit: 8c0dc1940e7779c7bf64a5a27fb3098aafca4507.
  - Builds native libraries for both arm64-v8a and x86_64 so the same APK can be launched in an Android x86_64 emulator while retaining the phone's ARM64 library.
  - Uses Android API 35 Pixel 2 emulator, installs and launches the release APK, checks process survival, captures activity state, full logcat and a launch screenshot into validation/android-native-probe/runtime-diagnostics/, and uploads diagnostics with the APK.
  - Emulator step is continue-on-error: true so logs/artifact can still be uploaded if runtime launch fails. Interpret emulator result separately from APK compilation and from PGEM10 physical-device acceptance.
- New GitHub Actions run started: 45393169372, https://github.com/sokfrut-tech/OGAM/actions/runs/45393169372. At last check, the build job was still in progress; emulator runtime step had not started yet. The branch head is 8c0dc1940e7779c7bf64a5a27fb3098aafca4507.
- PR #6 remains draft/open/unmerged; PR #4 remains draft/open/unmerged. Do not merge or start M2 based on emulator success alone. A successful emulator launch still does not substitute for the user's PGEM10 test.


## 2026-11-24 continuation — emulator timeout diagnosed and CI runner adjusted

- Re-checked completed GitHub Actions run 45393169372 after the user reported that the run eventually finished.
- Job 138441913934 concluded success, but the emulator step itself did NOT launch the APK. Its conclusion was also success only because continue-on-error: true is set on that diagnostic step.
- Full job log confirms the emulator never registered with ADB: repeated adb: device 'emulator-5554' not found, followed by Timeout waiting for emulator to boot. Thus this run produced no application runtime result.
- Downloaded artifact 14921016655 and inspected its contents. It contains only APK, checksum, and package-lock; no runtime-diagnostics files were generated because the emulator action failed before its script ran. This confirms we have no emulator logcat/screenshot from this run.
- The same job's APK build and native library checks completed successfully. This remains build evidence only, not app-launch evidence.
- Applied a CI-only correction to .github/workflows/jarvis-memory-m1-op-sqlite-probe.yml: pin runner from ubuntu-latest (which resolved to Ubuntu 26.04 in this run) to ubuntu-24.04, and set explicit headless emulator options (-no-window -no-audio -no-boot-anim -gpu swiftshader_indirect -no-snapshot-save).
- Correction commit: 92e9cd8ec4c1eb5b6ded9314443b572633879c8c on ci/jarvis-memory-m1-op-sqlite-device-probe-2026-11-24. Push should trigger a fresh run; inspect its actual emulator step conclusion and uploaded diagnostics before interpreting.
- PR #6 and PR #4 remain draft/open/unmerged. No change to production code and no claim of PGEM10 acceptance.

- Follow-up run after the runner correction: 45396893308 (https://github.com/sokfrut-tech/OGAM/actions/runs/45396893308), job 138454946957. At the latest inspection it was still running; SDK package installation was in progress and emulator launch had not yet started. Do not report a runtime result until that step completes.

## 2026-11-24 continuation — emulator root cause identified and corrected

- Inspected the complete log for run 45396893308 after it completed. The APK build/checksum stages succeeded, but the emulator action still timed out before ADB connected. The real root cause is explicit in the runner log: reactivecircus/android-emulator-runner automatically passed `-accel off` because Linux hardware acceleration is disabled, while Android Emulator 37.3.10.0 refuses software CPU emulation unless `ANDROID_I_WANT_MY_TCG=yes` is set. Exact log: `Software CPU emulation (-accel off) is not supported. A hardware CPU accelerator is required (or set ANDROID_I_WANT_MY_TCG=yes to force TCG software emulation).`
- This is a CI emulator infrastructure failure, not an application crash. No APK was installed/launched in that emulator attempt, so it provides no React Native/OP-SQLite runtime evidence.
- Fixed `.github/workflows/jarvis-memory-m1-op-sqlite-probe.yml` on the same isolated probe branch:
  - Added step environment `ANDROID_I_WANT_MY_TCG: 'yes'` to explicitly permit the runner's software CPU emulation mode.
  - Removed `continue-on-error: true` from the emulator step so a runtime/boot failure cannot masquerade as a green job.
  - Changed artifact upload to `if: always()` and `if-no-files-found: warn`, preserving the already-built APK even if emulator validation fails.
- Fix commit: `71a07d01908ecc66749858dc60ca8052c48778b5`.
- New run triggered by the fix: `45400312506`, https://github.com/sokfrut-tech/OGAM/actions/runs/45400312506. Job ID `138466850741`. At handoff update time it was still in progress; checkout and M1 source preparation passed, Node/Java setup passed, Android SDK setup was running. APK build and emulator launch had not yet been reached. Recheck before reporting a result.
- PR #6 remains draft/open/unmerged and targets M1 branch `feature/jarvis-step-1-memory-m1-2026-11-24`; PR #4 remains draft/open/unmerged. No production merge, no M2 start, and no PGEM10 physical-device acceptance.

## 2026-11-24 continuation — probe startup crash diagnosed, fixed, and verified PASS in Android 15 emulator

- Downloaded and inspected artifact `14925987676` (`runtime-diagnostics/logcat.txt`) from failed run `45404892708` on `ci/jarvis-memory-m1-op-sqlite-device-probe-2026-11-24`.
- Root cause of `com.jarvism1probe` launch crash (on both emulator and PGEM10):
  - All native libraries (`libreactnative.so`, `libhermesvm.so`, `libop-sqlite.so`, etc.) loaded cleanly (`ok`) and all 11 `arm64-v8a` `.so` libraries in the APK are 16 KB ELF page-aligned (`p_align=0x4000`).
  - `validation/android-native-probe/android/app/src/main/AndroidManifest.xml` configured `android:theme="@android:style/Theme.Material.NoActionBar"`, whereas `MainActivity` extends `ReactActivity` (`androidx.appcompat.app.AppCompatActivity`), throwing immediately in `onCreate()`: `java.lang.IllegalStateException: You need to use a Theme.AppCompat theme (or descendant) with this activity.`
- Root cause of CI emulator step syntax failure in `45404892708`: `reactivecircus/android-emulator-runner@v2` executes `script:` line-by-line via `/usr/bin/sh -c`, breaking multi-line `if ... fi` blocks (subsequently extracted to `.ci/run-jarvis-m1-emulator-probe.sh` in `7b39517f` / `a91efdbb`).
- Applied fix on top of `a91efdbb` in `sokfrut-tech/OGAM` PR #6 (`ci/jarvis-memory-m1-op-sqlite-device-probe-2026-11-24`), commit `956f7127a7656b8eb99fe3967da92c1a89054806`:
  - Added `validation/android-native-probe/android/app/src/main/res/values/styles.xml` (`AppTheme` inheriting `Theme.AppCompat.DayNight.NoActionBar`).
  - Updated `AndroidManifest.xml` to `android:theme="@style/AppTheme"`.
  - Added release-mode logcat markers `[JARVIS_M1_PROBE] PASS <json>` / `[JARVIS_M1_PROBE] FAIL <msg>` in `validation/android-native-probe/App.tsx`.
  - Updated `.ci/run-jarvis-m1-emulator-probe.sh` to launch with `am start -W`, poll `logcat` for `[JARVIS_M1_PROBE] (PASS|FAIL)`, capture `probe-result.txt` + `launch-screen.png` + `process-id.txt`, and fail if any crash signature or missing `PASS` marker is seen.
- Verified in GitHub Actions run `45414070190` (`https://github.com/sokfrut-tech/OGAM/actions/runs/45414070190`, job `138515587396`, `completed/success` in `18m26s`):
  - Logcat output (`runtime-diagnostics/probe-result.txt`):
    `[JARVIS_M1_PROBE] PASS {"sqliteVersion":"3.50.4","schemaVersion":1,"json1":true,"foreignKeys":true,"proposalRoundTrip":true,"explicitConfirmation":true,"rejection":true,"savepointRollback":true,"checkConstraint":true,"databasePath":"/data/user/0/com.jarvism1probe/databases/jarvis_memory.db","probeRecordId":"497a60b6-36dd-484f-bb07-41e639501c24"}`
  - Visual screenshot (`runtime-diagnostics/launch-screen.png`) confirms `PASS / Нативная проверка завершена` rendered by the app.
  - Updated artifact: `Jarvis-M1-OPSQLite-Native-Probe-APK` (`id=14932771575`, size `14,819,306` B, APK `31,572,769` B, SHA-256 `c71fb87b8654e8da75f97d0f50a824971c086a1a4228c1b710d01e878092f7e5`), all 11 `lib/arm64-v8a/*.so` libraries including `libop-sqlite.so` (`1,803,256` B) verified `p_align=0x4000`.
- Boundary preserved: emulator PASS confirms Android runtime + real native `@op-engineering/op-sqlite` 15.2.5 (`SQLite 3.50.4`, `JSON1=true`, `FK=true`, `SAVEPOINT`, `CHECK`). Physical OPPO Find X6 Pro (`PGEM10`) installation and PASS screen confirmation remain required before accepting Step 1 M1. PR #4 and PR #6 remain Draft and unmerged.



## Inventory refresh — 2026-11-24 17:52 local

### Current verified M1 native probe state
- OGAM PR #6 remains OPEN + DRAFT + UNMERGED; head `956f7127a7656b8eb99fe3967da92c1a89054806`, base `feature/jarvis-step-1-memory-m1-2026-11-24` at `a267478a8bf6b290e71b3d86992852b0b192a58f`.
- Latest Android native probe workflow run: `45414070190`, job `138515587396`, completed SUCCESS. This includes a real Android emulator app launch and OP-SQLite native runtime checks, not merely APK compilation.
- Verified runtime: SQLite 3.50.4; schema v1; JSON1 true; foreign keys true; proposal round-trip true; explicit confirmation true; rejection true; savepoint rollback true; CHECK constraint true. The app process remained alive and the PASS screen screenshot was captured.
- Fixed startup crash: Manifest used platform Material theme with ReactActivity/AppCompat; now uses AppCompat descendant `AppTheme`.
- Latest probe artifact: ID `14932771575`, name `Jarvis-M1-OPSQLite-Native-Probe-APK`, not expired at inventory time; archive 14,819,306 bytes; APK SHA-256 `c71fb87b8654e8da75f97d0f50a824971c086a1a4228c1b710d01e878092f7e5`.
- APK download: https://github.com/sokfrut-tech/OGAM/actions/runs/45414070190/artifacts/14932771575
- Workflow evidence: https://github.com/sokfrut-tech/OGAM/actions/runs/45414070190
- Physical OPPO Find X6 Pro PGEM10 install and PASS screen have NOT yet been confirmed. Do not claim phone acceptance or close M1 until user reports/produces the phone result.

### Pull request inventory (live GitHub snapshot)
- PR #1 Step 2 storage/privacy bridge — OPEN, DRAFT, UNMERGED; head `71cbffbbe2a5631732553dc4bd238b5d074af037`, base main.
- PR #2 Breeno/ColorOS adaptation research — OPEN, DRAFT, UNMERGED; head `85a9326f40c289bd007ff7f098b5f916a3ee0d16`, base main.
- PR #3 Android agent ecosystem research — OPEN, DRAFT, UNMERGED; head `56b667ff637bd5098df67dc76ef6afa7e5a5af46`, base Breeno research branch.
- PR #4 Step 1 M1 memory database foundation — OPEN, DRAFT, UNMERGED; head `a267478a8bf6b290e71b3d86992852b0b192a58f`, base Step 2 branch.
- PR #5 temporary CI validation — CLOSED, NOT MERGED; validation-only, obsolete.
- PR #6 isolated Android OP-SQLite probe — OPEN, DRAFT, UNMERGED; validation-only, base M1 PR #4 branch.

### Validation boundaries and next gates
- M1 source validation passed in secret-free GitHub Actions run `45382511098`: focused TypeScript, four Jest suites, schema compile and Node 26 SQLite DDL/constraints/savepoint checks. Jest native binding is stubbed in that focused harness; it is not Android native evidence.
- Native Android emulator validation passed in `45414070190` with actual OP-SQLite 15.2.5; still not physical-device acceptance.
- Full OGAM application build remains a separate blocked route because private foreign submodules `off-grid-ai/mobile-pro` and `off-grid-ai/shared` are inaccessible. Do not request or create `PRO_SUBMODULE_PAT`; do not confuse standalone probe APK with the full Jarvis app.
- GitLab fallback project `sokfrut-tech/jarvis` (ID `88675977`) exists, but pipelines failed before jobs due account-level identity verification; no CI tests ran there. CircleCI config was committed in its branch, but no connected CircleCI API/run was verified.
- M2/scheduler, prompt memory retrieval, automatic model writes, UI, sync and encryption are NOT implemented in M1 and remain gated. Do not merge PRs or change production branches without explicit user approval.
- Immediate next action: user installs the latest standalone M1 probe APK on OPPO PGEM10 and reports whether the app opens to PASS. If PASS, record device acceptance and review PR #4/#6 before planning M2; if not, collect exact phone error evidence and diagnose without asking the user to repeat an already-tried old APK.

## 2026-11-24 continuation — user reported PGEM10 M1 probe launched and working

- User reported directly after installing the updated standalone `Jarvis M1 Probe` APK (`Jarvis-M1-OPSQLite-Native-Probe-APK`, artifact `14932771575`, SHA-256 `c71fb87b8654e8da75f97d0f50a824971c086a1a4228c1b710d01e878092f7e5`, run `45414070190`, commit `956f7127a7656b8eb99fe3967da92c1a89054806`): **"Jarvis M1 Probe запустилась работает продлжаем что следующее"**.
- Evidence boundary preserved truthfully: user verbal launch/working confirmation on OPPO Find X6 Pro (`PGEM10`) received; phone screenshot / per-row PASS printout was not attached and is noted as optional archival confirmation.
- PR #4 / PR #6 code review summary prior to M2:
  - PR #4 core M1 implementation (`src/services/jarvisMemory/{types,schema,database,repository}.ts`) and all 4 focused Jest test suites (`schema`, `database`, `repositoryValidation`, `repositoryGuards`) passed isolated Node/TypeScript/Jest/SQLite CI (`45382511098`), native Android 15 OP-SQLite emulator probe (`45414070190`), and now user-confirmed launch/operation on physical `PGEM10`.
  - Cleanup note for finalizing PR #4: PR #4 still contains the earlier `PRO_SUBMODULE_PAT`-gated `.github/workflows/jarvis-memory-m1-android.yml` and temporary `src/screens/DeviceInfoScreen.tsx` probe hook, which are superseded by PR #6's secret-free standalone probe (`956f7127`).
- PR #4 and PR #6 remain `OPEN / Draft / UNMERGED`. Ready for user selection of the next workstream: Step 1 **M2** (secret guard, conflict detection + optimistic concurrency, deletion tombstones, expired cleanup, explicit confirmation UI + interactive M2 device probe APK) or PR #1 **Slice 9** (`@offgrid/models` remaining `35 → 0`).

## 2026-11-24 continuation — Jarvis Step 1 M2 implemented, verified in CI & Android 15 emulator (PR #7)

- User selected track `1` (Jarvis Memory Step 1 · M2).
- Created clean isolated branch `sokfrut-tech/OGAM:feature/jarvis-step-1-memory-m2-2026-11-24` based on PR #4 head (`a267478a8bf6b290e71b3d86992852b0b192a58f`), and opened Draft PR #7 (`https://github.com/sokfrut-tech/OGAM/pull/7`, targeting PR #4, `OPEN / Draft / UNMERGED`).
- Implemented M2 production modules and UI without requiring `PRO_SUBMODULE_PAT` or breaking existing M1 tests/contracts:
  - `src/services/jarvisMemory/types.ts`: M2 deletion, secret risk, conflict, draft, update patch, and scoped filter types.
  - `src/services/jarvisMemory/secretGuard.ts` (`MEM-014`/`MEM-021`): value-redacting detector blocking PEM private keys, API/cloud tokens, JWTs, Bearer/Basic/URI credentials, English/Russian credential field names, Luhn-validated card numbers, and wallet seed phrases.
  - `src/services/jarvisMemory/repository.ts`: secret gate on create/propose/update; scoped `findConflicts` (`MEM-010`, duplicate vs differing confirmed values without overwriting confirmed records); optimistic concurrency (`updateRecord` + `MemoryConcurrencyError`, `MEM-011`); savepoint-wrapped `deleteRecord` writing value-free `memory_deletion_tombstones` (`MEM-006`); fail-closed `listActiveConfirmed`, `listPendingProposals`, and `expireStale` clearing `user_approved_at = NULL` to satisfy schema `CHECK` (`MEM-005`).
  - `src/services/jarvisMemory/confirmationController.ts`: explicit `{ userAction: 'explicit_confirm' }` gate and Russian formatting helpers.
  - `src/components/jarvisMemory/MemoryProposalCard.tsx`: standalone RN confirmation card showing scope/kind, value preview, provenance, conflict warning banner, secret caution, and explicit save/reject actions.
- Added 3 M2 Jest suites (`secretGuard.test.ts`, `repositoryM2.test.ts`, `confirmationController.test.ts`) alongside all 4 M1 suites, secret-free harness `.ci/run-jarvis-memory-m2.sh`, and standalone interactive M2 Android app (`validation/android-native-probe/`, `com.jarvism2probe`, **`Jarvis M2 Memory`**).
- Exact-head GitHub Actions verification at commit `276f2f2ca489122b9145410b9552a199683604b3` (matching local Node `v26.13.1` + RN `0.83.1` runs):
  - **Focused M2 CI (`45427014939`, `https://github.com/sokfrut-tech/OGAM/actions/runs/45427014939`):** `completed/success` (`29s`) — strict `tsc --noEmit`, `Test Suites: 7 passed, 7 total` (`31 passed`), and end-to-end execution of compiled M1+M2 TypeScript services against real `node:sqlite` (`SQLite 3.54.1`, `checksPassed: true`).
  - **External Dependency Audit (`45427029659`, `https://github.com/sokfrut-tech/OGAM/actions/runs/45427029659`):** `completed/success`.
  - **Android Native OP-SQLite M2 Probe + Emulator (`45427014740`, `https://github.com/sokfrut-tech/OGAM/actions/runs/45427014740`):** `completed/success` (`15m0s`) — strict `npx tsc --noEmit`, OP-SQLite autolinking, ARM64+x86_64 release APK (`31,607,785` B, SHA-256 `3b7fc2ac873e156992e57fe478e1ed88b524f60e164ccc37abc3ee5ffef6ec87`), APK Signature Scheme v2 (`0x7109871a`), uncompressed 4-aligned `resources.arsc`, all 11 `arm64-v8a` `.so` libs 16 KB aligned (`zip_mod16k=0`, `p_align=0x4000`), live Android 15 emulator `PASS`:
    `[JARVIS_M2_PROBE] PASS {"sqliteVersion":"3.50.4","schemaVersion":1,"json1":true,"foreignKeys":true,"proposalRoundTrip":true,"explicitConfirmation":true,"rejection":true,"savepointRollback":true,"checkConstraint":true,"secretGuardBlocked":true,"conflictDetected":true,"optimisticConcurrency":true,"deleteWithTombstone":true,"expiryBoundary":true,"databasePath":"/data/user/0/com.jarvism2probe/databases/jarvis_memory.db"}`
    Visual screenshot `runtime-diagnostics/launch-screen.png` confirmed green `PASS` on all 7 M1+M2 rows + interactive sandbox UI.
- Artifact: `Jarvis-M2-OPSQLite-Native-Probe-APK` (`id=14938107025`, `https://github.com/sokfrut-tech/OGAM/actions/runs/45427014740/artifacts/14938107025`).
- Acceptance boundary: focused Node CI + Android 15 emulator OP-SQLite PASS verified; physical OPPO Find X6 Pro (`PGEM10`) installation and interactive test (automated PASS + secret block preset + save/confirm/relaunch persistence `MEM-004` + delete/tombstone `MEM-006`) remain to be confirmed by the user before closing M2 and proceeding to **M3** (management: inspect/edit/delete/export UI & controls) or **PR #1 Slice 9**. All PRs remain `Draft` and unmerged.

## 2026-11-24 continuation — physical OPPO PGEM10 M2 device acceptance confirmed

- User tested `Jarvis M2 Memory` (`com.jarvism2probe`, artifact `Jarvis-M2-OPSQLite-Native-Probe-APK`, `id=14938107025`, SHA-256 `3b7fc2ac873e156992e57fe478e1ed88b524f60e164ccc37abc3ee5ffef6ec87`, run `45427014740`, OGAM PR #7 HEAD `276f2f2ca489122b9145410b9552a199683604b3`) on physical OPPO Find X6 Pro (`PGEM10`, Android 16 / ColorOS 16.0.5) and reported: **`"1- да 2-да"`**:
  1. All 7 automated native M1+M2 OP-SQLite self-test rows reported green `PASS` on physical `PGEM10`.
  2. Interactive M2 sandbox flow passed on physical `PGEM10`: secret token blocked (`MEM-014`), proposal confirmed via `MemoryProposalCard`, conflict banner surfaced (`MEM-010`), confirmed record persisted across cold close/relaunch (`MEM-004`), and deletion created a tombstone (`MEM-006`).
- Evidence boundary preserved truthfully: user-reported physical-device PASS (no phone screenshot attached). Focused CI (`45427014939`) and Android 15 emulator runtime (`45427014740`) also remain green at exact HEAD `276f2f2ca489122b9145410b9552a199683604b3`.
- PR #7 (and PR #4/#6) remain `OPEN / Draft / UNMERGED`. Ready for user selection of **M3** (memory management UI/service: search/filter, edit confirmed records, portable JSON export with warning, disable switch, expired cleanup) or **PR #1 Slice 9** (`@offgrid/models` remaining `35 → 0`).

## 2026-11-24 continuation — Hybrid Jarvis Step 1 M3 + M4 implemented & verified in CI + Android 15 emulator (PR #8)

- User approved cross-breeding verified Factory patterns into **Этап 1: Hybrid Jarvis Memory Step 1 · M3 + M4** (`"давай"`).
- Created clean isolated branch `sokfrut-tech/OGAM:feature/jarvis-step-1-memory-m3-m4-2026-11-24` based on PR #7 head (`276f2f2ca489122b9145410b9552a199683604b3`), and opened Draft PR #8 (`https://github.com/sokfrut-tech/OGAM/pull/8`, targeting PR #7, `OPEN / Draft / UNMERGED`, HEAD `60746777c8f0b4afbef13ec709641290879b8c79`).
- Preserved `schema.ts` / `database.ts` v1, M1/M2 repositories, secret guards, and all 7 M1+M2 Jest suites completely untouched (`memory_settings` and `memory_undo_checkpoints` are lazily created by `managementService.ts`).
- Implemented M3 + M4 production modules and standalone RN UI without `PRO_SUBMODULE_PAT`:
  - `src/services/jarvisMemory/types.ts`: additive M3 search, settings, undo checkpoint, source deletion, export bundle, and M4 retrieval contracts.
  - `src/services/jarvisMemory/managementService.ts`:
    - Fail-closed global memory switch (`getMemoryState` / `setMemoryEnabled` / `assertMemoryEnabled`, `MemoryDisabledError`, `MEM-026`, PocketMind pattern) — blocks new proposals & prompt retrieval immediately while preserving stored rows.
    - Scoped substring & kind/status/expiry search (`searchRecords`, `MEM-025`, Nyral pattern).
    - Local 1-step Undo (`updateWithCheckpoint`, `deleteWithCheckpoint`, `undoLastChange` inside `SAVEPOINT jarvis_memory_undo`, PocketMind pattern) — restores pre-edit fields or re-inserts deleted rows while deleting the matching tombstone.
    - Explicit source conversation deletion handler (`handleSourceConversationDeleted`: `'delete_linked'` or `'keep_memory'`, `MEM-019`).
    - Portable JSON export (`exportPortableJson`, `MEM-020`, Nyral pattern) requiring `userInitiated: true`, emitting explicit RU/EN unencrypted warning, and re-screening every row through `assessSecretRisk`.
  - `src/services/jarvisMemory/confirmationController.ts`: checks `assertMemoryEnabled()` in `propose()` after `assertNoSecretRisk()`.
  - `src/services/jarvisMemory/retrievalService.ts`: deterministic M4 scoped prompt retrieval (`retrieveForPrompt`) reading **only** active `confirmed`, non-expired rows in active scopes (`global` + optional exact `projectId` / `conversationId`), Cyrillic/Unicode token + stem-prefix scoring, stable specificity ordering (`conversation > project > global`), strict `maxTokens` / `maxItems` budgeting, fail-closed on disabled/empty/invalid scope (`MEM-007/008/009/026`), and provenance citations (`[mem:<id8> | <scope> | <source>]`).
  - `src/components/jarvisMemory/MemoryManagerPanel.tsx`: standalone dark-slate RN panel (enable/disable card, 1-tap Undo banner, scoped search + kind chips, inline editor, delete, unencrypted JSON export preview).
- Added 2 real-SQLite Jest suites (`managementM3.test.ts`, `retrievalM4.test.ts`), secret-free harness `.ci/run-jarvis-memory-m3-m4.sh`, and upgraded `validation/android-native-probe/` to side-by-side **`Jarvis M3+M4 Memory`** (`com.jarvism3probe`, 3-tab UI: `Самотест` / `Память M3` / `Промпт M4`, Android 16 bottom-bar clearance `paddingBottom: 96`).
- Exact-head GitHub Actions verification at `60746777c8f0b4afbef13ec709641290879b8c79`:
  - **Focused M1–M4 CI (`45452539226`, https://github.com/sokfrut-tech/OGAM/actions/runs/45452539226):** `completed/success` (`29s`) — strict `tsc --noEmit`, **9/9 Jest suites (`39/39` tests)**, and compiled `node:sqlite` (`3.54.1`) M1–M4 integration (`checksPassed: true`).
  - **External Dependency Audit (`45452554820`, https://github.com/sokfrut-tech/OGAM/actions/runs/45452554820):** `completed/success` (`24s`).
  - **Android Native OP-SQLite M3+M4 Probe + Emulator (`45452539356`, https://github.com/sokfrut-tech/OGAM/actions/runs/45452539356):** `completed/success` (`16m15s`) — strict RN `0.83.1` + `op-sqlite 15.2.5` `tsc --noEmit`, ARM64+x86_64 release APK (`31,664,877` B, SHA-256 `68fe1585477f0eb61a124a4239086ebaf18c6e835135839a9ef023fdca7c66bd`), APK Signature Scheme v2 (`0x7109871a`), uncompressed 4-aligned `resources.arsc`, all 11 `lib/arm64-v8a/*.so` libs 16 KB aligned (`zip_mod16k=0`, `p_align=0x4000`), live Android 15 emulator `PASS`:
    `[JARVIS_M3_M4_PROBE] PASS {"sqliteVersion":"3.50.4","schemaVersion":1,"json1":true,"foreignKeys":true,"secretGuardBlocked":true,"conflictDetected":true,"optimisticConcurrency":true,"deleteWithTombstone":true,"expiryBoundary":true,"savepointRollback":true,"checkConstraint":true,"disableFailClosed":true,"searchAndFilter":true,"editAndUndo":true,"deleteAndUndo":true,"sourceDeleteAndExport":true,"scopedPromptRetrieval":true,"databasePath":"/data/user/0/com.jarvism3probe/databases/jarvis_memory.db"}`
    Visual inspection of `runtime-diagnostics/launch-screen.png` confirmed green `PASS` cards/rows on top of clean bottom navigation padding (emulator `System UI isn't responding` dialog was TCG CPU boot slowness on `com.android.phone`, while `com.jarvism3probe` `pid 2212` ran cleanly with `topResumedActivity` and zero errors).
- Artifact: `Jarvis-M3-M4-OPSQLite-Native-Probe-APK` (`id=14949233461`, https://github.com/sokfrut-tech/OGAM/actions/runs/45452539356/artifacts/14949233461).
- Acceptance boundary: focused CI + real `node:sqlite` + Android 15 emulator OP-SQLite PASS verified; physical OPPO Find X6 Pro (`PGEM10`) installation and interactive acceptance (Undo edit/delete, memory pause fail-closed, JSON export warning, and M4 prompt retrieval) remain to be tested by the user. All PRs remain `OPEN / Draft / UNMERGED`. Next after `PGEM10` confirmation: **Этап 2 (`OGAM PR #1 Slice 9`, `@offgrid/models` `35 → 0`)**.

## 2026-11-25 continuation — physical OPPO PGEM10 M3+M4 check passed & M5 overnight audit synced

- User tested **`Jarvis M3+M4 Memory`** (`com.jarvism3probe`, artifact `14949233461`, SHA-256 `68fe1585477f0eb61a124a4239086ebaf18c6e835135839a9ef023fdca7c66bd`, run `45452539356`, PR #8 `60746777c8f0b4afbef13ec709641290879b8c79`) on physical **OPPO Find X6 Pro (`PGEM10`)** and reported: **`"проверил работает"`** *(evidence boundary: user verbal confirmation; no screenshot attached)*. Recorded in PR #8 comment `7153684452`.
- Integrated overnight Factory research from `OGAM PR #3` (`ae6dc5e0e9ae05e3461f74b1410810c7cb94e417`):
  - **`JARVIS_M5_SECURITY_RESILIENCE_AUDIT_2026-11-24.md`:** classifies Step 1 **M5** as `PARTIAL` with two concrete fixes before closing Step 1:
    1. `M5-01` (Medium): move `updateWithCheckpoint` / `deleteWithCheckpoint` mutation + checkpoint insert into one atomic SQLite `SAVEPOINT` so checkpoint failure rolls back both cleanly.
    2. `M5-02` (Medium): replace silent `depth > 8` early return in `secretGuard.ts` (`scanValueRecursive`) with fail-closed / bounded iterative depth+node rejection and boundary tests.
  - **`OPENAI_MULTI_AGENT_ORCHESTRATION_RESEARCH_2026-11-24.md`:** Manager / Agents-as-tools pattern, progressive tool discovery, task-centric persistent `TaskLedger` / Symphony-style durability (reference for Step 2 after Step 1 M5 closes).
- All PRs in `OGAM` (`#1–#4`, `#6–#8`) and `Universal-AI-Factory` (`#27`, `#28`) remain **`OPEN / Draft / UNMERGED`**. Ready for user selection: **M5 Hardening (`M5-01`/`M5-02` + fault-injection/adversarial tests)** and/or **Этап 2 (`PR #1 Slice 9`, `@offgrid/models` `35 → 0`)**.

## 2026-11-25 continuation — Step 1 M5 security & resilience hardening implemented and verified in CI + Android 15 emulator (PR #9)

- User selected track `1` (M5 Hardening).
- Created clean isolated branch `sokfrut-tech/OGAM:feature/jarvis-step-1-memory-m5-hardening-2026-11-25` based on PR #8 (`60746777c8f0b4afbef13ec709641290879b8c79`), and opened Draft PR #9 (`https://github.com/sokfrut-tech/OGAM/pull/9`, targeting PR #8, `OPEN / Draft / UNMERGED`, HEAD `820c6652af70316757a7cbcc7abd328a35f2f71c`).
- Implemented fixes addressing all M5 findings without altering `schema.ts`, `database.ts`, `repository.ts`, or existing 9 M1–M4 Jest suites:
  - **`M5-01` (`src/services/jarvisMemory/managementService.ts`):** wrapped `updateWithCheckpoint` (`SAVEPOINT jarvis_memory_update_with_cp`), `deleteWithCheckpoint` (`SAVEPOINT jarvis_memory_delete_with_cp` wrapping nested delete savepoint + tombstone + checkpoint insert), and `handleSourceConversationDeleted(..., 'delete_linked')` (`SAVEPOINT jarvis_memory_source_delete`) atomically in SQLite savepoints so checkpoint/tombstone insertion errors roll back all mutations cleanly.
  - **`M5-02` (`src/services/jarvisMemory/secretGuard.ts`, `types.ts`):** replaced silent `depth > 8` early return with bounded iterative traversal `scanValueBounded` (`SECRET_SCAN_MAX_DEPTH = 8`, `SECRET_SCAN_MAX_NODES = 500`, branch-local cycle detection) failing closed with `'uninspectable_structure'`; stripped invisible zero-width/bidi characters, applied Unicode `NFKC`, and added mixed-script Latin/Cyrillic homoglyph folding (`pаssword` → `password`).
  - **Prompt delimiter defense (`src/services/jarvisMemory/retrievalService.ts`):** neutralized embedded newlines/control chars and `[JARVIS_CONFIRMED_MEMORY_BEGIN/END]` markers via `sanitizePromptInlineText`.
- Added 10th Jest suite `__tests__/unit/services/jarvisMemory/securityResilienceM5.test.ts` (SQLite `CREATE TEMP TRIGGER` fault injection + depth=8/9 + 501-node + circular + homoglyph + legacy depth-9 export redaction + prompt delimiter escaping + schema mismatch recovery), `.ci/run-jarvis-memory-m5.sh`, and upgraded standalone probe to **`Jarvis M5 Memory`** (`com.jarvism5probe`, uniquely named `dist/Jarvis-M5-Memory.apk`).
- Exact-head GitHub Actions verification at `820c6652af70316757a7cbcc7abd328a35f2f71c`:
  - **Focused M1–M5 Security CI (`45563132400`, https://github.com/sokfrut-tech/OGAM/actions/runs/45563132400):** `completed/success` (`31s`) — strict `tsc --noEmit`, **10/10 Jest suites (`43/43` tests)**, real `node:sqlite 3.54.1` fault-injection & M5 checks (`checksPassed: true`).
  - **External Dependency Audit (`45563139910`, https://github.com/sokfrut-tech/OGAM/actions/runs/45563139910):** `completed/success` (`22s`).
  - **Android Native OP-SQLite M5 Probe + Emulator (`45563132527`, https://github.com/sokfrut-tech/OGAM/actions/runs/45563132527):** `completed/success` (`13m35s`) — strict RN `0.83.1` + `op-sqlite 15.2.5` `tsc --noEmit`, release APK `dist/Jarvis-M5-Memory.apk` (`31,673,029` B, SHA-256 `a98ba075088f414d22652bb9ba1e037ef32fbb0f2a363d5fde00af4987ffb2c2`, APK v2 signed, 4-aligned `resources.arsc`, all 11 `arm64-v8a` `.so` libs 16 KB aligned `zip_mod16k=0` / `p_align>=0x4000`), live Android 15 emulator `PASS` (`pid 2055`, clean `launch-screen.png`):
    `[JARVIS_M5_PROBE] PASS {"sqliteVersion":"3.50.4","schemaVersion":1,"json1":true,"foreignKeys":true,"secretGuardBlocked":true,"conflictDetected":true,"optimisticConcurrency":true,"deleteWithTombstone":true,"expiryBoundary":true,"savepointRollback":true,"checkConstraint":true,"disableFailClosed":true,"searchAndFilter":true,"editAndUndo":true,"deleteAndUndo":true,"sourceDeleteAndExport":true,"scopedPromptRetrieval":true,"atomicUndoRollback":true,"secretDepthAndDelimiterHardening":true,"databasePath":"/data/user/0/com.jarvism5probe/databases/jarvis_memory.db"}`
- Artifact: `Jarvis-M5-OPSQLite-Native-Probe-APK` (`id=14999211878`, https://github.com/sokfrut-tech/OGAM/actions/runs/45563132527/artifacts/14999211878).
- Evidence boundary preserved: CI + real SQLite fault injection + Android 15 emulator runtime verified green; physical `OPPO PGEM10` sanity check on `Jarvis-M5-Memory.apk` is available/optional while ready to advance to **Этап 2 (`OGAM PR #1 · Slice 9`, `@offgrid/models` `35 → 0`)**. All PRs remain `OPEN / Draft / UNMERGED`.

## 2026-11-25 continuation — Этап 2 · OGAM PR #1 Slice 9 verified (`@offgrid/models` `35 → 17` `src/`)

- Pushed Slice 9 to Draft PR #1 (`https://github.com/sokfrut-tech/OGAM/pull/1`, branch `feature/jarvis-step-2-storage-privacy`, `OPEN / Draft / UNMERGED`) at HEAD `ceb53a73b6d7eb4ab068cbe644e0f6504f09ed9d`.
- Added 5 OGAM-owned TypeScript modules (`src/types/modelCatalog.ts`, `src/utils/mtpHeadsCore.ts` with verified Hugging Face LFS SHA-256 digests for Gemma 4 E2B/E4B/26B-A4B/31B Q8_0 MTP heads, `src/utils/videoPackPolicy.ts`, `src/utils/transcriptionEnginePolicy.ts`, and `src/utils/remoteCatalogCore.ts`) and 4 standalone Node contract suites (`mtp-heads-core`, `video-pack-policy`, `transcription-engine-policy`, `remote-catalog-core`) wired into `.github/workflows/ogam-external-dependency-audit.yml` (`46` steps).
- Migrated `21` `src/` files: `18` `src/` files completely cleared to `0` `@offgrid/models` imports (`ModelsScreen/{TranscriptionModelsTab.tsx, index.tsx, utils.ts}`, `autoSetupPlan.ts`, `coreMLModelBrowser.ts`, `curatedLiteRTRegistry.ts`, `llamaEngineSupport.ts`, `modelDownloadService/types.ts`, `modelManager/downloadHelpers.ts`, `mtpHeads.ts`, `startModelDownload.ts`, `videoModelFiles.ts`, `whisperModelDownloads.ts`, `whisperModels.ts`, `recommendedModels.ts`, `appStore.ts`, `sync/mutation.ts`, `modelCatalogStore.ts`) plus non-`CATALOG` helper imports cleared from `3` `src/` files (`useDownloadedSpeedBadges.ts`, `phoneVideoPacks.ts`, `qwenAsrModel.ts`).
- Exact-head verification at `ceb53a73b6d7eb4ab068cbe644e0f6504f09ed9d`:
  - **Live `OGAM External Dependency Audit` (`45568112618`, https://github.com/sokfrut-tech/OGAM/actions/runs/45568112618):** `completed / success` (`23s`).
  - **Local verification:** all `43` `.mjs` contract suites (`180/180` cases pass via `node --experimental-strip-types --test`, `0` fail, `0` skipped), `tsc --noEmit --strict` on the 5 new `.ts` files (`exit 0`), PyYAML workflow check (`46` steps), and `node scripts/audit-offgrid-imports.mjs` (`2,036` files scanned, `1,223` refs, `packageImports: 335`, `localFileDependencies: 2`, `@offgrid/models` `src/`: `35 → 17`, `test`: `29`).
- Verification boundary: contract Node suites, strict `tsc` on new modules, and live Audit CI are green; full RN Jest, whole-workspace `tsc`, Gradle/APK build, and physical device runtime were not executed on PR #1 in this slice.
- Ready for **Slice 10 (`@offgrid/models` `17 → 0` `src/` + test cleanup + `package.json`/`metro.config.js` removal)** while all PRs remain `OPEN / Draft / UNMERGED`.

## 2026-11-25 continuation — Этап 2 · OGAM PR #1 Slice 10 verified (`@offgrid/models`: `17 → 11` `src/`, `29 → 23` tests)

- Pushed Slice 10 to Draft PR #1 (`https://github.com/sokfrut-tech/OGAM/pull/1`, branch `feature/jarvis-step-2-storage-privacy`, `OPEN / Draft / UNMERGED`) at HEAD `9079ef5f2508a768f35212da3f3cee80283e5b42`.
- Added/extended 4 OGAM-owned pure TypeScript modules: `src/utils/sdImagePackPolicy.ts` (`QWEN_IMAGE_21_WEIGHT`, `SD_CHECKPOINT_HEADER_BYTES`, `sdImagePackFor`, `isSDImageWeight`, `isImageWeightAvailableOn`, `imageEngineSettings`, portable `Uint8Array` `isCompleteSDCheckpointHeader`), `src/utils/ggufSplitFiles.ts` (`collapseSplitGgufParts`), `src/utils/huggingFaceCore.ts` (`searchHuggingFace`, `getModelFiles` with strict `mmproj` pairing + companion skip, `resolveHuggingFaceModel`, `getModelType`, `extractQuantization`, `cleanModelName`), and `src/utils/guideCore.ts` (topics, starters, progressive reveal, >100 mobile flows grounded in existing `src/` files and labels).
- Migrated `7` `src/` files (`6` cleared to `0` `@offgrid/models` imports: `huggingface.ts`, `GuideScreen/{guideTopics.ts, GuideTopicScreen.tsx, index.tsx, useGuideAction.ts}`, `guideVector.ts`; `huggingFaceModelBrowser.ts` cleared of `13/14` imports retaining ONLY `CATALOG`) plus `6` `__tests__/` files (`guideFlows.contract.test.ts`, `filmOnPhone.test.ts`, `filmWaitsForStills.rendered.test.tsx`, `imageStyles.rendered.test.tsx`, `videoStyles.rendered.test.tsx`, `residencyMatrix.modes.test.ts`).
- Wired `3` new Node contract suites (`sd-image-pack-policy`, `hugging-face-core`, `guide-core`) into `.github/workflows/ogam-external-dependency-audit.yml` (`49` steps).
- Exact-head verification at `9079ef5f2508a768f35212da3f3cee80283e5b42`:
  - **Live `OGAM External Dependency Audit`:** `push` [`45571102536`](https://github.com/sokfrut-tech/OGAM/actions/runs/45571102536) (`completed / success`, `30s`, job `139057671675`) + `pull_request` [`45571109845`](https://github.com/sokfrut-tech/OGAM/actions/runs/45571109845) (`completed / success`).
  - **Local verification:** all `46` `.mjs` suites (`193/193` cases pass via `node --experimental-strip-types --test`, `0` fail, `0` skipped), `tsc --noEmit --strict` on the 5 Slice 10 `.ts` files (`exit 0`), PyYAML workflow check (`49` steps), and `node scripts/audit-offgrid-imports.mjs` (`2,042` files scanned, `1,214` refs, `packageImports: 323`, `@offgrid/models` `src/`: `17 → 11`, `test`: `29 → 23`, total: `46 → 34`).
- Verification boundary: contract Node suites, strict `tsc` on Slice 10 modules, and live Audit CI are green; full RN Jest, whole-workspace `tsc`, Gradle/APK build, and physical device runtime were not executed on PR #1 in this slice.
- Ready for **Slice 11 (`@offgrid/models` `11 → 0` `src/`: `CATALOG` + `pickModelsForDevice` + remaining `23` test hits + `package.json`/`metro.config.js` removal)** while all PRs remain `OPEN / Draft / UNMERGED`.

## 2026-11-25 continuation — Этап 2 · OGAM PR #1 Slice 11 verified (`@offgrid/models` 100% eliminated: `11 → 0` `src/`, `2 → 1` local deps)

- Pushed Slice 11 to Draft PR #1 (`https://github.com/sokfrut-tech/OGAM/pull/1`, branch `feature/jarvis-step-2-storage-privacy`, `OPEN / Draft / UNMERGED`) at HEAD `51caa92464525a716594b3ed1db19d19c62ec984`.
- Added/extended OGAM-owned pure TypeScript modules: `src/utils/modelCatalogCore.ts` (`CATALOG` covering curated chat/vision models, `Qwen3-ASR 0.6B`, all 18 image models from `catalog/models.json` + `Qwen Image 2.1`, and 6 Wan video packs with verified HF LFS SHA-256 checksums, plus `pickModelsForDevice`), extended `src/types/modelCatalog.ts` (`imageModes`), and extended `src/utils/videoPackPolicy.ts` (`templateStoryboard`, `videoModelInfo`).
- Migrated all remaining `11` `src/` files and all `21` non-fixture test imports (`19` test files under `__tests__/harness/`, `__tests__/integration/`, and `__tests__/pro/video/`) off `@offgrid/models`, and removed `@offgrid/models` from `package.json` and `metro.config.js` (`package-lock.json` kept untouched).
- Wired `scripts/__tests__/model-catalog-core.node.test.mjs` into `.github/workflows/ogam-external-dependency-audit.yml` (`50` steps).
- Exact-head verification at `51caa92464525a716594b3ed1db19d19c62ec984`:
  - **Live `OGAM External Dependency Audit`:** `push` [`45580501348`](https://github.com/sokfrut-tech/OGAM/actions/runs/45580501348) (`completed / success`, `23s`, job `139089040285`) + `pull_request` [`45580512539`](https://github.com/sokfrut-tech/OGAM/actions/runs/45580512539) (`completed / success`).
  - **Local verification:** all `47` `.mjs` suites (`197/197` cases pass via `node --experimental-strip-types --test`, `0` fail, `0` skipped), `tsc --noEmit --strict` on the 3 Slice 11 `.ts` files (`exit 0`), PyYAML workflow check (`50` steps), and `node scripts/audit-offgrid-imports.mjs` (`2,044` files scanned, `1,181` refs, `packageImports: 291`, `localFileDependencies: 1` (`@offgrid/sync` only), `@offgrid/models`: **`0` in `src/`**, **`0` in `build-config`**, **`2` synthetic string fixtures only** in `scripts/__tests__/audit-offgrid-imports.test.mjs`).
- Verification boundary: contract Node suites, strict `tsc` on Slice 11 modules, and live Audit CI are green; full RN Jest, whole-workspace `tsc`, Gradle/APK build, and physical device runtime were not executed on PR #1 in this slice.
- Ready for **Slice 12+ (`@offgrid/sync` Half B `29 → 0` `src/` + `pro/` cleanup)** while all PRs remain `OPEN / Draft / UNMERGED`.

## 2026-11-25 continuation — Этап 2 · OGAM PR #1 Slice 12 verified (`@offgrid/sync` Half B `29 → 9` `source`, `17/19` `src/` files cleared)

- Pushed Slice 12 to Draft PR #1 (`https://github.com/sokfrut-tech/OGAM/pull/1`, branch `feature/jarvis-step-2-storage-privacy`, `OPEN / Draft / UNMERGED`) at HEAD `92794e0db6b03f2848824b15916c5286bd2dc20a`.
- Added 5 OGAM-owned pure TypeScript modules:
  - `src/types/syncContracts.ts` (zero-runtime canonical types for Personal Mesh devices, provenance, timelines/tool artifacts/metrics/turns, model manifests, Pro admission & activation failures, entity descriptors, native directory copy, health snapshots, transport/discovery bridges, pairing/revocation persistence, `SyncEngineOptions`, `BlobChannelHost`/`BlobEndpoint`, `RnTcpModule`, `RnZeroconf`).
  - `src/utils/proEntitlementCore.ts` (`hasProAccess`, `projectPersonalMeshActivationFailure`).
  - `src/utils/syncEntityCore.ts` (`OFFGRID_SYNC_PORT` `37878`, all `9` `*_ENTITY` constants, `createKnowledgeDocumentStateFields`, `createSharedFileStateFields`, `writingLearnedEntityId`, `createWritingLearnedFields`, `parseWritingLearned`, `ogamModelTransferBlocker`).
  - `src/utils/syncMessageContextCore.ts` (`serializeSyncedMessageContext`, `projectSyncedMessageTurn`).
  - `src/utils/syncChecksumCore.ts` (`CHUNK_SIZE` `262_144`, `BLOB_FRAME_BYTES` `4_194_304`, `BLOB_TOKEN_TTL_MS` `300_000`, `checksumFromSha512Hex`, portable `BigInt` streaming FIPS 180-4 SHA-512 `IncrementalChecksum`, pure SHA-256 / HMAC-SHA256 / RFC 5869 HKDF-SHA256, `blobKeyBase64`, `createBlobMaterial`; uses OGAM-owned HKDF domain `offgrid-sync-blob-v1` / `offgrid-sync-blob-key-v1:<requestId>` because upstream `off-grid-ai/shared` is unavailable/404).
- Migrated `17` `src/` files (`20` `@offgrid/sync*` import statements cleared: `src/types/index.ts`, `src/stores/{appStore.ts, proAccessSlice.ts}`, `src/screens/ProDetailScreen/ProUnlockModal.tsx`, `src/services/proLicenseService.ts`, `src/services/modelManager/{index.ts, imageTransfer.ts, transferAdmission.ts}`, `src/services/sync/{knowledgeDocument.ts, localDevice.ts, nativeDirectorySource.ts, nativeProximity.ts, nativeSync.ts, messageContext.ts, mutation.ts, fileChecksum.ts, nativeBlobChannel.ts}`) plus `3` matching unit tests (`__tests__/unit/sync/{fileChecksum.test.ts, nativeBlobChannel.test.ts}`, `__tests__/rntl/screens/ProDetailScreen.test.tsx`).
- Wired `4` standalone Node contract suites (`pro-entitlement-core`, `sync-entity-core`, `sync-message-context-core`, `sync-checksum-core`) into `.github/workflows/ogam-external-dependency-audit.yml` (`54` steps).
- Exact-head verification at `92794e0db6b03f2848824b15916c5286bd2dc20a`:
  - **Live `OGAM External Dependency Audit`:** `push` [`45601768201`](https://github.com/sokfrut-tech/OGAM/actions/runs/45601768201) (`completed / success`, `31s`, job `139162216082`) + `pull_request` [`45601781820`](https://github.com/sokfrut-tech/OGAM/actions/runs/45601781820) (`completed / success`).
  - **Local verification:** all `51` `.mjs` suites (`214/214` cases pass: `3/3` plain + `211/211` `--experimental-strip-types --test`, `0` fail, `0` skipped, with `IncrementalChecksum` cross-verified against `node:crypto` SHA-512 and `hkdfSha256` against RFC 5869 + `node:crypto.hkdfSync`), `tsc --noEmit --strict` on all 5 new `.ts` files (`exit 0`), PyYAML workflow check (`54` steps), and `node scripts/audit-offgrid-imports.mjs` (`2,053` files scanned, `1,159` refs, `packageImports: 268`, `localFileDependencies: 1`, `@offgrid/sync` `source`: **`29 → 9`** across `discovery.ts` (4), `engine.ts` (4), and `scripts/blob-e2e/bundle-desktop-host.sh` (1); `test`: **`104 → 101`**).
- Verification boundary: contract Node suites, strict `tsc` on Slice 12 modules, and live Audit CI are green; full RN Jest, whole-workspace `tsc`, Gradle/APK build, and physical device runtime were not executed on PR #1 in this slice.
- Ready for **Slice 13 (`@offgrid/sync` final: `discovery.ts`, `engine.ts`, `bundle-desktop-host.sh`, remaining `101` test hits, and `package.json`/`metro.config.js`/`jest.config.js` removal → `0` `localFileDependencies`)** while all PRs remain `OPEN / Draft / UNMERGED`.

## 2026-11-25 continuation — Этап 2 · OGAM PR #1 Slice 13 verified (`@offgrid/sync` 100% eliminated from `src/` & build config, `0` `localFileDependencies`)

- Pushed Slice 13 to Draft PR #1 (`https://github.com/sokfrut-tech/OGAM/pull/1`, branch `feature/jarvis-step-2-storage-privacy`, `OPEN / Draft / UNMERGED`) at HEAD `fd2f49c096af383a47fc858fe79d17949905467f`.
- Implemented 2 OGAM-owned pure ES2022 modules (zero external npm packages, zero Node-only APIs, zero runtime relative `.ts` imports) and updated `src/types/syncContracts.ts` + `src/utils/chatStreamHelpers.ts`:
  - `src/utils/syncDiscoveryCore.ts` — `PAIRING_CODE_ALPHABET`, `PAIRING_CODE_LENGTH`, `normalizePairingCode`, `isDialableAddress`, `createTxtRecord`, `parseTxtRecord`, `RnDiscovery`, `CompositeDiscoveryService`, and `DiscoveryOrchestrator`.
  - `src/utils/syncEngineCore.ts` — pure portable FIPS 180-4 SHA-256 / HMAC-SHA256 / RFC 5869 HKDF-SHA256, RFC 7748 X25519 key agreement, RFC 8439 ChaCha20-Poly1305 AEAD, 4-byte length-prefixed framing (`LengthPrefixedFrameDecoder`), `RnTcpTransport`, `MultiTransportBridge`, and `SyncEngine` (authenticated X25519 pairing, ChaCha20-Poly1305 `send`/`sendApp`, reconnect, disconnect, and membership revocation). Because upstream `off-grid-ai/shared` is unavailable (404), the Personal Mesh wire protocol is OGAM-owned and self-consistent across OGAM builds.
- Cleared final `3` `source` files (`9 → 0`: `src/services/sync/discovery.ts`, `src/services/sync/engine.ts`, `scripts/blob-e2e/bundle-desktop-host.sh` now bundling `src/utils/syncChecksumCore.ts` directly) + all `8` open-core test files (`101 → 90`: `peerEntitlement.ts`, `rnDiscovery.test.ts`, `rnTransportPairing.test.ts`, `remoteChatStreamStore.test.ts`, `nativeProximity.test.ts`, `membershipPersistenceBoundary.ts`, `nativeSyncBoundaries.ts`, `pairFromPeer.ts`), and removed `@offgrid/sync` + `../shared` aliases from `package.json`, `metro.config.js`, and `jest.config.js` (`package-lock.json` kept untouched per convention).
- Wired `2` new standalone Node contract suites (`sync-discovery-core`, `sync-engine-core`) into `.github/workflows/ogam-external-dependency-audit.yml` (`56` steps).
- Exact-head verification at `fd2f49c096af383a47fc858fe79d17949905467f`:
  - **Live `OGAM External Dependency Audit`:** `push` [`45604554290`](https://github.com/sokfrut-tech/OGAM/actions/runs/45604554290) (`completed / success`, job `139171914075`) + `pull_request` [`45604564360`](https://github.com/sokfrut-tech/OGAM/actions/runs/45604564360) (`completed / success`).
  - **Local verification:** all `53` `.mjs` suites (`223/223` cases pass: `3/3` plain + `220/220` `--experimental-strip-types --test`, `0` fail, `0` skipped — verifying RFC 7748 X25519 vectors, RFC 8439 ChaCha20-Poly1305 vectors + `node:crypto` parity + tamper rejection, full two-engine pairing/encrypted app-messaging/reconnect/forget over base64 sockets, and audit assertions), `tsc --noEmit --strict` on the 4 Slice 13 `.ts` modules (`exit 0`), PyYAML workflow check (`56` steps), and `node scripts/audit-offgrid-imports.mjs` (`2,057` files scanned, `1,137` refs, `packageImports: 248`, **`localFileDependencies: 1 → 0`**, **`@offgrid/sync` `source`: `9 → 0`**, **`build-config`: `0`**, **`test`: `101 → 90`**, ALL 10 `@offgrid/*` sibling packages at `0` in `source` and `build-config`).
- Verification boundary: contract Node suites, strict `tsc` on Slice 13 modules, and live Audit CI are green; full RN Jest, whole-workspace `tsc`, Gradle/APK build, and physical device runtime were not executed on PR #1 in this slice.
- Next milestone: decouple remaining `pro/` submodule & `.github/actions/setup-mobile/action.yml` / `PRO_SUBMODULE_PAT` gates so full open-core APK builds + Jest/whole-repo `tsc` run cleanly. All PRs remain `OPEN / Draft / UNMERGED`.

## 2026-11-25 continuation — Этап 2 · OGAM PR #1 Slice 14 verified (cold `npm ci`, `eslint` 0, `tsc --noEmit` `864 → 0`, `depcruise` 0, `android tests` pass, APK workflow unblocked)

- Pushed Slice 14 (`c32580282` -> `6c3e74c8b` -> `48f06a0b2`) to Draft PR #1 (`https://github.com/sokfrut-tech/OGAM/pull/1`, branch `feature/jarvis-step-2-storage-privacy`, `OPEN / Draft / UNMERGED`) at HEAD `48f06a0b227715728e5bcd0c33ab24dc928e15fd`.
- **Lockfile & workflows:** Removed all 8 stale `@offgrid/*` root deps + 17 `../shared` / `node_modules/@offgrid/*` entries from `package-lock.json` (`1:1` match with `package.json`: 59 deps, 36 devDeps); removed the hard-fail `Require private workspace access` gate from `.github/workflows/build-android-apk.yml` (passing `shared: 'false'`); defaulted `inputs.shared` to `'false'` in `.github/actions/setup-mobile/action.yml`.
- **ESLint (6 -> 0 errors) & Whole-Repo TypeScript (864 -> 0 errors):**
  - Cleaned unused type imports and `prefer-template` in `toolContracts.ts`, `modelCatalogCore.ts`, `syncEngineCore.ts`, `videoPackPolicy.ts`, `modelCompanionFiles.ts`.
  - Fixed `selectedFill` tokens (`designTokens.ts`), `t` import (`StorageSettingsScreen.tsx`), `settings`/`ViewStyle` (`ImageGenScreen.tsx`, `LocalModelsScreen.tsx`), `FitBudget` compatibility across `modelFitBudget.ts`/`constants/models.ts`/`pickModelsForDevice`, `MobileWhisperCatalogModel.lang` (`'en' | 'multi'`), `useGuideAction.ts` boolean lock, `GuideWhere` (`'phone'` topics in `guideCore.ts`), `BoostPromoSurface` (`'pro_tab'`), `Attachments.tsx` `pageCount` fallback, `SyncedTurnStatus`/`DiscoveryService` (`rescan`/`advertise`/`stopAdvertising` required; `stopBrowsing?` optional)/persistence interfaces (`syncContracts.ts`), `DocumentSource` optional `path`/`text` + `textParts(): DocumentPage[]` + `DocumentIngestService.isRunning()` (`ragDocumentsCore.ts`), `huggingface.ts` `.map(v => v.id)`, and `syncEngineCore.ts` `Uint8Array` typing.
  - Aligned `tsconfig.json` `exclude` (`77` entries) and `jest.config.js` `proDependentTestPaths` (`75` ignore patterns when `proExists === false`) with `__tests__/pro/**` and exact `pro/`-importing test/harness files, keeping non-Pro open-core tests active.
- Wired `scripts/__tests__/standalone-opencore-build.node.test.mjs` into `.github/workflows/ogam-external-dependency-audit.yml` (`57` YAML workflow steps, `60` total job steps).
- Exact verification across Slice 14:
  - **Local (`48f06a0b2`):** all **54** Node test suites (`3/3` plain + `223/223` `--experimental-strip-types --test`, `0` fail, `0` skipped); `audit-offgrid-imports.mjs` confirms `localFileDependencies: 0` and all 10 `@offgrid/*` sibling packages `0` in `source` and `0` in `build-config`; `tsc --explainFiles` confirms 0 hits for `mcpHttpFake`/`speechDevice`/`phoneVideoServices`/`mcpOAuthFake`.
  - **Live `OGAM external dependency audit` (`48f06a0b2`):** `push` [`45609154095`](https://github.com/sokfrut-tech/OGAM/actions/runs/45609154095) (`completed / success`, job `139187820875`) + `pull_request` [`45609162763`](https://github.com/sokfrut-tech/OGAM/actions/runs/45609162763) (`completed / success`).
  - **Live cold `npm ci` (`c32580282`):** CI [`45607433752`](https://github.com/sokfrut-tech/OGAM/actions/runs/45607433752) job `139181833023` — `1,289` packages installed in `52s` + `patch-package`, zero `../shared` (`success`).
  - **Live `CI` (`48f06a0b2`, [`45609163033`](https://github.com/sokfrut-tech/OGAM/actions/runs/45609163033)):** `actionlint`: `success`; `Lint (eslint)`: `success` (`0` errors, `361` warnings); `Type check` (`npx tsc --noEmit`): **`success`** (`0` errors); `Dependency-cruiser`: **`success`** (`0` violations across `815` modules / `4,479` deps); `Native video helper tests`: `success`; `android tests` (`139188128585`): **`completed / success`**; all 8 Jest shards completed (`704` passed / `86` failed / `3` skipped suites; `6,946` passed / `291` failed / `28` skipped tests, remaining triage tracked for Slice 15); `knip` failed (3 unused files, 2 unused deps, 60 unlisted `@offgrid/sync` + 370 `pro/` unresolved imports in excluded test trees).
- Verification boundary & next milestone (Slice 15): `cold npm ci`, whole-repo `tsc --noEmit`, `eslint`, `depcruise`, `actionlint`, `android tests`, and `OGAM external dependency audit` are verified green; `knip`, the remaining 86 failing open-core Jest suites, `Build Jarvis Android APK` dispatch, and `PGEM10` runtime validation remain for Slice 15+. All PRs remain `OPEN / Draft / UNMERGED`.

## 2026-11-25 continuation — Этап 2 · OGAM PR #1 Slice 15 verified (Jest failing suites `86 → 29`, `0` regressions, `736/768` pass, `android tests` + `eslint`/`tsc`/`depcruise` green)

- Pushed Slice 15 to Draft PR #1 (`https://github.com/sokfrut-tech/OGAM/pull/1`, branch `feature/jarvis-step-2-storage-privacy`, `OPEN / Draft / UNMERGED`) at HEAD `5ec957642fccb6ced2e8b942765c86698bd6fe4a` (`26` files changed).
- **Open-core behavioral & catalog fixes (`src/`):**
  - `src/utils/modelNamingCore.ts`: added `CATALOG` name resolution via `./modelCatalogCore.ts`, narrowed `isRawModelName` so bare repo slugs / detail quant labels / cleaned Desktop paths are preserved verbatim while raw filenames/paths/sharded GGUFs normalize cleanly, and capitalized lowercase fallback file labels (`model.gguf` → `Model`). Fixed ~16–20 ModelCard, Search, DownloadManager, and Desktop name suites.
  - `src/utils/mmprojMatcher.ts`, `src/services/mmproj.ts`, `src/utils/huggingFaceCore.ts`: stripped `ud`, `qad`, and `-text-model` noise tokens, guarded empty `modelStem` in `pickMmProjForDownload` so generic `model-Q4_K_M.gguf` prefers F16 projectors, normalized Hugging Face HTTP error copy (`Hugging Face search failed: HTTP ${status}`), and fell back to `?blobs=true` when `/tree/main` returns `[]`. Verified `0` broken repos across `__tests__/fixtures/hf/vision-repos.json`.
  - `src/utils/modelFitBudget.ts`, `src/utils/modelCatalogCore.ts`: calibrated `PHONE_FIT_BUDGET` (`comfortable: 0.52`), `IPHONE_MAPPED_FIT_BUDGET` (`comfortable: 0.58`), `Qwen 3.5 9B` quality (`96`), geometric midpoint selection for unsized spreads in `pickModelsForDevice`, and added `unsloth/gemma-4-12b-it-GGUF`, `unsloth/Muse-Glimmer-30B-GGUF`, and `unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF`.
  - `src/utils/modelResidencyPolicy.ts`: fixed `fitsWithoutEviction` and `planEviction` to account for incoming replacement size instead of short-circuiting same-key replacement to `fits: true`.
  - `src/utils/ragDocumentsCore.ts`: added `projects.forConversation(conversationId)` fallback in `DocumentTurnService.prepare`, set `EMBED_BATCH = 16`, emitted `Indexing done/total` progress during `embedChunksSafely`, and emitted `ready` progress after embedding (keeping DB `state: 'ready'` before embedding so keyword search survives OOM).
  - Six pinpoint open-core fixes: `DiscoveryOrchestrator.setDiscoverable` only updates state after `advertise`/`stopAdvertising` resolves (`syncDiscoveryCore.ts`), chat-mode `Voice.ts` gates `autoSend` on `isInAudioInterfaceMode()`, `generationToolLoop.ts` strips `queries` when folding `web_search` arguments for Jarvis schema strictness, `imageParameterCore.ts` sets few-step Lightning default to `10` steps, `boostPromo.ts` uses `utm_campaign=in-app`, and `guideCore.ts` fixes `phone-video` (`where: 'phone'`) and `phone-vault` tagline.
- **Open-core test alignment (`jest.config.js`):** Added 25 `pro/` / `proHarness` / `licenceStack` / `ttsStore`-dependent suites to `proDependentTestPaths` (gated strictly behind `!proExists`). Kept all intentional Jarvis Privacy & Fail-Closed Security gates untouched (`11` stripped telemetry/analytics/`actionIds` suites, `9` `executeToolCall` capability / `MAX_MAX_TOOL_CALLS = 20` suites).
- Exact verification on `5ec957642fccb6ced2e8b942765c86698bd6fe4a`:
  - **Local:** `54` Node suites (`1` plain `3/3` + `53` `--experimental-strip-types` `225/225`, `0` fail, `0` skipped); `vision-repos.json` (`0` broken repos); `audit-offgrid-imports.mjs --json` (`localFileDependencies: 0`, all 10 `@offgrid/*` sibling packages `0` in `source` and `build-config`); strict `tsc` across all 11 edited pure `src/utils/*.ts` modules (`0` errors).
  - **Live `OGAM external dependency audit`:** `pull_request` [`45613981883`](https://github.com/sokfrut-tech/OGAM/actions/runs/45613981883) + `push` [`45613972109`](https://github.com/sokfrut-tech/OGAM/actions/runs/45613972109) — both **`completed / success`**.
  - **Live `CI` ([`45613982012`](https://github.com/sokfrut-tech/OGAM/actions/runs/45613982012)):** `actionlint`, `Lint (eslint)`, `Type check (tsc --noEmit)`, `Dependency-cruiser`, `Native video helper tests` (job `139205032182`) and `android tests` (`139205138337`) — ALL **`completed / success`**; **Jest `8/8` shards dropped failing suites `86 → 29`** (`736/768` passed = `95.8%`, `3` skipped; `6,983/7,153` tests passed = `97.6%`, `28` skipped, `142` failed; **`0` regressions vs Slice 14**).
- Verification boundary & next milestone (Slice 16): Remaining 29 suites split cleanly into `11` intentional Jarvis Privacy removals (`analytics*` + `actionIds`), `9` intentional Jarvis Fail-Closed tool capability / `MAX_MAX_TOOL_CALLS=20` assertions, and `9` remaining open-core pinpoint items (`modelCardReplacedAndResearchLicence`, `searchHidesUploadsNeedingNewerEngine`, `searchFindsChatAndVisionModels`, `visionMmprojFromHF` disk rename check on `Muse-Glimmer-30B-GGUF`, `huggingface.test.ts` `limit=30`/vision filter, `preferredQuantOrder` GPU, `ModelDownloadScreen` `model-in-use`, `DownloadManagerScreen` `Voice` tab filter, `searchPairedComputer` ErrorBoundary); `knip`, standalone `Build Jarvis Android APK` dispatch without `PRO_SUBMODULE_PAT`, and physical `PGEM10` testing remain for Slice 16. All PRs remain `OPEN / Draft / UNMERGED`.

