# Continuation Queue
Updated: 2026-11-23. Priority reflects safety and dependency order, not completion.

## P0 — Make UPKB the real entry point
- [ ] Finish branch and open draft PR; link UPKB from docs/MASTER_PROJECT_INDEX.md.
- [ ] Verify all database files and CSV validity; add schema/version and duplicate checks.
- [ ] Resolve Factory PR #26 discrepancy (open list vs non-null merge_commit_sha); fetch exact PR state.
- [ ] Audit current workflows/dispatcher and both Claude/Gemini inbox paths; complete one real end-to-end task with patch, tests and artifact.
- [ ] Audit all 12 repository handoffs, README, Actions, releases and recent commits; expand DOCUMENTS.csv. Do not claim exhaustive completion yet.

## P1 — Jarvis / OGAM
- [ ] Inspect Gemeni PR #148 diff and exact-head CI; distinguish implemented, stubbed and unverified.
- [ ] OGAM PR #1: standalone dependency inventory, Gradle build/manifest merge/Kotlin tests, then PGEM10 assistant role/microphone/lock-screen/privacy validation.
- [ ] OGAM PR #2: obtain exact Instructions 17.7.2 APK; complete JADX/apksigner/static evidence and clean-room transfer map.
- [ ] Continue China/India/worldwide source research; build Russian benchmark harness; compare at least three runs per model with quality/latency/RAM/thermal/ASR/TTS metrics and human scoring.
- [ ] Reconcile historical Gemeni draft PRs; do not merge blindly.

## P1 — Factory + Antigravity Mobile
- [ ] Verify Worker runtime health and D1; review https://localhost CORS before browser client.
- [ ] Inspect provider dispatch PR #19 and deployment notes PR #20; ensure dispatch is explicit/manual and not routine.
- [ ] Confirm task ledger persistence and real task/run state in Antigravity UI; no simulated progress.
- [ ] Check Factory PR #23/#26 live state, CI and branch divergence.

## P1 — AVTOY KOREA
- [ ] Inspect MAX outbox PR #81/#80/#79.
- [ ] Recheck ordered Telegram media PR #78 exact-head tests (historical 152/152); verify sequence and full-resolution images.
- [ ] Verify admin-only inquiry routing and current production Worker/bot; no public client phone/name leakage.

## P2 — Other repositories
- [ ] StampCleaner #5/#4/#3: inspect UI/video/still and extraction tests.
- [ ] RussSearchOPPO #15/#12/#11: reconcile branch divergence; fresh tests/build/security after schema changes.
- [ ] Voice Assistant: determine maintenance/reuse relationship to Jarvis; avoid duplicate implementation.
- [ ] russ-translation-models: inventory models/licenses and run reproducible translation benchmark.
- [ ] happ-proxy-pool: review threat model, privacy and real traffic evidence.
- [ ] Identify contents/purpose of sleep-button and breeno-apks.
- [ ] Forest 4G: gather band-specific signal measurements and verify B31/450MHz support.

## P3 — Cross-project research
- [ ] Verify candidates: Sarvam, Qwen, DeepSeek, GLM, Kimi, MiniMax, MiniCPM, Hunyuan/WeVisOne, Ling, Qwen ASR/TTS, LiteRT-LM/Omni, Fini, PocketWisdom/PocketPal, Native-LLM-for-Android and SmolChat-Android.
- [ ] Check licenses, model cards, hashes, quantizations, runtime and Snapdragon 8 Gen 2 fit.
- [ ] Research Google Antigravity IDE separately from Antigravity-Mobile and recover DNS test outcome.
