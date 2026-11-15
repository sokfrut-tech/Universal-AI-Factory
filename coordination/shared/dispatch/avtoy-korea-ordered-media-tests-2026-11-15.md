# Execute isolated AVTOY KOREA regression tests

Purpose: use the public Universal-AI-Factory GitHub-hosted runner to execute tests for a private target repository whose own hosted runner is unavailable.

Target repository: `sokfrut-tech/avtoy-korea-auto`
Target branch: `fix/ordered-media-sequence-main-2026-11-15`
Expected target commit: `e5924ad5b13cd19c752deb0c06086b7644002343`

Required commands:
- `node --check worker.js`
- `node --check media-order.js`
- `node --test worker.test.mjs media-order.test.mjs`

Safety:
- Checkout only the named private repository and branch.
- Use FACTORY_PAT only for checkout; do not print, persist, or expose its value.
- Do not modify or push to the target repository.
- Do not deploy, merge PR #78, access production KV, or export user data.
- Save only the sanitized run outcome and target commit SHA in the factory outbox/results folder.
- If FACTORY_PAT is missing or checkout fails, report that exact blocker. Do not request or print the token in chat.
- Execution profile: exact project Worker CI command plus full media-order regression suite (Node 22).
