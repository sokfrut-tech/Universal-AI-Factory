# Factory Security Toolchain Catalog

**Owner:** Universal AI Factory  
**Status:** Implementation baseline; per-project execution is tracked in the rollout ledger.

This catalog maps the tools shown in the user's reference screenshots to real factory capabilities. It distinguishes CI scanners from tools that require a dedicated analyst workstation or an explicitly authorized test target.

## 1. CI / source and dependency analysis

| Tool | Factory role | Execution | Result |
|---|---|---|---|
| Gitleaks | Secret and credential exposure | GitHub Actions on PR/push/schedule | Fails on detected secrets; never print secret values |
| CodeQL | Deep static analysis of supported source languages | Existing stack-specific project workflows | SARIF artifact / Code Scanning where plan permits |
| Semgrep | Multi-language SAST and custom rules | Shared reusable GitHub workflow | SARIF artifact; findings fail the job |
| Trivy | Dependency, filesystem, secret and misconfiguration checks | Shared reusable GitHub workflow | Critical/High findings fail; SARIF artifact |
| Dependency-native audits | Ecosystem-specific package risk | Project workflow (npm/Gradle/Python/etc.) | Lockfile-aware findings |

## 2. Web/API dynamic testing

| Tool | Use | Execution policy |
|---|---|---|
| OWASP ZAP | Passive baseline web/API assessment | Authorized staging host only; reusable DAST workflow |
| Wapiti | Active web application vulnerability assessment | Manual, authorized target only; rate-limited |
| Nuclei | Template-based known-exposure/CVE/misconfiguration checks | Manual, authorized target only; curated tags and low request rate |

The DAST workflow refuses to run unless the caller supplies the exact authorization phrase, an HTTPS target, and the hostname is present in SECURITY_ALLOWED_HOSTS. Configure the GitHub security-lab environment with required reviewers before using it. Do not point these tools at third-party systems or production unless the asset owner has explicitly approved the scope and test window.

## 3. Runtime, Windows and network laboratory

| Tool from screenshot | Factory use | Deployment |
|---|---|---|
| Wireshark | Inspect DNS/TLS/HTTP metadata and app traffic; investigate unexpected egress | Dedicated isolated lab VM or test device; capture only authorized test traffic |
| Sysmon | Windows process, driver, network and registry event telemetry | Windows analysis VM; install from Microsoft Sysinternals and use a reviewed configuration |
| Process Hacker | Process tree, handles, modules, threads and connections | Legacy tool; prefer maintained System Informer for new deployments |
| System Informer | Maintained process inspection successor | Analyst Windows VM; verify signed release and source |
| Ghidra | Offline APK/ELF/PE reverse engineering and decompilation | Analyst workstation; record artifact SHA-256 and Ghidra version |
| IDA Free | Additional disassembly and binary triage | Optional analyst workstation; Hex-Rays license/feature limits apply |
| Binary Ninja | Interactive binary analysis and scripting | Optional analyst workstation; commercial licensing/trial applies |

These desktop tools are not GitHub-hosted runners and are not represented as having executed just because their names appear in a report. Their evidence is attached to a task as a redacted report, tool version, target artifact hash and analyst notes. Do not upload signing keys, customer data, tokens, cookies or raw sensitive packet captures.

## 4. Project profiles

- **Android / native:** Gitleaks, CodeQL Kotlin/Java with a real Gradle build, Semgrep, Trivy, APK SHA-256, manifest/permission review; Ghidra and Wireshark in the lab; Sysmon only when investigating a Windows host.
- **Web / Worker / API:** Gitleaks, CodeQL JavaScript/TypeScript, Semgrep, Trivy, native dependency audit, ZAP/Wapiti/Nuclei against approved staging only; Wireshark for test traffic.
- **Python / service:** Gitleaks, CodeQL Python, Semgrep, Trivy and Python dependency audit; DAST only if an HTTP service is deployed.
- **Data/model repository:** Gitleaks, Trivy and manifest/schema validation; binary tools only if executable artifacts are present.

## 5. Evidence contract

Every security result records repository, commit SHA, tool/version, exact command/profile, run URL, findings/severity and remediation status. Use only PASS, FAIL, IN PROGRESS, NOT CONFIGURED, or NOT APPLICABLE. A tool that did not execute is not a PASS. A CI pass is not proof of production runtime security.
