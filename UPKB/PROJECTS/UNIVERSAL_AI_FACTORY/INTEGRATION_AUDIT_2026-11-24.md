# Factory Agent Integration Audit — 2026-11-24

## Scope
Read-only inspection of current `main`:
- `.github/workflows/inbox-dispatcher.yml`
- `.github/workflows/real-ai-agent-execution.yml`
- `coordination/AI_AGENT_USAGE_POLICY.md`
- `coordination/claude/README.md`
- `coordination/gemini/README.md`
- `docs/FACTORY_CONTINUATION_BRIEF.md`

## Verified findings

### 1. Inbox dispatcher
Source: `.github/workflows/inbox-dispatcher.yml`, main blob `8373751c037a0cf91719147deec8157aac84da5a`.
- Push paths include Claude, Gemini and ChatGPT inbox Markdown files.
- Workflow creates a technical receipt by copying the task into the relevant outbox.
- The receipt explicitly says it is NOT proof that an agent read or accepted the task.
- It does not invoke a model/API or execute the task.
- Current code is broader than the older note claiming the dispatcher watched only Claude.

### 2. Gemini execution
Source: `.github/workflows/real-ai-agent-execution.yml`, main blob `343e54074d640ee40a631ccbd6d63ae03bcc52ed`.
- Runs only on explicit files under `coordination/gemini/dispatch/*.md` or manual workflow dispatch.
- Enforces execution on main; uses a bounded job timeout.
- Calls Gemini Developer API and writes a substantive report into Gemini outbox.
- The workflow checks out the Factory repository only. It does not checkout a target project repository by default.
- The prompt explicitly prohibits claiming repository/device/log inspection unless evidence/access was supplied.
- It does not currently load UPKB core rules, project index, task context or project checkpoint automatically.

### 3. Claude
Source: `coordination/claude/README.md`, main blob `83f379058c11cfa446993f9cadaa1b4de69ee575`.
- Folder is an exchange convention, not an automatic Claude connection.
- Real exchange requires Claude to have repository access and independently read/write messages.
- No live Claude execution was confirmed in this audit.

### 4. Global policy
Source: `coordination/AI_AGENT_USAGE_POLICY.md`, main blob `15d33ce9d17cb176d4b0ce05ec68bf88278ef413`.
- GPT is default coordinator/implementer.
- Gemini is a quota-limited escalation expert; dispatch is explicit.
- Claude API is optional.
- Substantive reports and evidence are required; empty ACK is invalid.

## Integration gaps
1. UPKB is not yet loaded by the Gemini workflow.
2. The dispatcher receipts are not agent execution.
3. Claude automatic read/write/execution is unverified.
4. Target project repository checkout and scoped write access are not part of the current Gemini workflow.
5. No end-to-end proof exists that an agent reads UPKB before work and writes a checkpoint/handoff after work.

## Safe integration sequence
1. Review and merge the UPKB foundation PR before wiring workflows to files not yet on main.
2. Add a deterministic context builder that requires a project ID/repository in every dispatch task; include only core rules plus the matching project entry, checkpoint, relevant task records and explicitly linked documents.
3. Fail closed when project identity/checkpoint cannot be resolved; do not send the entire multi-project database to a model by default.
4. Inject the context into Gemini prompt and record the exact UPKB commit/hash used in its report.
5. Keep inbox dispatcher as receipt-only unless a separately designed, authorized execution path is implemented.
6. Add a write-back validator: reports must include evidence, commit/PR, tests, checkpoint update and unresolved risks. A report alone does not imply source changes.
7. Design GPT/Claude/Antigravity integration separately; do not imply they are connected because Gemini workflow is updated.
8. Test with a harmless synthetic task and verify exact context input, report output, index/checkpoint update and no unrelated repository writes.

## Safety boundary
This audit was read-only. No workflow, secret, permission, live deployment, agent dispatch or production environment was changed.
