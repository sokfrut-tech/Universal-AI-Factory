# Zero-cost decision: Qwen integration

Date: 2026-11-25

## Decision

**Do not integrate a hosted Qwen API into Jarvis or the factory.** The project constraint is strictly zero cost with offline-first operation. A free trial or temporary quota that requires payment verification and converts to pay-as-you-go is not a permanent free dependency.

## Why hosted Qwen is excluded

The current QwenCloud free-quota documentation says:
- free quota is only available in the Singapore region;
- it requires payment information verification to unlock;
- the new-user quota is generally valid for 90 days;
- after quota depletion or expiry, inference incurs pay-as-you-go charges unless a free-only stop is enabled;
- the documentation's free-quota-only setting is a console configuration, not a permanent no-billing guarantee.

Alibaba Cloud Model Studio's own pricing documentation also states that the referenced free quotas are Singapore-only and not available in other regions. This is not acceptable as the project's default because it is time-limited, region-specific and linked to billing setup.

Official sources:
- https://docs.qwencloud.com/resources/free-quota
- https://docs.qwencloud.com/developer-guides/getting-started/pricing
- https://www.alibabacloud.com/help/en/model-studio/model-pricing

## Local model candidates (research baseline, not device-tested)

| Candidate | Source | Published quant/file size | License | Decision |
|---|---|---:|---|---|
| Qwen3 0.6B GGUF Q4_0 | https://huggingface.co/ggml-org/Qwen3-0.6B-GGUF | ~429 MB | Apache-2.0 shown on model card | First low-storage smoke-test candidate |
| Qwen3 4B GGUF Q4_K_M | https://huggingface.co/Qwen/Qwen3-4B-GGUF | ~2.5 GB | Apache-2.0 shown on model card | Optional quality candidate after small model works |

Supporting official/runtime references:
- Qwen3 official repository describes model families and multilingual abilities: https://github.com/QwenLM/Qwen3
- Qwen3 official llama.cpp guide explains official GGUF use: https://github.com/QwenLM/Qwen3/blob/main/docs/source/run_locally/llama.cpp.md
- llama.cpp Android documentation: https://github.com/ggml-org/llama.cpp/blob/master/docs/android.md
- Qwen3 0.6B card: https://huggingface.co/Qwen/Qwen3-0.6B
- GGUF 0.6B quantization card: https://huggingface.co/ggml-org/Qwen3-0.6B-GGUF
- Qwen3 4B GGUF card: https://huggingface.co/Qwen/Qwen3-4B-GGUF

## Device implications

- GGUF file size is not the same as peak runtime RAM. Runtime memory also includes context/KV cache, backend buffers, tokenizer and the Android app.
- 0.6B Q4_0 is suitable only as a minimal smoke-test baseline; do not assume it is strong enough for a full Russian assistant or robust tool execution.
- 4B Q4_K_M is the more meaningful local prototype candidate, but actual throughput, peak RAM, temperature and battery impact must be measured on the OPPO Find X6 Pro.
- No Hexagon/NPU acceleration is claimed. Do not route Qwen to QNN/HTP unless a compatible backend/model path is built and tested.
- All model inference must stay on-device. Network access is only needed to download the model initially; once downloaded, inference should work offline.

## Factory implications

A GitHub-hosted workflow that calls a paid/limited remote endpoint violates the zero-cost requirement. A model file in an inbox, or a dispatcher ACK, is not proof of a running Qwen agent.

Automated Qwen execution remains **BLOCKED** until a local runner on existing user-owned hardware is verified and its operating cost, access boundary and report path are proven. Do not buy or enable a runner, cloud GPU, API credit or hosted inference plan.

## Acceptance criteria before considering integration

1. Exact model and license checked.
2. Model downloaded from its official/verified repository.
3. Hash and file size recorded.
4. Offline inference succeeds with network disabled after model download.
5. Fixed Russian prompt suite produces substantive results.
6. Peak RSS, generation speed, temperature and battery delta measured on the physical OPPO.
7. Existing assistant remains available as rollback/fallback.
8. No cloud requests, billing secrets, or paid dependencies are present.

## Status

This is a documentation-only decision. No model was downloaded, no device benchmark was run, no Qwen worker was invoked, and no application source code was changed.
