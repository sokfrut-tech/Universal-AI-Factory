# Antigravity Mobile — preliminary factory security self-review

- Автор: ChatGPT (self-review; not an independent external agent)
- Кому: Universal AI Factory / project security ledger
- Дата/время UTC: 2026-11-03 18:38Z
- Проект: sokfrut-tech/Antigravity-Mobile
- Статус: partial — automated scans in progress; independent Claude/Gemini reports not received
- Приоритет: critical
- Correlation ID: ANTIGRAVITY-MOBILE-SECURITY-2026-11-03
- Проверяемый baseline: main commit `11ded12a0a0b8d2ebd4f0adeb62601d4558e1c31`
- Security instrumentation PR: #4, branch `security/factory-baseline-2026-11-03`, current head `29e873d7a71079b266d649da891db531a05b0bfb`
- PR: https://github.com/sokfrut-tech/Antigravity-Mobile/pull/4

## 1. Что проверено непосредственно

### Android client
- `app/src/main/AndroidManifest.xml`: only INTERNET permission; `allowBackup=false`; launcher activity explicitly exported. No WebView, deep-link or broad storage permissions observed in manifest.
- `SecureTokenStore.kt`: AES/GCM/NoPadding, 12-byte IV from provider, 128-bit tag, randomized encryption, key held in AndroidKeyStore; bearer token is encrypted before SharedPreferences persistence. This is positive source evidence, not device/Keystore runtime validation.
- `FactoryApiClient.kt`: validates HTTPS URL and does not intentionally log bearer token. Runtime redirect behavior and real device behavior were not tested.
- `app/build.gradle.kts`: minSdk 24, target/compile SDK 35. Explicit versions are present; no Gradle wrapper or dependency lock/verification metadata found in tree.

### Worker/API
- `factory-api/src/index.js`: bearer token compared as SHA-256 digest; constant-time character comparison; parameterized SQL; task, detail and event reads are scoped by user_id; request body has streaming 256 KB cap; JSON UTF-8 decoding is fatal; exact-origin CORS rejects wildcard; responses use no-store/nosniff/referrer-policy; provider execution returns 503 and is not active.
- `factory-api/migrations/0001_initial.sql`: task and event user_id fields/indexes and basic SQL CHECK constraints exist.
- `factory-api/README.md` explicitly describes a single-owner bootstrap and says Cloudflare rate limiting must be configured before public exposure.
- Worker is not deployed; no production requests or Cloudflare configuration inspection were performed.

## 2. Preliminary findings

### HIGH — no rate limiting is implemented or deployment-gated
- Location: `factory-api/src/index.js` request routing/authentication; `.github/workflows/deploy-factory-api.yml` deploy sequence; `factory-api/README.md` security model.
- Evidence: no rate-limit binding or application-level throttling in Worker; deploy workflow proceeds from tests/migration/secret setup to deploy and does not verify a Cloudflare rate-limiting rule.
- Impact: if the authenticated endpoint is exposed publicly, a leaked/shared bearer token or abusive client can generate unbounded authenticated requests, causing D1 cost/availability pressure. The API README itself says rate limiting is required before exposure.
- Verdict: release BLOCK until a scoped Cloudflare rate-limit control is configured and verified, or an equivalent tested control is added. Do not deploy yet.

### MEDIUM — single shared owner token is not multi-user authorization
- Location: `factory-api/src/index.js:52` and `factory-api/README.md`.
- Evidence: every valid bearer token maps to literal principal `owner`.
- Impact: all clients possessing the token share one task namespace; no per-user identity or revocation boundary. This is acceptable only for a tightly controlled single-owner pilot and must not be presented as multi-user support.
- Remediation: keep single-owner scope explicit; before inviting users, implement per-user OAuth/OIDC/JWT identity, tenant mapping, per-user token lifecycle and cross-tenant tests.

### MEDIUM — list endpoint does not implement documented cursor pagination
- Location: `factory-api/src/index.js:179-193`; contract `contracts/openapi.yaml` describes cursor and nextCursor.
- Evidence: handler ignores cursor and always returns `nextCursor: null`.
- Impact: not currently a direct confidentiality flaw, but API contract and scalability expectations are not met. It can cause clients to believe all records have been returned.
- Remediation: implement stable cursor ordering and cursor validation, or revise contract and document bounded list behavior.

### MEDIUM — dependency audit is not reproducible yet
- Location: `factory-api/package.json`, `factory-api-check.yml`, repository dependency files.
- Evidence: no committed `package-lock.json` and no Gradle wrapper/lock verification metadata. Existing API CI uses `npm install`, resolving ranges on each run.
- Impact: transitive dependency versions may drift between builds; historical build provenance is weaker.
- Remediation: commit package-lock.json and use npm ci; add Gradle dependency locking/verification metadata or otherwise pin and record the resolved graph.

