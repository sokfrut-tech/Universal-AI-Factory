# OGAM local voice stack audit — 2026-11-25

## Executive result

The fork already contains substantially more local speech infrastructure than the earlier Qwen proposal assumed. Do not add a second ASR or LLM runtime before evaluating the existing implementation.

This is a source inspection only. No model was downloaded, no build/test was run in this audit, and no physical OPPO measurement is claimed.

## Verified in sokfrut-tech/OGAM main

Repository: https://github.com/sokfrut-tech/OGAM
Inspected branch: `main`
Package version: `0.0.125`

### Local text inference

- `package.json` includes `llama.rn` (pinned to `@ogai/llama.rn@0.13.0-b12560`).
- `src/services/llm.ts` owns a native `LlamaContext`, loads GGUF files, checks model memory requirements, tracks residency, GPU fallback and performance, and exposes tool-enabled generation.
- `src/services/providers/localProvider.ts` implements the existing local provider by delegating to `llmService`.
- The existing local provider already supports tool calling when the loaded model and generated tool path support it.

**Decision:** Qwen3 text GGUF should be tested through the existing llama.rn/localProvider path. Do not add another inference engine or a cloud endpoint.

### Local speech recognition

- `package.json` includes `whisper.rn`.
- `src/services/whisperService.ts` already imports and manages `QwenAsrEngine` as an alternative transcription engine.
- `src/services/qwenAsrModel.ts` identifies the phone-sized model as `ggml-org/Qwen3-ASR-0.6B-GGUF`, obtains the primary weights and audio projector from the shared model catalog, and checks platform/runtime/device memory eligibility.
- `src/services/qwenAsrEngine.ts` loads the GGUF plus audio projector through `llama.rn` multimodal support; it uses CPU on Android in the inspected implementation and a 4096-token context.
- `src/services/whisperModels.ts` retains multilingual Whisper choices and adds the Qwen3-ASR transcription card.
- `src/services/whisperModelDownloads.ts` downloads both Qwen ASR files using catalog metadata, exact sizes and optional SHA-256.
- `src/hooks/useWhisperTranscription.ts` owns the existing realtime capture / transcription interaction.

The official Qwen3-ASR project lists Russian among supported languages for the 0.6B and 1.7B models: https://github.com/QwenLM/Qwen3-ASR

**Important distinction:** Qwen3-ASR is a speech-to-text model, not the conversational text LLM. Its presence does not mean the Qwen3 chat model has been integrated or selected.

### Voice output (TTS)

The OGAM README states that on-device Kokoro TTS is part of the paid Pro tier. The free transcription path does not by itself provide a free talking assistant.

**Decision:** Do not add paid Kokoro/Pro dependencies. Evaluate Android's built-in `TextToSpeech` engine as the zero-cost first TTS prototype, with Russian voice availability checked on the actual OPPO. This is a proposal, not an existing verified implementation. If the device has no suitable offline Russian voice installed, report that limitation rather than silently switching to a paid/cloud voice.

## What this changes in the Jarvis plan

1. **Keep** the existing llama.rn local inference service and provider abstraction.
2. **Reuse** the existing Qwen3-ASR 0.6B path for Russian speech recognition, subject to verifying its catalog eligibility, download and on-device transcription.
3. **Do not duplicate** Whisper or Qwen ASR infrastructure.
4. **Prototype** free Android TextToSpeech separately; make voice selection and offline availability explicit.
5. **Build the assistant loop** only after these individual paths pass: user-approved mic capture → local ASR → existing local LLM → permission-gated action/tool → local TTS.
6. **Keep wake-word always-on listening out of the first slice.** It needs a separate battery/privacy/foreground-service design and device validation; a microphone button or hands-free session is not proof of a persistent hotword engine.

## Required next verification

### Static / repository checks
- Inspect shared `@offgrid/models` catalog entry for `ggml-org/Qwen3-ASR-0.6B-GGUF`: exact filenames, sizes, hashes, min-RAM gate and Russian language mapping.
- Inspect model picker and settings to establish how the Qwen ASR option is exposed in the current fork.
- Inspect whether any Android TTS bridge or voice-output implementation already exists before adding one.
- Inspect existing tests for `QwenAsrEngine`, `WhisperService`, language selection and memory admission.

### Physical OPPO Find X6 Pro acceptance
- Download over Wi-Fi only; record exact model files and hashes.
- Disconnect the network after download.
- Transcribe a fixed Russian prompt set (quiet speech, normal speech, names/numbers, noisy environment).
- Record success/failure, transcription latency, peak app memory, device temperature and battery delta.
- Test TTS with airplane mode enabled and verify Russian voice output.
- Confirm ASR and LLM do not compete for RAM: unload/eject behavior must remain safe.
- Keep the current app/model as rollback.

## Budget and privacy
- Zero paid APIs, subscriptions, API keys, hosted inference, paid runners or cloud fallback.
- Model download may use the network once; inference and speech processing must remain on-device.
- Do not upload microphone audio, transcripts, prompts, screen content or personal data.
- No app source code, APK, release, billing configuration or secrets were changed by this audit.

## Evidence and references

Inspected fork files:
- `package.json`
- `src/services/llm.ts`
- `src/services/providers/localProvider.ts`
- `src/services/whisperService.ts`
- `src/services/qwenAsrModel.ts`
- `src/services/qwenAsrEngine.ts`
- `src/services/whisperModels.ts`
- `src/services/whisperModelDownloads.ts`
- `src/hooks/useWhisperTranscription.ts`
- `docs/ARCHITECTURE.md`

Official model reference:
- Qwen3-ASR supported languages and model family: https://github.com/QwenLM/Qwen3-ASR
- GGUF conversion and llama.cpp usage: https://huggingface.co/ggml-org/Qwen3-ASR-0.6B-GGUF
- OGAM README / free-vs-Pro voice distinction: https://github.com/sokfrut-tech/OGAM/blob/main/README.md

## Status
**Source inspection: completed for the files listed above.**
**Build/tests: not run in this audit.**
**Physical-device verification: pending.**
**Free offline TTS: not yet implemented or verified.**
**Full Jarvis wake-word assistant: not yet implemented or verified.**
