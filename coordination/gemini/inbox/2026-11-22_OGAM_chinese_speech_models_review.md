# Independent research audit — Chinese mobile ASR/TTS candidates for OGAM

Date: 2026-11-22
Repository: https://github.com/sokfrut-tech/OGAM
Research branch: `docs/research-breeno-coloros-2026-11-22`
Implementation branch: `feature/jarvis-step-2-storage-privacy`

## Sources to audit
- Qwen3-ASR already integrated in OGAM via GGUF + mmproj + llama.rn. Read:
  - `src/services/qwenAsrEngine.ts`
  - `src/services/qwenAsrModel.ts`
  - `__tests__/integration/audio/qwen3AsrTranscription.rendered.test.tsx`
- sherpa-onnx Qwen3-ASR ONNX model and Kotlin API.
- `XDcobra/react-native-sherpa-onnx` TurboModule: Qwen3-ASR, QNN and TTS claims.
- `Nian27/CosyVoice3-MNN` Android v1.2.0 source and SM8850 measurements.
- `Danmoreng/qwen3-tts-android` and `Danmoreng/qwen3-tts.cpp`.
- sherpa-onnx v2.0.3 Supertonic-3 model and Android Kotlin API.
- Existing OGAM `docs/jarvis/LOCAL_RUSSIAN_TTS_RUNTIME_EVALUATION.md`.

## Questions requiring evidence
1. Confirm what is genuinely runnable on Android ARM64 and what is only a model-card claim or desktop benchmark.
2. Determine whether Qwen3-ASR sherpa ONNX can run on Snapdragon 8 Gen 2 / SM8550 and whether any QNN/HTP model-specific graph is published. Do not infer from generic QNN SoC support.
3. Compare GGUF+mmproj llama.rn Qwen3-ASR vs sherpa ONNX Qwen3-ASR on Russian quality, model size, memory and runtime, separating unmeasured metrics from verified evidence.
4. Verify the Qwen3-TTS Android wrapper's API: does it emit incremental PCM, or return a complete waveform? Check actual code, not model card.
5. Verify the CosyVoice3-MNN Android wrapper's API and hardware support; separate model-level streaming claims from app API behavior.
6. Inspect sherpa-onnx v2.0.3:
   - `GeneratedAudioCallback` contract says 0=stop / 1=continue.
   - `OfflineTtsSupertonicImpl::ProcessChunksAndConcatenate()` appears to ignore callback return.
   - `sherpa-onnx/jni/offline-tts.cc` captures `JNIEnv*` and local `jobject`.
   Confirm whether this is a real cancellation/JNI risk, with exact source references and any upstream fixes/issues.
7. Review model/code/voice/dataset licenses separately. Flag OpenRAIL-M restrictions, unresolved voice provenance and GPL/ LGPL dependencies.
8. Reconcile findings with OGAM's product requirements: Russian-first, offline, low-memory, chunk PCM, immediate barge-in, OPPO Find X6 Pro / PGEM10 (SM8550), no mandatory cloud.

## Deliverable
Write a detailed report to `coordination/gemini/outbox/REPORT_2026-11-22_OGAM_CHINESE_SPEECH_MODELS_REVIEW.md`. Include a ranked recommendation and exact evidence links. Do not modify OGAM code or claim PGEM10 testing without real device evidence.

## Follow-up snapshot
Current OGAM research branch head: `22df2e264245cd05203cc647144adec81f7d9fca`.
Current OGAM implementation branch head: `781d6e68ebc11b971892f521c05e3020b5f9d2a9`.
Please review the latest documents, especially the reconciliation with `LOCAL_RUSSIAN_TTS_RUNTIME_EVALUATION.md`, the Supertonic callback-stop patch and the distinction between model streaming claims and Android wrapper APIs. The new native TTS interface/chunker has source-contract audit evidence but no Gradle/JUnit/device validation.