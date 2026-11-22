# Independent Technical Audit Report — OGAM Breeno DEX Research & Native Assistant Baseline

- **Source task:** `coordination/gemini/inbox/2026-11-22_OGAM_breeno_dex_audit.md`
- **Task ID:** `OGAM-BREENO-DEX-AUDIT-2026-11-22`
- **Acceptance ACK:** `coordination/gemini/outbox/ACCEPTED_2026-11-22_OGAM_breeno_dex_audit.md` (commit `3536746`)
- **Author:** Gemini (Antigravity — independent evidence audit)
- **Requester:** ChatGPT
- **Status:** `completed_with_findings`
- **Date (UTC):** `2026-11-22T16:56Z`

---

## 1. Scope, Repositories, Branches & Commits Reviewed

| Target | Branch / PR | Inspected Commit SHA | Files Independently Read & Verified |
|---|---|---|---|
| `sokfrut-tech/OGAM` PR #2 | `docs/research-breeno-coloros-2026-11-22` ([#2](https://github.com/sokfrut-tech/OGAM/pull/2)) | `a5d5c71d` *(delta `e4ef6016` → `a5d5c71d`)* | `research/breeno/OPPO_LOCAL_APK_STATIC_ANALYSIS_2026-11-22.md`, `research/breeno/OPPO_APK_MANIFEST_AND_NATIVE_INVENTORY_2026-11-22.json`, `research/breeno/DEX_DECOMPILATION_AND_OGAM_TRANSFER_PLAN_2026-11-22.md`, `research/breeno/PR1_NATIVE_ASSISTANT_SOURCE_VERIFICATION_2026-11-22.md`, `research/breeno/OPPO_FIND_X6_PRO_DEVICE_EVIDENCE_2026-11-22.md`, `research/breeno/OPPO_BREENO_INSTRUCTIONS_PERMISSIONS_2026-11-22.md`, `research/breeno/OPPO_APK_ACQUISITION_RESEARCH_UPDATE_2026-11-22.md` |
| `sokfrut-tech/OGAM` PR #1 | `feature/jarvis-step-2-storage-privacy` ([#1](https://github.com/sokfrut-tech/OGAM/pull/1)) | `8ad6a6fd` *(with merge `b7c06988` over `main 14b27f7c`)* | `android/build.gradle`, `android/app/build.gradle`, `android/app/src/main/AndroidManifest.xml`, `android/app/src/main/res/xml/jarvis_voice_interaction.xml`, `android/app/src/main/res/values/bools.xml`, `android/app/src/main/res/values-v31/bools.xml`, `android/app/src/main/java/ai/offgridmobile/MainActivity.kt`, `MainApplication.kt`, all 9 files in `android/app/src/main/java/ai/offgridmobile/voice/*.kt`, all 3 Kotlin test files in `android/app/src/test/java/ai/offgridmobile/voice/*.kt`, `src/services/jarvisAssistantRole.ts`, `src/navigation/jarvisVoiceLinking.ts`, `src/screens/ChatScreen/index.tsx`, `src/screens/SettingsScreen.tsx` |
| OGAM CI Evidence | Open-core audit workflow | `8ad6a6fd` | GitHub Actions run `#45045542937` (`OGAM external dependency audit` -> `success`, 17 Node suites / 68 local cases) |

---

## 2. Environment & Honest Verification Boundary (Confirmed vs Inferred vs Unverified)

### 2.1 Workstation Tooling Check (`where`)
- **Available:** All 26 owner-supplied local APK files (`c:\Users\user\Desktop\codex\*.apk`), Python 3.12 static JSON/AXML extraction artifacts, full `sokfrut-tech/OGAM` PR #1 and PR #2 git trees, and Node `v26.13.1`.
- **NOT Installed / Unavailable:** `java` (NOT FOUND), `javac` (NOT FOUND), `jadx` (NOT FOUND), `apksigner` (NOT FOUND), `aapt2` (NOT FOUND), `apktool` (NOT FOUND), `adb` (NOT FOUND). Full RN `node_modules` / Android Gradle build was also not executed locally.

### 2.2 Strict Separation of Evidence Classes

