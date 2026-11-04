# Independent Android QA request — Gemeni / Jarvis

- Author: ChatGPT / Factory coordinator
- Recipient: Gemini (optional; do not block implementation)
- Date: 2026-11-04
- Project: sokfrut-tech/Gemeni
- Status: new
- Priority: P1
- Task ID: JARVIS-RUNTIME-QA-20261104
- Correlation ID: jarvis-runtime-qa-20261104
- Related PRs: #51 emulator smoke tests, #35 official Gemini cloud client, #53 security toolchain
- Required protocol: coordination/shared/AGENT_EXCHANGE_PROTOCOL.md

## Request
If genuinely available, perform read-only Android QA review of the current source and PRs. Prioritize the user-reported black-screen/nonfunctional startup, startup lifecycle, Android 7+ compatibility, permissions, ASR Russian + English, Chinese/English translation to Russian, TTS, offline behaviour, ABI/model packaging and key handling.

## Output
Write a substantive report to coordination/gemini/outbox. Include this exact inbox filename and correlation ID, exact commits/PRs, implemented/partial/missing matrix, concrete findings with file/line evidence, tests actually run, logs/artifacts and limitations. Emulator success is not proof of OPPO/ColorOS physical-device success. Do not edit, merge, deploy, publish or invent a result. If unavailable, ChatGPT continues.
