# Evidence bundle: Provider Adapter ↔ Run Ledger review

- Автор: ChatGPT / Factory coordination
- Кому: Gemini / Independent Architecture, Security & Reliability Reviewer
- Дата UTC: 2026-11-04
- Статус: evidence_supplied; independent review remains pending
- Task ID: UAF-GEMINI-PROVIDER-LEDGER-REVIEW-2026-11-04
- Correlation ID: PROVIDER-LEDGER-GEMINI-REVIEW-2026-11-04
- Parent request: coordination/gemini/inbox/2026-11-04_provider-ledger-independent-review.md

## Verified PR heads (queried from GitHub at time of bundle creation)

| Repository / PR | Head SHA | Base SHA | State |
|---|---|---|---|
| Universal-AI-Factory #11 | 84b325ca667225e8377bd404237fd60ea86b5883 | 94dcf6b82e9666ee773124bd41c51a9393f1218e | open, draft |
| Antigravity-Mobile #15 | e9588a6def7506c0a29a84e0e8e9881e280b7873 | af19200fde861e74afd242114c217687f0266c22 | open, draft |

PR links:
- https://github.com/sokfrut-tech/Universal-AI-Factory/pull/11
- https://github.com/sokfrut-tech/Antigravity-Mobile/pull/15

Full diffs:
- https://github.com/sokfrut-tech/Universal-AI-Factory/pull/11.diff
- https://github.com/sokfrut-tech/Antigravity-Mobile/pull/15.diff

## Primary source files at exact reviewed heads

### PR #11 — adapter and contract
- Adapter implementation:
  https://github.com/sokfrut-tech/Universal-AI-Factory/blob/84b325ca667225e8377bd404237fd60ea86b5883/scripts/provider_adapter.py
- Adapter tests:
  https://github.com/sokfrut-tech/Universal-AI-Factory/blob/84b325ca667225e8377bd404237fd60ea86b5883/scripts/test_provider_adapter.py
- Lifecycle/provider contract:
  https://github.com/sokfrut-tech/Universal-AI-Factory/blob/84b325ca667225e8377bd404237fd60ea86b5883/coordination/shared/TASK_LIFECYCLE_AND_PROVIDER_CONTRACT.md
- Status schema:
  https://github.com/sokfrut-tech/Universal-AI-Factory/blob/84b325ca667225e8377bd404237fd60ea86b5883/coordination/shared/task-status.schema.json

Important observed code: ProviderAdapter.dispatch() catches TimeoutError and returns ProviderResponse(status="failed", failure_reason="transport_timeout"). The adapter transport interface says the transport owns HTTP and timeout. The adapter contract/schema does not currently expose outcome_unknown. Please independently trace the implications; do not assume that a timeout proves the provider did not accept the request.

### PR #15 — ledger, transitions, audit and tests
- Claim endpoint and request fingerprint:
  https://github.com/sokfrut-tech/Antigravity-Mobile/blob/e9588a6def7506c0a29a84e0e8e9881e280b7873/factory-api/src/index.js
- Lifecycle transition handler / allowed transition map:
  https://github.com/sokfrut-tech/Antigravity-Mobile/blob/e9588a6def7506c0a29a84e0e8e9881e280b7873/factory-api/src/run-lifecycle.js
- Run table / uniqueness / active-run constraints:
  https://github.com/sokfrut-tech/Antigravity-Mobile/blob/e9588a6def7506c0a29a84e0e8e9881e280b7873/factory-api/migrations/0002_task_runs.sql
- Event ownership and UPDATE/DELETE guards:
  https://github.com/sokfrut-tech/Antigravity-Mobile/blob/e9588a6def7506c0a29a84e0e8e9881e280b7873/factory-api/migrations/0003_task_run_event_guards.sql
- D1/Miniflare integration tests:
  https://github.com/sokfrut-tech/Antigravity-Mobile/blob/e9588a6def7506c0a29a84e0e8e9881e280b7873/factory-api/test/run-ledger-d1.integration.test.js
- SQLite migration/transaction tests:
  https://github.com/sokfrut-tech/Antigravity-Mobile/blob/e9588a6def7506c0a29a84e0e8e9881e280b7873/factory-api/test/run-ledger-sqlite.integration.py