| Evidence Class | What Is Established |
|---|---|
| **Confirmed (Factually Proven)** | 1. All 26 entries in `OPPO_APK_MANIFEST_AND_NATIVE_INVENTORY_2026-11-22.json` match the package names, `versionName`/`versionCode`, `minSdk→targetSdk`, DEX class counts, native `.so` counts, and asset counts (`3.1`) reported in `OPPO_LOCAL_APK_STATIC_ANALYSIS_2026-11-22.md`.<br>2. **Exact build matches verified:** `Breeno-13.4.3.apk` (`com.heytap.speechassist`, `versionCode=130403`, metadata `08c04e4_261110`, SHA-256 `cf547e473283...`) matches screenshot `13.4.3_08c04e4_261110`; `Breeno Memory-16.11.5.apk` (`com.oplus.aimemory`, `versionCode=16011005`, metadata `008719b_260901`, SHA-256 `b9646e411867...`) matches screenshot `16.11.5_008719b_260901` and APKMirror hash/cert `b0a9bbfc05ee...`.<br>3. `Инструкции Breeno-17.2.4.apk` (`com.coloros.shortcuts`, `17002004`, `468698a_260701`) is verified older than the screenshot version `17.7.2_91aa93e_261102`.<br>4. Zero inspected APKs declare `VoiceInteractionService` or `BIND_VOICE_INTERACTION` in their decoded manifest.<br>5. In `OGAM` PR #1 (`8ad6a6fd`), all 18 native assistant/RoleManager/Bridge/PCM Kotlin/XML/TS files and 3 Kotlin test files exist as inspected source, and static Node contract CI (`#45045542937`) passed. |
| **Inferred (Plausible Structural Signal — Not Method Proof)** | - SystemUI (`com.android.systemui`) → Breeno summon path via `ACTIVATE_SPEECH_ASSIST` and `SpeechAssistAccessProvider`.<br>- `com.oplus.aimemory` → `com.oplus.dmp` SQLCipher/vector RAG runtime flow and Persona prompt assembly.<br>- Actual offline execution of bundled native libraries (`libttsoff.so`, `libbreeno-oai-vad-lib.so`, `libOplusAEC.so`, `libnnaec.so`, `libkws.so`) and `com.oplus.aiunit` worker delegation.<br>- `AnalogSkillService` Accessibility invocation semantics vs user confirmation flow. |
| **Unverified / Not Accessible / Not Tested** | - **Method-level DEX/Smali behavior** across all 26 APKs (no JADX decompilation run).<br>- **JDK `apksigner` full-body ZIP/signing verification** (only v1/v2/v3/v3.1 cert blocks extracted in Python).<br>- **Installed `com.coloros.shortcuts` `17.7.2_91aa93e_261102` APK** (absent from local 26-APK set) and live PGEM10 cert comparison.<br>- **OGAM PR #1 Kotlin/Gradle compilation, manifest merge, Kotlin/JUnit execution** (`3` launch-guard + `5` role-snapshot + `8` PCM-player tests exist in source, untested in Gradle), TypeScript (`tsc`), Jest, and **PGEM10 / ColorOS 16.0.5 on-device runtime behavior**. |

---

## 3. Part A — Findings in PR #2 Documents (`OPPO_LOCAL_APK_STATIC_ANALYSIS_2026-11-22.md`, JSON & Companion Research Docs)

### Finding A1 `[MEDIUM]` — Unverified "Phone Screenshot Build" Attribution for `SearchService` & Wrong Citation for `Shortcuts`
- **Location:** `research/breeno/OPPO_LOCAL_APK_STATIC_ANALYSIS_2026-11-22.md:30-38`.
- **Evidence:** Section 2 row 5 places `16.16.80_2f5f245_260902` in the **"Phone Screenshot Build"** column for `SearchService (com.oplus.dmp)` and links all rows to `OPPO_FIND_X6_PRO_DEVICE_EVIDENCE_2026-11-22.md`. However, `OPPO_FIND_X6_PRO_DEVICE_EVIDENCE_2026-11-22.md` only records screenshots for `Breeno 13.4.3_08c04e4_261110` and `Breeno Memory 16.11.5_008719b_260901`; `SearchService` (`com.oplus.dmp`) has **no phone screenshot** anywhere in PR #2. Additionally, row 4 (`Инструкции Breeno` `17.7.2_91aa93e_261102`) comes from `OPPO_BREENO_INSTRUCTIONS_PERMISSIONS_2026-11-22.md`, not `OPPO_FIND_X6_PRO_DEVICE_EVIDENCE_2026-11-22.md`.
- **Correction:** Mark `SearchService` Phone Screenshot Build as `Not captured on device screenshots (local APK versionName == filename)` and cite `OPPO_BREENO_INSTRUCTIONS_PERMISSIONS_2026-11-22.md` for `17.7.2_91aa93e_261102`.

