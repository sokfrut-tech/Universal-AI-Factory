# AVTOY KOREA — HTTP shutdown integration check (2026-11-15)

- Branch HEAD under test: `10ce21465f1b08e0aebf01f0b5b62af201c65666`.
- Exact helper implementation was copied from the verified GitLab source into an isolated Node v22.16.0 harness.
- Four helper tests passed: idempotency/order, forced close and awaited close callback, grace deadline validation, and YDB closure after an HTTP shutdown error.
- Additional real Node HTTP integration exercise:
  - Normal drain: request handler accepted an in-flight request; graceful shutdown waited for response completion; event order was `response.end` then `driver.close`; client received complete response.
  - Forced drain: request deliberately held beyond the 5 ms grace period; server force-closed the connection; client received `ECONNRESET` as expected for forced termination; YDB driver closed last.
- The first integration attempt began shutdown before the request reached the server and reset the connection. Test was corrected to await server-side request acceptance before triggering shutdown; corrected run passed both scenarios.
- This validates the helper against Node's HTTP server behavior in an isolated harness. It does **not** substitute for the full repository test suite, container build, or YDB integration.
- GitLab pipeline #547 failed before any job started (`started_at=null`, zero jobs): https://gitlab.com/sokfrut/avtoY-korea-auto/-/pipelines/3071063638
- Remaining blocker: no package lockfile in branch; Docker still uses `npm install`. A genuine lockfile must be generated in a trusted registry-connected environment before switching to `npm ci`.
