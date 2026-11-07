# Complex engineering task for Gemini — Jarvis emulator stalls

You are being invoked directly through the Gemini Developer API by Universal AI Factory. This is not a request for an ACK. Produce a rigorous independent engineering diagnosis.

## Objective
Diagnose the long-running Android emulator smoke-test jobs in repository `sokfrut-tech/Gemeni` (Jarvis app), identify the most likely stall point, and recommend a minimal safe workflow correction that makes emulator failures observable and prevents CI from hanging for 30+ minutes.

## Evidence confirmed from GitHub Actions
Four runs were inspected on 2026-11-07:
- Run 42347172763, job 128328589043, branch `fix/jarvis-tts-init-queue-2026-11-07`
- Run 42346984667, job 128328076036, branch `perf/jarvis-trim-desktop-native-assets-2026-11-07`
- Run 42346510482, job 128326481872, branch `docs/jarvis-qwen-device-validation-2026-11-07`
- Run 42346830463, job 128327125745, branch `feature/jarvis-qwen-self-diagnostic-2026-11-07`

In all four, checkout/JDK17/Gradle8.9 and earlier security/CodeQL jobs completed successfully; the final `Run Android emulator smoke tests` step remained `in_progress`. The following diagnostics/upload steps were pending because the emulator step had not exited. Fetching live job logs returned BlobNotFound while the jobs were active. Do not claim log-level proof of the precise hang.

## Workflow configuration observed in Gemeni PR #101
File `.github/workflows/factory-security.yml`:
- GitHub-hosted `ubuntu-latest`, Ubuntu 24.04
- emulator API 34, x86_64, google_apis, 4 cores
- boot timeout 900 seconds
- emulator options: `-no-window -gpu swiftshader_indirect -no-snapshot -noaudio -no-boot-anim -camera-back none`
- emulator action timeout 32 minutes
- job timeout 35 minutes
- then runs `./gradlew --no-daemon :app:connectedDebugAndroidTest`
- failure diagnostics run only after the emulator action returns failure; bounded adb diagnostics and artifact upload are configured after it.
- Earlier API35 attempts reportedly showed boot delays up to ~12 minutes and ADB Broken pipe; workflow comments say API34 was selected afterwards.

## Additional factory observation
The Universal-AI-Factory dispatcher had a malformed task-path matcher and duplicated trailing workflow content. It has now been replaced with a clean direct Gemini API workflow. This task itself is sent to Gemini using the repository secret `GEMINI_API_KEY`; default model is `gemini-3.8-flash`. The new runner is designed to save your full response in `coordination/gemini/outbox/`. No API key value is included in this task.

## Required report
1. Rank likely causes: emulator boot readiness, adb availability, Gradle connected-test deadlock, emulator action wrapper, software GPU rendering, cold boot, runner resource pressure, concurrency. State confidence and evidence for each.
2. Distinguish what is proven from what cannot be known without the step logs.
3. Explain the 32-minute action / 35-minute job timeout interaction and why diagnostics after the action cannot help until it exits.
4. Give a concrete minimal YAML/pseudodiff:
   - emit timestamped progress before/after emulator launch and each readiness check
   - wait for adb device with a hard deadline
   - poll `sys.boot_completed` and `init.svc.bootanim`
   - capture adb devices, emulator process, logcat, dmesg where permitted, and emulator console output on failure or timeout
   - apply an explicit timeout to connectedDebugAndroidTest
   - upload diagnostics with `if: always()`
   - ensure the overall step/job timeout leaves time for diagnostics
5. Recommend a controlled experiment matrix: keep API34 constant, compare GPU modes only one variable at a time, and avoid simultaneous workflow changes.
6. Recommend whether to limit concurrency. Note that separate GitHub-hosted jobs ordinarily run on separate VMs; parallel jobs do not prove a shared RAM bottleneck.
7. Do not recommend random retries as the main fix. If retry is proposed, justify exactly what transient condition it addresses.
8. State if this evidence supports changing app source code or only CI workflow instrumentation at this stage.

## Boundaries
- You cannot inspect the Gemeni repository or its other PR files from this task prompt; do not pretend otherwise.
- Do not claim access to the user's local Windows PC, `C:\dr`, WHPX/HAXM, local qemu process, allocated AVD RAM, or physical OPPO device.
- Do not claim to run tests or edit code.
- Do not create an ACK. Write a substantial, useful Markdown engineering report.


## Re-dispatch
This revision explicitly re-dispatches the same task after the direct API runner was repaired. Execute the full report now; do not return an ACK.
