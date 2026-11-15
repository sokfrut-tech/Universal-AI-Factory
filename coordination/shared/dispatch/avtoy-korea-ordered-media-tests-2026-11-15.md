# Execute isolated AVTOY KOREA regression tests

Purpose: use the public Universal-AI-Factory GitHub-hosted runner to execute tests for a private target repository whose own hosted runner is unavailable.

Target repository: `sokfrut-tech/avtoy-korea-auto`
Target branch: `fix/ordered-media-sequence-main-2026-11-15`
Expected target commit: `140c5330fe0517474be6f80ebe77acdc30ead78c`

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
