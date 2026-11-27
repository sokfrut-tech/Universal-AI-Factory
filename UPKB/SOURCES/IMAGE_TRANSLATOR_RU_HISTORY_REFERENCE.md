# Image Translator RU — conversation provenance and recovered requirements

- Project: `IMAGE_TRANSLATOR_RU`
- Canonical repository: not confirmed in the accessible GitHub inventory checked 2026-11-24.
- Evidence status: REPORTED / historical conversation retrieval; not a source-code verification.
- Historical conversation dates: 2026-11-11.
- Original Windows program intent: translate text inside images into Russian without changing the original image; save a separate translated copy.
- Historical assistant output mentioned ZIP candidates `Image_Translator_RU_Windows.zip` (v0.1), `Image_Translator_RU_Windows_v0.2.zip` and `Image_Translator_RU_Windows_v0.3.zip`; actual ZIP bytes were not located in the Library search performed on 2026-11-24. Do not claim these files are currently available or verified.
- Historical implementation discussion mentioned EasyOCR and Argos Translate. This is a reported design choice, not a verified dependency lock or working offline runtime.

## Recovered owner constraints

- Windows desktop application.
- Preserve the original image unchanged.
- Save a separate Russian-translated copy.
- Batch-process whole folders.
- Output directory: `Translated_RU`.
- Bilingual canvas: English/original text on the left, Russian translation on the right.
- The bilingual output canvas must have exactly the same pixel dimensions as the source image.
- Offline/autonomous operation is required.
- Architecture should allow additional source languages, with Russian as the target language.
- Preserve the original language text; do not overwrite it with Russian-only output.
- Manual correction/editing was included in the earlier v0.x concept.

## Evidence gaps

No canonical GitHub repository, original full specification file, source archive, executable, dependency lock, model weights, screenshots or reproducible build was located in this inventory. Earlier assistant statements about ZIP versions are historical claims only. No version is currently verified as buildable or runnable.

Do not conflate this Windows image-translation application with `sokfrut-tech/russ-translation-models`, which is a separate archive repository for offline translation models.

## Continuation gates

1. Recover the actual v0.1–v0.3 ZIP files or their original conversation attachments; inspect file bytes and hashes before importing.
2. If the files cannot be recovered, retain this reference as a requirements record and ask the owner for the original archive only when needed.
3. Verify EasyOCR/Argos Translate versions, model files, licenses, language coverage and offline behavior from actual manifests/code.
4. Test folder batch processing, source-image immutability, EN-left/RU-right composition, exact pixel dimensions and `Translated_RU` output.
5. Keep OCR extraction, translation, layout reconstruction and manual correction as separately testable stages.
6. Do not create a new canonical repository until existing archives and source history have been searched and preserved.
