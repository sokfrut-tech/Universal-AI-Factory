# AVTOY KOREA — static frontend / Object Storage integration blocker

**Date:** 2026-11-15  
**GitLab branch inspected:** `deploy/russian-tuqo-static-2026-11-15`  
**Production and cloud resources:** untouched.

## Confirmed incompatibility

The current static mirror scripts have two media URL models that are not yet joined:

- `build-static-catalog.mjs` validates that every media URL starts with `/media/`, copies local files into the output tree, and renders those local URLs into HTML.
- `publish-object-storage-media.mjs` is specifically a **Yandex Object Storage** uploader (uses Yandex IAM token, Yandex bucket, Yandex S3 endpoint and a configured public base URL). It returns an HTTPS URL map.
- `apply-object-storage-map.mjs` transforms the JSON snapshot's `/media/...` URLs into external HTTPS URLs.
- But the static HTML builder does not accept that transformed snapshot: it rejects media URLs not starting with `/media/`. It also copies media locally, which defeats the purpose of the separate object store.
- `verify-static-origin.mjs` currently rejects all external resource URLs in HTML/CSS and external runtime origins in JS, so it would also reject media embedded from a separate Object Storage host.

Therefore the current scripts do **not** yet provide a working static-site + separate-object-storage pipeline. This is a code integration gap, not a provider-registration problem.

## Provider-specific consequence

- The existing object-storage publisher is Yandex-specific. It does not upload to Cloud.ru.
- Cloud.ru remains a candidate provider from the free-tier research, but a Cloud.ru-compatible S3 adapter/configuration and its public-read/CORS/range behavior have not been implemented or tested.
- Do not assume the current GitLab branch can publish to Cloud.ru just because it uses S3-like object storage terminology.

## Required engineering fix before any deployment

Choose one of two coherent architectures and implement it consistently:

**A. Fully static bundle**
- Keep all media local under `pages/media/`.
- Static builder copies all media.
- No external media origin, no CORS dependency.
- Hosting capacity/size/traffic must be proven sufficient. SourceCraft public repo limits and large video practicality must be evaluated.

**B. Static frontend + external object storage**
- Snapshot contains local media paths before upload.
- Upload media and verify object hashes, MIME, length and public GET readback.
- Apply the remote URL map to a dedicated public snapshot.
- Update the static builder to allow only validated HTTPS media URLs from an explicit allowlist, while copying only local media.
- Update static-origin verification to allow only the exact configured media hostname for image/video resources; continue rejecting arbitrary external scripts, stylesheets, fonts, frames and runtime API dependencies.
- Test video byte-range requests (206), correct content-type, cache-control, HTTPS, anonymous read access and browser behavior.
- Add tests proving unknown hosts, credentials/query strings, unsafe paths and incomplete URL maps are rejected.

Do not broadly disable the external-origin verifier. Use a narrow host allowlist and only for media elements.

## Other confirmed findings
- SourceCraft is static-only, requires public repository output, has no custom-domain support and blocks Service Workers.
- The live AVTOY Worker page uses relative same-origin API paths and the inspected Worker has no CORS/preflight implementation. It cannot simply be moved to SourceCraft and continue calling the live API.
- The safer design is a generated public-only snapshot that has no dependency on live Worker APIs.
- No public output, media upload, bucket, DNS, Pages deployment, production export, account registration, card binding or payment has occurred.

## Next steps
1. Decide whether to implement fully static bundle or static frontend + external object storage. For a video catalog, B is likely more practical, but requires the narrow allowlist changes above.
2. Add integration tests for the selected flow and negative security cases.
3. Build a static prototype in a non-public staging directory and run it through the Factory Node runner with exact source hashes.
4. Only after a passing prototype, choose the actual provider. Do not recruit a Russian helper or spend money until a real registration gate is demonstrated and the user approves.
