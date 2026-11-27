# Jarvis voice audit addendum — Russian default and free TTS — 2026-11-25

This addendum corrects an important implementation detail found after the first audit note.

## Verified source detail: transcription language default

File inspected: `src/stores/whisperStore.ts` on `sokfrut-tech/OGAM` branch `main`.

The persisted Whisper state declares `transcriptionLanguage` and initializes it to:

```ts
transcriptionLanguage: 'en'
```

The Qwen3-ASR engine maps an explicitly selected language code to the model's language name and includes that name in the ASR prompt. Therefore, the fact that the model supports Russian does **not** prove the app currently selects Russian by default.

**Required acceptance:** set or select `ru` through the existing user-facing language setting, confirm that it survives app restart, and run a fixed Russian speech suite. Do not silently change the persisted default until the existing UI and migration behavior have been inspected and tests added.

## TTS scope

The OGAM README describes Kokoro on-device TTS as Pro-only. No free TTS implementation was confirmed in the inspected source files. Android platform `TextToSpeech` remains the first zero-cost prototype candidate, but it requires a small native bridge (or an existing compatible dependency) and a real device check for:
- installed Russian voice data;
- offline operation with airplane mode on;
- voice quality and intelligibility;
- lifecycle, interruption and audio-focus behavior;
- no cloud/network fallback.

## Current state

- Qwen3-ASR engine exists in source: **confirmed**.
- Official Qwen3-ASR model family supports Russian: **confirmed by upstream documentation**.
- App transcription language currently initializes as English: **confirmed in source**.
- Russian is selected by default in the installed APK: **not confirmed**.
- Free offline Android TTS in the app: **not confirmed / not implemented by this audit**.
- Wake-word always-on assistant: **not confirmed / not implemented by this audit**.
- Build, tests and OPPO runtime measurements: **not run in this audit**.

Source:
- https://github.com/sokfrut-tech/OGAM/blob/main/src/stores/whisperStore.ts
- https://github.com/QwenLM/Qwen3-ASR
- https://github.com/sokfrut-tech/OGAM/blob/main/README.md
