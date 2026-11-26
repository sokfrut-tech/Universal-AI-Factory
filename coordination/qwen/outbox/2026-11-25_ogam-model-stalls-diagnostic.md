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


## Test-coverage follow-up — 2026-11-26

Read-only inventory of the OGAM `main` test tree found relevant existing coverage:

- `__tests__/unit/services/llmEarlyStop.test.ts`: Stop before native completion starts; next reply succeeds.
- `__tests__/unit/services/generationService.test.ts`: Stop with partial output, Stop during prefill, ignore a late token after Stop, native Stop rejection handling, and queue drain ordering.
- `__tests__/integration/generation/queueStoppedReplySettlesTwice.rendered.test.tsx`: late native-stop settlement and exactly-one-turn-at-a-time queue behavior.
- `__tests__/unit/services/llmSafetyChecks.test.ts`: `safeCompletion` success and rejected-promise/native-error handling.

### Specific gap relevant to the reported hang

The inspected tests exercise completions that eventually settle (including a delayed native unwind) or reject. The `safeCompletion` tests do not cover a completion promise that remains pending forever. The Stop tests likewise do not establish recovery behavior when `stopCompletion()` resolves but the associated `completion()` promise never settles. There is therefore no demonstrated regression test for the exact indefinite-pending condition identified in the source trace.

This is a test-coverage gap, not proof that the device has entered that condition. The next test design should use a deliberately never-settling native completion, assert that Stop cannot falsely mark the native engine idle, assert that the context is not released, and assert that a subsequent request is not sent into the still-busy context. A separate test should cover a completion that settles after a bounded native-stop delay and prove normal recovery. These tests should be added only alongside a reviewed recovery design; do not change production behavior with a JavaScript-only timeout.

### Contract lookup status

- `rules.md` on OGAM `main` explicitly gives priority to `../.codex/ENGINEERING_CONTRACT.md`.
- The contract file is not present in the OGAM repository tree or the inspected Universal-AI-Factory repository tree. A GitHub code search scoped to the connected `sokfrut-tech` repositories did not locate it.
- This does not prove the file is absent from a private/local parent workspace; the path is outside the OGAM repository. No attempt was made to inspect or alter the user's PC/workspace.

### Verification boundary

- Read-only source and test inventory only.
- No tests executed; no source or test files modified; no build/APK produced; no device reproduction.


## Released APK source cross-check and exact regression-test gap — 2026-11-26

The source paths were re-checked at the exact OGAM commit used for the user's downloaded APK, `0cbc605a2480823099e2b96a1ebcf084f0b2d990`, as well as the current `main` source. The relevant completion/Stop behavior is present in both:

- Standard generation and `generateWithMaxTokens` await `safeCompletion(... completion ...)`; `safeCompletion` catches rejected errors but has no deadline for a promise that stays pending.
- Tool generation awaits the same `safeCompletion` wrapper and has no independent completion deadline.
- `stopGeneration()` sends `context.stopCompletion()`, then waits for `activeCompletionPromise` to settle before clearing the active-generation state.
- `waitForIdle(timeoutMs)` is a bounded observation only. A false result does not cancel native work or authorize context release.

### Important existing protection — and its boundary

OGAM already has `contextUnusable` / `isContextUsable()`. When a completion **returns** with an unexpected early-end result, `recordCompletionEnd()` marks the context unusable; the next model load replaces it, including when the same model file is selected again.

That mechanism does not cover an operation whose completion promise never returns: `recordCompletionEnd()` is reached only after the awaited completion resolves. So the existing backend-fault recovery does not resolve the indefinite-pending case.

### Existing test coverage, checked against the source

- `__tests__/unit/services/llm.test.ts` has a valuable release-order test ("never releases the context under a completion that was still being set up"). Its mocked completion emits a token and resolves immediately; it does not simulate an operation that remains pending after Stop.
- The same file's unload-while-generating test manually sets `isGenerating = true`; it verifies the Stop call precedes release but does not keep a real completion promise in flight.
- Its `activeCompletionPromise` Stop test resolves the injected promise before invoking Stop, so it does not exercise a never-settling active operation.
- `__tests__/harness/nativeBoundary.ts` can hold llama completions during prefill (`holdBeforeStream`) or mid-stream (`pauseAfter`), but its fake `stopCompletion()` releases those holds and lets the completion settle. It has no llama-completion mode that deliberately remains pending after Stop. The LiteRT fake does have a hang mode, but that is a different engine and does not exercise llama.rn's context lifecycle.

### Proposed regression test shape — not implemented

