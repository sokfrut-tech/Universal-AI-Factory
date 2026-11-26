# OGAM Android model stalls: Qwen-focused source diagnosis

Date: 2026-11-26 (Qwen3.5 variant confirmed)
Repository: `sokfrut-tech/OGAM`
Audited ref: `main`
Device target: OPPO Find X6 Pro / Snapdragon 8 Gen 2 (user-reported target)
Scope: read-only source inspection. No source changes, tests, build, or on-device reproduction.

## User-observed symptom

The Russian-labeled APK starts and works, but the model being tried is Qwen; responses sometimes take a long time or remain stuck.

The user confirmed the family is Qwen3.5. The exact size variant (0.8B, 2B, or 9B), quantization, selected inference backend, and whether the stall occurs during load, prompt prefill, reasoning, or token decoding are still unknown. Do not assume every Qwen3.5 size behaves the same.

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

## Qwen3.5-specific findings and diagnostic plan

- OGAM `src/constants/models.ts` lists these trending Qwen3.5 repositories: `unsloth/Qwen3.5-0.8B-GGUF`, `unsloth/Qwen3.5-2B-GGUF`, and `unsloth/Qwen3.5-9B-GGUF`.
- This is a trending-family list, not proof that one of these exact variants is installed or selected on the user's phone. The runtime model selection and downloaded GGUF metadata still need to be identified.
- For the OPPO Find X6 Pro target, do not assume the 9B variant is appropriate merely because it appears in the trending list. A 0.8B or 2B quantized variant is a more conservative first performance baseline; this is a test recommendation, not a measured benchmark or a forced model change.



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
- User confirmed the model family is Qwen3.5; exact size (0.8B/2B/9B), quantization, and selected backend remain unknown. OGAM's trending list contains all three sizes.
- Device reproduction: not performed.
- Source changes, tests, and builds: none.

## User confirmation — exact size

On 2026-11-26 the user confirmed that the selected conversational model is **Qwen3.5-2B**. This narrows the investigation from the family to the 2B size, but does not yet identify the exact GGUF filename, quantization (Q4/Q5/etc.), backend actually used at runtime, or whether the delay occurs during load, prefill, reasoning, or decode. Do not describe the model as Q4 unless the app's selected file confirms it.

For the next controlled comparison, keep the current 2B model unchanged and first capture its exact filename/quantization and backend. Compare a short prompt with reasoning disabled/enabled only if the UI exposes that setting; record time-to-first-token and tokens/sec. Test Stop and a subsequent short turn. Avoid changing multiple settings simultaneously.

## Updated status

- Confirmed by user: Qwen3.5-2B is the selected model size.
- Still unknown: exact GGUF variant/quantization, backend, context length actually applied at runtime, and failure phase.
- No app code changed; no test/build or physical-device reproduction performed.

## Follow-up source trace — standard and tool generation / Stop path

Read-only inspection of the current `main` source on 2026-11-26 adds these details:

- In `src/services/llm.ts`, the standard text path registers the entire generation operation in `nativeWork` before context-window and attachment preparation awaits. The native completion is awaited through `safeCompletion`; the first-token timestamp is recorded only when a token callback arrives. No watchdog checks elapsed time or lack of token callbacks.
- `activeCompletionPromise` is a rejection-swallowing mirror of the full generation operation. `stopGeneration()` sets `stopRequested`, invokes native `context.stopCompletion()`, then awaits that mirror without a timeout. Thus the UI can show an immediate stop/partial reply at the generation-service layer, while the underlying native work may still remain pending and block safe reuse.
- `waitForIdle(15000)` is a bounded observation only. It races the active promise against a timer and reports whether the service is idle; it does not cancel native work or make it safe to release the context.
- The tool-call path (`generateResponseWithTools` → `generateWithToolsImpl`) also stores an active promise and awaits `safeCompletion` without a generation watchdog. It uses the same stop-aware context proxy supplied by `LLMService`.
- `generateWithMaxTokens` is another unbounded native completion path, used by internal routing/summarization helpers.
- Context release deliberately waits until all registered native work settles before calling `release()`. This is an important safety invariant: a timeout fix must not clear `isGenerating`, drop `nativeWork`, or release/reload the context merely because a JS timer expired.

### Diagnostic conclusion refined

The code supports a credible mechanism for a persistent spinner / blocked next turn: native completion can remain pending; `safeCompletion` does not time it out; Stop waits for that same completion to settle; and the queue's recovery depends on the generation operation finishing. This is a source-level explanation, not proof that this user's Qwen3.5-2B incident is caused by it. The same code paths serve other model families, so Qwen-specific attribution still requires runtime logs.

### Safe next engineering step

Before editing production code, obtain the missing parent workspace engineering contract referenced by OGAM `rules.md` (`../.codex/ENGINEERING_CONTRACT.md`) or an explicit confirmation that it is not available/required for this scoped audit. Then add a narrow instrumentation/test plan covering:
1. time from send to native completion start;
2. time to first visible answer token and first reasoning token separately;
3. decode tokens/sec after first token;
4. actual backend and GPU/HTP fallback;
5. Stop during prefill, Stop during decode, and whether the next short turn starts;
6. tool-call and internal max-token completion paths.

Do not introduce a bare `Promise.race` timeout around native JSI completion. Any eventual watchdog needs a native-stop handshake, a bounded wait for unwind, explicit quarantined/busy state if unwind fails, preserved partial output, and tests proving the context is never released while native work remains active.

## Follow-up status

- Additional source paths inspected: `src/services/llm.ts`, `src/services/llmToolGeneration.ts`, and `src/services/generationService.ts`.
- Confirmed source-level risk: no first-token/generation watchdog in standard, tool, or max-token completion paths; Stop awaits native completion without a deadline.
- No source edits, tests, builds, APK changes, or device reproduction performed.
