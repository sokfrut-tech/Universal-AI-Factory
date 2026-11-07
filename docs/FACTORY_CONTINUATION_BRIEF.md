# Universal AI Factory — Continuation Brief
Updated: 2026-11-06

## Mission
A reusable, secure and economical development factory coordinating AI agents and producing Android/PC apps, websites, automation, design/media assets, tests and security evidence. GitHub must preserve project state so another assistant can resume.

## User constraints
- User works mainly from Android; avoid asking them to inspect logs or copy large code blocks.
- Give exact short phone steps only when user action is essential.
- Ask before spending money, exposing services/data, destructive actions or production-impacting changes.
- No Google Play publishing unless separately requested.
- Prefer free/local tools and disclose capability limits.

## Agent policy
Canonical policy: coordination/AI_AGENT_USAGE_POLICY.md.
- ChatGPT coordinates and implements by default through available repository tools.
- Gemini is a limited escalation expert for material blockers, architecture uncertainty or independent high-risk review.
- Claude API is optional; absent key must not stop other tasks.
- No automatic Gemini invocation on ordinary inbox pushes. Explicit dispatch/manual run only.
- Keep retries low. Never describe a plan-only response as a code change.

## Coordination contract
- Separate Claude and Gemini inbox/outbox under coordination/.
- Every task states target repo, branch/base, scope, acceptance criteria, supplied context, test commands and expected artifact.
- Responses must contain substantive findings or patch evidence; empty ACK is invalid.
- Dispatcher must discover both agent folders.
- Never put secrets in task files/logs. Track task ID, request, response, PR, commit and tests.

## P0 — trustworthy execution
1. Inspect .github/workflows/real-ai-agent-execution.yml and inbox dispatcher against the canonical policy.
2. Verify Gemini triggers only from explicit dispatch/manual invocation, not routine inbox pushes.
3. Verify missing Claude key does not fail independent jobs.
4. Audit retry limits, timeouts, API errors and redacted logs.
5. Confirm whether runner checks out target repository and supplies source. If not, label its output review/plan only.
6. Add workflow lint, secret scanning, least-privilege and deploy-gate checks.

## P1 — reusable capabilities
- Templates for Android, web/Worker, desktop and automation projects.
- Build/test/release pipelines with artifact links and truthful progress.
- Security gates: secret scan, dependency audit, static checks and permission review.
- Agent task ledger, run evidence, cost/retry limits and resumable state.
- Visual asset handoff folder with naming/provenance.
- Cloudflare integration using repository secrets only; never print secret values.
- Optional image/video/audio tools only where cost, licensing and availability are clear.

## P2 — Antigravity control surface
Coordinate with sokfrut-tech/Antigravity-Mobile. It must display real task/run state and use authenticated scoped API endpoints, not fake progress or decorative Kanban.

## Security/release rules
Least privilege; secrets never in source/logs; production deploy only after required checks; no auto-merge based solely on agent claims. Preserve audit trail: change, commit, tests, workflow run, artifact and deployment result.

## Immediate resume checklist
- [ ] Read current workflows and dispatcher.
- [ ] Inspect latest Actions runs/logs; separate historic failures from current behavior.
- [ ] Verify policy changes referenced by commits fad0b0f, 42ac394 and 14b45f2 are on default branch.
- [ ] Check any still-running Gemini job; do not launch routine calls.
- [ ] Document target-repository checkout limitation, if still present.
- [ ] Complete one real end-to-end task with patch, tests and artifact before scaling.


## 2026-11-07 — фабричный dispatch audit (continuation)

### Confirmed current state
- `.github/workflows/inbox-dispatcher.yml` watches Claude/Gemini/ChatGPT inboxes and writes a **non-authoritative receipt only**. It does not call Claude or Gemini.
- `.github/workflows/real-ai-agent-execution.yml` is the substantive Gemini API execution path. It watches `coordination/gemini/dispatch/*.md` on main and supports manual `workflow_dispatch` with exact `task_file` input. It calls Gemini Developer API and writes a substantive report to `coordination/gemini/outbox/`.
- A second workflow, `.github/workflows/gemini-direct-api.yml`, also watched the same Gemini dispatch path and independently called the Gemini API. This created duplicate calls/reports and potential duplicate cost.
- Claude inbox currently has no verified automatic Claude API execution workflow in the inspected paths. Receipt is not proof of Claude execution. Do not claim live Claude dispatch until a real provider run/report is observed.
- Existing Gemini reports in outbox prove that direct Gemini API calls have succeeded in earlier runs, but they do not prove that every current inbox message is automatically delivered or reviewed.

### Change prepared in PR
- Branch: `fix/single-gemini-dispatch-2026-11-07`
- Commit: `fd1df977e035e94b9bae797251133680b5c70fab`
- Change: remove obsolete duplicate `.github/workflows/gemini-direct-api.yml`; retain `.github/workflows/real-ai-agent-execution.yml` as the single Gemini execution path.
- PR must be reviewed and CI checked before merge. No merge performed by this work.

### Safe dispatch protocol after the duplicate-workflow fix is merged
1. Confirm only one active workflow listens to `coordination/gemini/dispatch/*.md`.
2. Check task filename has no existing matching report, and check latest Actions run for same task to prevent duplicate invocation.
3. Add exactly one self-contained Markdown task file under `coordination/gemini/dispatch/` on main. This push is an explicit Gemini API invocation and may incur API quota/cost.
4. Verify one workflow run, model, successful API response, non-empty report, commit SHA and report contents. Do not accept an ACK as a report.
5. If failure, inspect run/log and correct the cause before retrying; no blind repeated dispatch.
6. For Claude, use only an actual connected Claude API/agent workflow. If no provider key or execution path exists, mark blocked and keep task as a review brief; never fake Claude output.

### Current project coordination finding
- Jarvis PR #7 run #11 is red at emulator Vosk-listening marker timeout; APK build and independent emulator probe passed. The artifact is available in RussSearchOPPO Actions run 42374316368, artifact ID 13575596341.
- Jarvis continuation brief is in RussSearchOPPO PR #9, branch `docs/jarvis-continuation-brief`, head `d3e6103d261151cbb1d9e85c4ce44bc756336deb`.
- Before dispatching an independent Gemini root-cause review, wait until duplicate dispatch workflow removal is merged; otherwise one task can invoke Gemini twice.


### 2026-11-07 — дополнительная проверка последнего Gemini API run
- Run: [42367422075](https://github.com/sokfrut-tech/Universal-AI-Factory/actions/runs/42367422075), job `128389041601`, workflow `Real Gemini Agent Execution`, attempt 2.
- Resolve task step passed and selected `coordination/gemini/dispatch/2026-11-07_jarvis-emulator-hang-direct-api.md`.
- API call failed after configured retries: primary `gemini-3.1-pro-preview` returned HTTP 429 `RESOURCE_EXHAUSTED` twice; fallback `gemini-3.8-flash` returned HTTP 503 `UNAVAILABLE` twice; final fallback request timed out after 75 seconds with curl exit 28 / HTTP 000. No report was committed. This is a provider quota/availability failure, not a task parser failure.
- Retry script currently classifies 429 as transient and allows up to five attempts. Review quota-aware retry policy (distinguish exhausted quota from short rate limit, honor Retry-After where provided, bound total wall-clock) before blind retries. Do not repeatedly dispatch this same task until provider availability/quota is confirmed.
- PR #23 head commit `b5850b069541e0ba0412ac8084294e6d6828ec1c`; PR open and mergeable at last check; no checks had appeared at time of inspection. Recheck latest CI before merge.
