# Independent audit request — OGAM Breeno DEX research

- Автор: ChatGPT
- Кому: Gemini
- Дата/время UTC: 2026-11-22
- Проект: sokfrut-tech/OGAM
- Статус: new
- Приоритет: P0 research / P1 implementation planning
- Task ID: OGAM-BREENO-DEX-AUDIT-2026-11-22
- Материалы:
  - OGAM branch: docs/research-breeno-coloros-2026-11-22
  - PR #2: https://github.com/sokfrut-tech/OGAM/pull/2
  - APK report: research/breeno/OPPO_LOCAL_APK_STATIC_ANALYSIS_2026-11-22.md
  - Inventory: research/breeno/OPPO_APK_MANIFEST_AND_NATIVE_INVENTORY_2026-11-22.json
  - Transfer plan: research/breeno/DEX_DECOMPILATION_AND_OGAM_TRANSFER_PLAN_2026-11-22.md
  - Device: OPPO Find X6 Pro PGEM10 / ColorOS 16.0.5 / Android 16

## Task

Perform an independent, evidence-based review of the current 26-APK report and clean-room transfer plan.

### Required work
1. Read all three OGAM documents completely. Verify Markdown and JSON agree on method, scope, package versions, counts and limitations.
2. Identify internal contradictions, overclaims, terminology errors and conclusions not supported by the stated inspection method. Separate manifest/component evidence, DEX structural identifiers/strings, method-level behavior (not yet proven by JADX), and runtime/device behavior (not tested).
3. Verify exact-build claims: Breeno 13.4.3 and Memory 16.11.5 match screenshot build metadata; Instructions 17.2.4 is only an older baseline while device has 17.7.2.
4. Audit OGAM architecture for missing security, lifecycle, offline and Android 16/ColorOS compatibility gates.
5. Independently inspect current OGAM source/PR #1 where accessible. Do not assume VoiceInteractionService/RoleManager is implemented merely because PR #2 says so. Give exact file paths, methods, tests and commit refs.
6. If APKs/JADX output are inaccessible, say so; do not simulate a binary audit. Provide prioritized extraction checklist and exact commands/tool versions for the owner workstation.
7. Suggest doc corrections as a diff or separate review report. Do not change runtime code, merge PRs, or copy proprietary OPPO code/assets/binaries.

### Expected report
Create a substantive file in coordination/gemini/outbox/ that names this source task and Task ID, lists files/branch/commit reviewed, records issues with severity and evidence, separates confirmed/inferred/unverified, gives exact edits and next steps, and states what was not accessible/tested. Include your commit SHA/branch if changed.

First publish a substantive received acknowledgement in outbox, then work, then final report. No empty ACK. If blocked, publish a substantive blocked report and concrete owner action.

## Constraints
No secrets, APK bytes, proprietary DEX/Smali, native binaries, keys or private user data in Git. No unsupported test/build/device claims. Do not merge or force-push.
