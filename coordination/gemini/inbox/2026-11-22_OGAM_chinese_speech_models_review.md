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

## Latest research/implementation snapshot (supersedes earlier head)
Current OGAM research branch head: `22df2e264245cd05203cc647144adec81f7d9fca` (research work remains on that branch).
Current implementation branch head: `ee505f901db3f0ee6a8d0026c333b306b2c45efa`.
New evidence to reconcile:
- sherpa-onnx v2.0.3 is the latest upstream release on 2026-11-22; official Android AAR is 52,411,426 bytes, SHA-256 `4c766e2e74c9d33d595338c21fe3b305c73ba45d47e96a235675c33142a2ec50`.
- Official Kotlin API emits callback PCM during generation, but Supertonic C++ still ignores callback return; native cancellation patch remains required.
- JNI path inspected is synchronous through `tts->Generate`; the prior suspicion of an async cross-thread callback is not proven. Please correct that nuance.
- CosyVoice3-MNN research branch reports Flow-only RTF estimate ~3.69 on Honor BKQ_AN90/Adreno 840 and explicitly fails real-time gate; demote from default conversational candidate.
- See updated `docs/jarvis/LOCAL_RUSSIAN_TTS_RUNTIME_EVALUATION.md` on the implementation branch for evidence links and details.

## Additional correction and new compact-model plan
Latest OGAM implementation branch head: `7b399c5261e09f365ca44d81fb053dbe68af8c08`.
Latest TTS docs now include `docs/jarvis/TINY_VOCA_RU_ANDROID_PORT_PLAN.md`.
Correction: the earlier ~3.69 CosyVoice Flow RTF was only the original 10-step Stage-1 estimate. Newer upstream two-step distillation results report a cool concurrent Honor BKQ_AN90 pipeline at RTF 0.63 and a hot post-preparation run at RTF 1.29. The student used only 20 train + 4 held-out Chinese utterances from one speaker; full runtime is ~2.25 GB PSS, ~1.3 GiB storage, 10–15 s cold start, and only SM8850 validated. Please update your ranking accordingly: CosyVoice is not batch-only, but high-resource experimental; tiny-voca-ru is the leading compact prototype pending frontend parity, exact model hashes and SM8550 tests.
Also audit tiny-voca-ru: 4.53M params, ~21.4 MB ONNX, Apache-2.0 weights/code, MIT RUAccent assets, CC BY 4.0 dataset, 61-symbol IPA frontend, lite homograph 56%, full model 91.6% against reference. Its published CPU speed is Ryzen 3600X only, not Android.