### Finding A2 `[MEDIUM]` — Package Group & Certificate-Cluster Count Contradiction Across Both Markdown and JSON
- **Location:** `OPPO_LOCAL_APK_STATIC_ANALYSIS_2026-11-22.md:20, 56-84, 89-99`; `OPPO_APK_MANIFEST_AND_NATIVE_INVENTORY_2026-11-22.json` (`role_group`).
- **Evidence:**
  1. `Поиск-6.0.apk` (`reactivephone.msearch`, third-party Russian search app signed by `53d2a5e09c30`) is placed inside `oppo_coloros_breeno_ecosystem` (the `"20 system APKs"` / §3.2 `"15 ecosystem APKs"` group), while `Browser-40.10.25.2.apk` (`com.heytap.browser`) and `阅读-9.17.0.apk` (`com.heytap.reader`) sit in the `"6 third-party companion APKs"` group (§3.3 / `third_party_or_companion`).
  2. Section 4 line 89 states *"Across the **19** OPPO/Oplus/ColorOS/HeyTap APKs ... form **two main privileged clusters** plus several independent HeyTap certs"*, yet the bulleted list immediately below enumerates **4** clusters, and the actual count of OPPO/Oplus/ColorOS/HeyTap/SystemUI packages in the 26 APKs is **21** (`5` in §3.1 + `14` OPPO-family in §3.2 + `Browser` + `Reader` in §3.3), or **19** excluding `Browser` & `Reader`.

### Finding A3 `[MEDIUM]` — Manifest Terminology Overclaim on `AIUnit` Worker Sandboxing
- **Location:** `OPPO_LOCAL_APK_STATIC_ANALYSIS_2026-11-22.md:172`.
- **Evidence:** Section 5.5.1 describes `com.oplus.aiunit`'s `ServiceProcess0..200` as **"201 sandboxed `ServiceProcess0..200` worker processes"**. Independent inspection of the extracted raw manifest entries shows `201/201` declare `process=":worker0..200"`, `exported=false`, `foregroundServiceType=['dataSync']`, and **`0/201` declare `android:isolatedProcess="true"`**. In Android terminology, `"sandboxed process"` typically implies `isolatedProcess="true"` (empty-permission isolated UID), whereas these are standard multi-process worker slots sharing `com.oplus.aiunit`'s app UID for crash/OOM/model isolation.

### Finding A4 `[MEDIUM]` — Missing Epistemic Labels (Manifest/String Signals Stated as Runtime Proof) & Size Unit Mixing
- **Location:** `OPPO_LOCAL_APK_STATIC_ANALYSIS_2026-11-22.md:108-186, 201`.
- **Evidence:**
  1. Claims such as SystemUI dispatch into Breeno (§5.1.1), offline TTS/VAD/AEC execution (§5.1.3), `aimemory` querying `com.oplus.dmp` Persona (§5.2), `AIUnit` worker delegation via `libaiunit_sdk_core.so` (§5.5.1), and OCR cloud fallback (§5.5.3) rely solely on manifest components, `.so` filenames, `content://` string constants, and HTTPS hostnames without explicit `[inferred — awaiting JADX method & airplane-mode trace]` tags.
  2. Section 6 line 201 writes `Breeno (130 MB)` and `Global Search (110 MB)` alongside `142 MB custom WebView` — mixing decimal compressed APK sizes (`130.83 MB` = `124.8 MiB`, `110.57 MB` = `105.4 MiB`) with uncompressed shared library size (`libheytapwebview.so = 142,006,736` bytes = `142.0 MB` / `135.4 MiB`). Note: `OPPO_LOCAL_APK_STATIC_ANALYSIS_2026-11-22.md` §1 honestly states JADX/apksigner were not run, and `DEX_DECOMPILATION_AND_OGAM_TRANSFER_PLAN_2026-11-22.md` §1 (`bfc324af`) explicitly reinforces the method boundary — adding inline markers in §5–§6 brings both docs into full alignment.

### Finding A5 `[LOW-MEDIUM]` — Stale Unedited Sections & Superseded PR #1 Commit/Run Refs
- **Locations & Evidence:**
  1. `OPPO_FIND_X6_PRO_DEVICE_EVIDENCE_2026-11-22.md:53-55, 83-84` still lists *"Exact ColorOS version currently installed... Android API level, firmware build fingerprint, security patch"* under **"Not confirmed"** and asks for an `About device` screenshot, contradicting the later header (`line 5`) and Section 7 (`lines 93-103`) added to the same file confirming `ColorOS 16.0.5`, `PGEM10_16.0.5.1201(CN01C20P01)`, `Android 16`, kernel, and `1 August 2026` security update (with only `ro.build.fingerprint` and API int remaining unprinted).
  2. `PR1_NATIVE_ASSISTANT_SOURCE_VERIFICATION_2026-11-22.md:58-67` & `DEX_DECOMPILATION_AND_OGAM_TRANSFER_PLAN_2026-11-22.md:86` cite PR #1 run `#45039077226` (commit before PR #1 merged `main` in `b7c06988` and reached `8ad6a6fd` with run `#45045542937`). Additionally, PR #2's `PR1_NATIVE_ASSISTANT_SOURCE_VERIFICATION_2026-11-22.md` did not catch the 5 Android Kotlin/XML security/compile issues documented in Part B below.

---

## 4. Part B — Independent Audit of OGAM PR #1 Native Assistant Source (`8ad6a6fd`)

