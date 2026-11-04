# Factory continuation brief — Universal AI Factory

**Updated:** 2026-11-04  
**Canonical portfolio:** docs/PROJECT_PORTFOLIO_AND_CONTINUATION_PLAN_2026-11-04.md  
**Exchange protocol:** coordination/shared/AGENT_EXCHANGE_PROTOCOL.md  
**Tool registry:** docs/TOOL_INTEGRATION_REGISTRY.md  
**Security ledger:** docs/FACTORY_SECURITY_ROLLOUT.md  
**Correlation:** universal-ai-factory-continuation-20261104

## Mission
Coordinate all owner repositories with durable plans, provider-neutral task orchestration, real agent execution, shared tools, security gates and auditable handoffs. GitHub is an asynchronous exchange ledger, not a magical live channel.

## Open work observed 2026-11-04
- #11 Claude/Gemini provider adapter and lifecycle contract (draft).
- #12 tool integration registry (draft).
- #14 manual runner hardening (draft).
- #15 portfolio roadmap (draft).
- #6 universal inbox dispatcher (open; mergeability conflict reported).
- #8 owner-submitted Gemini response evidence.
- #7 Whisper security evidence.
- #10 shared security toolchain.
- #1 Hermes Agent core plan.

## Hard rules
- Claude/Gemini are optional; ChatGPT continues directly if unavailable.
- Do not mark providers healthy or runs executed without real authenticated provider evidence.
- ACK and inbox receipt are not task completion.
- Keep adapter state, provider health, task status and event transport distinct.
- Use durable ledger, idempotency, correlation IDs, append-only events, concurrency protection and explicit outcome_unknown for ambiguous dispatch.
- Never expose credentials in Git/logs; server-side secrets only.
- Require owner approval for merges, deployments, destructive changes, production DB migrations and secrets.

## Next actions
1. Review PR #11 adapter contract and identify exactly what is implemented versus mocked.
2. Reconcile #11 with Antigravity Mobile #15 ledger; create shared API contract tests.
3. Repair/replace ACK-only dispatcher #6; preserve original messages and correlated substantive replies.
4. Review manual runner #14 and security scans; keep deny-by-default tool scopes and approvals.
5. Build mock provider tests for duplicate dispatch, timeouts, correlation mismatch, retries and event ordering.
6. Only if a provider is truly configured, run a non-production end-to-end smoke test and record provider execution ID plus substantive response.
7. Update the portfolio and project briefs at every closeout.

## Resume
Read portfolio plan and exchange protocol, refresh all open PRs and workflow runs, then take the next unblocked action. Do not wait for Claude/Gemini; their substantive reviews are optional and must be recorded honestly.
