# Universal AI Factory — portfolio plan and restart guide

**Updated:** 2026-11-04  
**Owner:** repository owner  
**Coordinator:** ChatGPT (continues directly when external agents are unavailable)  
**Correlation ID:** factory-portfolio-20261104  
**Canonical exchange protocol:** [coordination/shared/AGENT_EXCHANGE_PROTOCOL.md](../coordination/shared/AGENT_EXCHANGE_PROTOCOL.md)  
**Tool registry:** [TOOL_INTEGRATION_REGISTRY.md](TOOL_INTEGRATION_REGISTRY.md)  
**Security baseline:** [FACTORY_SECURITY_ROLLOUT.md](FACTORY_SECURITY_ROLLOUT.md)

## 1. Operating contract — applies to every current and future repository

1. This document and the project briefs in each repository are the durable source of truth. Conversation history is supplemental.
2. Every project keeps a `docs/FACTORY_CONTINUATION_BRIEF.md` with goal, owner requirements, current verified state, open PRs, decisions, blockers, exact next steps and evidence links.
3. Every meaningful work session updates the brief and this portfolio index with commit SHA, PR, CI run IDs, artifacts, checks actually performed and remaining work.
4. Use GitHub inbox/outbox messages following the shared protocol. An inbox file is only a request; an ACK proves receipt only; only a substantive correlated response is an agent result.
5. Claude and Gemini are optional collaborators. If either is unavailable, slow, unconfigured or silent, ChatGPT proceeds with implementation, tests and repository updates. Never fabricate an external response or call self-review independent review.
6. Before code changes: inspect README/AGENTS, branch and PR inventory, recent commits, workflow state, existing implementations and user requirements. Work on a dedicated branch; do not overwrite another agent's branch.
7. No force push, secret disclosure, production deployment, remote database migration, domain/DNS change, destructive operation, merge or Play publication without explicit owner approval.
8. Never claim a feature, provider connection, test, build, deployment or physical-device result without exact observable evidence.
9. Preserve existing working functionality and local user data. Prefer additive migrations and regression tests.
10. Every deliverable must be resumable from a clean session using this file plus the repository brief; do not require the user to relay messages between agents.

## 2. Project portfolio and priorities

The authenticated GitHub inventory returned ten repositories. Open PR snapshot was checked on 2026-11-04; statuses can change and must be refreshed before decisions.

| Priority | Repository | Mission / owner requirements | Snapshot and next action |
|---|---|---|---|
| P0 | `Universal-AI-Factory` | Universal coordinator, real agent/provider dispatch, secure tools, shared protocols and reusable factory workflow | PRs #11, #12, #14, #15, #6, #8, #7, #10, #1 open. Continue contract-first provider dispatch and truthful inbox/outbox. Do not merge conflicting/unsafe PRs blindly. |
| P0 | `Antigravity-Mobile` | Android AI command center; Fallout/Wasteland UI; multi-project sessions/windows; task delegation, agents, approvals, artifacts and visible real progress | PRs #17, #15, #14, #7, #6, #4 open. Reconcile #14/#15/#17/#7 on an integration branch; preserve task board, API settings, Keystore, idempotent submission and real polling. Latest UI fixes need fresh CI. |
| P1 | `Gemeni` | Jarvis Android voice assistant for Chinese OPPO/ColorOS; Russian and English speech recognition/translation, Russian responses, useful installable APK, local-first where possible | PRs #53 security, #51 emulator tests, #35 Gemini cloud client open. Continue black-screen/runtime diagnosis, actual voice pipeline, VoiceInteraction/Accessibility integration and OPPO validation. LLM review artifacts are not independent review unless a real model response is recorded. |
| P1 | `avtoy-korea-auto` | Professional vehicle import website and Telegram bot; admin-only private enquiries; moderated buyer photo/video reviews | PRs #57 security, #56 CodeQL availability, #50 warranty wording, #42/#40 logo, #17 accessibility, #13 KV, #2 catalogue/moderation open. Diagnose webhook/site using logs and live checks; do not touch production/main without approval. |
| P1 | `RussSearchOPPO` | Russian-language search/voice support on Chinese OPPO/ColorOS, Android 7+ compatibility | PR #3 security onboarding open. Preserve existing successful baseline; verify app functionality on target device and language pipeline. |
| P2 | `voice-assistant` | Shared voice assistant foundation/components | PR #15 security onboarding open. Audit README, architecture, build and intended relationship to Jarvis before expanding scope. |
| P2 | `russ-translation-models` | Russian translation model assets/manifests and reproducible model packaging | PR #2 security onboarding open. Validate provenance, licenses, checksums, manifests and integration tests. |
| P2 | `happ-proxy-pool` | Verify public proxy nodes with real Xray HTTPS traffic | PR #3 security onboarding and #1 traffic verification prototype open. Keep tests isolated; no credential harvesting or unsafe proxy use. |
| P3 | `sleep-button` | Project exists in inventory; requirements not established in current verified context | Inspect repository and recover its original brief before code changes. |
| P3 | `breeno-apks` | APK archive/support repository; requirements and content need fresh inspection | Inspect inventory, provenance and intended role; no assumptions or binary replacement. |

