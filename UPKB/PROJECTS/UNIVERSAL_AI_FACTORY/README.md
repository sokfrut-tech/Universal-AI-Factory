# Universal AI Factory

- Project ID: `UNIVERSAL_AI_FACTORY`
- Repository: https://github.com/sokfrut-tech/Universal-AI-Factory
- Discovery source: `docs/MASTER_PROJECT_INDEX.md`
- Current UPKB branch: `feature/upkb-knowledge-base-bootstrap`

## Purpose
Cross-project agent orchestration, reusable factory workflows, CI and shared engineering infrastructure. UPKB is being bootstrapped here as a shared knowledge/discovery layer.

## Known constraints
- ChatGPT is default coordinator; Gemini is quota-limited specialist; Claude API optional.
- No empty ACKs. Require actual artifact/commit and test evidence.
- Failed required checks must block deployment.
- No paid services or unexpected spending without explicit approval.
- See `coordination/AI_AGENT_USAGE_POLICY.md` and `docs/OPERATING_STANDARD_HIGH_INTELLIGENCE_v1.0_2026-11-01.md`.

## Next
Audit dispatcher and workflows; define a minimal UPKB read/write integration contract; do not claim agent integration until an end-to-end task proves it.
