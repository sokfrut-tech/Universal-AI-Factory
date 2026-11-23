# UPKB — mandatory operating rules
Updated: 2026-11-23

## Before work
- Start from this knowledge base, not chat recollection.
- Resolve the project by repository and project_id. Read its latest handoff, README, relevant source, open PRs, recent commits, Actions, releases and deployment state.
- Distinguish plan, source implementation, unit tests, CI, successful build, installed APK, device validation and production evidence.
- Use newest verifiable evidence and exact commit/PR head SHA. Mark stale data HISTORICAL.
- Search before creating duplicate records.
- User works mainly from Android and is nontechnical. Request action only for credentials, device interaction, approval or other unavailable capability; provide short exact phone steps.
- Do not issue PC/Termux/bash/PowerShell/Python commands to the user while those executors are disabled.
- Do not run physical-device tests or claim device validation without explicit authorization and evidence.

## During work
- One task has one task_id, target repo, branch/base, scope, acceptance criteria, expected evidence and dependencies.
- Use feature branches; preserve unrelated work; no direct production/main changes unless explicitly authorized and gates pass.
- An agent plan is not implementation. Empty ACK is not a deliverable. Code changes require commit/PR evidence.
- Research records must identify original source/revision, date, license, platform compatibility, inspected scope and unknowns.
- Model comparisons require pinned version/hash, license, hardware/runtime, prompt set, repeated runs, scoring rubric, latency/memory/quality metrics and human review. Discovery is not benchmarking.
- No proprietary APK code, credentials, private user data or secrets. Clean-room implementation and license review only.
- No paid APIs, spending, public exposure, production deployment, destructive action or secret rotation without explicit approval.
- Prefer free, local and offline-first solutions. Private context must not be sent externally by default.

## After work (required)
1. Append ACTIVITY_LOG.md with task_id, UTC timestamp, agent, project, scope, outcome, changed paths, branch, commit/PR, tests and exact results, artifacts, risks and next action.
2. Update PROJECTS.csv status, last_verified_utc, active branch/PR, last commit and next action.
3. Register artifacts in DOCUMENTS.csv with URL/path, type, area, date, author and status.
4. Add durable technical choices to DECISIONS.md and model/source investigations to RESEARCH_REGISTER.md.
5. Update CONTINUATION_QUEUE.md and SEARCH_INDEX.md when priorities/keywords change.
6. Record failures as well as successes. Correct history by appending a dated correction, not deleting old evidence.
7. Attribute authorship truthfully: ChatGPT, Claude, Gemini, Kimi, Antigravity, Codex, human or automation.

## Sources of truth
- Source repository code/PR/CI is authoritative for implementation state.
- UPKB is authoritative for cross-project navigation, decisions, research register and continuation queue.
- Chat history is contextual evidence, not implementation proof.
- If sources conflict, preserve both references, prefer newer verifiable evidence and log the discrepancy.
- v1 uses GitHub Markdown/CSV, immediately searchable. Future SQLite/FTS or generated indexes must preserve readable source files and Git history.
