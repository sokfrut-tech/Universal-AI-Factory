# Independent code review request — OGAM Jarvis native TTS groundwork

Date: 2026-11-22
Repository: https://github.com/sokfrut-tech/OGAM
Branch: `feature/jarvis-step-2-storage-privacy`
Current branch head when assigned: `96b0b966636a6ee1a3620a9e5a5967ab11b7b100`

## Scope
Independently review the following newly added Kotlin code and tests. Do not modify files or merge anything. Return a report with exact file/line references and severity.

1. `android/app/src/main/java/ai/offgridmobile/voice/JarvisTtsBackend.kt`
2. `android/app/src/main/java/ai/offgridmobile/voice/JarvisSpeechChunker.kt`
3. `android/app/src/test/java/ai/offgridmobile/voice/JarvisSpeechChunkerTest.kt`
4. `android/app/src/test/java/ai/offgridmobile/voice/JarvisTtsBackendContractTest.kt`
5. `android/app/src/main/java/ai/offgridmobile/voice/JarvisPcmStreamPlayer.kt`
6. `android/app/src/test/java/ai/offgridmobile/voice/JarvisPcmStreamPlayerTest.kt`

## Review requirements
- Check Kotlin syntax and Android/JVM compatibility with project's minSdk 24, Kotlin/Gradle pins and JUnit 4.13.2.
- Find chunker bugs with Russian abbreviations, initials, decimal numbers, punctuation across fragments, newline, very long tokens, whitespace, Unicode and reset/flush after barge-in.
- Check callback contract: stale chunks must not reach a newer AudioTrack generation; no callback on UI thread.
- Check TTS backend capability contract: batch vs sentence-chunked vs model-streaming, native cancellation honesty, sample-rate validation, resource lifecycle, request ID safety.
- Identify missing tests and propose exact tests.
- Do not claim tests passed unless you ran them in an environment with evidence. If private dependencies prevent Gradle, state the blocker.
- No proprietary code copying and no model/API dependency recommendations outside Apache/MIT-compatible code unless separately flagged for license review.

## Output
Write a substantive report to `coordination/claude/outbox/REPORT_2026-11-22_OGAM_JARVIS_TTS_KOTLIN_REVIEW.md`. Do not create empty ACK files.

## Follow-up snapshot (use this instead of the earlier assignment head)
Current implementation branch head: `781d6e68ebc11b971892f521c05e3020b5f9d2a9`.
Additional changes since the original request:
- Added `scripts/__tests__/jarvis-tts-backend.node.test.mjs` and wired it into the external dependency audit workflow.
- Source-contract audit run 423 passed on commit `a8113ac77c35108dc9f2a88da9f990923e9bbd08`: https://github.com/sokfrut-tech/OGAM/actions/runs/45058086277
- Fixed the stale assistant launch guard source assertion in `android-assistant-contract.node.test.mjs`.
- Added Supertonic callback-stop patch under `patches/sherpa-onnx/v2.0.3-supertonic-callback-stop.patch`; it is not applied to a compiled AAR.
Review the latest branch head, not the earlier snapshot. Gradle/JUnit and device tests are still not verified.

## Latest review target (supersedes earlier head)
Current OGAM implementation branch head: `ee505f901db3f0ee6a8d0026c333b306b2c45efa`.
Newer chunker changes since the prior snapshot:
- Handles closing quotes/brackets when identifying sentence ends.
- Handles spaced Russian abbreviations such as `т. д.`, `т. п.`, and `и т. д.`.
- Adds JUnit regression tests `keepsSpacedRussianAbbreviationsInsideTheSameSentence` and `closesQuotedSentenceBeforeStartingTheNextSentence`.
- Node source-contract test now checks for both regression fixtures and helper branches.
- A local isolated Kotlin compile/harness passed 7 cases, but Gradle/JUnit is still unverified.
Review this latest head. The full CI is blocked by private workspace package resolution and Jest load failures; do not attribute those to Kotlin without evidence.

## Final current implementation head for this review
Latest OGAM implementation branch head: `7b399c5261e09f365ca44d81fb053dbe68af8c08`.
No Kotlin source changes since the previous review target; the latest commits update TTS evaluation/port plan and handoff docs. Please still review the current Kotlin files at this branch head and include any chunker edge cases around max-length splits and abbreviation boundaries.