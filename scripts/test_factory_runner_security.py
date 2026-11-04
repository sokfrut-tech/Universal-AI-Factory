#!/usr/bin/env python3
"""Static regression checks for the factory runner's least-privilege boundary."""
from pathlib import Path
import re

workflow = Path(".github/workflows/factory-runner.yml").read_text(encoding="utf-8")
inbox = Path(".github/workflows/inbox-dispatcher.yml").read_text(encoding="utf-8")
whisper = Path(".github/workflows/verify-whisper-jarvis.yml").read_text(encoding="utf-8")

required = [
    "permissions:\n  contents: read",
    "type: choice",
    "avtoy-korea-auto",
    "RussSearchOPPO",
    "Antigravity-Mobile",
    "happ-proxy-pool",
    "persist-credentials: false",
    "actions/upload-artifact@v4",
    "retention-days: 14",
    "inventory_only",
    "no task auto-discovery",
    "secrets.FACTORY_TARGETS_READ_TOKEN",
    "Missing FACTORY_TARGETS_READ_TOKEN",
    "fetch-depth: 0",
    "for-each-ref --format='%(refname)' refs/remotes/origin",
    "Remote branch refs fetched:",
]
for marker in required:
    assert marker in workflow, f"missing security control: {marker}"

for forbidden in (
    "contents: write",
    "github.event.inputs.",
    "secrets.FACTORY_PAT",
    "secrets.GITHUB_TOKEN",
    "git push",
    "merge_pr_43_and_verify",
    "sync_task_to_target",
    "find . -maxdepth",
):
    assert forbidden not in workflow, f"unsafe legacy behavior remains: {forbidden}"

assert "\npush:\n" not in workflow, "push trigger must not run the manual audit"
target_checkout = workflow.split("name: Checkout allowlisted target (read-only)", 1)[1]
assert "fetch-depth: 0" in target_checkout.split("      - name:", 1)[0]
assert "token: ${{ secrets.FACTORY_TARGETS_READ_TOKEN }}" in target_checkout.split("      - name:", 1)[0]

# The old inbox workflow generated ACK-only receipts and pushed them to main.
# Until a real provider adapter exists, it must remain explicitly inert.
assert "permissions:\n  contents: read" in inbox
assert "workflow_dispatch:" in inbox
assert "contents: write" not in inbox
assert "secrets." not in inbox
assert "git push" not in inbox
assert "actions/checkout@" not in inbox
assert "did not invoke Claude" in inbox
assert "No task was read" in inbox

# Legacy Whisper workflow must remain inert and make no verification claims.
assert "permissions:\n  contents: read" in whisper
assert "contents: write" not in whisper
assert "secrets." not in whisper
assert "git push" not in whisper
assert "no verification is claimed" in whisper

task_pattern = re.compile(
    r"^coordination/(claude|gemini)/inbox/[A-Za-z0-9._-]+\.md$"
)
valid = [
    "coordination/claude/inbox/task-1.md",
    "coordination/gemini/inbox/2026-11-04_review.md",
]
invalid = [
    "../../secrets.md",
    "/tmp/task.md",
    "coordination/claude/inbox/../../secret.md",
    "coordination/claude/outbox/result.md",
    "coordination/claude/inbox/subdir/task.md",
    "coordination/claude/inbox/task;echo-pwned.md",
    "tasks/random.md",
]
assert all(task_pattern.fullmatch(item) for item in valid)
assert not any(task_pattern.fullmatch(item) for item in invalid)

print("OK: least privilege, allowlist, scoped cross-repo token, full branch refs, task-path boundary, no writes, report artifact, and inert legacy dispatchers.")
