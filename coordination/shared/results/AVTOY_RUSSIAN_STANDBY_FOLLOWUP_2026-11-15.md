# AVTOY Russian standby follow-up — media-order gate correction

Date: 2026-11-15
Branch: `deploy/russian-tuqo-static-2026-11-15`
New commit: `e3ccc7eb8fa8225a522cf771f0e172b356d2679b`
Previous reviewed commit: `2ab8c4751cad6b105e6936eb9f597afbbc47639a`

## New defect found and fixed

The live-public-export safety helper `standby/scripts/media-order-eligibility.mjs` originally recognized only `item.type === "photo"` and `item.type === "video"`. It did not normalize image documents (for example `type:"document", mime_type:"image/jpeg"`) to photos, nor recognize the compatibility fields `mediaType` and `is_video`.

That allowed a mixed image-document/video album with no `mediaOrderKnown:true` proof to pass the live-export order gate. Downstream mirror and parity paths already normalize image documents, so this was an inconsistency and a real fail-open gap in the live export path.

Correction in commit `e3ccc7eb8fa8225a522cf771f0e172b356d2679b`:
- normalize image documents with JPEG/PNG/WebP/GIF MIME types to `photo`;
- recognize `mediaType` and `is_video` compatibility fields;
- retain fail-closed behavior when `mediaOrderKnown === false`;
- add tests for image-document + video, JPEG/PNG, compatibility fields, homogeneous albums, and explicitly verified mixed albums.

## Execution status

GitLab automatically created pipeline `3069961646` for the exact new commit, but it failed immediately with no jobs returned by the Jobs API. Pipeline details show no start time, no duration, and no YAML error. This is a pre-job infrastructure/pipeline execution failure; it does not establish that the new tests pass or fail.

The public Universal-AI-Factory runner is available for the AVTOY Worker suite, but it has not yet been wired to execute this private GitLab branch. The helper and test source are committed and verified by re-fetching the exact branch contents; they have not been executed in Node in this turn.

## Remaining release gates

- Execute `node --test scripts/media-order-eligibility.test.mjs` and the complete `npm run check && npm test` on this exact branch commit.
- Run a sanitized fixture through inventory → mirror (mocked Telegram responses) → snapshot build → parity → manifest → static build.
- Do not export live approved production data or deploy Pages until these gates pass and the owner explicitly approves.

No production Worker, KV, DNS, Telegram webhook, or paid resource was changed. This is a primary-coordinator source review, not an independent third-party audit.
