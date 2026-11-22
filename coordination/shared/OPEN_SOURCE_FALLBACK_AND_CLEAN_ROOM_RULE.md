# Global engineering rule: open-source fallback and clean-room implementation

- Effective date: 2026-11-22
- Scope: all current and future projects, repositories, factories and agent handoffs owned or directed by sokfrut-tech.
- Status: standing project rule

## Mandatory rule

When a required feature, dependency, model, platform, repository or service is unavailable, inaccessible, discontinued, paywalled, region-locked or incompatible, do not silently drop the feature and do not stop at the first blocker.

1. Define the required behaviour as a platform-independent capability and identify the missing part precisely.
2. Search for public implementations and technical references across relevant ecosystems. Do not limit research to GitHub: include GitLab, GitCode, Gitee, AtomGit, ModelScope, OpenI, Hugging Face, Codeberg, vendor documentation, academic publications and other reputable public sources; include Chinese, Indian and other regional sources when relevant.
3. Compare multiple independent candidates. Inspect actual source, release history, build instructions, tests, dependency tree, model/card metadata and runtime evidence. A README, demo video, model name or marketing claim is not implementation proof.
4. Check repository code license, model/weight license, voice/dataset provenance, native-binary provenance, notices, redistribution terms and dependency licenses separately. Never infer that the license of a wrapper grants rights to its model assets or datasets.
5. Prefer a compatible, actively maintained, license-cleared open implementation where it fits. Otherwise reproduce the required behaviour independently using public platform APIs and documented protocols (clean-room implementation).
6. Never copy proprietary source, decompiled code, firmware, private APIs, OEM signing keys, authentication tokens, private endpoints or restricted assets without explicit rights. Do not bypass access controls. User-supplied binaries may be inspected read-only within authorized scope; do not install or execute unknown artifacts on a daily-use device.
7. Preserve the original capability requirement even if the original provider is unavailable. Update the plan with the chosen alternative, compatibility adapters, tests and any unavoidable limitations.
8. Mark evidence honestly: confirmed from source, inferred from identifiers/docs, not tested, blocked by missing artifacts/access, or verified at runtime. Never report an unavailable capability as implemented, or a plan as a working feature.
9. Save reusable findings, decisions, references, licenses, hashes and next steps in the project repository and link them from the central handoff. This must allow another agent to continue without the user copying chat context.

## Agent execution contract

- Do not ask the user to manually investigate source repositories when an authorized repository or research tool is available to the agent.
- Ask the user only for essential owner-controlled input that cannot be obtained safely (for example, an exact local APK, device test, or explicit permission).
- If an external service is unavailable, continue with a public reference and clean-room alternative; do not create a no-op stub that falsely reports success.
- Do not merge code or choose a production model solely because a candidate was found. Apply licensing, build, test, security and target-device gates.
- Keep paid/cloud services optional unless the user explicitly chooses otherwise. For local-first projects, do not introduce silent network fallback.

## Required handoff fields

For every significant blocked feature, record:
- desired user-visible behaviour;
- exact missing dependency/access/capability;
- source candidates inspected and source links;
- license/provenance status;
- chosen alternative or why none is acceptable;
- files/modules to implement;
- acceptance tests and target environments;
- known gaps and the next responsible action.

This rule is mandatory for every current and future project; it is not limited to OGAM / Jarvis.
