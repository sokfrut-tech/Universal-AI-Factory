# Universal AI Factory — Master Project Index
Updated: 2026-11-06

Purpose: the single entry point for resuming active projects without relying on chat history. Repository state is the durable source of truth.

## Global operating rules
1. ChatGPT is the default coordinator and implementer. Continue independently when external agents are unavailable.
2. Gemini is a quota-limited escalation expert only: use for a genuine blocker, difficult architecture choice, or independent high-risk review. Do not trigger on routine inbox pushes. Batch questions; keep retries low.
3. Claude API is optional. Missing ANTHROPIC_API_KEY must not block other work.
4. An agent plan is not an implementation. Require a patch/commit and test evidence. Empty ACK files are not deliverables.
5. Prefer free, local and offline-first solutions. No paid APIs or unexpected spending without explicit approval.
6. Before merge/deploy inspect the diff, run tests/build/security checks and verify the exact result. Failed required checks must block deployment.
7. Ask the user only for decisions, credentials, device actions or other steps that cannot safely be done by the agent. User mainly works from Android phone.
8. Maintain a cross-project technology radar: research useful tools, algorithms and implementation mechanics; adopt only after license, security, compatibility and test review. Research is not integration.

## Jarvis AI source audit
- Primary repository: [sokfrut-tech/Gemeni](https://github.com/sokfrut-tech/Gemeni).
- Repository-wide audit and cross-language source inventory: [docs/REPOSITORY_WIDE_AI_AUDIT_2026-11-06.md](https://github.com/sokfrut-tech/Gemeni/blob/main/docs/REPOSITORY_WIDE_AI_AUDIT_2026-11-06.md).
- Jarvis is an AI agent, not only a voice assistant. Preserve reasoning, planning, memory, perception, tool use, controlled learning and evidence-based execution as core product requirements.

## Cross-project technology radar
- Research snapshot and adoption gates: [docs/TECHNOLOGY_RADAR_AI_TOOLS_2026-11-06.md](TECHNOLOGY_RADAR_AI_TOOLS_2026-11-06.md).
- Reusable patterns: typed tools/skills, bounded agent loop, action verification, controlled memory, local-first fallbacks, safety confirmations, device E2E evidence and model provenance.

## Project index

| Project | Repository | Handoff | First resume step |
|---|---|---|---|
| Factory | sokfrut-tech/Universal-AI-Factory | docs/FACTORY_CONTINUATION_BRIEF.md | Audit dispatcher, workflows and a real end-to-end task |
| StampCleaner / Neon Club | sokfrut-tech/stamp-cleaner | https://github.com/sokfrut-tech/stamp-cleaner/blob/main/docs/PROJECT_HANDOFF_2026-11-06.md | Inspect PR #4/source; validate cleaning pipeline and dancer animation |
| RussSearchOPPO / Jarvis | sokfrut-tech/RussSearchOPPO | https://github.com/sokfrut-tech/RussSearchOPPO/blob/main/docs/PROJECT_HANDOFF_2026-11-06.md | Recheck PR #1/CI; make offline voice loop demonstrably work |
| Antigravity Mobile | sokfrut-tech/Antigravity-Mobile | https://github.com/sokfrut-tech/Antigravity-Mobile/blob/main/docs/PROJECT_HANDOFF_2026-11-06.md | Inspect APK/source/API; connect UI to real factory state |
| AVTOY KOREA | sokfrut-tech/avtoy-korea-auto | https://github.com/sokfrut-tech/avtoy-korea-auto/blob/main/docs/PROJECT_HANDOFF_2026-11-06.md | Recheck PR #55/Worker; verify private inquiries and Telegram media |
| Forest 4G | No dedicated repository confirmed | This document, below | Confirm measurements and create/confirm dedicated repo before implementation |

## Forest 4G connectivity — planning brief
Goal: reliable 4G deep in a forest, prioritizing reception margin and weather resilience over lowest price. A temporary shelter setup should later be portable to a future forest home. 5G is not required.

Known context: bands B3, B38, B31 (450 MHz), B20 and B7 have been discussed. Existing VARIUS Forester MIMO 2x2 antenna is installed but connection is unstable during weather changes.

Requirements:
- Confirm operator bands, signal measurements and router/modem support at the actual installation point.
- B31/450 MHz is a key requirement; verify chipset, firmware and operator compatibility, not just marketing claims.
- External MIMO antenna, appropriate connectors/cable-loss budget, weatherproof mounting, safe grounding/lightning protection.
- Keep vulnerable modem/router electronics protected indoors, not exposed on the mast.
- Consider dual-SIM/operator failover only after checking coverage and device support.
- Compare Russian-market/Ozon and KROKS options; verify specifications and availability.
- Prefer a compact kit transferable from temporary shelter to future home.

Next step: record operator/SIM, per-band RSRP/RSRQ/SINR, antenna model/cable and candidate datasheets. No purchase recommendation until B31 and environmental suitability are verified.

## Resume protocol
1. Open this index and the project handoff.
2. Recheck default branch, open PRs, latest commits, Actions, releases and deployment. Historical statuses below are leads, not live truth.
3. Read linked architecture, QA and decision documents; prefer newest source-backed evidence.
4. Inspect source before describing implemented functionality.
5. Start with the first unchecked P0 item. Make a small change and run targeted then full relevant checks.
6. Record commit SHA, exact tests/results, artifact URL and remaining risks.
7. Use status labels: Verified (checked now), Historical (must recheck), Planned, Implemented-unverified, Blocked (with evidence and next action).
