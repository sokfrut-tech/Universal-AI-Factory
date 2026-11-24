# Active Pull Request CI Snapshot — 2026-11-24

Source: GitHub REST PR and check-runs APIs, checked 2026-11-24. This is a point-in-time snapshot; recheck before making decisions.

## Passing checks observed
- Gemeni PR #148: secret scanning, CodeQL and build succeeded.
- OGAM PR #7: isolated M2 OP-SQLite ARM64 APK build, import/workspace scan, focused M1+M2 TypeScript/Jest/SQLite integration succeeded.
- OGAM PR #6: isolated OP-SQLite ARM64 APK build and import/workspace scan succeeded.
- Antigravity Mobile PR #19: CodeQL, Trivy, Semgrep, Gitleaks, Compose UI tests, debug APK build and unit tests succeeded.
- StampCleaner PR #3: Android check succeeded.

## Failed checks observed — do not merge
- AVTOY KOREA PR #78: CodeQL, secret scan, worker tests, deploy, check, director/release evidence, functional/regression and security/privacy checks all reported failure.
- AVTOY KOREA PR #81: secret scan, CodeQL and two validate checks reported failure.
- Antigravity Mobile PR #20: Factory API checks workflow failed at `npm test`; build and Compose UI tests succeeded; D1 migrations and Wrangler deploy dry-run were skipped.
- RussSearchOPPO PR #15: no check runs returned and API reported mergeable=false.

## Important diagnostic limitation
For AVTOY PR #78 and #81, the Actions job API returned jobs with empty step lists and runner_id=0. The observed failed conclusions are real API data, but the underlying failure cause is not available from those job records. Do not invent a root cause. Retrieve run logs or reproduce in a controlled branch before fixing.

## Interpretation
- A successful APK build/test is not proof of a successful install or launch on the user's OPPO device.
- A successful Android UI test does not prove Factory API deployment/provider execution.
- Any required failing security or functional check blocks merge/deployment until diagnosed and fixed.
