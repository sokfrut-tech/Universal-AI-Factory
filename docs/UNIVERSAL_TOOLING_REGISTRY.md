# Universal Tooling Registry and Factory Integration Plan

**Created:** 2026-11-04  
**Status:** Inventory and integration contract; not a claim that every provider is already callable by Factory runtime.

## Objective

Make the Universal AI Factory the coordination and execution layer for every tool capability available to the ChatGPT operator in this environment, and make the capability inventory reusable by every current and future project.

The operator can use tools directly today. Factory agents can use them autonomously only after an explicit, tested adapter/credential/permission path exists. Never represent operator-only access as agent access.

## Capability inventory

| Capability family | Available tools in this environment | Useful factory work | Current integration status |
|---|---|---|---|
| GitHub source control | Repository/branch/file/commit reads and writes, PRs, issues, reviews, diffs, Actions runs/jobs/logs/artifacts, releases and repository discovery | Source intake, scoped branch work, PR lifecycle, code review evidence, CI/artifact verification | Direct operator access; factory-native GitHub workflows exist. Agent/runtime delegation and least-privilege token path must be verified per action. |
| Files and knowledge | Files search/read/find/list/materialize/library management/share | Read project briefs, specs, logs and attachments; archive reports and evidence | Direct operator access. No automatic factory access to private conversation/library files. Export only approved project artifacts. |
| Web research | Web search/open/click/find, business/product/availability search, image search | Technical research, vendor/API documentation, current security advisories, product/service evidence | Direct operator access; no generic unrestricted web credential is implied for agents. |
| Image generation | Image generation and image editing | Original assets, mockups, visual concepts, image edits | Direct operator access; not an existing Factory API. Human approval required before committing generated assets. |
| App deployment | AppDeploy: app inventory/status, source inspection, resource uploads, secrets setup, deploy/version/domain operations | Build/deploy web apps, inspect versions and runtime configuration | Direct operator access. Destructive actions, secret changes, domain changes and production deploys require explicit approval and a scoped adapter. |
| UI/design engineering | MagicPath: projects, themes, components, canvas inspection/editing, code sessions/builds, asset upload/export, skills | UI prototypes, design-system inspection, component generation and review | Direct operator access. Agent access requires explicit workspace/project authorization and API adapter. |
| Product analytics | PostHog query/analytics tool | Usage analysis, funnels, retention, errors and experiment evidence | Direct operator access if connected; factory access and project scoping must be tested. |
| Automation/scheduling | Automations: create/list/peek/run/update, event-source discovery and notifications | Scheduled QA, recurring health checks, reports and event-driven tasks | Direct operator access. Factory should request explicit schedule/trigger approval; do not create automations silently. |
| OpenAI API setup | OpenAI Platform: API-key setup and target discovery | Configure API-backed agents/services | Direct operator access. Never expose key material in prompts, logs, issues, artifacts or source control. |
| Agent security policy | ArmorCodex: policy read/update and intent-plan registration | Enforce coding-agent boundaries, approvals and tool restrictions | Direct operator access. Policy changes require review and should be recorded with rationale and rollback. |
| Installed skills | Skills discovery/read for code, repository engineering guardrails, AppDeploy onboarding, MagicPath and PostHog | Reusable specialist procedures and quality gates | Direct operator access. Skills are instructions, not credentials or proof of agent execution. |
| Personal context | Personal context retrieval | Recover project decisions and prior constraints | Operator-only; never export unrelated or sensitive personal context into Factory. |
| Runtime utilities | Python, container, file generation and inspection | Data processing, archive inspection, test helpers, reports and artifacts | Operator execution environment only; no persistent Factory worker access is implied. |

## Mandatory integration model

1. **Capability registry:** each tool/adapter records capability ID, owner, supported operations, input/output schema, authentication mode, required scopes, data classification, side-effect level, timeout, retry policy, idempotency key, audit fields, and health status.
2. **Four access states:** `operator_only`, `adapter_pending`, `agent_enabled`, `blocked`. Never infer `agent_enabled` from a connector being visible to ChatGPT.
3. **Least privilege:** separate read, write, deploy, secret-management and destructive scopes. Default to read-only. Use per-project allowlists and short-lived credentials where supported.
4. **Approval gates:** require explicit approval for production deploys, merge to protected branches, secret creation/rotation/deletion, custom-domain changes, data deletion, policy weakening, public releases, paid usage and scheduled external actions.
5. **Secret hygiene:** secrets live only in the relevant provider's secret store. Logs and task records may include presence/status and secret reference names, never values. Never ask the user to paste secrets into chat or commit them.
6. **Task lifecycle:** `received -> queued -> dispatched -> running -> completed|failed|blocked`. An ACK means only `received`; it is not execution evidence.
7. **Evidence:** every completed task returns correlation ID, repository/project, branch/commit/PR or deployment ID, tests/checks, artifact links and known limitations. Failed or blocked tasks report the exact safe reason.
8. **Isolation:** agents work on scoped branches and project allowlists. No cross-project writes. No automatic merge or production deployment.
9. **Auditability:** persist who/what invoked a capability, target, timestamp, approval, outcome and evidence pointer. Redact sensitive values.
10. **Fallback:** when no safe adapter exists, the coordinator may use its direct operator tools and then publish a factual report; do not pretend the Factory runtime performed the action.

## Initial implementation order

### P0 — Provider execution and task truth
- Complete Factory issue #11: real Claude/Gemini provider dispatch, truthful lifecycle states, correlation IDs, idempotency, missing-credential diagnostics and tests.
- Add a generic capability-adapter contract and registry schema.
- Add provider health checks that report configured/not configured without revealing secret values.

### P1 — GitHub and CI as the first native adapter
- Formalize the existing GitHub workflows as a project-scoped adapter.
- Support repository allowlists, branch-only writes, PR creation/review, Actions status and artifact retrieval.
- Require human approval for merge, release, repository settings, secrets and protected-branch changes.

### P2 — Quality and engineering services
- Add read-only research/documentation, static analysis, test execution, dependency/security scanning and artifact inspection adapters where runners and credentials exist.
- Treat image generation, MagicPath and design work as optional asset/component pipelines with review before repository writes.

### P3 — Deployment, analytics and automation
- Add AppDeploy, PostHog and Automations adapters only after scope, tenant/project mapping, audit logs and approval gates are tested.
- Deployment and automation writes stay approval-gated.

### P4 — Broader tool bridge
- Evaluate Files, web research, image generation, Python/container and OpenAI Platform individually. Conversation-private files, personal context and runtime-local files must not be exposed wholesale to agents.

## Acceptance tests

- Registry enumerates every capability family above and accurately marks the access state.
- Missing credentials produce `blocked` with a safe diagnostic, not a false success.
- Duplicate task delivery does not duplicate side effects.
- Read-only credentials cannot write; project A credentials cannot write project B.
- Approval-gated operations are blocked without an approval record.
- Secrets never appear in logs, reports, PRs, artifacts or test output.
- Timeout/provider failure are reported distinctly from completed execution.
- Every completion has a verifiable evidence pointer.
- Existing factory workflows and project pipelines remain functional.

## Current known blocker

Factory issue #11 is open: the current inbox dispatcher has previously produced ACK-only receipts, and provider dispatch has returned `503 provider_not_configured`. Until actual Claude/Gemini invocation is demonstrated, those agents remain `adapter_pending`/ `blocked`, not active workers.

## Operating rule for all future projects

Every new project brief should include a Factory task record, project allowlist, selected specialist roles, required capabilities, approval boundaries, test/evidence requirements and a final human-readable status report. Reuse this registry; do not build ad-hoc unsafe tool access per project.
