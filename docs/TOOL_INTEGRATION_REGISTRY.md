# Factory Tool Integration Registry

**Updated:** 2026-11-04  
**Scope:** Universal AI Factory and every current/future project owned by this workspace.  
**Rule:** this registry records verified capabilities and fallback routes. A listed tool is not considered connected merely because a repository contains a configuration file.

## 1. Available in the current ChatGPT workspace

| Tool / integration | Verified availability | Factory use | Boundary |
|---|---|---|---|
| GitHub MCP | Connected | Repositories, branches, PRs, files, workflow runs, artifacts, review comments | Repository permissions still apply; never expose tokens |
| PostHog MCP | Connected | Product analytics, feature flags, errors, traces and monitoring | Use only for projects actually connected to the relevant PostHog project |
| AppDeploy | Connected | App source inspection, resource/secret configuration, deployment and status | AppDeploy is not a Cloudflare control plane |
| MagicPath | Connected | UI canvas, component inspection, design-to-code workflow | Use for design/UI work only |
| ArmorCodex | Connected | Read/update coding-agent security policies and register intent plans | Policy changes must remain scoped and auditable |
| OpenAI Developers | Connected | OpenAI API/platform guidance and development workflows | Not a Google/Android documentation connector |

## 2. Required capability mapping and safe fallbacks

| Requested capability | Direct connector status | Factory fallback |
|---|---|---|
| Android CLI / SDK / Gradle | No dedicated Android CLI connector is exposed in this workspace | Run pinned Android SDK + Gradle commands in GitHub Actions; retain build logs, test reports, APK/AAB and SHA-256 as artifacts. Use local build only when a real runner is available. |
| Google Developer Knowledge MCP | No dedicated Google Developer Knowledge connector is exposed | Consult official Android/Google developer documentation; use Context7 only as an optional documentation index after installation, and verify critical APIs against official sources. |
| Cloudflare API / Workers | No dedicated Cloudflare connector is exposed | Use existing GitHub Actions workflows with narrowly scoped Cloudflare secrets and Cloudflare API calls. Never print secret values. Keep deployment approval separate from code changes. |
| Chrome DevTools | No dedicated Chrome DevTools connector is exposed | Use Playwright + Chromium in CI for browser smoke tests, console/network checks and screenshots. Label this as Playwright validation, not DevTools MCP. |
| Antigravity SDK | No dedicated Antigravity SDK connector is exposed | Use the SDK's official package/docs and repository-specific build/test workflow; do not invent SDK endpoints or claim a live SDK connection. |
| Universal AI Factory roles/skills | Factory standards and repo workflows exist | Apply dispatcher/architect, implementer, independent reviewer and QA/security roles. If separate agents are not actually invoked, label the review as a separate self-review. |
| Factory API / MCP Gateway | API code and Android client integration exist; provider execution was previously reported as not configured | Keep task submission, event transport and actual provider execution as separate health states. Never report a task as executed until a configured runner returns real execution evidence. |

## 3. Default tool selection by project

- **All repositories:** GitHub MCP for source/PR/CI evidence; security baseline from docs/CYBERSECURITY_SKILLS_FACTORY_STANDARD.md.
- **Android / OPPO / Jarvis:** Android SDK + Gradle CI, Kotlin/Android static analysis, emulator instrumentation where supported, APK verification and SHA-256. Browser tools are not a substitute for device testing.
- **Web / Worker:** GitHub CI, stack-appropriate tests, Playwright browser checks, secret/dependency scanning. Cloudflare deployment only through the project's approved workflow and secrets.
- **Analytics-enabled services:** PostHog for errors, traces, funnels and usage only after the project is connected to the correct workspace.
- **UI design:** MagicPath for editable design work; verify the exported implementation in the target app/browser.
- **Security:** ArmorCodex policy review plus deterministic CI scanners. Agent review never replaces scanners.

## 4. Connection and permission rules

1. Prefer already connected tools; do not install duplicate connectors.
2. Request installation only for a concrete missing capability and only after checking the plugin's actual tool list.
3. Do not bypass OAuth, account ownership, organization policy, approval gates, billing, repository permissions or secret protections.
4. A workaround may replace an unavailable connector only when it provides the same required observable check; label the substitute accurately.
5. Never store raw credentials in this repository. Store only secret names, scopes, and configuration status.
6. Keep least-privilege permissions, explicit timeouts, concurrency controls and auditable logs.
7. Do not deploy, publish, rotate credentials, change DNS, or mutate production infrastructure merely because a connector is available. Those remain separate authorization boundaries.

## 5. Acceptance checks for future tool onboarding

A tool is **CONNECTED** only after a real authenticated read-only smoke test succeeds. It is **OPERATIONAL** only after a safe representative operation and its result are verified. Otherwise use **AVAILABLE**, **NOT INSTALLED**, **NOT CONFIGURED**, **BLOCKED**, or **FALLBACK ACTIVE**.

For every onboarding change, record:
- exact tool/provider and verified tool names;
- repositories/projects in scope;
- permission boundary and secret names (never values);
- smoke-test evidence and timestamp;
- fallback route and its limitations;
- owner action still required, if any.

## 6. Current status snapshot (2026-11-04)

- Connected in this workspace: GitHub, PostHog, AppDeploy, MagicPath, ArmorCodex, OpenAI Developers.
- Not exposed as dedicated connectors: Android CLI, Google Developer Knowledge, Cloudflare, Chrome DevTools, Antigravity SDK.
- Fallback routes are documented above; they must be implemented and verified per project before being reported as operational.
- The Factory API provider-runner limitation remains a separate blocker until an actual provider is configured and an end-to-end task run is observed.