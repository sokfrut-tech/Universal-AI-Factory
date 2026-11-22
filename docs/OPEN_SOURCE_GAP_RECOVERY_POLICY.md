# Cross-project rule: recover unavailable capabilities from working open sources

**Status:** Mandatory global engineering rule  
**Applies to:** Every existing and future project, repository, factory, agent and technical workflow under `sokfrut-tech`  
**Effective:** 2026-11-22

## Core rule

**If something required is unavailable, inaccessible, private, discontinued, broken, or otherwise unusable, do not stop at the blocker and do not silently remove the feature. Search for working alternatives in public sources, inspect how they implement the capability, and integrate or adapt a suitable solution into our project.**

Third-party dependencies are allowed. We do not have to reimplement everything ourselves. Choose the best practical route:
1. Use an accessible and maintained dependency when it genuinely fits.
2. Vendor/adapt a suitable open implementation into our own repository when that gives us a reliable, self-contained result.
3. Reimplement the behavior from public specifications, tests and multiple references when direct reuse is unsuitable.
4. If no safe/usable solution exists, preserve the feature boundary, document the exact blocker, and continue with independent work rather than pretending it works.

## Mandatory recovery workflow

1. **Identify the gap:** record the exact unavailable component, required behavior, current failure evidence and affected consumers.
2. **Search broadly:** inspect official upstreams, public GitHub projects/forks, package registries, standards, technical papers and other credible open sources. Search for the capability/behavior, not only the original project's name.
3. **Inspect working implementations:** read actual source files, tests, dependency manifests, release/build instructions and issue history. A README, star count or claimed feature is not proof that it works.
4. **Compare candidates:** assess feature coverage, maintenance/activity, supported platforms/architectures, API compatibility, performance, offline behavior, security, dependency footprint, build reproducibility and migration cost.
5. **Check rights and provenance:** verify the exact repository and file-level licence, copyright notices, attribution, patents, model-weight/data/asset terms and transitive dependency licences. A public repository is not automatically open-licensed. Never copy code without a compatible licence. Respect copyleft obligations; when incompatible, use it as a behavioral reference and implement independently.
6. **Choose the integration path:** use a dependency, vendor a minimal source subset, adapt the implementation, or independently reproduce the behavior. Prefer the smallest complete vertical slice over wholesale copying of an unrelated application.
7. **Preserve product behavior:** map old contracts, data formats, user-visible features, security boundaries and edge cases. Do not replace a mature capability with a reduced demo or a no-op stub.
8. **Integrate into our project:** own the configuration, version pins, patches, tests, notices and operational documentation. Avoid unnecessary reliance on another party's private repository, account, secret or service. External services may be used when available and suitable; they must not become an undisclosed hard dependency.
9. **Prove it works:** add regression/contract tests, run focused and full relevant tests, clean install/build, security/licence checks and device/runtime verification where applicable. Test the exact commit being delivered.
10. **Record the result:** save source URLs, exact commit/tag, files reused/adapted, licence evidence, notices, dependency versions, tests/results, limitations and future update procedure in the project's repository and handoff.

## Non-negotiable safeguards

- No empty folders, fake packages, placeholder implementations, swallowed errors or skipped tests to make CI green.
- Never claim an alternative is integrated or working until code, configuration and verification evidence exist.
- Do not remove or downgrade a user-requested feature just because its original provider is inaccessible.
- Do not assume that a fork is current or complete; compare its base commit and feature coverage.
- Keep security-critical areas (cryptography, pairing, authentication, sync, permissions, payments and data deletion) behind explicit threat-model review and dedicated tests before replacement.
- Preserve original copyright and required notices. Track upstream changes and pin versions/commits for reproducibility.
- Do not introduce paid APIs, subscriptions, unexpected spending or new user accounts without approval. Prefer free/local/offline-capable choices when they satisfy the requirement.
- If credentials, permissions, hardware access or a user-only action are genuinely required, state exactly what is blocked and ask only for that action; continue all independent research and implementation meanwhile.

## Candidate evaluation record

For every adopted candidate, record:
- capability and project contract being replaced or extended;
- upstream repository/package and exact commit/version;
- source files and tests inspected;
- licence and attribution/NOTICE obligations;
- transitive dependencies and their licences;
- changes made locally and why;
- regression, build, security and runtime evidence;
- known gaps, risks, update strategy and rollback path.

## Definition of done

The capability is considered migrated only when the project owns a reproducible integration, required notices are preserved, old behavior is covered by tests, relevant checks pass, and runtime behavior is verified to the degree appropriate for the feature. Research alone is not implementation. A passing documentation-only CI run is not proof of a working product.

## Default instruction to every agent

When encountering an unavailable component, **search → inspect → compare → license-check → adapt/integrate → test → document**. Do not stop after reporting “inaccessible”. Apply this rule automatically to all existing work and every new project unless the user explicitly directs otherwise.
