# Independent Research Audit — Mobile Offline ASR/TTS Candidates for OGAM / Jarvis

- **Date completed:** 2026-11-27
- **Inbox task:** `coordination/gemini/inbox/2026-11-22_OGAM_chinese_speech_models_review.md` (with all 4 follow-up snapshots up to `91996d2013950d3cb85bb60b4899f49c89e1750b`)
- **Scope & honesty boundary:** Source, metadata, patch and architecture audit grounded in inspected repository files (`src/services/qwenAsrEngine.ts`, `src/services/qwenAsrModel.ts`, `docs/jarvis/LOCAL_RUSSIAN_TTS_RUNTIME_EVALUATION.md`, `docs/jarvis/TINY_VOCA_RU_ANDROID_PORT_PLAN.md`, `patches/sherpa-onnx/v2.0.3-supertonic-callback-stop.patch`) and official runtime documentation. **No physical OPPO Find X6 Pro (`PGEM10` / `SM8550`) device benchmarks or ORT Android AAR builds were executed in this audit.**

---

## Executive Ranked Recommendation (Offline-First Russian on OPPO PGEM10)

| Rank | Role | Candidate | Verdict | Key Blocker / Gate |
|---|---|---|---|---|
| **1 (Active ASR)** | Speech-to-Text | **Whisper (`whisper.rn`) + Qwen3-ASR 0.6B (`llama.rn` CPU)** | Keep both side-by-side (`Whisper` proven baseline; `Qwen3-ASR` integrated in `src/services/qwenAsrEngine.ts`) | Run paired Russian WER + latency/thermal telemetry on physical `PGEM10`; no SM8550 QNN graph exists for Qwen3-ASR |
| **1 (Compact TTS)** | Text-to-Speech | **`tiny-voca-ru`** (`egnch/tiny-voca-ru`, 4.53M, ~21.4 MB ONNX, 24 kHz) | **Leading compact prototype** (`SENTENCE_CHUNKED` via `JarvisPcmStreamPlayer`) | Pin exact HF ONNX revision & SHA-256; establish Qwen3-TTS VoiceDesign F/M voice provenance; port full 61-symbol IPA/normalizer/stress Python frontend to Kotlin; measure ORT AAR footprint & SM8550 latency |
| **2 (Streaming Alt TTS)** | Text-to-Speech | **`sherpa-onnx v2.0.3` + `Supertonic-3`** (~99M params, 31 langs incl. `ru`) | Conditional fallback with callback PCM | C++ `OfflineTtsSupertonicImpl::ProcessChunksAndConcatenate()` ignores `0=stop` without applying/rebuilding `v2.0.3-supertonic-callback-stop.patch`; **OpenRAIL-M** use restrictions; ~380–415 MB weights & vendor ~832 MB peak RAM |
| **3 (Legal/Data Blocked)** | Text-to-Speech | **`GarAlex/local-tts` (Vosk 0.7 RU)** | Keep deferred | MIT C ABI, but `docs/CYRILLIC.md` marks dictionary/voice rights lineage unresolved |
| **4 (High-Resource Exp)** | Text-to-Speech | **`CosyVoice3-MNN`** | Experimental high-resource track ONLY (not compact default) | 2-step distillation measured on Honor `BKQ_AN90` / Adreno 840 only (cool RTF `0.63`, hot `1.29`, 20 train / 4 held-out Chinese speaker clips), ~2.25 GB PSS, ~1.3 GiB storage, 10–15 s cold start; **untested on SM8550** |
| **Excluded / Separate** | TTS | `Piper / eSpeak NG`, `TeraTTSv2`, `Danmoreng/qwen3-tts-android` | Not OGAM Apache/MIT default | Piper `piper-phonemize` is `GPL-3.0-or-later`; TeraTTSv2 ~1.17 GB + custom commercial-attribution OpenRAIL-M; Qwen3-TTS full batch & heavy RAM |

