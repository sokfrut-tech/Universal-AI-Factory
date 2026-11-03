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

| `Antigravity-Mobile` | Security audit requested from Claude and Gemini on 2026-11-03 (correlation `ANTIGRAVITY-MOBILE-SECURITY-2026-11-03`) after PR #3 merged. | **IN PROGRESS**: no project-specific Gitleaks/CodeQL/dependency security lane confirmed yet; Worker not deployed; await substantive agent reports and deterministic scans before PASS/release. |


## Factory-wide toolchain rollout (2026-11-03)

- Added shared reusable CI workflow: `.github/workflows/factory-security-reusable.yml` (Semgrep SAST + Trivy filesystem/dependency/misconfiguration/secret checks; SARIF artifacts).
- Added reusable authorized DAST workflow: `.github/workflows/factory-dast-reusable.yml` (OWASP ZAP passive baseline, Wapiti and Nuclei; HTTPS-only, exact-host allowlist, explicit authorization phrase, security-lab environment).
- Added `docs/SECURITY_TOOLCHAIN_CATALOG.md` and `docs/SECURITY_LAB_RUNBOOK.md` mapping all screenshot tools to CI or isolated lab roles.
- Updated the factory security standard and new-project bootstrap to require the shared toolchain.
- Desktop lab tools (Wireshark, Sysmon, System Informer / legacy Process Hacker, Ghidra, IDA Free, Binary Ninja) are documented as **NOT CONFIGURED / NOT RUN** until a dedicated analyst VM is provisioned and versioned evidence is attached.
- Reusable workflows are not a PASS by themselves. Each project must call the reusable static workflow, execute it on a PR, triage findings and record the run.


## Factory-wide security toolchain implementation (2026-11-03)

