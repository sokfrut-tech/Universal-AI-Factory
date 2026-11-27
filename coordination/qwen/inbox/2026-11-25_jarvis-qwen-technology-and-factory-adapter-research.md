# Qwen local-first research task — Jarvis + Universal AI Factory

- Date: 2026-11-25
- Requested by: project owner
- Coordinator: ChatGPT
- Status: QUEUED — no Qwen execution is claimed
- Budget constraint: **strictly zero cost**. No paid API, billing account, card, subscription, metered fallback, or paid runner.
- Scope: public-source research and local architecture only; do not modify application source, secrets, billing, or deployment.

## Objective

Assess whether open-weight Qwen models can improve two targets without introducing any ongoing service cost:

1. **Jarvis Android** — local-first assistant for OPPO Find X6 Pro (PGEM10), Snapdragon 8 Gen 2, Android 16 / ColorOS. Offline operation is a core requirement.
2. **Universal-AI-Factory** — auditable multi-agent workflow. A Qwen worker is acceptable only if it runs on existing user-owned hardware or another genuinely no-cost local resource. Do not assume GitHub-hosted compute or a free hosted inference endpoint is unlimited or free.

## Strict zero-cost rules

- Do not call Alibaba Cloud Model Studio, QwenCloud, OpenAI-compatible hosted endpoints, inference providers, or any other hosted model API.
- Do not add API keys, billing setup, card verification, paid subscriptions, pay-as-you-go configuration, or automatic paid fallback.
- Do not run model hosting, deployment, fine-tuning, paid GPU, paid CI, or paid storage.
- Cloud free trials are not treated as a permanent free solution. Record them only as excluded options.
- Open model weights and open-source inference software may be evaluated for local execution. Account for storage, power, data and thermal costs; no inference can be called "free" if it requires a paid service.
- No cloud audio, screen, prompts, source code, or personal data uploads.

## Questions to answer

### A. Open-weight Qwen models

Use official Qwen / Hugging Face model cards and the exact repository license. Identify:
- Smallest viable Qwen text models with downloadable official GGUF variants.
- Exact model IDs, file sizes by quantization, license, provenance, supported context, multilingual/Russian evidence.
- Which candidate is suitable for an initial OPPO test and which is only an optional higher-quality candidate.
- Runtime compatibility with llama.cpp on Android/ARM64; distinguish official support from untested assumptions.

### B. Jarvis device feasibility

Compare local Qwen 0.6B, 1.7B and 4B quantizations where available. Evaluate:
- Download/storage size, runtime RAM (not just file size), context/KV-cache impact.
- Snapdragon 8 Gen 2 CPU/Adreno/QNN feasibility; do not claim NPU/Hexagon acceleration unless the exact backend supports this model and is tested.
- Thermal, battery and latency risks.
- Russian conversation, instruction-following and tool-call evaluation with fixed prompts and repeatable scoring.
- Offline fallback to the current model if Qwen fails or exceeds resource limits.
- Exact candidate source paths in OGAM/Jarvis, only after inspecting repository contents provided to you. Do not guess paths.

### C. Factory architecture

- Do not implement a hosted Qwen API adapter.
- Determine whether an actual Qwen worker can run on existing user-owned hardware at zero additional cost.
- GitHub inbox files and Actions receipts are not proof of a Qwen model invocation.
- If no available local execution host is verified, mark automated Qwen dispatch as BLOCKED; do not create an ACK or fabricate an outbox report.
- Recommend a safe local bridge only if it can be run on the user's existing device/computer without exposing private network services publicly or adding paid infrastructure.

### D. Ranked recommendation

Return:
1. Test locally now.
2. Prototype behind a feature flag.
3. Keep under research.
4. Reject/defer, with reasons.

Do not replace the existing local model until actual device measurements justify it.

## Required report format

Save one substantive Markdown report in `coordination/qwen/outbox/` containing:
1. Executive summary and zero-cost compliance.
2. Verified model facts with exact source URLs and dates.
3. Cloud/hosted options explicitly excluded from implementation.
4. Open-weight model comparison and file sizes.
5. Snapdragon 8 Gen 2 feasibility, clearly separating estimates from measurements.
6. Jarvis integration files inspected and minimal prototype proposal.
7. RAM/storage/thermal/battery benchmark plan.
8. Licensing/provenance and security review.
9. Ranked recommendations and unresolved questions.
10. Exact files/commits inspected and commands/tests actually run.

## Evidence rules

- Prefer official Qwen and ggml-org sources, model cards, exact LICENSE files, and llama.cpp Android docs.
- No invented device measurements, source inspections, tests, API calls, or runtime performance.
- Label vendor claims, estimates, and independently measured results separately.
- If the report cannot be completed from available public sources, explain the gap and leave the outbox empty rather than creating an ACK.

## Constraints

Research only. No APK changes, production deployment, merge, billing activation, secrets, or paid service. Preserve local-first operation and the user's ability to use Jarvis without internet.
