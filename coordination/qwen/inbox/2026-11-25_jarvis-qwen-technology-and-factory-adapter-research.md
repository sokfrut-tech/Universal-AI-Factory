# Qwen independent research task — Jarvis + Universal AI Factory

- Date: 2026-11-25
- Requested by: project owner
- Coordinator: ChatGPT
- Status: QUEUED — this file is not proof of a Qwen API invocation
- Scope: research and architecture review only; do not modify application source or secrets

## Objective

Independently assess the next useful Qwen technologies and recommend a practical integration path for two distinct targets:

1. **Jarvis Android** — local-first assistant for OPPO Find X6 Pro (PGEM10), Snapdragon 8 Gen 2, Android 16 / ColorOS. Offline operation is a core requirement.
2. **Universal-AI-Factory** — multi-agent GitHub workflow where tasks, evidence and handoffs must be durable and auditable.

## Questions to answer

### A. Qwen technology status

Verify using official Qwen sources and dated release notes:

- Qwen4-Max: actual capabilities, context, tool use, modality, API availability, pricing/limits if public, data handling, and whether downloadable open weights exist.
- Qwen3.8-Omni-Flash and Qwen3.8-LiveTranslate: supported input/output modalities, Russian support, streaming behavior, speaker separation, API constraints and costs.
- Current smaller open-weight Qwen models that can realistically run on Android Snapdragon 8 Gen 2. Verify exact model IDs, parameter sizes, quantization formats, license, source URLs and download availability.
- Do not infer that a cloud model has local/offline weights. Distinguish API models from open-weight releases.

### B. Jarvis integration recommendation

Compare at least these options:

1. Local Qwen model through the existing llama.cpp / llama.rn / GGUF route.
2. Optional Qwen cloud provider adapter behind explicit user consent.
3. Optional streaming translation mode for live multilingual conversations.

For each option provide:
- What source files/interfaces in the current OGAM/Jarvis code would be affected (inspect repository before naming exact paths).
- RAM, storage, thermal, battery and latency risks on Snapdragon 8 Gen 2.
- Russian quality evaluation plan with repeatable prompts and scoring.
- Offline behavior and fallback.
- Privacy, permission and microphone-data boundaries.
- License and model-weight provenance.
- A rollback strategy.

Do not recommend replacing the existing local model until measured device results justify it.

### C. Factory multi-agent integration

Review the current factory protocol and the open provider-dispatch work. Recommend a Qwen provider adapter that:
- Uses a separate explicit provider/model configuration.
- Reads credentials only from GitHub Actions secrets; never print, commit or echo secret values.
- Has bounded timeouts/retries, idempotency and correlation IDs.
- Distinguishes received, queued, dispatched, running, completed, failed and blocked.
- Writes substantive results to `coordination/qwen/outbox/`; an ACK alone is not a result.
- Does not claim a Qwen agent was invoked unless a real API response and provider/model metadata are recorded.
- Does not modify another repository without a scoped branch and explicit authorization.

### D. Independent recommendation

Return a ranked decision:
- Implement now (if any).
- Prototype behind a feature flag.
- Keep under research.
- Reject / defer, with reasons.

Prefer the smallest useful integration over a broad rewrite.

## Required report format

Save one substantive Markdown report in `coordination/qwen/outbox/` with:

1. Executive summary.
2. Verified facts with direct official source URLs and publication dates.
3. Cloud vs open-weight vs fully offline comparison table.
4. Device feasibility for OPPO Find X6 Pro / Snapdragon 8 Gen 2.
5. Factory provider-adapter proposal.
6. Security/privacy/licensing review.
7. Benchmarks and acceptance tests.
8. Ranked recommendations and unresolved questions.
9. Exact files/commits inspected and any commands/tests actually run.

## Evidence rules

- Cite official model cards, official API docs, release notes and source repositories.
- For licenses, inspect the exact model/repository license; do not assume one license covers every package or weight.
- Label vendor performance figures as vendor-reported, not independently measured.
- Never fabricate test results, device measurements, API calls or source inspection.
- If unable to access a source or execute a benchmark, state that explicitly.
- Do not create an empty ACK file. If no substantive answer can be produced, leave the outbox empty and report the blocker through the available real dispatch mechanism.

## Constraints

- Research only. No APK changes, production deployment, merge, billing activation, or secret changes.
- No cloud audio/screen upload without explicit user consent.
- Preserve local-first operation and the user's ability to use Jarvis without internet.