### 4.1 Complete Verified File, Symbol & Test Inventory (Inspected Directly in PR #1)

| File | Verified Symbols / Declarations | Commit |
|---|---|---|
| `android/app/src/main/AndroidManifest.xml` | `JarvisAssistantBridgeActivity` (`exported=false`, `excludeFromRecents=true`, `noHistory=true`); `JarvisVoiceInteractionService` (`BIND_VOICE_INTERACTION`, `enabled=@bool/jarvis_voice_interaction_enabled`, `exported=true`); `JarvisVoiceInteractionSessionService` (`BIND_VOICE_INTERACTION`, `exported=true`, `process=":jarvis_voice"`); `MainActivity` `offgrid://oauth` & `offgrid://pro` `VIEW` filters (`offgrid://assistant` removed from `BROWSABLE`) | `e801dad3` |
| `android/app/src/main/res/xml/jarvis_voice_interaction.xml` | `<voice-interaction-service>` with `sessionService`, `recognitionService`, `supportsAssist="true"`, `supportsLocalInteraction="false"` | `9a4eaa95` |
| `android/app/src/main/res/values/bools.xml` & `values-v31/bools.xml` | `jarvis_voice_interaction_enabled` = `false` (default) / `true` (`v31`) | `97166461`, `bae5b0de` |
| `android/app/src/main/java/ai/offgridmobile/MainActivity.kt` | `isJarvisAssistantIntent(intent)`, `acceptJarvisAssistantIntent(intent)`, `onNewIntent(intent)`, `onCreate(savedInstanceState)` calling `JarvisAssistantLaunchGuard.consume(token)` and stripping unauthenticated `offgrid://assistant/voice` intents | `08f2e6f4` |
| `android/app/src/main/java/ai/offgridmobile/MainApplication.kt` | Registers `JarvisAssistantRolePackage()` in `reactHost` `packageList` | `ff1d0785` |
| `.../voice/JarvisVoiceInteractionService.kt` | `onReady()` disables `SHOW_WITH_ASSIST | SHOW_WITH_SCREENSHOT` | `d696a8ad` |
| `.../voice/JarvisVoiceInteractionSessionService.kt` | `onNewSession(args)` returns `JarvisVoiceInteractionSession(this)` | `16743581` |
| `.../voice/JarvisVoiceInteractionSession.kt` | `init { setUiEnabled(false) }`, `onShow()` launches `JarvisAssistantBridgeActivity` via `startAssistantActivity` (API 26+) or `startVoiceActivity`, then `finish()` | `e18905c6` |
| `.../voice/JarvisAssistantBridgeActivity.kt` | Non-exported trampoline; calls `JarvisAssistantLaunchGuard.issue()` and starts `MainActivity` with `EXTRA_LAUNCH_TOKEN`, then `finish()` | `44efc320` |
| `.../voice/JarvisAssistantLaunchGuard.kt` | `@Synchronized` single-slot one-use UUID token (`issue()`, `consume()`, `resetForTesting()`) | `67630626` |
| `.../voice/JarvisAssistantRoleModule.kt` | `@ReactMethod getStatus(promise)`, `requestAssistantRole(promise)`, `readStatus()`, `BaseActivityEventListener` | `5b13196e` |
| `.../voice/JarvisAssistantRolePackage.kt` & `RoleSnapshot.kt` | Registers `JarvisAssistantRoleModule`; pure `JarvisAssistantRoleSnapshot.from(...)` (`supported && roleAvailable && roleHeld && activeService`) | `441adbf5`, `c110f888` |
| `.../voice/JarvisPcmStreamPlayer.kt` | Engine-neutral mono Float32 `AudioTrack` + `AudioFocus` player with monotonic `generation` token (`begin`, `write`, `finish`, `cancel`, `close`) — currently `internal` with no production callers | `9629cefb` |
| `android/app/src/test/java/ai/offgridmobile/voice/*Test.kt` | `JarvisAssistantLaunchGuardTest` (`3` `@Test`s), `JarvisAssistantRoleSnapshotTest` (`5` `@Test`s), `JarvisPcmStreamPlayerTest` (`8` `@Test`s) — **NOT executed in Gradle** | `d846dd6e`, `1fa0b8df`, `ad67ff24` |
| `src/services/jarvisAssistantRole.ts` & `src/navigation/jarvisVoiceLinking.ts` & `src/screens/{ChatScreen,SettingsScreen}` | Typed JS bridge (`getJarvisAssistantRoleStatus`, `requestJarvisAssistantRole`), Settings UI status/request, navigation route `Chat -> assistant/voice`, one-shot `InteractionManager` mic handoff preserving drafts | `2c1703d4`, `8b452ed0` |

### 4.2 Code-Level Security, Build & Runtime Defects Found in PR #1 (Not Caught in PR #2 Verification)

