# Factory Security Rollout Ledger

**Updated:** 2026-11-03  
**Purpose:** Track repository onboarding to the factory cybersecurity baseline. Re-check live GitHub status before release decisions.

## Integrated repositories

| Repository | Integration | Current scope / limitation |
|---|---|---|
| `avtoy-korea-auto` | Merged PR #55 | Gitleaks and CodeQL JavaScript/TypeScript configured. Confirm a fresh post-merge run before calling it passed. |
| `Gemeni` | Merged PR #48 and PR #50 | Gitleaks baseline, Sherpa-ONNX Android dependency, Piper API alignment, Kotlin CodeQL and full debug APK build. Emulator smoke tests are being added separately in PR #51. |
| `voice-assistant` | Merged PR #13 and PR #14 | Gitleaks and CodeQL Java/Kotlin passed in PR checks; PR #14 merged on 2026-11-02. |
| `happ-proxy-pool` | Merged PR #2 | Gitleaks and CodeQL Python configured. |
| `russ-translation-models` | Merged PR #1 | Gitleaks and JSON manifest validation configured. CodeQL is not currently configured. |
| `RussSearchOPPO` | Merged PR #1 and PR #2 | Gitleaks, Kotlin CodeQL, Android APK build and Hive preflight are configured. |

## Verified Android project outcomes (2026-11-02)

### `RussSearchOPPO`

- PR [#2](https://github.com/sokfrut-tech/RussSearchOPPO/pull/2) merged as commit `350c68f67d8b306b610f85e5c7784f07b48fb58e`.
- PR-head checks passed: Factory Security Baseline run [41525177318](https://github.com/sokfrut-tech/RussSearchOPPO/actions/runs/41525177318), APK build [41525177238](https://github.com/sokfrut-tech/RussSearchOPPO/actions/runs/41525177238), Hive preflight [41525177211](https://github.com/sokfrut-tech/RussSearchOPPO/actions/runs/41525177211).
- Post-merge main checks also passed: CodeQL/Gitleaks [41526516615](https://github.com/sokfrut-tech/RussSearchOPPO/actions/runs/41526516615), APK [41526517066](https://github.com/sokfrut-tech/RussSearchOPPO/actions/runs/41526517066), Hive preflight [41526516494](https://github.com/sokfrut-tech/RussSearchOPPO/actions/runs/41526516494), Hive diagnostic [41526516755](https://github.com/sokfrut-tech/RussSearchOPPO/actions/runs/41526516755).
- CodeQL SARIF was archived as an Actions artifact and inspected: 0 findings. This private repository cannot upload to GitHub Code Scanning without GitHub Advanced Security; artifact-only SARIF is not Security-tab integration.

### `Gemeni` / Jarvis

- PR [#50](https://github.com/sokfrut-tech/Gemeni/pull/50) merged as commit `992b438415020d9aa9af44360e44f30f7e7c22c7`.
- Added Sherpa-ONNX Android AAR v1.13.8, corrected Piper TTS config for that API, and excluded the duplicate transitive JVM module using its exact group `com.github.k2-fsa.sherpa-onnx`.
- Final PR-head run [41527715049](https://github.com/sokfrut-tech/Gemeni/actions/runs/41527715049) passed: Gitleaks, Kotlin compilation, full `:app:assembleDebug`, APK verification/upload, and CodeQL. Archived CodeQL SARIF was inspected: 0 findings.
- APK artifact: `jarvis-debug-apk-1f81491506a1832d1a9476081cdb9b0886281b96`, 104,509,798 bytes compressed artifact; extracted APK 146,803,901 bytes; SHA-256 `41493119449266a6817438572ddaed800f4caae3791ccdd4edd56a9bc49dd4e1`.
- APK contains Sherpa JNI libraries for `arm64-v8a`, `armeabi-v7a`, `x86`, and `x86_64`.
- Post-merge Factory Security Baseline run [41528783083](https://github.com/sokfrut-tech/Gemeni/actions/runs/41528783083) and Build Jarvis run [41528782915](https://github.com/sokfrut-tech/Gemeni/actions/runs/41528782915) were triggered on main; check live status before release.

## Jarvis runtime gate and factory evidence

- Post-merge Jarvis Director / agent review run [41528782937](https://github.com/sokfrut-tech/Gemeni/actions/runs/41528782937) completed the director intake and specialist checks for QA, Android/ColorOS, UI/UX, research, security, NDK/GLES, functional and speech.
- The deterministic factory release gate returned **REQUIRES_RUNTIME_EVIDENCE**. It explicitly requires emulator runtime tests, real tool side effects, speech pipeline tests, VoiceInteraction invocation, and OPPO/ColorOS device validation.
- The agent review artifacts state that LLMs were not configured; specialist outputs are deterministic evidence only. Do not represent them as independent LLM reviews.
- PR [#51](https://github.com/sokfrut-tech/Gemeni/pull/51) adds Android API 35 emulator instrumentation for launcher UI, microphone permission/runtime state and accessibility settings. Its CI run is in progress. Emulator success still does not prove real OPPO/ColorOS behavior.

| `Antigravity-Mobile` | Security tooling PR [#7](https://github.com/sokfrut-tech/Antigravity-Mobile/pull/7) opened 2026-11-03. | **IN PROGRESS**: adds Gitleaks, Semgrep, Trivy and Kotlin CodeQL as a reusable gate wired into the existing APK PR workflow. Checks are pending; do not merge or mark PASS until the first PR run completes and findings are triaged. ZAP/Nuclei and desktop/runtime tools remain authorized-lab-only. |

## Not onboarded

- `breeno-apks` — empty repository at last inventory; no workflow can be integrated until project files exist.
- `sleep-button` — empty repository at last inventory; no workflow can be integrated until project files exist.

## Mandatory bootstrap for every new project

1. Start with [PROJECT_SECURITY_BOOTSTRAP.md](PROJECT_SECURITY_BOOTSTRAP.md).
2. Reference [CYBERSECURITY_SKILLS_FACTORY_STANDARD.md](CYBERSECURITY_SKILLS_FACTORY_STANDARD.md) from the repository's `AGENTS.md` or equivalent.
3. Classify the actual stack before selecting scanners. Do not apply Android/Gradle jobs to unrelated projects.
4. Add secret scanning, stack-appropriate dependency audit, static analysis, least-privilege workflow permissions, project-specific regression tests, artifact SHA-256, and weekly scans where applicable.
5. For CodeQL, use a real build for compiled languages such as Kotlin. Do not use `build-mode: none` for Kotlin.
6. When Code Scanning upload is unavailable, preserve generated SARIF as an Actions artifact and label the limitation explicitly. Private repositories generally require GitHub Advanced Security for Security-tab upload.
7. Open a focused PR per repository. Inspect logs and artifacts; do not weaken existing checks to obtain a green result.
8. Merge only after required checks pass. Verify post-merge runs and record exact commit SHA and run links here.
9. Label checks as PASS, FAIL, IN PROGRESS, NOT CONFIGURED, or NOT APPLICABLE. A workflow file existing is not proof that a scanner passed.

## Evidence policy

A configured workflow is not evidence of a successful scan. A successful CI scan is not proof of production runtime security. Record the tested commit, run ID, scanner result, unresolved findings, and runtime tests separately.
