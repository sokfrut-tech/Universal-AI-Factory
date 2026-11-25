# OGAM Android model stalls: source-level diagnosis

Date: 2026-11-25
Repository: `sokfrut-tech/OGAM`
Audited ref: `main`
Device target: OPPO Find X6 Pro / Snapdragon 8 Gen 2 (user-reported target)
Scope: read-only source inspection. No source changes, tests, build, or on-device reproduction.

## User-observed symptom

The Russian-labeled APK starts and works, but local models sometimes take a long time to answer or remain stuck without producing a reply.

The exact model, model quantization, selected inference backend, time-to-first-token, and whether the stall occurs during model loading or after pressing Send were not supplied. Therefore no single root cause can yet be assigned.

## Confirmed code facts

### 1. Model initialization has a GPU/HTP timeout, but this is not a generation timeout

- `src/services/llmHelpers.ts` defines bounded initialization timeouts: Android Adreno GPU init 25 seconds and HTP/NPU init 30 seconds.
- The timeout wraps GPU/HTP context initialization through `tryGpuInit`. CPU-only initialization is returned directly and does not use that GPU timeout.
- These limits protect context creation only; they do not bound token generation after a model is loaded.

Source:
https://github.com/sokfrut-tech/OGAM/blob/main/src/services/llmHelpers.ts

### 2. Standard local generation awaits the native completion without an evident wall-clock watchdog

- `src/services/llm.ts` sets `isGenerating = true`, registers native work, then awaits `safeCompletion(ctx, () => ctx.completion(...), 'generateResponse')`.
- In the inspected method, there is no first-token deadline or total-generation deadline around that await.
- `isGenerating` is reset in `finally`, so if the native promise remains pending indefinitely, the service remains busy until native completion resolves or the user successfully stops it.
- The wrapper `safeCompletion` is imported from the helper module; its implementation must be inspected before concluding whether it supplies any hidden timeout. The call site itself does not show one.

Source:
https://github.com/sokfrut-tech/OGAM/blob/main/src/services/llm.ts

### 3. The UI has a state-machine queue and error recovery, but it depends on the provider settling

- `src/services/generationService.ts` serializes queued turns and resets state after completion/error.
- `src/services/generationServiceHelpers.ts` handles provider readiness and catches thrown generation errors.
- If a native completion neither resolves nor rejects, normal error handling cannot run and the queue cannot drain. This is a likely explanation for a persistent spinner / stuck send state, not yet confirmed on the user's device.

Sources:
https://github.com/sokfrut-tech/OGAM/blob/main/src/services/generationService.ts
https://github.com/sokfrut-tech/OGAM/blob/main/src/services/generationServiceHelpers.ts

### 4. Default inference settings can be demanding

- `src/stores/appStore.ts` defaults `contextLength: 4096`, `nThreads: 0` (auto), and `nBatch: 0` (auto).
- `src/services/llmHelpers.ts` resolves auto batch to backend-specific values (CPU/OpenCL/Metal generally 512; HTP 128) and uses the hardware-recommended thread count.
- A 4096 context is not proof of the cause, but it increases KV-cache and prompt-prefill work compared with a smaller context. Low-memory mapped loading is explicitly slower.

Sources:
https://github.com/sokfrut-tech/OGAM/blob/main/src/stores/appStore.ts
https://github.com/sokfrut-tech/OGAM/blob/main/src/services/llmHelpers.ts
https://github.com/sokfrut-tech/OGAM/blob/main/src/services/llm.ts

## Root-cause candidates (not yet confirmed)

1. Native llama.cpp/llama.rn completion promise stalls on a specific model/backend.
2. GPU initialization timed out and the app fell back to CPU, making generation appear frozen due to very low token speed.
3. Low-memory mapped loading, memory pressure, or a large context makes prompt prefill very slow.
4. Reasoning/thinking consumes a long time before ordinary answer tokens appear.
5. Thermal throttling after sustained inference reduces token speed.

Do not disable GPU globally or replace the model stack before collecting evidence.

## Safe diagnostic data needed

Ask for one model at a time:
- Exact model name as shown in the app and quantization (Q4/Q5/Q8, if shown).
- Whether the spinner starts immediately after Send or during model loading/switching.
- Whether any tokens/reasoning appear at all, and approximate wait time.
- Whether Stop responds, and whether a new message works after Stop.
- If available, copy the in-app Debug Logs around `[LLM]`, `[GenerationService]`, `GPU`, `Memory check`, `Generated`, `First token`, and `timed out`. Redact personal prompts, file paths containing private names, and any tokens/secrets.

## Recommended fix direction after reproduction

- Inspect `safeCompletion` implementation and native completion error semantics first.
- Add a cancellable first-token watchdog and/or a conservative total stall detector that invokes the existing stop path, reports a useful error, preserves partial output, and releases/reloads an unusable context safely. Do not use a bare Promise.race that abandons native work and frees the context while JSI is still running.
- Add tests for no-first-token timeout, timeout after partial output, Stop races, and recovery on the next turn.
- Add an explicit UI hint when GPU fallback to CPU or low-memory mode is active.
- Benchmark one representative small GGUF on the target phone with the same prompt, recording load time, time-to-first-token, decode tokens/sec, memory, and temperature.

## Status

- Source-level likely failure mode: unbounded native generation wait is plausible; exact implementation of imported `safeCompletion` remains to be inspected.
- Device reproduction: not performed.
- User model/quantization: unknown.
- Code changes: none.
- Tests/build: none.
