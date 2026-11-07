# Jarvis ACK Authentication Protocol v1

Status: proposed for integration; not production key provisioning.
Applies to: Message Broker v2.5 candidate.

## Required ACK metadata

An ACK Markdown file must contain YAML front matter with:

- `task_id`: unique ID of this ACK message.
- `from`: identity of the acknowledging participant.
- `to`: identity of the original task sender.
- `ack_task_id`: exact `task_id` of the task being acknowledged.
- `signature`: 64 hexadecimal characters, lowercase recommended.

The broker also checks that ACK `from` equals the original task's `Target` and ACK `to` equals the original task's `Source`.

## Canonical HMAC input

UTF-8 encode this exact string. Separators are single LF bytes (0x0A), with no CR bytes and no trailing LF:

```text
jarvis-ack-v1
<ack_task_id>
<from>
<to>
<task_id>
```

Here the final `<task_id>` is the ACK file's own task_id, not the original task's ID.

Compute HMAC-SHA256 using the shared secret bytes:

```text
signature = lowercase_hex(HMAC-SHA256(UTF8(secret), UTF8(canonical_input)))
```

The current PowerShell implementation uses UTF-8 bytes for the secret and canonical input. Signature comparison is fixed-length and accumulates byte differences rather than returning on the first mismatched byte.

## Secret handling

- Broker reads the secret from process environment variable `JARVIS_ACK_HMAC_KEY`.
- Missing secret is fail-closed.
- Secret shorter than 32 UTF-8 bytes is fail-closed.
- Never commit the secret, put it in a Markdown task, APK, log, or test artifact.
- CI uses an isolated test-only value; it is not a production credential.
- Before enabling real inter-agent ACKs, generate a cryptographically random secret of at least 32 bytes and provision it separately to each trusted participant through a secret manager or protected environment configuration.
- Define rotation and revocation procedures before production use.

## Security properties and limitations

HMAC authenticates possession of a shared secret and protects ACK contents from parties that do not know that secret. It does not provide non-repudiation or distinguish which participant used a shared secret if multiple participants share the same key. Prefer per-agent keys and a key-identity field in a future protocol revision if independent agent identity is required.

Do not enable Gemini HTTP transport or merge this candidate into production based only on CI. End-to-end signing and verification by the actual Gemini dispatch workflow and broker runtime remain separate release gates.
