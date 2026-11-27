# Jarvis APK: Russian UI localization audit

Date: 2026-11-25
Repository audited: `sokfrut-tech/OGAM`
Audited ref: `main`
Scope: read-only inspection of localization entry points and representative user-facing screens. No app source changed; no build, tests, or device checks were run.

## User requirement

The installed Jarvis AI APK must have a Russian-language interface, not merely a Russian app label or Russian speech-recognition option. Do not treat ASR language selection as UI localization.

## Confirmed source findings

1. `package.json` has no `i18next` or `react-i18next` dependency in the inspected dependency list. GitHub code search for `i18next`, `react-i18next`, `localization`, and `ru.json` returned no matches (code-search indexing may be incomplete, so this is evidence, not proof of absence).
2. Expected translation entry points such as `src/i18n.ts`, `src/i18n/index.ts`, `src/localization/`, `src/translations/`, `src/locales/en.json`, and `src/locales/ru.json` were not found at those paths.
3. Representative React Native screens contain English user-facing strings directly in JSX:
   - `src/screens/SettingsScreen.tsx`: Settings, Model settings, Document search, Remote servers, Security, Device information, Storage, Engine updates, etc.
   - `src/screens/ModelSettingsScreen/index.tsx`: General, Text, Image, Voice, Transcription model, Language, Voice turns, and related descriptions.
   - `src/components/TranscriptionLanguageSelect.tsx`: Language and English-only description copy.
4. Android `android/app/src/main/res/values/strings.xml` has English app/system labels (`Off Grid AI`, `Copy to Off Grid AI`, `Improve`). No `values-ru/strings.xml` was found at the expected path.
5. This is separate from speech recognition. `transcriptionLanguage: 'en'` in `src/stores/whisperStore.ts` controls speech-to-text, not the visible UI language.

Source links:
- https://github.com/sokfrut-tech/OGAM/blob/main/package.json
- https://github.com/sokfrut-tech/OGAM/blob/main/src/screens/SettingsScreen.tsx
- https://github.com/sokfrut-tech/OGAM/blob/main/src/screens/ModelSettingsScreen/index.tsx
- https://github.com/sokfrut-tech/OGAM/blob/main/src/components/TranscriptionLanguageSelect.tsx
- https://github.com/sokfrut-tech/OGAM/blob/main/android/app/src/main/res/values/strings.xml
- https://github.com/sokfrut-tech/OGAM/blob/main/src/stores/whisperStore.ts

## Conclusion

The inspected core UI is English-first and appears to use hard-coded English copy in at least the audited screens. Changing the APK display name to `Джарвис AI` and selecting Russian ASR does not translate the interface. The previously built Russian-named APK must not be described as fully Russian-localized.

## Recommended implementation plan

1. Create a proper localization layer with Russian (`ru`) as the default for this Jarvis build and English (`en`) as fallback.
2. Centralize strings in typed translation resources; do not perform blind global text replacement because it can alter prompts, model identifiers, logs, test fixtures, or user data.
3. Translate all user-facing surfaces, not just Settings: onboarding, tabs, chat composer, model catalog and downloads, permissions/errors, voice mode, dialogs, accessibility labels, notifications, Android system labels, and Pro/disabled-feature messaging.
4. Keep technical model names, filenames, URLs, code, and user-authored content unchanged.
5. Add tests for locale selection, fallback keys, and representative screen labels; add a source audit for untranslated UI strings.
6. Build a new APK only after CI checks pass. Keep it as a separate draft PR until reviewed. Physical OPPO verification remains a separate step.

## Status

- Russian speech-to-text support: separate feature; does not translate UI.
- Russian UI framework: not found in inspected source paths.
- Audited screens: English strings embedded directly in UI components.
- Complete Russian localization: not implemented.
- App code changed: no.
- Build/tests/device verification: none.
