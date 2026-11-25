# OGAM voice settings and free TTS follow-up

Date: 2026-11-25
Repository audited: `sokfrut-tech/OGAM`
Audited ref: `main`
Scope: read-only source inspection. No application files changed. No build, tests, APK, or physical-device checks were run.

## Confirmed findings

### 1. There is already a transcription-language selector

- `src/screens/ModelSettingsScreen/index.tsx` renders the Voice tab and includes `TranscriptionLanguageSelect`.
- `src/components/TranscriptionLanguageSelect.tsx` uses the shared `transcriptionLanguages(...)` catalog, binds to `useWhisperStore`, and calls `setTranscriptionLanguage`.
- Qwen ASR and Whisper use separate model-specific language lists. The selector checks whether the persisted value is supported by the active model and falls back to the first available option if not.
- `src/services/qwenAsrEngine.ts` maps language codes to Qwen's language names using the same shared catalog, so the selector and model prompt are intended to stay aligned.

Source links:
- https://github.com/sokfrut-tech/OGAM/blob/main/src/screens/ModelSettingsScreen/index.tsx
- https://github.com/sokfrut-tech/OGAM/blob/main/src/components/TranscriptionLanguageSelect.tsx
- https://github.com/sokfrut-tech/OGAM/blob/main/src/services/qwenAsrEngine.ts

### 2. The English default is persisted

- `src/stores/whisperStore.ts` initializes `transcriptionLanguage: 'en'`.
- The same field is included in `PersistedWhisperState` and in `partialize`, so the selected value is stored in AsyncStorage.
- The store uses Zustand persist with a hydration-gated storage merge. Simply changing the initializer to `'ru'` would not necessarily change existing installs because the saved `'en'` value can be restored over the default.
- A safe change needs an explicit migration policy. Do not silently overwrite an existing user's deliberate English selection. For fresh installs, a Russian default is straightforward; for old installs, either preserve the saved preference and expose the existing selector, or introduce a one-time migration only if the product explicitly accepts treating legacy `'en'` as the old default.

Source links:
- https://github.com/sokfrut-tech/OGAM/blob/main/src/stores/whisperStore.ts
- https://github.com/sokfrut-tech/OGAM/blob/main/src/utils/hydrationGatedStorage.ts

### 3. Free core currently has no visible TTS settings

- `src/screens/ModelSettingsScreen/index.tsx` obtains the TTS settings component from `SLOTS.generationSettingsTts`; the comment explicitly describes it as a Pro feature injected through a slot.
- `src/bootstrap/slotRegistry.ts` documents the free-build behavior: empty slots render no Pro component.
- `package.json` contains no standalone React Native TTS dependency. The dependency list includes `@offgrid/speech`, but that is a shared workspace package, not proof of an Android TTS output implementation.
- `android/app/src/main/java/ai/offgridmobile/MainApplication.kt` manually registers existing native packages; no TTS package is registered there. This is not a complete proof that no auto-linked or shared TTS path exists elsewhere, so a repository-wide search/build inspection is still required before implementation.

Source links:
- https://github.com/sokfrut-tech/OGAM/blob/main/src/screens/ModelSettingsScreen/index.tsx
- https://github.com/sokfrut-tech/OGAM/blob/main/src/bootstrap/slotRegistry.ts
- https://github.com/sokfrut-tech/OGAM/blob/main/package.json
- https://github.com/sokfrut-tech/OGAM/blob/main/android/app/src/main/java/ai/offgridmobile/MainApplication.kt

## Recommended next implementation sequence

1. Inspect the shared speech package's exact language catalogue and the tests around `TranscriptionLanguageSelect` / `whisperStore`.
2. Decide the backward-compatible Russian-default migration explicitly. Keep the existing selector; do not add a duplicate setting.
3. Audit all source paths and dependencies for an existing TTS engine before adding anything.
4. If none exists, prototype Android's built-in `android.speech.tts.TextToSpeech` behind a small native module. Check Russian voice availability and whether the selected voice works offline on the target device. Do not assume that a downloaded system voice is present.
5. Keep TTS independent of Qwen ASR and the LLM residency slot where possible; avoid keeping multiple large models resident. Start speaking only after the assistant has a completed response, with stop/cancel controls and explicit user activation.
6. Verify tests/build in CI before producing another APK. Physical OPPO verification remains separate.

## Status

- Language selector: confirmed present.
- Russian Qwen3-ASR language support: confirmed by upstream model documentation in the previous research note.
- Current default: English, persisted.
- Free built-in Android TTS: candidate only; not implemented or device-verified.
- App code changes: none.
- Tests/build/device checks in this audit: none.