1. Load a fake llama context. Replace its next `completion()` with a deferred promise that remains pending; make `stopCompletion()` resolve immediately without resolving that completion.
2. Start a real service generation and call Stop without awaiting it directly. After a bounded observation window, assert Stop is still pending, `waitForIdle(shortWindow)` is false, and no second completion is issued into that context.
3. Start unload/reload and assert the old context's `release()` has not been called while the completion remains pending.
4. Resolve the deferred completion as test cleanup. Then assert Stop/unload drain in the expected order and that a subsequent model load/reply works.
5. Repeat with `stopCompletion()` rejecting, then repeat the core lifecycle assertions through the tool and max-token paths where applicable.

The test must not leave a permanently pending promise in Jest teardown. It should hold the operation beyond the observation window, assert the safe-busy behavior, then explicitly resolve it for cleanup. This models a native operation that outlives the watchdog window without making the test process itself hang forever.

### Engineering conclusion

The downloaded APK commit confirms this is not only a later `main`-branch concern: the same no-deadline Stop/completion wait is in the code used for that build. This still does **not** prove that Qwen3.5-2B is the specific cause on the user's OPPO; no device logs or reproduction have been collected.

A watchdog may report slow/no-first-token progress and request native Stop, but it must not treat the timer as cancellation. Until native completion actually settles, the engine/context must remain marked busy or quarantined; no new completion, cache mutation, context release, or reload may use that same live context. No production fix is chosen in this note.

### Verification boundary

- Exact APK source commit and current `main` checked read-only.
- Existing test and harness code inspected read-only.
- No tests run, no app/test/harness source edits, no build/APK produced, and no OPPO device reproduction.


## Native-boundary harness review — 2026-11-26

A focused read of the exact APK-source test harness confirms why the current green stop tests do not reproduce the reported failure mode:

- In `__tests__/harness/nativeBoundary.ts`, the scripted llama completion can pause before streaming (`holdBeforeStream`, around lines 524–532) or mid-stream (`pauseAfter`, around lines 604–613).
- Its fake `stopCompletion()` (around lines 684–691) always sets the stop flag and invokes the stored release callback. The held completion therefore resumes and resolves with an interrupted result. The harness cannot currently represent “native stop acknowledged, but completion Promise remains pending”.
- The `completion()` wrapper tracks the in-flight call until `runCompletion()` exits (around lines 662–681); there is no separate switch for a stop-resistant completion.
- In `src/services/llm.ts`, `doUnloadModel()` requests stop when `isGenerating` is true, then waits for every tracked `nativeWork` item before releasing the context (around lines 390–414). This is the correct memory-safety invariant, but an indefinitely pending native call means unload/reload also waits indefinitely.
- The existing “never releases the context under a completion that was still being set up” unit test (around lines 2083–2100) uses a completion that emits a token and immediately resolves. It does not keep the completion pending through Stop.
- The existing active-completion Stop test resolves its injected promise before calling Stop (around lines 2310–2325), so it does not test a genuinely in-flight completion that ignores Stop.

### Narrow test-harness extension proposal — not implemented

Add an opt-in test-only mode for llama completion where `stopCompletion()` records the stop request but does not release the completion promise. Keep the deferred completion handle available to the test so it can be resolved during cleanup. Then cover:

1. Stop resolves its native stop request but the completion remains pending; engine remains busy and `waitForIdle` returns false.
2. A second completion is not sent to the same context.
3. Unload/reload does not call `context.release()` while the old completion is pending.
4. Once the test releases the deferred completion, Stop and unload drain in order and a fresh context can generate again.
5. A separate delayed-settlement case proves normal recovery after native unwind.

This should be a harness/test-only change first, not a production timeout. It can establish the lifecycle contract before any recovery mechanism is designed. Do not make the fake return an invented “successful cancellation” while the completion is still active.

### Recommended recovery states — design only

- `READY`: context can accept generation.
- `GENERATING`: one native completion owns the context.
- `STOP_REQUESTED`: stop sent; completion is still tracked.
- `DRAINING`: stop requested and waiting for native unwind.
- `QUARANTINED`: unwind did not complete within the observation window; no new completion, cache mutation, unload, release, or reload may reuse this context. Surface a clear recovery message rather than leaving an endless spinner.

A watchdog may transition the UI/service into a visible timeout state and request native stop. It must not transition the context to `READY` or release it merely because the JavaScript timer elapsed. A safe in-process recovery from `QUARANTINED` requires a verified native cancellation/reinitialization boundary; absent that, process restart is safer than reusing or freeing a context still owned by native work.

### Verification boundary

- Direct read-only inspection of the exact APK commit's `llm.ts`, `llm.test.ts`, and `nativeBoundary.ts`.
- No tests executed; no OGAM source, test, or harness files modified; no APK built; no physical-device reproduction.
