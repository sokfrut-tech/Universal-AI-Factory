# Factory Security Rollout Ledger

**Updated:** 2026-11-02  
**Purpose:** Track repository onboarding to the factory cybersecurity baseline. Re-check live GitHub status before release decisions.

## Integrated repositories

| Repository | Integration | Current scope / limitation |
|---|---|---|
| `avtoy-korea-auto` | Merged PR #55 | Gitleaks and CodeQL JavaScript/TypeScript configured. Confirm a fresh post-merge run before calling it passed. |
| `Gemeni` | Merged PR #48; CodeQL and build follow-up in PR #50 | Gitleaks baseline merged. PR #50 adds Sherpa-ONNX Android dependency, CodeQL Java/Kotlin and APK build validation. |
| `voice-assistant` | Merged PR #13 and PR #14 | Gitleaks and CodeQL Java/Kotlin passed in PR checks; PR #14 merged on 2026-11-02. |
| `happ-proxy-pool` | Merged PR #2 | Gitleaks and CodeQL Python configured. |
| `russ-translation-models` | Merged PR #1 | Gitleaks and JSON manifest validation configured. CodeQL is not currently configured. |
| `RussSearchOPPO` | Merged PR #1; CodeQL follow-up in PR #2 | Gitleaks baseline merged. PR #2 adds manual Kotlin CodeQL extraction and Android APK validation. |

## Open security and build follow-ups (2026-11-02)

| Repository | PR | Change | Latest observed status |
|---|---:|---|---|
| `RussSearchOPPO` | [#2](https://github.com/sokfrut-tech/RussSearchOPPO/pull/2) | CodeQL Java/Kotlin with explicit JDK 17, Gradle 8.9, Android SDK and manual Kotlin build; archive SARIF as artifact | Latest run for head `4ed5954c69113517810f85e5c7784f07b48fb58e`: Gitleaks PASS, CodeQL PASS, SARIF archived (0 findings), Android debug APK build and artifact upload PASS, Hive preflight PASS. Code scanning upload is unavailable because this is a private repository without GitHub Advanced Security; do not describe artifact-only SARIF as GitHub Security-tab integration. |
| `Gemeni` | [#50](https://github.com/sokfrut-tech/Gemeni/pull/50) | Add official Sherpa-ONNX Android AAR v1.13.8, align Piper TTS config with its Kotlin API, run CodeQL Java/Kotlin and build APK | Head `a96aeded99df44860be8f9ba8075ab2d8750a427`: Gitleaks PASS; Kotlin compile PASS; CodeQL PASS; SARIF archived (0 findings). Latest run `41525882355` additionally builds full debug APK and is IN PROGRESS. |
| `voice-assistant` | [#14](https://github.com/sokfrut-tech/voice-assistant/pull/14) | Add CodeQL Java/Kotlin without Gradle autobuild | Gitleaks and CodeQL passed; existing Security workflow passed; PR #14 merged. |

Do not merge open follow-up PRs until their latest-head checks finish successfully and the diff is reviewed.

## Not onboarded

- `breeno-apks` — empty repository at last inventory; no workflow can be integrated until project files exist.
- `sleep-button` — empty repository at last inventory; no workflow can be integrated until project files exist.

## Mandatory bootstrap for every new project

1. Start with [PROJECT_SECURITY_BOOTSTRAP.md](PROJECT_SECURITY_BOOTSTRAP.md).
2. Reference [CYBERSECURITY_SKILLS_FACTORY_STANDARD.md](CYBERSECURITY_SKILLS_FACTORY_STANDARD.md) from the repository's `AGENTS.md` or equivalent.
3. Classify the actual stack before selecting scanners. Do not apply Android/Gradle jobs to unrelated projects.
4. Add secret scanning, stack-appropriate dependency audit, static analysis, least-privilege workflow permissions, project-specific regression tests, artifact SHA-256, and weekly scans where applicable.
5. For CodeQL, use a real build for compiled languages such as Kotlin. Do not use `build-mode: none` for Kotlin.
6. When Code Scanning upload is unavailable, preserve the generated SARIF as an Actions artifact and label the limitation explicitly. Private repositories generally require GitHub Advanced Security for the Security-tab upload.
7. Open a focused PR per repository. Inspect logs and artifacts; do not weaken existing checks to obtain a green result.
8. Merge only after required checks pass. Verify the post-merge run and record exact commit SHA and run links here.
9. Label checks as PASS, FAIL, IN PROGRESS, NOT CONFIGURED, or NOT APPLICABLE. A workflow file existing is not proof that a scanner passed.

## Evidence policy

A configured workflow is not evidence of a successful scan. A successful CI scan is not proof of production runtime security. Record the tested commit, run ID, scanner result, unresolved findings, and runtime tests separately.
