# BRIDGE ONE — continuation research update

Date: 2026-11-24
Scope: recovery of original v9.3.0 artifacts and elimination of false-positive source candidates.

## 1. Library and attachment inventory
- Listed the user's Library recursively, filtering archives/APKs/XPI.
- The returned inventory contained 24 matching archive/application files; none was named `bridge_one_termux_bundle.tar.gz`, `bridge_one_universal_firefox.xpi`, `BRIDGE_ONE_Universal_WebView_v9.3.0.apk`, or `BRIDGE_ONE_Universal_Companion_v9.3.0.apk`.
- Current conversation attachment listing is empty.
- Semantic Library search for the exact BRIDGE ONE archive/APK names also returned no matching BRIDGE ONE artifact. Results were unrelated project files.
- Therefore the old attachments mentioned in prior conversation are not presently accessible as Library files or current-turn attachments in this session. Do not claim they are available for decompilation.

## 2. Connected GitHub repository inventory
- Listed all 12 repositories returned for owner `sokfrut-tech`.
- No repository is named BRIDGE ONE / bridge-one / bridge_one.
- `sokfrut-tech/voice-assistant` was inspected as a possible false-positive candidate:
  - README describes a simple Russian speech assistant with Vosk/system recognition, TTS, and map navigation.
  - MainActivity uses Android speech APIs and Vosk; no WebView JavaScript bridge, Termux server, MEM adapter, or executor dispatch is present in the inspected source.
  - Manifest requests RECORD_AUDIO and INTERNET and declares map package queries; no WebView/foreground service/executor components are declared there.
  - This repository is not BRIDGE ONE and must not be used as its source.
- `sokfrut-tech/Gemeni` was inspected by recursive tree (182 paths, not truncated):
  - Only two paths match broad bridge-name filtering: `BreenoBridgeProvider.kt` and `security_bridge.cpp`.
  - `BreenoBridgeProvider.kt` is a read-only Android ContentProvider exposing installed Breeno compatibility/version fields. It is not a WebView/Termux/agent executor bridge.
  - `security_bridge.cpp` is a small JNI SHA-256 wrapper. It is not a BRIDGE ONE executor bridge.
  - No paths matched Termux, WebView, executor, MEM 8495, 8493, or 8494 naming.
  - Gemeni is the separate Jarvis ColorOS Assistant project; do not conflate its Breeno compatibility provider with BRIDGE ONE.
- `voice-assistant` and `Gemeni` are now positively ruled out as BRIDGE ONE source candidates based on the inspected files.

## 3. Search-index caveat
- A follow-up batch of GitHub code-search requests was rate-limited (HTTP 429). No conclusions are drawn from that failed batch.
- Earlier exact identifier searches did not find BRIDGE ONE implementation in the connected account; apparent numeric matches in `Gemeni/repair-evidence/failed.log` were only timestamp fragments.
- No code-search results from unrelated public repositories are treated as evidence about this user's private/local build.

## 4. Current verified conclusion
- The connected repositories and accessible Library do not currently contain the original BRIDGE ONE v9.3.0 source/archive/APKs.
- The exact executor protocol for PC 8493 and Termux 8494 remains unknown.
- MEM 8495 is the only verified working service from the user's latest result.
- Executors 8493 and 8494 remain disabled per the current BRIDGE ONE brief.
- No device command was issued. No binary was modified, rebuilt, or functionally tested.

## 5. Next recovery path
A source-level protocol trace requires one of:
1. The original BRIDGE ONE repository URL/name or a Git bundle/ZIP of its source.
2. A private authenticated artifact-transfer route that makes the original Termux bundle/APKs available to this analysis environment.
3. A fresh attachment of the original archive in a chat where it is accessible as a current conversation file.

Once recovered, inspect in this order:
- Termux server routes and request dispatch;
- executor registry/service IDs and enable/disable state;
- request/response envelope and `BRIDGE_ONE_RESULT` serialization;
- MEM 8495 adapter/parser and `#!mem*` operations;
- WebView native bridge origin allowlist and JS-facing methods;
- Firefox extension transport and companion-app IPC;
- timeout, unavailable-service, partial-output, and error paths.

## Guardrails
- No shell/PowerShell commands to the user's phone while executors are disabled.
- Do not use unrelated Jarvis/voice-assistant/PowerShell-broker code as a guessed BRIDGE ONE protocol.
- Do not expose private APKs or source archives through public upload endpoints.
- No claim of decompilation, fix, rebuild, or successful functional test without artifact-level evidence.
