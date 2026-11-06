# AI agent usage policy

Updated: 2026-11-06

## Default operating mode

- ChatGPT is the primary coordinator and implementation agent in the active development workflow. It handles routine coding, repository edits, debugging, tests, documentation, and verification through the available GitHub/repository tools.
- Gemini API is a limited-quota specialist, not an always-on worker. Do not call Gemini for routine tasks, status checks, ordinary edits, or work ChatGPT can complete reliably.
- Use Gemini only when the coordinator identifies a material difficulty: unresolved root-cause analysis after a reasonable investigation, a high-impact architecture decision, an independent review of a risky change, or a genuinely ambiguous technical trade-off.
- Claude API is optional and disabled when its paid API key is absent. Missing Claude credentials must never block other work.
- Never assume Gemini API is free or has unlimited quota. Minimize calls, batch related questions into one well-scoped request, and avoid automatic retries that could multiply quota consumption. Retry only transient service errors with a small bounded retry count.

## Dispatch rules

- Files placed in agent inboxes are queued context and do not invoke an API by themselves.
- A Gemini request must be explicitly dispatched by the coordinator by adding a task file under `coordination/gemini/dispatch/`.
- The `real-ai-agent-execution.yml` push trigger watches only that dispatch directory. The manual workflow dispatch remains available for deliberate one-off runs.
- Each Gemini dispatch should contain one consolidated task with the exact question, relevant evidence, constraints, and expected output.
- Save every returned substantive report under `coordination/gemini/outbox/`; do not treat empty acknowledgements as completed work.

## Honest status

- A configured API key proves only that a secret is present; it does not prove the model request succeeded.
- Record actual model, API outcome, report path, and any unresolved limitations. Never claim that an agent edited another repository unless it actually had source access and made a verifiable change.
