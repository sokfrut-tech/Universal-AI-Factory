# BRIDGE ONE — transfer and channel boundary findings

Date: 2026-11-24

## Existing Factory exchange channel is not the device-executor protocol
Reviewed `coordination/shared/AGENT_EXCHANGE_PROTOCOL.md`.
It defines GitHub as an asynchronous mailbox for ChatGPT, Claude, and Gemini:
- agent inbox/outbox Markdown files;
- a message is not considered delivered merely because it exists;
- a full read/respond/read-back correlation test is required;
- GitHub Actions structural checks do not prove an external agent read or answered the message.

This protocol does not define local Android/Termux executors 8493/8494, does not expose a phone shell, and does not define `BRIDGE_ONE_RESULT`. It must not be reused as an assumed executor protocol.

## Existing shared-assets transfer folder is image-specific
Reviewed `shared-assets/reference-images/README.md` and the Antigravity reference-transfer handoff:
- persistent folder is for reference images, logos, screenshots and design examples;
- `.transfer/` was a temporary bridge for compressed JPEG/base64 image copies;
- its workflow was created for image handoff to Antigravity, not arbitrary binary/source archive ingestion.

Therefore the image transfer mechanism is not a verified or approved route for BRIDGE ONE APK/XPI/source archive transfer.

## Transfer decision
- Do not place BRIDGE ONE private APKs/source archives in the public Factory repository or its public shared-assets folder.
- Do not treat the agent inbox/outbox as a binary transport or local command channel.
- The previously documented AppDeploy resource intake is also unsuitable for this purpose.
- A dedicated private authenticated intake is still required; it must have explicit authentication, upload size limits, retention policy, and a verified way for the analysis environment to retrieve the uploaded bytes.

## Evidence and status
- No BRIDGE ONE bytes were transferred.
- No local executor was activated or called.
- No device-side command was issued.
- No binary was decompiled, changed, or rebuilt.
