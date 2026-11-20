# Ferrite DSP external-runner preflight — 2026-11-20

## Scope and safety

- Source repository: `sokfrut-tech/russsearchoppo`, branch `feat/ferrite-neon-vad`.
- Observed branch HEAD: `587cccbdd5889fbc0b767eb61af88941f3cafd44`.
- No changes were made to the GitLab repository or its `main` branch.
- GitLab pipeline IID 24 / ID `3091199404`, for the observed HEAD, failed immediately: `started_at=null`, `duration=null`, `queued_duration=null`. This is not evidence of a source compilation/test failure because no job started.
- The GitHub Actions workflow is manual-dispatch only and requires repository secret `GITLAB_READ_TOKEN`. No successful external-runner execution has been confirmed.

## Source-level checks against the runner workflow

The following items were verified directly from the current GitLab branch tree and file contents:

1. Ferrite DSL files present:
   - `tools/ferrite/vad.fe`
   - `tools/ferrite/ring_preroll.fe`
   - `tools/ferrite/whisper_pcm.fe`
2. All four JNI exports use `#jni(ru_russsearch_oppo_VoiceCore)`: `detect_voice_adaptive`, `ring_push_i16`, `ring_drain_to_f32`, and `pcm_i16_to_f32`. The compiler derives the Kotlin class filename from the JNI class suffix, so `VoiceCore.kt` is consistent with the DSL.
3. The Ferrite compiler CLI explicitly supports `--out <path>`, `--kotlin <path.kt>`, and `--lib <name>`; the workflow invocation matches these flags.
4. The host test `tools/ferrite/test_ferrite.c` includes `ferritecore.c`, and the branch contains `tools/ferrite/test_stubs/jni.h`. The workflow generates `app/src/main/cpp/ferrite/ferritecore.c` and includes both the generated-code directory and JNI test stubs, matching that include layout.
5. The CMake file conditionally adds the Ferrite subdirectory only when its CMakeLists exists and a prebuilt library is absent; it unconditionally adds `whisper.cpp`. The repository tree does not contain the whisper submodule directory, while `.gitmodules` declares its canonical path. The runner's pinned whisper restore is therefore still required.
6. App Gradle configuration is currently ARM64-only (`abiFilters += listOf("arm64-v8a")`) with minSdk 24 and NDK `27.2.12479018`. The external runner's x86_64 output is an additional cross-compile check, not evidence that the APK packages x86_64.

## Remaining unverified items

- The workflow has not yet been executed on GitHub Actions; secret availability and GitLab token authentication remain unverified.
- Rust compilation, generated output, ASan/UBSan tests, vectorization/SIMD checks, JNI symbol checks, and 16 KB ELF alignment remain unverified until a real run produces logs/artifacts.
- This workflow does not build an APK. APK build must wait for a verified Gradle bootstrap and restored CMake dependency graph.

## Next action

Owner must add `GITLAB_READ_TOKEN` (read_repository only) to GitHub repository Actions secrets and manually dispatch **Ferrite DSP — GitLab external verification** for `feat/ferrite-neon-vad`. Do not paste the token into chat or commit it.
