# Independent Gemini task — Jarvis Android emulator stalls

## Goal
Independently diagnose why four Jarvis Android emulator smoke-test jobs remain in progress for a long time and propose the smallest evidence-backed correction. This is a READ-ONLY analysis task; do not change repositories or claim to have run an emulator.

## Repository evidence supplied
Target app repository: sokfrut-tech/Gemeni.
Workflow file: .github/workflows/factory-security.yml, branch fix/jarvis-tts-init-queue-2026-11-07.

The workflow has:
- secrets scan and CodeQL jobs
- emulator-smoke depends on CodeQL
- runs-on ubuntu-latest, job timeout 35 minutes
- emulator action timeout-minutes 32
- API 34, x86_64, google_apis, 4 cores, boot timeout 900 seconds
- options: -no-window -gpu swiftshader_indirect -no-snapshot -noaudio -no-boot-anim -camera-back none
- connected test command: gradle --no-daemon :app:connectedDebugAndroidTest
- failure diagnostics are captured only after the emulator action fails, with bounded adb commands and uploaded artifacts.

Four runs checked at 2026-11-07 06:45 UTC:
- run 42347172763, job 128328589043, branch fix/jarvis-tts-init-queue-2026-11-07
- run 42346984667, job 128328076036, branch perf/jarvis-trim-desktop-native-assets-2026-11-07
- run 42346510482, job 128326481872, branch docs/jarvis-qwen-device-validation-2026-11-07
- run 42346830463, job 128327125745, branch feature/jarvis-qwen-self-diagnostic-2026-11-07

In all four, checkout/JDK17/Gradle8.9 completed successfully and the single step "Run Android emulator smoke tests" was still in_progress. Following diagnostic and upload steps were pending. GitHub job-log download returned BlobNotFound while jobs were active, so there is no direct emulator stdout yet.

Important: these are GitHub-hosted jobs; do not assert that all four share one VM or RAM pool. Four parallel jobs may consume repository/account concurrency but each hosted runner is ordinarily isolated.

## Required analysis
1. Inspect this workflow configuration for likely emulator boot / ADB / Gradle connected-test stall mechanisms.
2. Explain why current failure diagnostics may not help if emulator action itself hangs or times out.
3. Recommend an evidence-first sequence: step-level log capture, boot readiness checks, adb wait-for-device, boot_completed, emulator console/adb diagnostics, test command timeout, artifacts even on failure, bounded retries only if justified.
4. Consider whether -gpu swiftshader_indirect + 4 cores + cold boot + no snapshot is an appropriate hosted runner profile; distinguish hypotheses from proven causes.
5. Recommend whether to serialize emulator jobs or cap concurrency, and explain that job-level GitHub concurrency can serialize across refs but will trade throughput for predictability.
6. Suggest a minimal workflow patch with exact YAML or pseudodiff, but do not claim it is tested.
7. Identify app-side test code risks only if source evidence is supplied; do not invent.

## Constraints
- Do not claim to access local Windows C:\dr, the user's physical OPPO, local RAM, WHPX/HAXM, or qemu process.
- Do not claim to have run tests or edited code.
- Explicitly label confirmed facts vs hypotheses.
- Write a substantive report to coordination/gemini/outbox/REPORT_2026-11-07_jarvis-emulator-hang-root-cause.md in this factory repository.
- If unable to access Gemini API or the report cannot be committed, state the exact failure; never write a fake ACK/report.
