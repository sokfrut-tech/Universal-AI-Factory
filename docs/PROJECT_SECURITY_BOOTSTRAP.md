# Project Security Bootstrap

Use this checklist when creating any new repository or project under Universal AI Factory.

## Before first production release

- [ ] Add this factory standard as a reference: `docs/CYBERSECURITY_SKILLS_FACTORY_STANDARD.md`.
- [ ] Add project-specific agent instructions (`AGENTS.md` or equivalent) covering scope, privacy, secrets, branch policy and verification.
- [ ] Define assets, trust boundaries, user data, public endpoints, authentication and threat model.
- [ ] Add secret scanning (Gitleaks or ecosystem equivalent) without exposing matched values in logs.
- [ ] Add dependency/lockfile audit and a scheduled update process.
- [ ] Add static analysis appropriate to the language (CodeQL where supported).
- [ ] Harden GitHub Actions: minimal permissions, safe PR triggers, timeouts, concurrency, no secrets in fork PRs.
- [ ] Add tests for authorization, privacy, input validation, error handling and replay/idempotency where relevant.
- [ ] Add release artifact SHA-256 and tested commit SHA evidence.
- [ ] Define BLOCK/WARN/PASS policy and a documented exception process.
- [ ] Confirm all required checks run on pull requests before production deployment.
- [ ] Document what CI does not prove (live runtime, infrastructure, credentials, external integrations).

## Repository-specific adaptation

Do not blindly copy Android, Worker, Node, Python or other project checks into unrelated repositories. Choose scanners and tests based on the actual stack. Keep existing stronger controls. Never remove or weaken a required check to obtain a green workflow.

## Future-project rule

A new project is not ready for production until its security lane is implemented, exercised on a test change, and included in the release gate. If a scanner or integration is unavailable, mark it BLOCKED or NOT CONFIGURED rather than pretending it ran.

## Tooling bootstrap

- [ ] Read `docs/TOOL_INTEGRATION_REGISTRY.md` and select only the tools needed for this project's stack.
- [ ] Verify each connector with a real smoke test; if unavailable, use the documented fallback and label it accurately.
- [ ] Do not add credentials to source control or bypass provider/organization approval gates.
