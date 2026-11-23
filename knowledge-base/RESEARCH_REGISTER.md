# Research Register
Updated: 2026-11-23. Research is not adoption; candidate discovery is not a benchmark.

## R001 — China/India/worldwide local AI and assistant ecosystem
- projects: P014 / OGAM / Jarvis
- status: RESEARCHED_PARTIAL
- channels previously searched/reported: GitHub, GitLab, GitCode, Gitee, AtomGit, ModelScope, OpenI, Hugging Face and specialized Android/ML repositories.
- candidates/models previously identified: Sarvam-105B-1711 (India), Qwen family, DeepSeek V4 Flash, GLM, Kimi, MiniMax M3, MiniCPM, Hunyuan/WeVisOne, Ling; PocketWisdom/PocketPal; Native-LLM-for-Android; SmolChat-Android; Qwen3-ASR/TTS; LiteRT-LM/Omni; Fini.
- actual inspection: prior work specifically reported source/description audits of Fini and LiteRT Omni; other items are candidate leads with mixed inspection depth. No confirmed OPPO runtime comparison.
- prior artifacts reported: OGAM CHINA_INDIA_MODEL_LANDSCAPE_2026-11-22.md (commit 5e3142d); comparison plan (commit 714013d); handoff 0037df9; Gemini audit fdb796b. Resolve these abbreviated SHAs to full commits and exact paths.
- adoption: none implied.
- next: fetch referenced files from OGAM PR #2; validate source/revision/license/weights/hash/hardware; choose on-device candidates for Snapdragon 8 Gen 2 / Adreno / NPU; build reproducible Russian benchmark.

## R002 — OPPO/Breeno/ColorOS assistant research
- project: P003 / OGAM
- status: RESEARCHED_PARTIAL; evidence recorded in open draft PR #2.
- device: OPPO Find X6 Pro / PGEM10, ColorOS 16.0.5, build PGEM10_16.0.5.1201(CN01C20P01), Android 16.
- APK evidence: 26 owner-supplied APKs statically inventoried. Breeno 13.4.3_08c04e4_261110 and Breeno Memory 16.11.5_008719b_260901 matched device screenshots; SearchService 16.16.80 inventoried. Exact Instructions 17.7.2 APK missing; only 17.2.4 analyzed.
- inspected: hashes, ZIP inventory, signer fingerprints, decoded manifests/components/permissions, DEX structural identifiers/strings, native and asset inventories.
- not done: full JADX Java/Smali decompilation, complete apksigner verification, installation/execution, dynamic tracing and target-device tests. No proprietary code/assets/secrets committed.
- external source audits reported: ZorvAI (Apache-2.0), Eta (GPL-3.0), Phtomt (AGPL-3.0 canonical GitHub; mirror license discrepancy), PocketMind (Apache-2.0), AzCode (MIT), Aries AI (AGPL-3.0). License compatibility required; clean-room transfer only.
- next: obtain exact Instructions 17.7.2 APK; finish permitted static/dynamic analysis; map public Android APIs and OEM restrictions without copying proprietary implementation.

## R003 — Android local inference and speech
- projects: P002 / P003
- status: RESEARCHED_PARTIAL / IMPLEMENTATION_UNVERIFIED.
- candidates/components in earlier plans: llama.cpp JNI, Qwen family, GGUF, LiteRT-LM, MNN/QNN, OpenCL, Whisper/Vosk ASR, Silero VAD, Piper/Kokoro TTS.
- earlier Jarvis design selected llama.cpp JNI as first runtime spike; this is not proof of on-device inference.
- OGAM PR #2 records six local candidates: Qwen3.5-4B baseline, lower-refusal/abliterated experiments, Gemma 4 E2B/E4B; no weights downloaded and no production default selected at that evidence point.
- next: pin upstream commit, model revision, license, checksum, quantization and memory budget; compare quality/latency/RAM/thermal/audio across repeated Russian tests.

## R004 — Jarvis feature roadmap and agent architecture
- project: P002
- status: IMPLEMENTATION_IN_PROGRESS_UNVERIFIED.
- planned capability areas: planner/tasks, calendar, reminders/timers/alarms, web search/browser, local music/radio/media, maps/navigation, weather/news/utilities, voice, local memory/learning, phone/system control, SaveVideo and interactive orb.
- invariants: bounded/cancellable plans, typed allowlisted tools, per-action authorization, postcondition verification, private context local, cloud fallback off by default, no silent data egress.
- latest known Gemeni PR #148 title describes offline brain + Qwen2.5 + Piper RU voice + interactive orb + SaveVideo + Control Center. PR description is scope claim, not proof of complete integration. Exact-head CI/device validation required.
- next: inspect PR diff; classify each component implemented/stubbed/unverified; inspect tests and current Actions; install only after build gate and user authorization.

## R005 — Factory and Antigravity Mobile
- projects: P001 / P004
- status: IMPLEMENTATION_PARTIAL.
- Factory has docs, shared assets and coordination folders for ChatGPT, Claude and Gemini. Latest main push in repository metadata was 2026-11-22; latest visible commit refreshed OGAM review evidence.
- continuation brief requires explicit dispatch, Gemini only for material escalation, Claude optional, target-repo checkout and real patch/test evidence, no empty ACK and no routine dispatch.
- Antigravity PR #20 says main Worker bootstrap deployed 2026-11-04, D1 migrations and secret names configured, but runtime health needs independent check; provider dispatch disabled on main; deployed CORS origin https://localhost needs review before browser client.
- PR #19 is unmerged provider-dispatch candidate.
- next: verify Worker health, dispatcher, both Claude/Gemini inbox paths, target repo checkout and real end-to-end task.

## R006 — AVTOY KOREA
- project: P005
- status: ACTIVE_MAINTENANCE.
- current open PR list includes #81 durable MAX reply outbox, #80 specification, #79 operator commands and #78 Telegram mixed-media album order; #78 historically reported 152/152 Factory-runner tests, exact-head evidence must be refreshed.
- prior work includes PR #26 album grouping/edit-before-publish; later media quality, SEO and CI improvements.
- next: inspect #81/#80/#79 dependencies; reconcile #78 ordering; verify admin-only numbered inquiries, photo preservation/no duplicates/full resolution and Russia accessibility using current production evidence.

## R007 — Other repositories
- StampCleaner/Neon Club: PR #5 portrait video side panel/still mode, #4 Cyber Glam theme, #3 Android/web extraction parity.
- RussSearchOPPO: PR #15 safe agent contracts; earlier CI at cd205313 predates strict schema changes; fresh CI required. PR #12 model downloader and #11 Qwen spike remain open.
- Voice Assistant: separate repo with Vosk-related dependency updates and handoff; relation to Jarvis/RussSearchOPPO unresolved.
- russ-translation-models: model research repo; PR #3 handoff, #2 security tooling; no benchmark confirmed.
- happ-proxy-pool: PR #1 prototype using real Xray HTTPS checks; no operational quality guarantee established.
- sleep-button and breeno-apks: repositories exist; purpose/content not yet audited.
- Forest 4G: planning only; B31/450 MHz and weather resilience are key; no dedicated repo confirmed.

## R008 — Google Antigravity IDE DNS issue
- project: separate from Antigravity-Mobile.
- status: BLOCKED_HISTORICAL.
- prior diagnosis: cloudcode-pa.googleapis.com failed DNS through 10.255.255.254:53; HTTPS/proxy checks awaited. No resolution confirmed.
- next: recover exact diagnostics before prescribing changes.
