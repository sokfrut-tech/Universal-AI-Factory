# Factory Security Rollout Ledger

**Updated:** 2026-11-02  
**Purpose:** Track repository onboarding to the factory cybersecurity baseline. Re-check live GitHub status before release decisions.

## Integrated repositories

| Repository | Integration | Current scope / limitation |
|---|---|---|
| `avtoy-korea-auto` | Merged PR #55 | Gitleaks and CodeQL JavaScript/TypeScript configured. Initial CodeQL run failed on Actions API permission; `actions: read` was added. Confirm a fresh post-merge run before calling it passed. |
| `Gemeni` | Merged PR #48 | Gitleaks baseline merged. CodeQL Java/Kotlin is being added separately in PR #50. |
| `voice-assistant` | Merged PR #13 | Gitleaks baseline merged. CodeQL Java/Kotlin is being added separately in PR #14. |
| `happ-proxy-pool` | Merged PR #2 | Gitleaks and CodeQL Python configured. |
| `russ-translation-models` | Merged PR #1 | Gitleaks and JSON manifest validation configured. CodeQL is not currently configured. |
| `RussSearchOPPO` | Merged PR #1 | Gitleaks baseline merged. CodeQL Java/Kotlin is being added separately in PR #2. |

## Open security follow-ups (2026-11-02)

| Repository | PR | Change | Latest observed status |
|---|---:|---|---|
| `RussSearchOPPO` | [#2](https://github.com/sokfrut-tech/RussSearchOPPO/pull/2) | CodeQL Java/Kotlin with `build-mode: none`, avoiding Gradle autobuild incompatibility | Gitleaks passed; CodeQL in progress; Android APK build passed; Hive preflight passed. |
| `Gemeni` | [#50](https://github.com/sokfrut-tech/Gemeni/pull/50) | Add CodeQL Java/Kotlin without Gradle autobuild | Gitleaks passed; CodeQL in progress. |
| `voice-assistant` | [#14](https://github.com/sokfrut-tech/voice-assistant/pull/14) | Add CodeQL Java/Kotlin without Gradle autobuild | Gitleaks passed; CodeQL in progress; existing Security workflow in progress at last check. |

Do not merge these follow-up PRs until their required checks finish successfully and the diff is reviewed.

## Not onboarded

- `breeno-apks` — empty repository at last inventory; no workflow can be integrated until project files exist.
- `sleep-button` — empty repository at last inventory; no workflow can be integrated until project files exist.

## Mandatory bootstrap for every new project

1. Start with [PROJECT_SECURITY_BOOTSTRAP.md](PROJECT_SECURITY_BOOTSTRAP.md).
2. Reference [CYBERSECURITY_SKILLS_FACTORY_STANDARD.md](CYBERSECURITY_SKILLS_FACTORY_STANDARD.md) from the repository's `AGENTS.md` or equivalent.
3. Classify the actual stack before selecting scanners. Do not apply Android/Gradle jobs to unrelated projects.
4. Add secret scanning, stack-appropriate dependency audit, static analysis, least-privilege workflow permissions, project-specific regression tests, artifact SHA-256, and weekly scans where applicable.
5. Open a focused PR per repository. Inspect logs and artifacts; do not weaken existing checks to obtain a green result.
6. Merge only after required checks pass. Verify the post-merge run and record exact commit SHA and run links here.
7. Label checks as PASS, FAIL, IN PROGRESS, NOT CONFIGURED, or NOT APPLICABLE. A workflow file existing is not proof that a scanner passed.

## Evidence policy

A configured workflow is not evidence of a successful scan. A successful CI scan is not proof of production runtime security. Record the tested commit, run ID, scanner result, unresolved findings, and runtime tests separately.
