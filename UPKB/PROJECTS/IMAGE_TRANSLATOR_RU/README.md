# Image Translator RU

- Project ID: `IMAGE_TRANSLATOR_RU`
- Platform: Windows desktop (recovered from prior conversation)
- Repository: not confirmed
- Evidence status: REPORTED / historical conversation requirements recovered

## Goal
Translate text inside images into Russian without modifying the original image. Save a separate translated copy and preserve the original-language content.

## Recovered owner requirements
- Batch-process whole folders.
- Save output under `Translated_RU`.
- Produce a bilingual canvas with English/original text on the left and Russian on the right.
- The bilingual canvas must have exactly the same pixel dimensions as the source image.
- Work autonomously/offline.
- Allow additional source languages with Russian as the target.
- Include manual correction/editing.
- Preserve the source image unchanged.

## Historical implementation leads (not verified)
Earlier v0.x discussion mentioned EasyOCR and Argos Translate. Prior assistant outputs named ZIP candidates `Image_Translator_RU_Windows.zip` (v0.1), `Image_Translator_RU_Windows_v0.2.zip` and `Image_Translator_RU_Windows_v0.3.zip`. The actual ZIP bytes were not found in the Library search performed on 2026-11-24; do not claim they are currently available, buildable or runnable.

## Provenance
See [UPKB/SOURCES/IMAGE_TRANSLATOR_RU_HISTORY_REFERENCE.md](../../SOURCES/IMAGE_TRANSLATOR_RU_HISTORY_REFERENCE.md) for the recovered conversation date, exact constraints, missing artifacts and continuation gates.

## Professional terminology profiles
Required domains include radio communications, IT, electronics, programming, engineering, robotics, physics, mathematics and cybersecurity. Use domain dictionaries and context-aware terminology consistently across a batch.

## Evidence gaps
No canonical GitHub repository, original full specification file, source archive, executable, dependency lock, model weights, screenshots or reproducible build has been confirmed. Do not conflate this Windows application with `sokfrut-tech/russ-translation-models`, which is a separate model-archive repository.

## Next
Recover the actual v0.1–v0.3 ZIPs or original attachments and inspect hashes/content. If unavailable, keep this requirements baseline and obtain the original archive before implementation or creating a new canonical repository.