*(Note: in the separate native Kotlin app `sokfrut-tech/Gemeni`, offline Sherpa-ONNX Piper `ru_RU-dmitri-medium` / `ruslan` and `SherpaRussianAsrEngine` are already wired as a standalone native path with explicit licensing notice, separate from OGAM's Apache/MIT workspace boundary.)*

---

## Detailed Answers to Questions 1–8 (Reconciled with Latest Follow-ups)

### 1. Android ARM64 Runnable Reality vs Model-Card / Desktop Claims
- **`tiny-voca-ru` (`81x` RTF):** Strictly an **AMD Ryzen 5 3600X (4 CPU threads)** desktop benchmark (`onnxruntime`). Android ARM64 ORT throughput, peak RSS, and homograph runtime cost (`omograph.onnx` 10 MB INT8) are **unmeasured**.
- **`Supertonic-3` (~380 MB / ~832 MB RAM):** Derived from Soniqo SDK measurements on Galaxy S23 Ultra; HF repository total size is reported as ~415 MB depending on asset subset.
- **`CosyVoice3-MNN`:** Only validated on **SM8850 (Honor `BKQ_AN90`, Adreno 840)**, not on Snapdragon 8 Gen 2 (`SM8550`). The initial 10-step Stage-1 Flow estimate (~`3.69` RTF) is superseded by a 2-step distilled PoC (cool `0.63` RTF concurrent, **hot `1.29` RTF** after warmup, trained on 20 Chinese clips + 4 held-out from 1 speaker). With ~`2.25` GB PSS, ~`1.3` GiB weights and `10–15` s cold start, it cannot sit beside a local 3B–4B LLM on 12 GB RAM devices as a default conversational voice.

### 2. Qwen3-ASR on Snapdragon 8 Gen 2 (`SM8550`) & QNN/HTP Reality
- **Current OGAM integration (`src/services/qwenAsrEngine.ts` lines 41–54, `qwenAsrModel.ts`):** Runs `ggml-org/Qwen3-ASR-0.6B-GGUF` + audio projector `mmproj` (`llama.cpp` mtmd `qwen3a`) strictly on **Android CPU** (`n_gpu_layers: 0`, `devices: ['CPU']`, `n_ctx: 4096`).
- **QNN / HTP verdict:** Generic Snapdragon 8 Gen 2 (Hexagon V73) compatibility in Qualcomm QAIRT / sherpa-onnx / React Native wrappers is **not** proof that a Qwen3-ASR ONNX encoder/decoder or precompiled QNN context binary exists and works out of the box on `SM8550`. Treat both `llama.rn` Qwen3-ASR and sherpa ONNX Qwen3-ASR as **CPU-first paths** until an actual `SM8550` QNN graph, NPU delegate test, and APK native `.so` audit prove hardware acceleration.

### 3. Qwen3-ASR `llama.rn` (GGUF + `mmproj`) vs Sherpa ONNX Qwen3-ASR
- **`llama.rn` GGUF (`qwenAsrEngine.ts`):** Reuses OGAM's already-bundled `llama.cpp` runtime (zero extra ORT AAR APK bloat), supports language pinning prefill (`language <Name><asr_text>`), respects `minRamGb` memory gating (`qwenAsrModel.ts:83-90`). However, loading a second `llama.cpp` `4096`-token context competes directly with the main chat LLM context for RAM unless coordinated or unloaded between turns.
- **`sherpa-onnx` ONNX (`XDcobra/react-native-sherpa-onnx` or official AAR v2.0.3):** Official v2.0.3 Android AAR (`52,411,426` bytes, SHA-256 `4c766e2e74c9d33d595338c21fe3b305c73ba45d47e96a235675c33142a2ec50`) adds substantial native ABI footprint if duplicated alongside `llama.rn`. Russian WER/RTF comparison between `Whisper Small`, `Qwen3-ASR 0.6B GGUF`, and `Qwen3-ASR ONNX` on identical PGEM10 microphone recordings remains **unmeasured**.

### 4 & 5. Qwen3-TTS Android Wrapper & CosyVoice3-MNN Streaming Honesty
- **Wrapper vs model streaming distinction:** Even where a diffusion/flow model claims streaming conceptually, an Android wrapper API that returns a concatenated `Float32Array` waveform only after synthesizing the whole text is **`BATCH`** (or **`SENTENCE_CHUNKED`** if invoked one sentence at a time by Kotlin).
- Under OGAM's `JarvisTtsBackend` contract, wrappers that accumulate an entire waveform (`tiny-voca-ru` upstream `synthesize()`, batch `qwen3-tts-android`) **must** declare `JarvisTtsOutputMode.SENTENCE_CHUNKED` (invoked sentence-by-sentence via `JarvisSpeechChunker`) or `BATCH`, reserving `MODEL_STREAMING` solely for engines that genuinely deliver intermediate PCM blocks before generation ends.

### 6. Sherpa-ONNX v2.0.3 Supertonic Cancellation & JNI Correction
- **Cancellation bug confirmed:** `OfflineTtsSupertonicImpl::ProcessChunksAndConcatenate()` ignores the `GeneratedAudioCallback` return value (`0 = stop`, `1 = continue`). Calling `generateWithCallback` without rebuilding native `.so` with `patches/sherpa-onnx/v2.0.3-supertonic-callback-stop.patch` stops forwarding chunks to `JarvisPcmStreamPlayer`, but C++ inference continues burning CPU/battery until all text chunks finish. Therefore an unpatched build MUST set `supportsNativeCancellation = false`.
- **JNI thread-safety nuance corrected:** Inspection of the synchronous `OfflineTts::Generate` JNI call path shows callbacks execute synchronously on the caller thread inside `tts->Generate` rather than from an unattached background C++ worker thread. Thus local `jobject` / `JNIEnv*` capture is safe *as long as* synchronous invocation holds, though any future async thread pool in C++ would require `NewGlobalRef` and JVM `AttachCurrentThread`.

### 7. License, Provenance & Compliance Audit

| Component | Code License | Weights / Assets License | Dataset / Voice Provenance Risks | Gate |
|---|---|---|---|---|
| `tiny-voca-ru` | Apache-2.0 (`yilbegan`) | Apache-2.0 (`egnch`) + MIT (`ruaccent`) | `CC BY 4.0` (`20,287` clips / `23.82h`). F/M voices generated via **Qwen3-TTS 1.7B VoiceDesign**; reference speaker consent & exact HF ONNX SHA-256/revision still missing! | Attribution + resolve speaker provenance + pin immutable HF commit/SHA-256 |
| `sherpa-onnx` v2.0.3 | Apache-2.0 | Depends on model | Clean code AAR (`52.4 MB`), rebuilt AAR needed for Supertonic stop patch | Safe Apache-2.0 runtime |
| `Supertonic-3` | — | **OpenRAIL-M** | Use-based restrictions & mandatory notice/license pass-through (~415 MB HF / ~380 MB subset) | Legal review of OpenRAIL-M before bundling/distribution |
| `GarAlex/local-tts` (Vosk 0.7) | MIT | Model card Apache-2.0, **but caveat** | `docs/CYRILLIC.md` leaves dictionary/training-voice lineage unresolved | **Blocked** until rights chain cleared |
| `CosyVoice3-MNN` | Apache-2.0 | Model-specific (FunAudioLLM/CosyVoice terms) | Too heavy (~2.25 GB PSS) + Chinese-only 2-step PoC distillation | Experimental research only |
| `TeraTTSv2` | Custom python (`trust_remote_code`) | Custom `terattsv2-openrail-m-commercial-attribution` | `langswap/dialogs-ru-emotional-conversations` consent unverified + public product credit required + ~1.17 GB | Excluded from default |
| `Piper / eSpeak NG` | GPL-3.0-or-later (`piper-phonemize`) | Voice-dependent | Permissive/mixed voice packs, but `eSpeak NG` dependency introduces copyleft obligations | Excluded from OGAM Apache/MIT binary unless explicitly accepted |

### 8. Next Concrete Actions for `tiny-voca-ru` & OPPO `PGEM10` Validation

1. **Authorized Metadata Lock (No binary download needed first):** Query HF API (`https://huggingface.co/api/models/egnch/tiny-voca-ru?blobs=true`) to pin exact commit revision, `onnx/model.onnx`, `onnx/model.json`, `accent.onnx`, `omograph.onnx` sizes and SHA-256s, and verify the F/M Qwen3-TTS VoiceDesign provenance chain before adding to OGAM catalog.
2. **Audit `91.6%` Accuracy Attribution Explicitly:** Document clearly that `91.6%` is the `ruaccent turbo3.1` reference (vs `56.0%` for `tiny-voca-ru` lite mode), NOT an independent production pass on Jarvis Russian utterances.
3. **Evaluate ORT Android Footprint in Isolation:** Measure `com.microsoft.onnxruntime:onnxruntime-android` (`1.32.0` MIT) `arm64-v8a` AAR size delta, ProGuard/R8 rules, and cold-load RSS in a minimal instrumentation harness before adding ORT to main `OGAM`.
4. **Port 61-Symbol Python Frontend with Golden Fixtures:** Port `symbols.py`, `clean.py`, `numbers.py`, `normalize.py`, `stress.py`, `g2p.py` incrementally with bit-exact golden test cases from Python (never a lossy Cyrillic-to-ASCII shortcut).
5. **Reconcile `PGEM10` Gate:** Run the standardized Russian prompt suite on physical OPPO Find X6 Pro measuring cold load, TTFA, RTF (`cool` vs `15/30 min` hot), peak native RSS, barge-in latency (`100 ms / 500 ms`), and offline mode.
