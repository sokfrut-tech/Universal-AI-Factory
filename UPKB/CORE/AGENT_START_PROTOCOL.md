# Mandatory Agent Start Protocol

Every human or AI agent working on any indexed project must follow this protocol.

## Before work
1. Read `UPKB/README.md`, `CORE/RULES.md`, `CORE/SECURITY.md`, and this file.
2. Search `INDEX/MASTER_INDEX.json` by project, task, document, branch, commit, issue/PR, and checkpoint.
3. Read the project's `PROJECTS/<PROJECT_ID>/README.md`, latest checkpoint, active tasks, decisions and linked handoffs.
4. Re-open primary sources at their recorded refs. Treat old statuses as historical until refreshed.
5. Inspect repository instructions (AGENTS.md and equivalent), branch/head, worktree status, diff, open PRs and relevant CI.
6. Inspect environment registry before starting services or tests that may use ports, devices, containers, cloud resources or paid services.
7. Record a task claim with agent identity, timestamp, target repository/branch and exclusive write-surface.

## During work
- Keep scope tied to the user's request and project acceptance criteria.
- Do not overwrite uncommitted or unowned work.
- Keep one integration owner per shared branch/schema/environment.
- Record meaningful decisions, experiments, commands, outcomes and evidence as they happen.
- Do not call external agents unless their actual tool/API is available and the task justifies it.
- Never put secrets in prompts, logs, commits, indexes or handoffs.

## Before handoff
1. Inspect the complete diff and exact branch head.
2. Run relevant tests/build/security checks; record exact commands and exit status.
3. Verify outputs independently; distinguish source implementation from device/runtime acceptance.
4. Update checkpoint, task status, document metadata and append-only journal.
5. Register any created environment and report cleanup status.
6. Provide next action, blockers, required access and evidence links.
7. Release the task claim only after the handoff is durable.

## Failure handling
If an index, file, repository or environment cannot be read, record the exact attempted location and error. Do not infer absence from a single failed endpoint. Retry via a supported alternate read path, then mark UNKNOWN if still unresolved.
