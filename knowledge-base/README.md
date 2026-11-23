# Universal Project Knowledge Base (UPKB)
Version 1.0.0 | Created 2026-11-23 | Owner sokfrut-tech

## Purpose
A searchable, append-only cross-agent memory for projects, documents, research, decisions, work sessions, evidence, risks and exact continuation points. Project repositories remain authoritative for code and tests; this database is authoritative for navigation and cross-project continuity.

## Mandatory agent entry sequence
1. Read OPERATING_RULES.md.
2. Search PROJECTS.csv by project_id, repository and aliases.
3. Search DOCUMENTS.csv for handoffs, architecture, research, QA and decisions.
4. Read the latest project handoff and inspect live GitHub state: default branch, recent commits, open PRs, Actions, releases and deployment.
5. Read ACTIVITY_LOG.md, DECISIONS.md, RESEARCH_REGISTER.md and CONTINUATION_QUEUE.md.
6. Verify evidence at the exact current commit before acting.
7. After work, append the journal and update registries in the same PR.

## Database map
- PROJECTS.csv — one row per known project/repository.
- DOCUMENTS.csv — document/artifact metadata, source URL/path, affected area, date, author and status.
- ACTIVITY_LOG.md — append-only journal.
- RESEARCH_REGISTER.md — research questions, candidates, sources, findings and adoption gates.
- DECISIONS.md — accepted/rejected/conditional decisions.
- CONTINUATION_QUEUE.md — prioritized stop/resume points.
- OPERATING_RULES.md — mandatory agent protocol.
- SEARCH_INDEX.md — keyword and alias navigation.

## Record fields
Unique ID, project ID, title, artifact type, canonical URL/path, affected area, created/updated date, author/agent, status, evidence, related task/PR/commit, dependencies, risks and next action. Use UTC ISO-8601 for machine-readable dates. Never store credentials, tokens, secrets or private user data.

## Status vocabulary
VERIFIED_NOW; VERIFIED_EVIDENCE; HISTORICAL; IMPLEMENTED_UNVERIFIED; RESEARCHED; PLANNED; BLOCKED; UNKNOWN.

## Coverage warning
Initial inventory covers 12 repositories visible in the connected GitHub account on 2026-11-23 plus cross-project initiatives found in memory. It is not yet an exhaustive audit of every file, PR, commit, workflow or conversation. Fill gaps incrementally and never claim full audit until reconciled.

## Canonical links
- Master index: ../docs/MASTER_PROJECT_INDEX.md
- Factory continuation brief: ../docs/FACTORY_CONTINUATION_BRIEF.md
- Repository: https://github.com/sokfrut-tech/Universal-AI-Factory
