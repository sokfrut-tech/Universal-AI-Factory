# UPKB Core Rules

Updated: 2026-11-24

## Authority and evidence
- Source repositories and their commits remain authoritative for code and release state. UPKB is the cross-project discovery, provenance, history and continuation layer.
- Distinguish `VERIFIED`, `REPORTED`, `PLANNED`, and `UNKNOWN`. A remembered status is historical until rechecked.
- Every material claim must point to a source: repository/path/ref, commit, PR, workflow run, artifact, device observation or user report.
- An agent summary is not proof. Verify artifacts and exact revisions independently.
- Never silently replace source documents with summaries. Preserve provenance and links.

## Agent workflow
1. Read `CORE/AGENT_START_PROTOCOL.md`.
2. Find the project and task in the indexes; read the checkpoint and linked source documents.
3. Inspect repository instructions, current branch/head, status and diff before editing.
4. Claim one write-surface; coordinate before overlapping changes.
5. Make scoped changes and run focused then broad relevant checks.
6. Record exact commit, commands, exit codes, test counts, artifact links and remaining risks.
7. Update project checkpoint, relevant indexes and append-only journal.
8. Hand off the next actionable step and required access.

## Safety
- Never store tokens, passwords, private keys, recovery codes or secrets in UPKB.
- Avoid personal data; store only the minimum project-relevant metadata.
- Never deploy, publish, merge, delete, rotate credentials or alter live infrastructure without explicit authorization.
- Do not delete or stop unknown environments, processes, containers, ports or user data.
- Register created test environments and clean up only resources demonstrably created by the current task.
- Mark unavailable evidence as UNKNOWN; do not fabricate missing details.

## Conflict and concurrency
- One owner per write-surface (file/schema/branch/environment) at a time.
- Parallelize read-only discovery; serialize shared writes and integration.
- Preserve existing project-specific rules when stricter. If rules conflict, stop and document the conflict.