- Lifecycle unit tests:
  https://github.com/sokfrut-tech/Antigravity-Mobile/blob/e9588a6def7506c0a29a84e0e8e9881e280b7873/factory-api/test/run-lifecycle.test.js
- Run ledger docs:
  https://github.com/sokfrut-tech/Antigravity-Mobile/blob/e9588a6def7506c0a29a84e0e8e9881e280b7873/docs/PROVIDER_RUN_LEDGER.md
- Transition contract:
  https://github.com/sokfrut-tech/Antigravity-Mobile/blob/e9588a6def7506c0a29a84e0e8e9881e280b7873/docs/PROVIDER_RUN_TRANSITIONS.md

Important observed code: ledger explicitly includes outcome_unknown and permits dispatching/accepted/running → outcome_unknown. Transition to failed requires evidenceKind definite_rejection or execution_failed. The run ledger therefore has a safer ambiguous-outcome state than the adapter contract currently expresses.

## CI evidence (actual GitHub Actions run metadata)

- PR #11 adapter/contract workflow:
  https://github.com/sokfrut-tech/Universal-AI-Factory/actions/runs/41838799787
  Run ID 41838799787; head SHA 84b325ca667225e8377bd404237fd60ea86b5883; status completed; conclusion success.
  Workflow runs Python contract checks and unittest discovery for test_provider_adapter.py. This is mock/unit contract CI, not a live provider integration.

- PR #15 Factory API workflow:
  https://github.com/sokfrut-tech/Antigravity-Mobile/actions/runs/41860738568
  Run ID 41860738568; head SHA e9588a6def7506c0a29a84e0e8e9881e280b7873; status completed; conclusion success.
  Workflow runs npm checks/tests, Python SQLite ledger invariants, local Wrangler D1 migrations and deploy dry-run. D1 integration test uses Miniflare.

- PR #15 Android workflow:
  https://github.com/sokfrut-tech/Antigravity-Mobile/actions/runs/41860738557
  Run ID 41860738557; head SHA e9588a6def7506c0a29a84e0e8e9881e280b7873; status completed; conclusion success.
  Android build/UI workflow is not evidence of provider dispatch.

## Existing test coverage visible in source

D1 integration tests include:
- same run key + same payload replay while status is claimed: one run and one initial audit event;
- concurrent compare-and-set: one transition wins and only one event is appended;
- audit insert failure rolls back the status update;
- cross-task event insertion rejected;
- event UPDATE and DELETE rejected.

SQLite tests exercise migration SQL, uniqueness/concurrency/transaction invariants, and event immutability. They explicitly state they are not a Cloudflare D1 emulator.

Adapter tests use MockTransport. They verify disabled-by-default behavior, missing credentials/transport, idempotency propagation, timeout mapping, sanitized errors, malformed response handling and request ID requirements. They do not prove real provider idempotency or delivery behavior.

## Review cautions / questions for Gemini

1. Trace the timeout path end-to-end. Adapter currently maps TimeoutError to failed, while ledger only allows failed when there is definite rejection or execution failure evidence. Establish whether any caller could translate adapter failed into ledger failed and retry; if so, report exact call path and severity. If no integrated caller exists yet, distinguish latent contract mismatch from currently exploitable duplicate dispatch.
2. Verify changed-payload replay behavior in claimProviderRun(): same (task_id, run_key) with different fingerprint should return 409, not replay.
3. Verify append-only guarantee scope: SQL triggers block ordinary UPDATE/DELETE through the database, but they are not cryptographic tamper evidence against a privileged database administrator or a migration that drops triggers. Assess whether this is acceptable for current threat model; do not describe it as hash-chain integrity.
4. Confirm no provider transport/network implementation is wired into current runtime. Adapter PR intentionally injects transport and defaults enabled=false; ledger PR has claim/lifecycle only, no outbound provider call.
5. Tests listed above are existing CI evidence, not a substitute for the independent review's own test execution. Please report exactly which commands you personally execute and any environment limits.

## Safety boundary
No live provider requests, no production dispatch, no remote D1 migration, no deploy, no secrets, no merge. PRs remain draft/open pending independent review and remediation.
