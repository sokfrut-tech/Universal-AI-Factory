# BRIDGE ONE 9.3.0 — transfer-path assessment (2026-11-23)

## Goal
Inspect the actual BRIDGE ONE Android/WebView APKs, Firefox extension, and Termux bundle without asking the user to attach the same files again in ChatGPT.

## New check
Reviewed the connected AppDeploy binary-resource upload workflow.

## Finding
AppDeploy's resource intake is not a suitable recovery channel for the Termux bundle or source project:
- It accepts binary app resources only, under `public/resources/`.
- It explicitly excludes source files, source manifests, and complete projects.
- Upload completion is retained only temporarily (24 hours when unbound).
- The upload workflow is designed for later binding to an AppDeploy app, not for delivering a private source archive into this analysis environment.

The APK/XPI files are binary, but this intake still does not provide a verified private handoff into the analysis container. Therefore do not route the user's project binaries through this public-app-resource workflow.

## Current hard boundary
- The Termux service previously returned a healthy response on `127.0.0.1:8793`, but that address is local to the Android device.
- This cloud session cannot directly connect to the phone's localhost or download its files.
- Device-side executors 8493/8494 are disabled by the user's BRIDGE ONE brief; do not issue shell commands.
- Prior attachment limit remains in force; do not ask for repeated ChatGPT attachments.

## Safe next step
A private, authenticated transfer endpoint is required (for example, a private repository or private object-storage intake) with a device-side upload initiated by the existing Termux environment. Before proposing any device action, establish a concrete endpoint, authentication method, privacy boundary, size limit, and exact one-step transfer. Do not expose source archives through a public URL.

## Verification status
No source archive or APK was available in this session for byte-level inspection. No app has been modified. No repaired build or successful functional test is claimed.
