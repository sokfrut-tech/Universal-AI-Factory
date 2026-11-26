# OGAM Android model stalls: Qwen-focused source diagnosis

Date: 2026-11-26
Repository: `sokfrut-tech/OGAM`
Audited ref: `main`
Device target: OPPO Find X6 Pro / Snapdragon 8 Gen 2 (user-reported target)
Scope: read-only source inspection. No source changes, tests, build, or on-device reproduction.

## User-observed symptom

The Russian-labeled APK starts and works, but the model being tried is Qwen; responses sometimes take a long time or remain stuck.

The exact Qwen model variant, quantization, selected inference backend, and whether the stall occurs during load, prompt prefill, reasoning, or token decoding are still unknown. Do not assume every Qwen variant behaves the same.

## Confirmed code facts

### 1. Initialization timeouts are separate from generation

- `src/services/llmHelpers.ts` defines Android Adreno GPU init timeout 25 seconds and HTP/NPU init timeout 30 seconds.
- These bound GPU/HTP context creation only. CPU-only initialization is not bounded by those GPU timeouts.
- They do not limit token generation after the context has loaded.

Source: https://github.com/sokfrut-tech/OGAM/blob/main/src/services/llmHelpers.ts

### 2. Native completion has no first-token or wall-clock watchdog

- `src/services/llm.ts` awaits `safeCompletion(ctx, () => ctx.completion(...), 'generateResponse')`.
- `src/services/llmSafetyChecks.ts` implements `safeCompletion` as try/catch around `completionFn()`. It catches rejected promises and performs error handling, but it does not impose a timeout.
- Therefore, if the native completion promise remains pending, this wrapper does not make it settle.
- The same unbounded completion pattern exists in `src/services/llmToolGeneration.ts` and `generateWithMaxTokens` in `llm.ts`.

Sources:
https://github.com/sokfrut-tech/OGAM/blob/main/src/services/llm.ts
https://github.com/sokfrut-tech/OGAM/blob/main/src/services/llmSafetyChecks.ts
https://github.com/sokfrut-tech/OGAM/blob/main/src/services/llmToolGeneration.ts

### 3. Existing native Stop and context-lifetime protections must be preserved

The current source already contains meaningful safeguards; the earlier recommendation to add a safe stop path must be narrowed:

- `stopAware()` wraps completion and re-sends `ctx.stopCompletion()` if Stop arrives while native completion is starting.
- `stopGeneration()` calls the native `context.stopCompletion()` and then awaits the active completion promise.
- `nativeWork` tracks native operations; unload waits for all tracked work before releasing the context.
- `contextUnusable` marks a completion that ended early so a later model load replaces the context.
- `waitForIdle()` has a 15-second default wait bound, but it only returns whether the engine became idle; it does not cancel a stuck native completion.
- Crucially, `stopGeneration()` itself awaits the active completion without its own deadline. If native Stop does not unwind a stuck completion, Stop and the next turn may remain blocked.

Source:
https://github.com/sokfrut-tech/OGAM/blob/main/src/services/llm.ts

### 4. Queue recovery still depends on the generation attempt settling

The generation service serializes work and has abort/error handling. Those mechanisms cannot fully recover from a native promise that remains pending. This is consistent with the reported stuck state, but has not been reproduced on the phone.

Source:
https://github.com/sokfrut-tech/OGAM/blob/main/src/services/generationService.ts

### 5. Performance settings are possible contributors, not proven causes

- The app store defaults inspected previously include context length 4096 and automatic threads/batch.
- A larger context increases KV-cache and prompt-prefill work; mapped low-memory loading is documented as slower.
- A failed GPU/HTP initialization may result in CPU fallback. That can look like a hang if token speed becomes very low.
- Reasoning mode can delay visible answer text even while the model is working.

These are hypotheses to distinguish with timing and logs, not grounds to change settings blindly.

## Qwen-specific diagnostic plan

1. Identify the exact Qwen entry and quantization selected in the app. Do not conflate Qwen3-ASR (speech recognition) with a conversational Qwen GGUF model.
2. Record model load duration separately from time-to-first-token and decode speed.
3. Capture whether reasoning tokens appear before answer text.
4. Record the selected backend and whether the app reports GPU/HTP fallback to CPU.
5. If the native completion stalls, test whether Stop returns and whether the next turn succeeds. Preserve the existing `stopAware`, `nativeWork`, and context-release ordering.

## Safe fix direction after reproduction

- Add a first-token watchdog and progress/stall diagnostics around the native completion.
- A watchdog must invoke the existing native stop path and wait for native work to unwind; it must not merely race the promise and pretend the engine is idle.
- If Stop does not unwind within a bounded recovery window, keep the context quarantined and report that a safe reload is required. Never release a context while its JSI/native completion may still be running.
- Preserve partial output and test Stop races, no-first-token timeout, timeout after partial output, and next-turn recovery.
- Do not disable GPU globally, reduce context globally, or replace the Qwen model stack without measured evidence.

## Status

- Confirmed: the standard generation path has no first-token or total-generation timeout; `safeCompletion` is error handling, not a watchdog.
- Confirmed: native Stop, native-work tracking, and context-release ordering already exist and must be preserved.
- Confirmed: `stopGeneration()` can still wait indefinitely for the active completion if native Stop fails to unwind it.
- User confirmed the model being tried is Qwen; exact Qwen variant/quantization remains unknown.
- Device reproduction: not performed.
- Source changes, tests, and builds: none.
