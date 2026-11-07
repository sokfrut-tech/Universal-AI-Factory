# Cross-project factory dashboard — 2026-11-04

Tracker: https://github.com/sokfrut-tech/Universal-AI-Factory/issues/16

## Operating rules
- Free-first: core functionality local/offline; no mandatory paid API.
- No merge, production deployment, publishing, paid model call, destructive Cloudflare change or force-push without explicit user approval.
- An external factory/Claude/Gemini worker counts only after an actual execution produces artifact/commit/report and test evidence. ACK/open PR is not execution.
- Never weaken tests. Record exact head SHA and CI evidence. Update continuation/status/changelog/handoff docs.

## Project status snapshot

| Project | Verified evidence | Next action / blocker |
|---|---|---|
| Universal-AI-Factory | PR #11 contract tests passed (41874229960); PR #14 runner security tests passed (41835758930) | PR #11 has no HTTP transport and performs no network calls. Finish local orchestration and evidence ledger; do not claim real Claude/Gemini execution. |
| Antigravity-Mobile | PR #19 Android build/emulator UI, security and Factory API checks passed (41897846860, 41897846886, 41897846007) | PR #20 Factory API failed at npm test (41896999880); Android workflow passed. Diagnose and fix npm test. Verify D1/deployment separately. |
| AVTOY KOREA | PR #57 Worker checks/tests/security/review/deploy passed (41706682505, 41706681318, 41706681320, 41706681374, 41706681160) | PR #58 Worker tests/review passed, security baseline failed (41899023810). Fix security. Verify Telegram webhook/live response separately; preserve media album and privacy requirements. |
| RussSearchOPPO | PR #3 APK/Hive preflight/security passed (41705538426, 41705537360, 41705537382); PR #4 APK/security passed (41879065510, 41879065591) | Complete local voice pipeline and physical OPPO/ColorOS verification. CI APK is not device validation. |
| Gemeni / Jarvis | PR #61 local Factory Hive core draft; security run 41906635607 was in progress at last check | PR #51 emulator smoke failed (41898206294; secret scan passed). Inspect logs/artifacts. Verify PR #61 exact-head security, Gradle tests and APK build. Reconcile PR bases carefully. |

## Active work links
- UAF tracker: https://github.com/sokfrut-tech/Universal-AI-Factory/issues/16
- UAF provider contract: https://github.com/sokfrut-tech/Universal-AI-Factory/pull/11
- UAF runner security: https://github.com/sokfrut-tech/Universal-AI-Factory/pull/14
- UAF roadmap: https://github.com/sokfrut-tech/Universal-AI-Factory/pull/15
- Antigravity runtime: https://github.com/sokfrut-tech/Antigravity-Mobile/pull/19
- Antigravity API checks: https://github.com/sokfrut-tech/Antigravity-Mobile/pull/20
- AVTOY security: https://github.com/sokfrut-tech/avtoy-korea-auto/pull/57
- AVTOY continuation: https://github.com/sokfrut-tech/avtoy-korea-auto/pull/58
- RussSearchOPPO security: https://github.com/sokfrut-tech/RussSearchOPPO/pull/3
- RussSearchOPPO continuation: https://github.com/sokfrut-tech/RussSearchOPPO/pull/4
- Jarvis hive core: https://github.com/sokfrut-tech/Gemeni/pull/61
- Jarvis emulator: https://github.com/sokfrut-tech/Gemeni/pull/51

## Execution order
1. Antigravity #20 — fix npm test and re-run API checks.
2. AVTOY #58 — fix security failure.
3. Jarvis #51 — fix emulator smoke; #61 — verify security/build/tests on exact head.
4. UAF #11/#14 — local orchestrator, task ledger and security hardening; provider transport remains opt-in.
5. RussSearchOPPO — voice integration and physical OPPO test plan.
6. AVTOY — live Worker/Telegram verification and media regressions.

## Evidence protocol
One implementation owner per shared file. Independent factories may review in parallel. Each task needs correlation ID, scope, forbidden actions, acceptance criteria, budget, artifact and evidence. A green workflow on an older SHA does not verify a newer head. A docs-only workflow does not verify application code. Preserve historical reports; update this dashboard only after fresh checks.
