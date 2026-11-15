# AVTOY KOREA — SourceCraft compatibility audit

**Date:** 2026-11-15  
**Repository inspected:** `sokfrut-tech/avtoy-korea-auto`  
**Base branch tree:** `d921807d2c71d51493b3c6574bff4ad933a54515`  
**Ordered-media PR head inspected:** `e5924ad5b13cd19c752deb0c06086b7644002343`  
**Production status:** untouched. No deployment, DNS change, export, or account registration.

## Findings

1. The repository tree on both main and PR #78 contains no `public/`, `index.html`, standalone frontend source directory, service-worker file, or web-app manifest. The tree has `worker.js`, tests, `wrangler.toml`, docs, and source assets only.
2. `wrangler.toml` declares Cloudflare Worker Assets at `./public`, but that directory is absent from the inspected Git trees. This mismatch must be resolved before assuming the repo itself can be directly published as a static site. Do not create a placeholder public directory or change production config without understanding the existing deployed source.
3. The public AVTOY site HTML is embedded in `worker.js` as a template string and returned by the Worker root route. The Worker also serves the admin page separately.
4. The embedded public page makes same-origin relative requests to:
   - `/api/request`
   - `/api/reviews`
   - `/api/cars`
   It also loads media from relative Worker API paths.
5. The inspected Worker source has no `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, or OPTIONS preflight handler. Therefore moving this frontend to SourceCraft's different origin and merely leaving API requests pointed at the existing Worker would fail browser CORS. SourceCraft does not offer a server-side proxy; its official docs say static HTML/CSS/JS only.
6. SourceCraft also blocks Service Workers and custom domains. No Service Worker was found in the inspected Git trees, but the absence of a file in this repo does not prove the deployed app has none. The public frontend currently does not show an obvious service-worker registration in the Worker HTML.

## Conclusion

**SourceCraft is not a drop-in mirror for the existing live AVTOY site.** It remains a possible host for a separately generated, sanitized static snapshot, but that requires a deliberate architecture:
- generate public-only JSON/HTML snapshot from approved records;
- place media in a separately accessible object store (Cloud.ru or another verified store);
- use absolute media URLs and configure bucket CORS/public-read safely;
- remove all dependence on same-origin Worker APIs from the static mirror, or add a separately reviewed CORS/proxy design (not production-authorized);
- ensure no client/admin PII, bot tokens, private records, or unapproved material enters the public SourceCraft repository.

The safer next technical step is to inspect the current live site's complete embedded HTML/API contract and the existing approved-media export builder, then produce a **non-deployed architecture prototype** and test it locally/through the Factory runner. Do not modify the production Worker, Cloudflare assets, KV, DNS, Telegram webhook, or publish a public mirror yet.

## Next actions
1. Review the root HTML in `worker.js` and enumerate all API routes and media dependencies.
2. Review the standby exporter/snapshot builder and verify whether it emits a complete static catalog with all media, privacy sanitization, and deterministic ordering.
3. Design the mirror so the frontend and media work cross-origin without relying on missing CORS headers.
4. Keep SourceCraft as a candidate only after a generated static prototype passes functional checks.
5. Do not recruit a Russian helper yet; try user-owned Yandex/Cloud.ru signup only when the technical path is selected. No card binding/top-up without explicit approval.