#### Finding B1 `[HIGH]` — High-Probability Kotlin Compile Risk in `JarvisAssistantRoleModule.kt` Under RN `0.83.1`
- **File:** `android/app/src/main/java/ai/offgridmobile/voice/JarvisAssistantRoleModule.kt:34-40, 93`
- **Issue:**
  1. `object : BaseActivityEventListener()` overrides `onActivityResult(activity: Activity?, requestCode: Int, resultCode: Int, data: Intent?)` with nullable `Activity?`. React Native `0.78+`/`0.83.1` (`package.json:71`) migrated `ActivityEventListener.onActivityResult` to non-null `activity: Activity`, which causes Kotlin `overrides nothing` / signature mismatch errors unless verified against the exact RN `0.83.1` `.aar`. Notice **no other module** in `android/app/src/main/java/ai/offgridmobile/**` overrides `BaseActivityEventListener`.
  2. Line 93 reads bare `val activity = currentActivity` instead of `reactApplicationContext.currentActivity` / `reactContext.currentActivity` used by all 7 other OGAM native modules (`DownloadManagerModule`, `SyncDownloadsModule`, `EnginePackModule`, `MediaShareModule`, `ProblemReportModule`, `ScribeEntryModule`, `VideoGenerationModule`). Calling `reactContext.currentActivity` avoids deprecation/visibility drift across RN versions.
- **Gate:** Must compile cleanly under `:app:compileDebugKotlin` before claiming Android readiness.

#### Finding B2 `[HIGH]` — Missing `Intent.FLAG_ACTIVITY_NEW_TASK` When Launching Activity from `:jarvis_voice` Session
- **File:** `android/app/src/main/java/ai/offgridmobile/voice/JarvisVoiceInteractionSession.kt:30-42`
- **Issue:** `JarvisVoiceInteractionSession` constructs `Intent(getContext(), JarvisAssistantBridgeActivity::class.java)` with only `FLAG_ACTIVITY_CLEAR_TOP or FLAG_ACTIVITY_SINGLE_TOP` — omitting `Intent.FLAG_ACTIVITY_NEW_TASK` before `startAssistantActivity(launchIntent)` / `startVoiceActivity(launchIntent)`. Calling `startActivity`/`startAssistantActivity` from a non-Activity `Service` context (`VoiceInteractionSessionService` in `:jarvis_voice`) requires `FLAG_ACTIVITY_NEW_TASK` on Android, otherwise Android throws `AndroidRuntimeException: Calling startActivity() from outside of an Activity context requires the FLAG_ACTIVITY_NEW_TASK flag`.

#### Finding B3 `[HIGH]` — Hardcoded Production Package Name in `jarvis_voice_interaction.xml` Breaks `.dev` Debug Builds & Violates `ComponentName` Semantics
- **File:** `android/app/src/main/res/xml/jarvis_voice_interaction.xml:10` vs `android/app/build.gradle:95, 141`
- **Issue:** Line 10 sets `android:recognitionService="ai.offgridmobile/ai.offgridmobile.voice.JarvisVoiceInteractionService"`.
  1. AOSP `VoiceInteractionServiceInfo` (`ComponentName.unflattenFromString` / framework parsing with package name) expects a class name relative to the service's package (e.g., `ai.offgridmobile.voice.JarvisVoiceInteractionService`), not a `pkg/cls` flattened component string pointing to a hardcoded package.
  2. Even worse, `android/app/build.gradle:141` configures `applicationIdSuffix ".dev"` on debug builds (and the APK workflow builds arm64 debug!), making the debug package `ai.offgridmobile.dev`. Hardcoding `ai.offgridmobile/` fails component/package equality checks in `VoiceInteractionServiceInfo` on debug APKs, potentially preventing ColorOS/Android from recognizing OGAM debug builds as eligible in `RoleManager`.

#### Finding B4 `[MEDIUM-HIGH]` — Case/Trailing-Slash Forged Assistant Intent Bypass in `MainActivity.kt` & Token Staleness
- **Files:** `android/app/src/main/java/ai/offgridmobile/MainActivity.kt:34-40, 108-110`; `JarvisAssistantBridgeActivity.kt:13-30`; `JarvisAssistantLaunchGuard.kt:12-33`
- **Issue:** `isJarvisAssistantIntent(intent)` checks exact string equality:
  `intent.action == Intent.ACTION_VIEW && data.scheme == "offgrid" && data.host == "assistant" && data.path == "/voice"`.
  - If an external app launches exported `MainActivity` with `OFFGRID://assistant/voice?startVoice=1`, `offgrid://ASSISTANT/voice?startVoice=1`, or `offgrid://assistant/voice/?startVoice=1`, `isJarvisAssistantIntent()` returns **`false`**, so `MainActivity` **never checks the one-time token and forwards the intent** into React Native `Linking`, where React Navigation's URL parser (`jarvisVoiceLinking.ts:14-18`, case/slash tolerant) can still activate `ChatScreen` with `startVoice: true`!
  - Additionally, `JarvisAssistantLaunchGuard` issues a token with no expiration TTL (`SystemClock.elapsedRealtime()` check) and stores only a single `pendingToken` — if bridge `onCreate` runs before another lifecycle event cancels or delays `MainActivity`, a stale token lingers indefinitely until overwritten or consumed.

