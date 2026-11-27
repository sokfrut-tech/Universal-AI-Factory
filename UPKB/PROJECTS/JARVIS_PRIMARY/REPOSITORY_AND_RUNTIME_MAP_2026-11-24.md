# Jarvis project map and runtime acceptance — 2026-11-24

## Keep these codebases separate
1. **Primary Jarvis product** — `sokfrut-tech/Gemeni`. Persistent handoff: `docs/CONTINUATION_STATE.md`. Product is a Russian-speaking OPPO/ColorOS assistant/agent. Main branch is explicitly NOT release-ready; the latest user-reported black screen with only static Jarvis text is a hard regression.
2. **OGAM / Off Grid AI fork** — `sokfrut-tech/OGAM`. Separate fork and separate PR chain. Recent work is a Jarvis memory subsystem prototype (M1/M2), not a replacement for the primary Jarvis app.
3. **RussSearchOPPO** — separate repository with a 2026-11-06 handoff and Hive project memory; relationship to Gemeni must be resolved from source history, not guessed.

## Primary Jarvis / Gemeni — verified current leads
- `docs/CONTINUATION_STATE.md` says the black-screen APK is a known user-observed failure.
- Acceptance requires real microphone capture, Russian ASR, tool/action dispatch, TTS, VoiceInteraction registration, accessibility/AIDL where applicable, visible native renderer, security checks, emulator and ultimately OPPO runtime evidence.
- PR #148 is open, non-draft, head `769e50e782aafb2698b9ff31f429725087c22ecc`; its observed checks (secret scan, CodeQL, build) passed. It adds pinned llama.cpp Android source/build support and additional runtime smoke tests (native library init, minimize/resume, text query and tabs).
- Passing PR #148 CI is not evidence that the APK was installed and launched successfully on the user's physical OPPO Find X6 Pro (PGEM10).
- Main-branch `docs/CURRENT_STATUS.md` is last updated 2026-10-28 and describes project as NOT RELEASE READY. Its embedded 2026-11-06 audit describes main source limitations and old PR chain. Treat it as historical until refreshed from current head.

## OGAM memory M1/M2 — verified current leads
- PR #7 open draft: `feature/jarvis-step-1-memory-m2-2026-11-24`, head `276f2f2ca489122b9145410b9552a199683604b3`, base M1 branch `feature/jarvis-step-1-memory-m1-2026-11-24`.
- M2 includes deterministic secret screening, scoped conflict detection, optimistic concurrency, SQLite tombstones, expiry boundary enforcement and explicit confirmation UI.
- PR body reports 7 Jest suites / 31 tests and real `node:sqlite` integration; live CI check-runs for focused tests, import/dependency scan and isolated Android ARM64 APK build all returned SUCCESS.
- PR #7 adds an isolated Android probe app with package `com.jarvism2probe`, not the primary Jarvis package. This APK is a test harness for memory integration, not the user-facing Jarvis product APK.
- PR #6 is the isolated M1 OP-SQLite probe (package `com.jarvism1probe`), also not the main Jarvis APK.
- PR #7 acceptance explicitly remains draft/unmerged until CI and physical OPPO Find X6 Pro runtime checks are confirmed.
- The observed PR #7 CI checks do not prove physical-device install/launch. Do not claim the M2 probe works on the user's phone without a device result.

## Critical distinction for current user issue
A black-screen / app-collapsing report must be diagnosed against the exact APK package name, version, SHA-256, source repo/branch/commit and Android logcat. Never assume the M1/M2 probe APK is the primary Jarvis APK. Never treat a successful Gradle/CI build as device runtime acceptance.

## Next actions
1. Ask for / retrieve the exact installed APK artifact identity only if not available in the active device/test context.
2. Verify artifact package/applicationId, versionCode/versionName, SHA-256 and originating repo/branch/commit.
3. Read the corresponding uploaded emulator/device artifact logs, screenshot, process PID and Activity launch result.
4. Separate outcomes: built, installed, launched, process stayed alive, UI rendered, memory probe PASS, actual OPPO physical device accepted.
5. Update Gemeni and OGAM project checkpoints independently. Do not merge either PR automatically.