### LOW — idempotency key is not bound to request payload
- Location: `factory-api/src/index.js` createTask handler.
- Evidence: an existing key for the same user returns the original task even if a later request supplies a different payload.
- Impact: retries are safe for the current Android client's fingerprinted key, but arbitrary clients can accidentally reuse a key for a different task and receive the prior task without a conflict.
- Remediation: store a canonical request hash with the key and return 409 when the same key is reused with a different payload.

## 3. Workflow and supply-chain review
- Existing Android/API workflows use read-only permissions for PR build/test jobs; no Cloudflare deployment secrets are referenced by those PR jobs.
- Deployment workflow is workflow_dispatch-only and validates presence/format of required secret values without printing them. No deploy was triggered.
- Existing workflows use version tags (e.g. checkout@v4/setup-java@v4), not immutable SHAs. New PR #4 pins the actions it adds to immutable SHAs.
- API CI uses `npm install`; no committed lockfile found.
- No secret scan, CodeQL, dependency vulnerability lane was present in main before PR #4.

## 4. Security baseline added for review
PR #4 adds:
- Gitleaks full-history scan (SARIF artifact);
- CodeQL Java/Kotlin with manual Gradle build and JavaScript/TypeScript analysis, SARIF artifact-only;
- npm audit of resolved Worker dependencies and Android Gradle dependency graph resolution;
- weekly Dependabot for Gradle, npm and GitHub Actions;
- root AGENTS.md referencing factory security/exchange standards.
All newly added GitHub Actions are SHA-pinned; permissions are read-only; no deploy secrets are used.

Initial workflow run `41695425276` exposed an incorrect Gitleaks CLI flag (tool usage error, NOT a leak finding). The flag was corrected in commit `29e873d7a71079b266d649da891db531a05b0bfb`; fresh PR run `41695570348` was pending at report time. Do not count the failed first invocation as a completed scan.
- Initial dependency audit job on run `41695425276` completed successfully; npm audit and Gradle dependency graph resolution steps were green.
- CodeQL jobs on run `41695425276` were still running at report time.
- No SARIF result has yet been inspected; no scanner PASS is claimed.

## 5. Not checked / blocked
- No real Android device or emulator installation/launch, Keystore invalidation/recovery, network interception or API 24 device validation.
- No live Cloudflare D1, Worker, TLS, WAF, rate-limit rule, secrets, domain or production configuration.
- No external provider dispatch; intentionally disabled.
- No CodeQL findings report or successful Gitleaks scan result yet.
- No complete Gradle CVE advisory scan or reproducible dependency lockfile.
- No independent substantive Claude or Gemini audit report. Claude dispatcher produced only an automatic receipt explicitly stating execution is not confirmed. Gemini outbox has no report for this correlation ID.

## 6. Preliminary decision
**BLOCK for public deployment / release.** The Worker is not deployed, rate limiting is not evidenced, and the new secret/CodeQL scan jobs have not all completed. This is a preliminary self-review, not a final factory security PASS. Reassess after fresh PR #4 checks, SARIF inspection, and substantive independent reviewer reports.

## 7. Fresh scan evidence (2026-11-03 18:40Z)

On PR #4 head `a9a36718066517365c0ba84d690a741a3d1b4cae`, workflow run [41695960923](https://github.com/sokfrut-tech/Antigravity-Mobile/actions/runs/41695960923):

- **Gitleaks v8.24.2: PASS, 0 findings** in the generated SARIF (0 results). The full-history scan and SARIF artifact upload both succeeded. Artifact ID: `13262505451`; artifact digest: `sha256:cb26ef71196396431a48bc63f0d46379a73ff20daf2f27478d522a245ef46444`.
- **npm audit: PASS at high severity threshold, 0 vulnerabilities reported** for the Worker dependency resolution generated during this run. This does not substitute for a committed lockfile.
- **Gradle dependency graph: PASS** — `:app:dependencies --configuration debugRuntimeClasspath` completed successfully. This is dependency resolution/inventory, not a full Gradle CVE audit.
- **CodeQL JavaScript/TypeScript and Java/Kotlin: IN PROGRESS** at time of this update. SARIF export artifact-path handling was corrected in PR head `a9a367...`; await the fresh run's artifacts and inspect finding counts before claiming PASS.
- The earlier run `41695425276` was cancelled after the first Gitleaks invocation failed due to an unsupported CLI flag. That was a workflow invocation defect, not evidence of a detected secret. The corrected run above succeeded.

No secret values were emitted in the report or logs reviewed.
