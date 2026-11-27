# Isolated Patch Executor — Phase 2 Design Brief (2026-11-05)

## Status

Design-only proposal. No patch application, repository writes, command execution, network access, merge, deployment, or secret access is implemented by this document.

Depends on:
- PR #19 `feat(factory): add safe no-network patch validator` (validation-only; 20 unit tests; CI run 41913807427 passed).
- PR #20 `security: harden factory runner workflow` (manual, metadata-only, read-only workflow; CI run 41914519011 passed).

## Objective

Define a narrowly scoped, disposable executor that can prove whether a validated unified diff applies to an exact base revision and run an explicitly approved, bounded verification command set without exposing credentials or mutating the user's working repository.

The executor is NOT an autonomous agent with shell access. It is a constrained test appliance.

## Non-goals

- No automatic merge, push, PR creation, release, deployment, DNS, webhook, database migration, or production action.
- No execution of shell snippets, scripts, workflow files, Makefiles, Gradle tasks, package lifecycle hooks, or instructions supplied inside task text unless a separately reviewed policy explicitly allows the exact command.
- No access to host home directories, user data, SSH agents, cloud credentials, GitHub PATs, environment secrets, Docker socket, Kubernetes credentials, or production services.
- No outbound network during patch application or tests by default.
- No claim that a passing sandbox test proves production readiness or device behavior.

## Trust boundaries

1. **Task intake:** task content is untrusted data. Only task IDs, repository allowlist key, exact base SHA, patch bytes, and a policy profile cross the intake boundary.
2. **Validator:** PR #19 validator remains pure and side-effect-free. Do not add filesystem or subprocess responsibilities to it.
3. **Executor:** separate process/container/VM with a disposable workspace and no credentials. It receives a bounded validated patch and immutable repository snapshot.
4. **Policy:** verification commands are selected from a version-controlled allowlist keyed by repository and policy revision. Never accept arbitrary command strings from task content.
5. **Evidence:** executor emits structured metadata and bounded logs; no raw secrets or unrestricted environment dump.
6. **Human gate:** an independent reviewer inspects the diff and evidence. Owner approval is required before any action outside the sandbox.

## Required sandbox properties

- Fresh disposable workspace per task; destroy it after evidence collection.
- Pin exact repository and base commit SHA; fail closed if fetched snapshot does not match.
- No mounted host directories, writable shared caches, Docker socket, privileged mode, host PID/network namespaces, or inherited credentials.
- Default network disabled at the OS/container boundary, not merely by an application flag.
- Read-only base snapshot; only the disposable worktree is writable.
- CPU, memory, process count, disk, patch bytes, file count, output bytes, and wall-clock limits.
- Non-root UID, restrictive umask, minimal environment, fixed locale/timezone, sanitized PATH.
- No symlinks, hardlinks, devices, FIFOs, sockets, submodules, or path traversal in patch outputs.
- Reject case-folding/path-normalization collisions and duplicate paths on case-insensitive targets.
- Resolve every path component with lstat/no-follow semantics; ensure canonical destination remains beneath workspace root before create/open/rename.
- Reject unexpected file modes and executable-bit changes unless repository policy explicitly permits them.
- Do not follow symlinks already present in the base tree when resolving patch destinations.

## Patch application protocol

1. Verify intake envelope schema and size limits.
2. Re-run PR #19 validation inside the executor; never trust a caller-supplied validation report.
3. Materialize an immutable snapshot for the exact allowlisted repository/base SHA using a trusted fetch mechanism before entering the no-network execution phase.
4. Verify snapshot commit identity and repository identity.
5. Inspect the base tree for symlinks, submodules, special files, and path collisions; reject unsupported trees or affected paths.
6. Apply the patch using a pinned, audited implementation inside the disposable workspace only. The chosen implementation must not invoke hooks or external commands and must enforce no-follow path handling. If this cannot be guaranteed, stop and keep the phase validation-only.
7. Verify resulting changed paths/modes against the validator report and policy.
8. Run only repository-specific, predeclared verification profiles. No commands are read from task content.
9. Capture exit codes, durations, resource usage, test summaries, tool versions, and hashes.
10. Destroy workspace and temporary credentials/material after producing the evidence bundle.

## Verification profile contract

Each profile must declare:
- repository identifier and policy version;
- exact executable and argument vector (no shell interpolation);
- working directory;
- whether network is required (default false; any exception requires a separate review and isolated proxy allowlist);
- timeout and resource limits;
- expected report paths and maximum output size;
- required test levels (unit, lint/typecheck, build, integration/emulator where feasible);
- prohibited operations and expected failure behavior.

A command that can install dependencies, run lifecycle scripts, access the network, modify Git metadata, spawn unbounded children, or access host resources must be treated as high risk and separately constrained. Prefer prebuilt, hash-pinned toolchains and dependencies.

## Evidence bundle

Produce a machine-readable JSON manifest plus bounded text reports:
- task ID and correlation ID;
- repository allowlist key and exact base SHA;
- patch SHA-256 and byte count;
- changed file paths, change types, and modes;
- sandbox image/runtime digest and policy revision;
- toolchain versions;
- each verification command profile ID, exit status, duration, and resource limits;
- test totals and failures;
- artifact hashes and truncation flags;
- explicit network-disabled assertion from the sandbox runtime;
- final status: `rejected`, `applied_in_sandbox`, `tests_passed_in_sandbox`, or `tests_failed_in_sandbox`.

Never include environment variables wholesale, tokens, credentials, private user data, or unredacted task content.

## Failure behavior

Fail closed on missing policy, unknown repository, base SHA mismatch, unsupported filesystem object, path ambiguity, resource limit, timeout, network availability, unexpected command, patch mismatch, or incomplete evidence. Preserve a minimal redacted failure record; do not retry by relaxing controls.

## Acceptance criteria before implementation is considered complete

- Threat model and command profiles reviewed independently.
- Tests cover traversal, absolute paths, Windows paths, Unicode normalization/case collisions, symlinked parent components, hardlinks, special files, pre-existing symlinks, mode changes, malformed patches, resource exhaustion, timeout, and evidence redaction.
- Integration test proves patch application changes only the disposable workspace and leaves source repository/base snapshot unchanged.
- Network isolation is verified at runtime by an external boundary test, not a self-reported boolean alone.
- No secret is available to the executor process.
- Failure injection proves cleanup and evidence generation on every exit path.
- Fresh CI on exact commit passes; no test is skipped to obtain green status.
- Independent security review and explicit owner approval before enabling any executor workflow.

## Implementation sequence

A. Threat model + policy schema review (no execution).
B. Build isolated workspace prototype with synthetic fixtures only.
C. Add no-follow path inspection and filesystem-object rejection.
D. Add audited patch application with applicability checks.
E. Add repository-specific fixed verification profiles.
F. Add resource/network isolation tests and evidence bundle.
G. Independent review; keep disabled until owner approval.

## Current state and handoff

- PR #19 is validation-only and must remain the boundary for pure diff validation.
- PR #20 hardens the legacy workflow into manual metadata-only review; do not run the old workflow or treat it as an executor.
- No executor is currently authorized or available. Until phases A–G are implemented and reviewed, factory behavior remains intake + static validation + read-only reporting.
- Next action: inspect repository instructions and existing workflow policy, then implement phase A review/tests in a separate draft PR. Do not merge or enable dispatch without explicit approval.