- PR [#10](https://github.com/sokfrut-tech/Universal-AI-Factory/pull/10) adds the canonical catalog, lab runbook, reusable Semgrep + Trivy workflow, authorized DAST workflow, updated baseline/bootstrap, and a security workflow for the factory repository itself.
- Shared CI workflow is pinned by callers to immutable commit revisions. Trivy action was corrected to a verified immutable release commit after the first run exposed that the old 0.28.0 reference was not resolvable.
- Semgrep gate and SARIF export are separate steps because the current Semgrep SARIF path can report nosemgrep-suppressed findings. The gate is the exit-code source; SARIF is an evidence artifact.
- DAST is manual only. It requires HTTPS, exact hostname allowlisting via SECURITY_ALLOWED_HOSTS, the explicit authorization confirmation, and a reviewed security-lab GitHub environment. No production or third-party scan has been launched.
- Desktop tools remain NOT CONFIGURED / NOT RUN until a dedicated isolated analyst VM is provisioned: Wireshark, Sysmon, System Informer (legacy Process Hacker), Ghidra, IDA Free and Binary Ninja.

### Project onboarding PRs

| Repository | PR | First observed result / follow-up |
|---|---:|---|
| avtoy-korea-auto | [#57](https://github.com/sokfrut-tech/avtoy-korea-auto/pull/57) | Initial Gitleaks and Trivy passed; Semgrep identified 18 mutable GitHub Action references. All identified action references were pinned to immutable commits; latest rerun queued. |
| RussSearchOPPO | [#3](https://github.com/sokfrut-tech/RussSearchOPPO/pull/3) | Initial Gitleaks, CodeQL and Trivy passed; Semgrep identified 25 mutable action references plus the expected launcher activity export. Actions pinned and launcher finding annotated; latest rerun in progress. |
| voice-assistant | [#15](https://github.com/sokfrut-tech/voice-assistant/pull/15) | Initial Gitleaks and Trivy passed; Semgrep identified 13 mutable action references, missing Dependabot cooldowns and launcher activity export. Actions pinned, 7-day cooldown added and launcher finding annotated; latest rerun queued. |
| Gemeni | [#53](https://github.com/sokfrut-tech/Gemeni/pull/53) | Initial Gitleaks and Trivy passed; Semgrep identified 43 mutable action references, six dynamic urllib endpoint uses, one privileged workflow_run checkout of incoming code, and the launcher activity. Actions pinned; privileged workflow_run now checks out trusted default-branch code only, drops contents write and does not push from the privileged job. Dynamic endpoint findings remain for review. |
| russ-translation-models | [#2](https://github.com/sokfrut-tech/russ-translation-models/pull/2) | Gitleaks, Trivy and JSON manifest validation passed; Semgrep identified three mutable action references. They were pinned; latest rerun queued. |
| happ-proxy-pool | [#3](https://github.com/sokfrut-tech/happ-proxy-pool/pull/3) | Initial Gitleaks and Trivy passed; Semgrep identified seven mutable action references and one dynamic urllib URL use. Action references pinned; dynamic URL finding remains for review. |
| Antigravity-Mobile | [#7](https://github.com/sokfrut-tech/Antigravity-Mobile/pull/7) | APK build, Factory API checks, Gitleaks, CodeQL and Trivy passed. Semgrep's two remaining results are launcher activity export and AES-GCM nonce detection; both are annotated with the actual invariants (launcher-only entry point; Android Keystore randomized IV). Latest rerun queued. |

**Important:** project PRs are not merged. The findings above are the first-run evidence, not a claim that all follow-up scans have passed. Merge only after the latest run is green or each remaining finding has a documented, owner-approved disposition. Do not count an annotated finding as fixed until the fresh scan confirms suppression.


### Latest verified CI outcomes (2026-11-03)

| Repository / PR | Run evidence | Current interpretation |
|---|---|---|
| Universal-AI-Factory / #10 | [41705928259](https://github.com/sokfrut-tech/Universal-AI-Factory/actions/runs/41705928259) | Gitleaks, Semgrep and Trivy passed on the central factory PR after pinning workflow actions and fixing shell-input interpolation. |
| avtoy-korea-auto / #57 | [41706682505](https://github.com/sokfrut-tech/avtoy-korea-auto/actions/runs/41706682505) | Gitleaks, Semgrep and Trivy passed; CodeQL is still running with local SARIF artifact output because GitHub Code Scanning is disabled for this repository. Worker tests and factory review passed; PR-triggered deploy workflow did not satisfy its main-branch deployment condition. |
| RussSearchOPPO / #3 | [41705538426](https://github.com/sokfrut-tech/RussSearchOPPO/actions/runs/41705538426), APK [41705537382](https://github.com/sokfrut-tech/RussSearchOPPO/actions/runs/41705537382), Hive [41705537360](https://github.com/sokfrut-tech/RussSearchOPPO/actions/runs/41705537360) | Gitleaks, Semgrep, Trivy and CodeQL passed; APK build and Hive preflight passed. |
| voice-assistant / #15 | Security [41706345495](https://github.com/sokfrut-tech/voice-assistant/actions/runs/41706345495), CodeQL [41706345071](https://github.com/sokfrut-tech/voice-assistant/actions/runs/41706345071) | Gitleaks, Semgrep, Trivy and Java CodeQL passed after changing the analysis build target from a nonexistent Kotlin task to the actual Java compile task. |
| Gemeni / #53 | [41706798734](https://github.com/sokfrut-tech/Gemeni/actions/runs/41706798734) | Fresh run in progress after pinning actions, removing the privileged workflow_run PR checkout, and validating configured HTTP(S) model endpoints. Do not mark PASS until this run finishes. |
| russ-translation-models / #2 | [41705581385](https://github.com/sokfrut-tech/russ-translation-models/actions/runs/41705581385) | Gitleaks, Semgrep, Trivy and model manifest validation passed. CodeQL is NOT APPLICABLE to this data-only repository at present. |
| happ-proxy-pool / #3 | [41706803823](https://github.com/sokfrut-tech/happ-proxy-pool/actions/runs/41706803823) | Gitleaks, Semgrep, Trivy and Python CodeQL passed after validating the fixed HTTPS source allowlist. |
| Antigravity-Mobile / #7 | Security [41706087791](https://github.com/sokfrut-tech/Antigravity-Mobile/actions/runs/41706087791), APK [41706087577](https://github.com/sokfrut-tech/Antigravity-Mobile/actions/runs/41706087577), API [41706087472](https://github.com/sokfrut-tech/Antigravity-Mobile/actions/runs/41706087472) | Gitleaks, Semgrep, Trivy, Kotlin/Java CodeQL, APK build and Factory API checks passed. |

All project PRs remain open and unmerged. Passing checks above apply to the exact PR commits/runs shown; later commits require fresh runs. Desktop lab tools and DAST remain NOT RUN until a lab host, approved staging host allowlist and environment reviewers are configured.

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
