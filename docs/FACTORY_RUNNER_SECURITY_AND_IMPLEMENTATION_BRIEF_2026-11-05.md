# Factory Runner: security assessment and implementation brief

- Date: 2026-11-05
- Status: `planned` / security findings confirmed by source inspection
- Owner: Universal AI Factory coordinator
- Scope: local-first, free-by-default task execution shared by Antigravity Mobile and Jarvis
- Related: `coordination/shared/AGENT_EXCHANGE_PROTOCOL.md`

## Executive decision

Do not treat the current `.github/workflows/factory-runner.yml` as a secure general-purpose code executor. It is currently an audit/report workflow, not a patch runner, and its current inputs/permissions are too broad for untrusted task content. Keep it out of any automatic production execution path until the hardening items below are addressed.

This brief authorizes design and isolated implementation work only. It does not authorize production deployment, repository writes by an automated agent, merges, secrets access, or live infrastructure changes.

## Confirmed findings from current workflow source

1. The workflow grants repository-wide `contents: write` although its task is primarily audit/reporting.
2. `github.event.inputs.task_file` and `target_repo` are interpolated directly into shell script text. Treat workflow_dispatch input as untrusted; pass inputs through environment variables and validate them before use.
3. The task file is selected by newest filesystem mtime when no explicit path is supplied. That is not a trustworthy task-selection or identity mechanism; use an explicit task ID/path and immutable commit SHA.
4. The workflow checks out a target repository using a user-provided repository suffix. The allowed repository set is not enforced by an allowlist.
5. The report copies the full task file into a generated report. Incoming task files must be treated as untrusted data and checked for secrets/oversized content before copying or processing.
6. The current workflow does not apply patches, run target-project tests, produce a validated diff/evidence manifest, or obtain independent review. It must not be described as an implementation executor.

## Required architecture

### Phase 0 — harden the existing workflow before any execution

- Set `permissions: contents: read` by default; grant write only in a separate, narrowly scoped job if a concrete write is required.
- Pass all workflow inputs via `env:`; never splice user-controlled values into shell source.
- Validate target repository against a fixed allowlist of approved `owner/repo` pairs.
- Validate task path as a normalized relative path rooted under `coordination/<agent>/inbox/`; reject absolute paths, `..`, symlinks escaping the root, NUL/control characters, and unexpected extensions.
- Require explicit task ID, source inbox path, and immutable source commit SHA. Do not choose the newest file by mtime.
- Do not copy raw task contents into logs/reports by default; record path, SHA-256, size, and a short sanitized summary.
- Pin third-party actions to full commit SHAs before enabling execution.
- Keep the workflow manual until a separate security review approves its scope.

### Phase 1 — local, no-network patch validator (first executable slice)

Implement a small deterministic library/CLI with no shell execution and no network access. It accepts:
- approved target repository identifier;
- pinned base commit SHA;
- unified diff text with a strict maximum byte size;
- explicit task ID and correlation ID.

It must:
- reject empty/oversized patches and unsupported binary patches;
- reject absolute paths, traversal, path separators that escape the checkout, symlinks, submodules, and writes outside the allowlisted workspace;
- reject duplicate/conflicting file paths and malformed diff headers;
- canonicalize every destination path and prove it remains inside the workspace;
- never read or print secrets;
- produce a normalized patch summary and SHA-256 digest;
- make no repository/network/production changes.

Acceptance tests must cover traversal, absolute paths, symlink escape, binary patch, duplicate paths, oversized patch, malformed headers, valid add/modify/delete within the allowed root, and deterministic digest output.

### Phase 2 — isolated test runner (separate approval gate)

Only after Phase 1 passes:
- create a disposable checkout/worktree pinned to the approved base SHA;
- use an unprivileged isolated container/runner with no secrets, no write token, restricted/no network, and CPU/memory/time limits;
- apply only a validated patch;
- run only repository-declared allowlisted test/build/security commands;
- collect exit codes, bounded logs, diff, artifact hashes, and an evidence manifest;
- destroy the workspace after producing the evidence bundle.

No automatic PR creation, push, merge, release, or deployment.

### Phase 3 — review and owner approval

- An independent reviewer must inspect the diff and evidence; the executor cannot approve its own output.
- A machine-readable evidence manifest records task ID, target repo, base SHA, patch SHA-256, changed paths, commands, exit statuses, artifact hashes, and reviewer identity/result.
- Only after explicit owner approval may a separate workflow create a PR. It must never merge or deploy.

## Shared contract for Antigravity Mobile and Jarvis

Both clients submit the same task envelope:
- `task_id`, `correlation_id`, `project_id`, `target_repo`, `base_sha`, `task_spec_ref`, `created_at`, `requested_capabilities`, `approval_state`.
- State transitions: `new -> accepted -> running -> review -> approved -> pr_created`; alternatives: `blocked`, `failed`, `cancelled`.
- Every transition is append-only and idempotent. Duplicate dispatch with the same task/run id must not execute twice.
- Offline mode stores tasks in a local inbox/outbox and syncs later; cloud/provider availability is optional.
- Claude/Gemini are optional reviewers/executors only when a real response artifact with matching correlation ID is received. An ACK file alone is not execution evidence.
- Free/local execution is the default. Paid provider calls require explicit per-run cost acknowledgement.

## Acceptance gates

| Gate | Required evidence | Current status |
|---|---|---|
| Workflow least privilege and safe inputs | workflow tests + review | blocked / not hardened |
| Patch validator | unit tests for all cases above | not implemented |
| Isolated runner | containment tests + no-secret proof | not implemented |
| Evidence manifest | schema + deterministic tests | not implemented |
| Independent review gate | reviewer identity + recorded result | not implemented |
| Owner approval gate | explicit approval audit event | not implemented |
| Antigravity/Jarvis integration | contract tests + offline test | planned |

## Immediate next tasks

1. Replace the existing workflow's broad permissions and shell interpolation; retain audit-only behavior.
2. Implement Phase 1 patch validator as a small, dependency-light module with unit tests.
3. Add a security workflow that runs validator tests and secret scanning on every PR.
4. Integrate the shared task envelope into Antigravity and Jarvis only after the contract tests pass.

## Non-goals

- No arbitrary shell command execution from agent-generated tasks.
- No unattended self-modifying code or self-approval.
- No mandatory paid model/API.
- No production deployment or remote database migration.
- No assumption that a GitHub inbox file means Claude/Gemini actually read or answered it.