#### Finding B5 `[MEDIUM]` — Missing Android 16 / ColorOS 16 Lifecycle, Audio-Focus, & Permission Architecture Gates
1. **Un-gated Session Service below API 31 (`AndroidManifest.xml:137-142`):** `JarvisVoiceInteractionSessionService` omits `android:enabled="@bool/jarvis_voice_interaction_enabled"`, leaving an exported `BIND_VOICE_INTERACTION` service enabled on Android 7–11 even when `JarvisVoiceInteractionService` is disabled.
2. **Lock-screen, BAL & ColorOS 16 freeze gates:** ColorOS 16 Background Activity Launch (Android 14–16 BAL restrictions), lock-screen summon (`setShowWhenLocked` / keyguard behavior), and ColorOS strict background/auto-start killing of `:jarvis_voice` remain completely untested on `PGEM10`. Also `ProcessTextActivity` (`ai.offgridmobile.clipboard`) and `ImproveTextActivity` (`ai.offgridmobile.scribe`) sit exported in `AndroidManifest.xml` without documented Android 16 PII/redaction tests.
3. **PCM player audio usage & CPU spin (`JarvisPcmStreamPlayer.kt:136, 276`):** Uses `AudioAttributes.USAGE_MEDIA` instead of `USAGE_ASSISTANT` (making Android audio routing & Ducking treat Jarvis speech as music rather than assistant voice), busy-waits via `LockSupport.parkNanos(100_000L)` (up to 10,000 wakeups/sec when the track buffer is full; should back off `5–10 ms` or use `WRITE_BLOCKING` off-main-thread), and stays `internal` with no TTS backend yet. Note also `JarvisVoiceInteractionService.onCreate` / session cold-start latency vs React Native warm start is not budgeted.
4. **Broad Manifest Permissions vs Minimum Principle (`AndroidManifest.xml:31-65`):** Declares `MANAGE_EXTERNAL_STORAGE`, `READ_MEDIA_IMAGES/VIDEO`, `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`, `FOREGROUND_SERVICE_SPECIAL_USE`, `FOREGROUND_SERVICE_CONNECTED_DEVICE`, `READ/WRITE_CALENDAR`, `CAMERA`, `RECORD_AUDIO`. Requires an explicit Play/ColorOS offline permission-denial & airplane-mode matrix before release.

---

## 5. Part C — Suggested Concrete Doc Diffs for PR #2 (Review Only — No Files Modified in PR #2)

Apply cleanly in `sokfrut-tech/OGAM` PR #2 (`docs/research-breeno-coloros-2026-11-22`):

```diff
--- a/research/breeno/OPPO_LOCAL_APK_STATIC_ANALYSIS_2026-11-22.md
+++ b/research/breeno/OPPO_LOCAL_APK_STATIC_ANALYSIS_2026-11-22.md
@@ -20,16 +20,18 @@
 - DEX structural header/table extraction ... on 19 OPPO/ColorOS/Breeno system APKs plus `SearchService`, `QuickSearchBox`, `Ads` and lightweight inventory on third-party/companion apps (including `Поиск-6.0.apk` / `reactivephone.msearch`).
 
 ## 2. Exact-Build Verification Gate (Section 3 Check)
 
-Manifest `<meta-data>` embeds `versionCommit` and `versionDate` fields in several ColorOS/HeyTap APKs, allowing exact build verification against the previously captured OPPO Find X6 Pro screenshots (`OPPO_FIND_X6_PRO_DEVICE_EVIDENCE_2026-11-22.md`):
+Manifest `<meta-data>` embeds `versionCommit` and `versionDate` fields in several ColorOS/HeyTap APKs, allowing comparison against the previously captured OPPO Find X6 Pro screenshots (`OPPO_FIND_X6_PRO_DEVICE_EVIDENCE_2026-11-22.md` for Breeno & Memory; `OPPO_BREENO_INSTRUCTIONS_PERMISSIONS_2026-11-22.md` for Instructions):
 
 | ... |
-| **SearchService (`com.oplus.dmp`)** | `com.oplus.dmp` | `16.16.80_2f5f245_260902` | `SearchService-16.16.80_2f5f245_260902.apk` | `16.16.80_2f5f245_260902` (`16016080`) | ... | Exact filename/version match |
+| **SearchService (`com.oplus.dmp`)** | `com.oplus.dmp` | *Not captured in device screenshots* | `SearchService-16.16.80_2f5f245_260902.apk` | `16.16.80_2f5f245_260902` (`16016080`) | ... | **Local APK filename == manifest match (phone build unverified)** |
 
 @@ -89 +91 @@
-Across the 19 OPPO/Oplus/ColorOS/HeyTap APKs, manifests and v2/v3 signing certificates form **two main privileged clusters** plus several independent HeyTap certs:
+Across the 21 OPPO/Oplus/ColorOS/HeyTap/SystemUI APKs (`19` excluding `Browser` & `Reader`), manifests and v2/v3 signing certificates form **four** main signer/trust groupings (two core Oplus platform/OS keys, one ColorOS UX key, plus HeyTap/OEM certs):
 
 @@ -172 +174 @@
-- Exposes `AIUnitService` ... + **201 sandboxed `ServiceProcess0..200` worker processes**.
+- Exposes `AIUnitService` ... + **201 non-exported `:worker0..200` worker processes** (`isolatedProcess=false`; crash/OOM isolation within app UID, not OS-isolated sandboxes).
```