## 3. Universal AI Factory execution model

- Coordinator: clarify acceptance criteria, split work into bounded tasks, serialize conflicting writes and track dependencies.
- Implementer: ChatGPT directly or an actually available provider/agent. Provider health and capabilities must be checked before routing.
- Independent reviewer: Claude/Gemini/another actual independent actor where available. If unavailable, record `NOT_RECEIVED`; ChatGPT may perform a clearly labelled self-review and deterministic verification.
- QA/security: project-specific CI, tests, scanners and artifact inspection.
- User: approve only high-impact actions and receive concise status/result, not routine technical relay requests.

Provider states must be separate: configured, authenticated, healthy, capability-available, dispatched, accepted, running, completed. A GitHub message, ACK, queued workflow or API key name is not proof of execution.

## 4. Work queue — order of execution

### Track A — Factory control plane
1. Review PR #11 provider adapter lifecycle and guard contract.
2. Reconcile durable ledger semantics with Antigravity Mobile PR #15: idempotency, append-only events, concurrency/CAS, timeout and `outcome_unknown`.
3. Repair or replace the old ACK-only dispatcher PR #6; no ACK-as-execution.
4. Keep manual runner safe (PR #14); preserve read-only defaults, least privilege and approval boundaries.
5. Add a deterministic integration test with mock provider, duplicate dispatch, timeout, replay, correlation mismatch and failure paths.
6. Only then run a controlled non-production live provider smoke test if a provider is genuinely configured.

### Track B — Antigravity Mobile
1. Fresh CI for PR #17 latest head; repair failures, do not weaken tests.
2. Integrate PR #14 Fallout reference and PR #15 durable ledger with PR #17 navigation in one tested line; reconcile PR #7 security baseline.
3. Preserve current local task storage, API settings, Keystore encryption, idempotent task submission and real progress polling.
4. Implement sessions/projects and event timeline with offline-safe persistence.
5. Connect real agents only through the Factory API; no fake progress/replies.
6. Produce APK only from a verified commit, with test report and SHA-256. No Play Store.

### Track C — Jarvis / OPPO
1. Inspect PR #51 emulator tests and PR #35 official Gemini client; validate exact head CI.
2. Diagnose black screen with logcat/crash evidence and startup UI tests.
3. Verify ASR languages Russian + English, Chinese-to-Russian and English-to-Russian translation, TTS, microphone permissions and offline behaviour.
4. Verify VoiceInteraction/Accessibility behaviour without bypassing OS permissions.
5. Produce a sideloadable APK with artifact provenance; physical OPPO/ColorOS testing remains a separate gate.

### Track D — AVTOY Korea
1. Inspect latest main and feature branches, PRs #57/#56/#50/#42/#40/#13/#2 and workflow failures.
2. Reproduce site availability, Telegram webhook health and `/start` using non-secret diagnostics.
3. Confirm enquiries go only to administrators' personal Telegram IDs; never to the group.
4. Fix review moderation so rejected/failed submissions can be retried and all selected photos/videos remain attached.
5. Verify KV binding and bot/group/admin configuration by secret names only; never print token values.
6. No production deploy, main merge or webhook mutation without explicit owner approval.

### Track E — remaining repositories
1. Verify security PRs against each repo's actual language/stack and exact CI result.
2. Inspect each project brief and identify real user-facing priorities.
3. Do not invent requirements for sleep-button or breeno-apks.
4. Keep model binaries, proxy tests and voice components provenance-checked and separately tested.

## 5. Standard project continuation brief

Each repository must contain `docs/FACTORY_CONTINUATION_BRIEF.md` with:
- project mission and exact user requirements;
- constraints and prohibited actions;
- verified repository state (branch, commit, PRs);
- current feature matrix: done / partial / missing / blocked;
- issues and reproducible symptoms;
- decisions and rationale;
- exact files and workflows changed;
- tests run, run IDs, artifacts and checksums;
- agent handoffs and correlated substantive responses;
- next 3–10 actions, ordered by priority;
- resume instructions for a new ChatGPT/Claude/Gemini session.

## 6. Session closeout and restart

At the end of every work session:
1. Update the project brief and this portfolio index.
2. Save a timestamped report in `coordination/chatgpt/outbox/`.
3. Record active branch/PR/head SHA and workflow run URLs.
4. Record pending Claude/Gemini inbox messages and explicitly state whether substantive replies were received.
5. Leave code unmerged unless required checks and owner approval are satisfied.

At the start of a new session:
1. Read this portfolio plan and the relevant project brief.
2. Refresh repository PRs, branch heads, workflow runs and artifacts.
3. Read newest agent outbox reports and verify their correlation IDs.
4. Continue the next unblocked action; do not ask the owner to repeat known requirements.

## 7. Current coordination policy

ArmorCodex hosted policy store was updated to version 2 with merge-mode rules requiring approval for GitHub PR merge, auto-merge and AppDeploy deployment, denying force-push and requiring approval for branch deletion. This hosted policy store is advisory unless a connected local enforcement hook consumes it; repository CI and GitHub permissions remain authoritative.

## 8. Latest coordination references

- Antigravity Mobile roadmap: [PR #17](https://github.com/sokfrut-tech/Antigravity-Mobile/pull/17)
- Factory roadmap: [PR #15](https://github.com/sokfrut-tech/Universal-AI-Factory/pull/15)
- Antigravity audit report: [2026-11-04 report](../coordination/chatgpt/outbox/2026-11-04_antigravity-roadmap-audit-report.md)
- Shared exchange protocol: [AGENT_EXCHANGE_PROTOCOL.md](../coordination/shared/AGENT_EXCHANGE_PROTOCOL.md)

**Status:** portfolio plan written; individual project briefs and agent handoffs are being added. Open PRs remain open; no production changes or merges are authorized by this document.


## 9. Continuation brief PRs created in this session

All are draft documentation PRs; none has been merged. Their current mergeability must be refreshed before review; the first create response reported `mergeable=false` for these new branches, so inspect base conflicts/merge state rather than assuming ready.

| Repository | Continuation PR | Branch |
|---|---:|---|
| Gemeni | [#54](https://github.com/sokfrut-tech/Gemeni/pull/54) | `factory/continuation-brief-2026-11-04` |
| RussSearchOPPO | [#4](https://github.com/sokfrut-tech/RussSearchOPPO/pull/4) | `factory/continuation-brief-2026-11-04` |
| avtoy-korea-auto | [#58](https://github.com/sokfrut-tech/avtoy-korea-auto/pull/58) | `factory/continuation-brief-2026-11-04` |
| voice-assistant | [#16](https://github.com/sokfrut-tech/voice-assistant/pull/16) | `factory/continuation-brief-2026-11-04` |
| russ-translation-models | [#3](https://github.com/sokfrut-tech/russ-translation-models/pull/3) | `factory/continuation-brief-2026-11-04` |
| happ-proxy-pool | [#4](https://github.com/sokfrut-tech/happ-proxy-pool/pull/4) | `factory/continuation-brief-2026-11-04` |
| Antigravity-Mobile | [#17](https://github.com/sokfrut-tech/Antigravity-Mobile/pull/17) | `feat/agent-command-center-shell-2026-11-04` |

The Factory portfolio and continuation handbook are included in existing Factory PR #15. The Factory project-specific continuation brief is also in that branch.

## 10. Optional agent handoffs placed in Factory inbox

- Claude: `coordination/claude/inbox/2026-11-04_factory-provider-contract-review.md` — read-only P0 provider/ledger/dispatcher contract review.
- Gemini: `coordination/gemini/inbox/2026-11-04_jarvis-runtime-qa-review.md` — read-only Jarvis runtime/Android QA.
- Claude: `coordination/claude/inbox/2026-11-04_avtoy-korea-telegram-review.md` — read-only AVTOY Telegram/moderation review.
- Antigravity-specific optional Claude/Gemini review requests are in the inbox paths listed in the Antigravity roadmap.

These messages are repository handoff requests only. No delivery, acceptance or substantive agent response is asserted. ChatGPT remains responsible for continuing implementation if no agent response arrives.

## 11. Repositories with no initial commit

GitHub returned `Git Repository is empty` for `sleep-button` and `breeno-apks`, so a branch and in-repository continuation file could not be created. Their requirements are not inferred. The portfolio records them as P3 pending recovery of source files or an initial README/commit. Once a first commit exists, create the standard continuation brief and security bootstrap.

## 12. Hosted safety policy update

ArmorCodex hosted policy version 2 was created in merge mode, preserving existing rules and adding:
- require approval for GitHub PR merge;
- require approval for GitHub auto-merge;
- require approval for AppDeploy deployment;
- deny GitHub force-push;
- require approval for GitHub branch deletion.

Important: this hosted policy store is advisory unless a connected local enforcement hook consumes it. GitHub permissions, branch protection and CI remain the authoritative repository controls.
