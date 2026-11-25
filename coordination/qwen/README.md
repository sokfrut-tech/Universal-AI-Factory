# Qwen agent channel

This directory reserves a durable exchange location for Qwen-related research and provider work.

- `inbox/`: task requests for a Qwen executor.
- `outbox/`: substantive Qwen reports and verifiable results.
- A file in `inbox/` is only queued context. It does **not** invoke Qwen.
- No Qwen dispatcher/provider invocation has been verified as configured at the time this channel was created.
- Do not write empty ACKs or represent queued work as completed.
- Any future dispatcher must follow `coordination/shared/AGENT_EXCHANGE_PROTOCOL.md` and `coordination/AI_AGENT_USAGE_POLICY.md`.