```diff
--- a/research/breeno/OPPO_FIND_X6_PRO_DEVICE_EVIDENCE_2026-11-22.md
+++ b/research/breeno/OPPO_FIND_X6_PRO_DEVICE_EVIDENCE_2026-11-22.md
@@ -52,12 +52,11 @@
 Not confirmed:
-- Exact ColorOS version currently installed. A ColorOS 16 promotional image is not proof the device itself runs ColorOS 16.
-- Android API level, firmware build fingerprint, security patch.
+- Exact `ro.build.fingerprint` string and compiled Android API integer (resolved later in §7 from the Settings > Version screenshot: ColorOS 16.0.5, build `PGEM10_16.0.5.1201(CN01C20P01)`, Android 16, security update `1 August 2026`).
```

Additionally, update `OPPO_APK_MANIFEST_AND_NATIVE_INVENTORY_2026-11-22.json` to move `Поиск-6.0.apk` (`reactivephone.msearch`) from `oppo_coloros_breeno_ecosystem` to `third_party_or_companion` (and decide explicitly whether HeyTap `Browser`/`Reader` belong in an `oppo_heytap_companion` bucket), and update `PR1_NATIVE_ASSISTANT_SOURCE_VERIFICATION_2026-11-22.md` to cite PR #1 HEAD `8ad6a6fd` / run `#45045542937` plus Findings B1–B5.

---

## 6. Part D — Owner Workstation Verification & JADX / `apksigner` / `Shortcuts 17.7.2` Extraction Plan

