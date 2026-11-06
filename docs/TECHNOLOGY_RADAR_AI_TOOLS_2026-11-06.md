# AI Technology Radar — 2026-11-06

Purpose: continuously identify useful open-source tools, algorithms, architectures and implementation techniques, then selectively adapt them across the user's applications and the Universal AI Factory. A repository being discovered or researched does NOT mean its code has been integrated.

## Standing user direction

Research practical AI tools and the underlying mechanics, not only repositories named Jarvis. Reuse useful capabilities across projects where they fit. Prefer free, open-source, local/offline-first and API-24-compatible Android options where feasible. No paid services or unexpected spending without explicit approval.

## Candidate review

### 1. Open Jarvis — Android agent reference
Source: https://github.com/tokenarc/open-jarvis
Upstream README describes Accessibility-based app control, screen OCR/vision, voice input/output, memory graph, app intelligence, skills, MCP support, scheduler, notification/clipboard intelligence, tutorial mode, risky-action confirmation, and action verification.
Potential adaptations for RussSearchOPPO:
- Typed tool/skill registry with explicit input/output schemas.
- Plan -> execute one action -> inspect screen/state -> verify -> recover loop.
- App capability catalogue and app-to-app task chaining.
- Local task history and useful preference memory.
- Permission and confirmation gates for sensitive actions.
- Tutorial mode that explains actions before executing them.
Do not copy the whole project blindly. Verify current source, license of every dependency, data handling, model-provider costs, Android API floor, permissions, and whether each claimed feature is actually implemented. Do not import cloud-provider requirements into the offline baseline.

### 2. Google ARTEMIS — Android automation and test reference
Source: https://github.com/google/artemis
Upstream describes natural-language Android workflow automation, logs, and integration with coding assistants; repository license shown as Apache-2.0.
Potential adaptations:
- Device-level E2E scenarios for launch, navigation, permissions and command execution.
- Action traces and screenshots as test evidence.
- Deterministic replay of critical workflows.
- Use as a QA harness before claiming ColorOS/OPPO runtime success.
Treat benchmark success claims as upstream claims, not proof for this app or device. Check device compatibility and actual setup cost before adopting.

### 3. PalmClaw — mobile agent architecture reference
Source: https://github.com/ModalityDance/PalmClaw
Upstream describes on-device sessions, context management, memory, skills, tools, agent loop, device integrations, channels, and explicit execution boundaries. The model may be provided by a configured API.
Potential adaptations:
- Modular agent loop separated from model provider.
- Structured device tools for files, calendar, contacts and hardware.
- Per-tool permission checks and workspace boundaries.
- Session memory and skill packages.
- Optional MCP/channel adapters without making them mandatory.
Keep local execution and user privacy as defaults; remote LLM providers remain optional adapters, not required infrastructure.

### 4. Sherpa-ONNX — offline speech stack
Source: https://github.com/k2-fsa/sherpa-onnx
Upstream supports local ASR, TTS, VAD, keyword spotting, speaker tasks, enhancement and source separation across Android and other platforms.
Potential adaptations:
- Experimental Russian ASR/TTS/VAD/KWS engine behind a stable speech interface.
- Retain Vosk as the known baseline until measured A/B results prove a replacement.
- Validate model licenses, checksums, ABI/native library collisions, APK size, memory, latency, battery and Russian accuracy.
- Do not claim a Russian wake word is solved until tested on the target phone.

## Reusable design patterns to evaluate across applications

1. Tool registry: each capability has a stable ID, schema, permission requirements, timeout, and typed result.
2. Agent loop: understand request -> make a bounded plan -> request confirmation when needed -> execute -> verify -> report.
3. Evidence-first execution: every important action produces a result or explicit failure, not a fake success/progress indicator.
4. Memory with controls: local task history and project state; avoid storing secrets or sensitive data; provide user-visible controls.
5. Skill packages: reusable, versioned capabilities with tests and clear permissions.
6. Fallback routing: local/free path first; optional external provider only when configured and approved.
7. Safety boundaries: destructive, financial, communication and privacy-sensitive actions require confirmation; deny-by-default for unknown tools.
8. Device automation QA: test on emulator and real target device; screenshots/logs and post-action assertions required.
9. Model/resource manager: downloadable models with provenance, license, checksum, storage estimate, RAM tier and uninstall option.
10. Cross-project reuse: move generic capabilities into factory libraries only after a working prototype and tests demonstrate reuse value.

## Integration gates

A candidate may move through these states:
- DISCOVERED — found, not yet inspected.
- REVIEWED — source, license, dependencies, security and compatibility inspected.
- PROTOTYPED — isolated proof of concept exists.
- TESTED — automated tests and target-device tests pass.
- ADOPTED — merged into a product with documented evidence.

Never describe DISCOVERED/REVIEWED/PROTOTYPED as integrated. Do not copy code or models until license and attribution obligations are understood. Preserve the current working baseline and integrate behind interfaces where practical.

## Immediate Jarvis priority

1. Finish and review PR #5 command regression tests and CI gate; it is green in the three observed workflow runs, but remains an open PR until reviewed/merged.
2. Create a typed AssistantTool/skill boundary and permission/confirmation policy before broadening device control.
3. Prototype screen/action verification and trace logging, borrowing ideas from Open Jarvis and ARTEMIS without importing whole projects.
4. Evaluate Sherpa-ONNX AAR/native libraries and Russian models in isolation; keep Vosk fallback.
5. Validate real OPPO/ColorOS runtime behavior before declaring features complete.

## Source references checked

- Open Jarvis: https://github.com/tokenarc/open-jarvis
- Google ARTEMIS: https://github.com/google/artemis
- PalmClaw: https://github.com/ModalityDance/PalmClaw
- Sherpa-ONNX: https://github.com/k2-fsa/sherpa-onnx

Last reviewed: 2026-11-06. Recheck upstream repositories and licenses before each actual adoption; this document is a research snapshot, not a permanent guarantee.
## Jarvis is an AI agent — product-level requirement
The owner explicitly clarified on 2026-11-06 that Jarvis is an artificial intelligence, not merely a voice assistant. The product architecture must provide reasoning/planning, persistent user-controlled memory, tool/skill use, device perception, voice, model routing, controlled learning, agent coordination and verified action execution. The full source inventory and current implementation gaps across all connected project repositories are documented in https://github.com/sokfrut-tech/Gemeni/blob/main/docs/REPOSITORY_WIDE_AI_AUDIT_2026-11-06.md.