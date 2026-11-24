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