Execute strictly on the local workstation (`c:\Users\user\Desktop\codex\`) into an **isolated analysis directory OUTSIDE any Git repository** (e.g., `C:\breeno_jadx_work\`):

### 6.1 Required Pinned Tools
1. **Java JDK:** Eclipse Temurin JDK **17.0.13+** (required by JADX & Android build-tools).
2. **JADX:** `jadx` **v1.5.1** (<https://github.com/skylot/jadx/releases/tag/v1.5.1>, record downloaded `.zip` SHA-256).
3. **Android Build-Tools `36.0.0`** (`apksigner`, `aapt2` — matches `compileSdkVersion = 36` in `OGAM/android/build.gradle`) + **Android Platform-Tools** (`adb`).

### 6.2 Ordered Read-Only Workstation Commands (PowerShell)

```powershell
# 0. Preserve SHA-256 before/after and create out-of-repo scratch root
$work = "C:\breeno_jadx_work"
New-Item -ItemType Directory -Force -Path "$work\jadx_out", "$work\device_17_7_2" | Out-Null
Get-FileHash "c:\Users\user\Desktop\codex\*.apk" -Algorithm SHA256 |
  Export-Csv "$work\apk_sha256_baseline.csv" -NoTypeInformation

# 1. Verify full APK cryptographic signatures & certs (P0 APKs first)
$apks = @(
  "c:\Users\user\Desktop\codex\Breeno-13.4.3.apk",
  "c:\Users\user\Desktop\codex\Breeno Memory-16.11.5.apk",
  "c:\Users\user\Desktop\codex\SearchService-16.16.80_2f5f245_260902.apk",
  "c:\Users\user\Desktop\codex\Сервисный модуль ИИ-16.1.33_spshop.apk",
  "c:\Users\user\Desktop\codex\Быстрый поиск Breeno-16.12.2.apk"
)
foreach ($apk in $apks) {
  apksigner verify --verbose --print-certs "$apk" | Out-File "$work\$(Split-Path $apk -Leaf).apksigner.txt" -Encoding utf8
}

# 2. Pull exact Breeno Instructions 17.7.2 & verify live system package certs read-only from PGEM10
adb devices -l
adb shell pm path com.coloros.shortcuts | Out-File "$work\device_17_7_2\pm_path.txt" -Encoding utf8
# Replace <path> below with output of pm path (read-only pull; no install/modify):
adb pull <path> "$work\device_17_7_2\com.coloros.shortcuts_17.7.2.apk"
adb shell dumpsys package com.heytap.speechassist | Out-File "$work\device_17_7_2\speechassist_dumpsys.txt" -Encoding utf8
adb shell dumpsys package com.oplus.aimemory | Out-File "$work\device_17_7_2\aimemory_dumpsys.txt" -Encoding utf8
adb shell getprop ro.build.fingerprint | Out-File "$work\device_17_7_2\build_fingerprint.txt" -Encoding utf8

# 3. Decompile priority APKs strictly outside Git with JADX 1.5.1
jadx --deobf --show-bad-code -j 6 -d "$work\jadx_out\breeno_13.4.3" "c:\Users\user\Desktop\codex\Breeno-13.4.3.apk"
jadx --deobf --show-bad-code -j 6 -d "$work\jadx_out\aimemory_16.11.5" "c:\Users\user\Desktop\codex\Breeno Memory-16.11.5.apk"
jadx --deobf --show-bad-code -j 6 -d "$work\jadx_out\dmp_16.16.80" "c:\Users\user\Desktop\codex\SearchService-16.16.80_2f5f245_260902.apk"
jadx --deobf --show-bad-code -j 6 -d "$work\jadx_out\aiunit_16.1.33" "c:\Users\user\Desktop\codex\Сервисный модуль ИИ-16.1.33_spshop.apk"
jadx --deobf --show-bad-code -j 6 -d "$work\jadx_out\shortcuts_17.7.2" "$work\device_17_7_2\com.coloros.shortcuts_17.7.2.apk"
```

### 6.3 Prioritized Method-Level JADX Inspection Checklist (Never Commit Raw Output)
1. **P0 — `Breeno 13.4.3`:**
   - `SpeechService`: `onStartCommand` / intent dispatch table, `FOREGROUND_SERVICE` start/stop vs cancel/barge-in, audio-focus acquisition.
   - `OmniMind` classes: confirm whether planner is a multi-step DAG executor or an HTTP/LLM router; inspect confirmation callbacks.
   - `AnalogSkillService` & JNI bridges (`BreenoWakeupVprint`,VAD, AEC, `ttsoff`): confirm confirmation prompts and offline vs network fallback branches.
2. **P0 — `Breeno Memory 16.11.5` & `SearchService 16.16.80`:**
   - Trace `DataShareProvider` → `com.oplus.dmp` `SearchProvider`/`IndexProvider`, Room schemas, SQLCipher passphrase derivation/lifecycle (confirm key isolation), and `ChunkConfig.json` invocation during document/PDF ingest.
3. **P1 — `Instructions 17.7.2` (once pulled from `PGEM10`):**
   - Diff manifest/services/triggers vs `17.2.4`; trace `TaskMonitorService` and `ISceneService` rule schema.
4. **Export Rule:** Commit only human-authored clean-room architectural notes citing `(APK SHA-256, package/build, class, method signature, confidence)`. Never commit APK bytes, DEX/Smali, native `.so`, keys, `AUTH_CODE`s, or private phone data.

---

## 7. Next Action Items Summary

1. **Before running OGAM native build tests:** Fix PR #1 Findings **B1** (`JarvisAssistantRoleModule.kt` RN `0.83.1` override & `reactApplicationContext.currentActivity`), **B2** (`FLAG_ACTIVITY_NEW_TASK` in `JarvisVoiceInteractionSession.kt`), **B3** (`jarvis_voice_interaction.xml` hardcoded `ai.offgridmobile/` package blocking `.dev`), **B4** (`MainActivity.kt` case-insensitive scheme/host/normalized path + launch token TTL), and **B5** (`JarvisVoiceInteractionSessionService` API < 31 flag, `USAGE_ASSISTANT`, backoff park).
2. **PR #2 doc cleanup:** Apply Section 5 diffs (`OPPO_LOCAL_APK_STATIC_ANALYSIS_2026-11-22.md`, `OPPO_FIND_X6_PRO_DEVICE_EVIDENCE_2026-11-22.md`, `OPPO_APK_MANIFEST_AND_NATIVE_INVENTORY_2026-11-22.json`, and `PR1_NATIVE_ASSISTANT_SOURCE_VERIFICATION_2026-11-22.md`).
3. **Owner workstation:** Install pinned JDK 17 + JADX `1.5.1` + Android build-tools `36.0.0` + `adb`, run Section 6 commands on `PGEM10`, pull `com.coloros.shortcuts 17.7.2`, and verify Kotlin/Gradle compile on OGAM PR #1 once `../shared` migration completes.
