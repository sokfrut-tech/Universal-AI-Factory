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
