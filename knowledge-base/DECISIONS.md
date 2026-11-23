# Decision Register
Append-only decisions and accepted invariants.

## DEC-001 — GitHub knowledge base is cross-agent durable memory
Date: 2026-11-23 | Agent: ChatGPT | Status: ACCEPTED
Maintain a human-readable, machine-searchable database in Universal-AI-Factory. Project repositories remain source of truth for code; UPKB provides cross-project index, document catalog, activity history, decisions, research and resume queue.

## DEC-002 — Evidence labels are mandatory
Date: 2026-11-23 | Agent: ChatGPT | Status: ACCEPTED
A plan, PR description, source implementation, passing static check, successful build, installed APK and device-validated behavior are separate evidence levels. Never collapse them into "done".

## DEC-003 — Preserve append-only history
Date: 2026-11-23 | Agent: ChatGPT | Status: ACCEPTED
Correct errors by appending a dated correction linked to the earlier record. Do not silently erase history.

## DEC-004 — Research adoption gate
Date: 2026-11-23 | Agent: ChatGPT | Status: ACCEPTED
No model/library/framework becomes a production dependency until source revision, license, security, platform support, hardware fit, reproducible tests and rollback path are reviewed.

## DEC-005 — Local-first privacy
Date: 2026-11-23 | Agent: ChatGPT | Status: ACCEPTED
Private context, conversations, contacts, calendar, files and device data must not be sent externally by default. Cloud fallback requires explicit per-request consent and exact disclosure of data leaving the device.

## DEC-006 — Mobile-first operator experience
Date: 2026-11-23 | Agent: ChatGPT | Status: ACCEPTED
Instructions must be short, exact and phone-friendly; avoid requiring manual repository/log inspection when an agent can inspect it.
