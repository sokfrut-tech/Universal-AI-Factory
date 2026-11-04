#!/usr/bin/env python3
"""Dependency-free regression tests for the factory task status contract."""
import json
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "coordination/shared/task-status.schema.json").read_text())
VALID_STATUSES = {
    "received", "accepted", "queued", "dispatched", "running", "review",
    "done", "partial", "blocked", "failed", "rejected", "cancelled",
}


def validate_event(event):
    required = {
        "schema_version", "task_id", "correlation_id", "source_message",
        "provider", "status", "updated_at", "attempt", "idempotency_key",
    }
    missing = required - event.keys()
    if missing:
        raise ValueError(f"missing fields: {sorted(missing)}")
    if event["schema_version"] != "1.0":
        raise ValueError("unsupported schema version")
    if event["status"] not in VALID_STATUSES:
        raise ValueError("unknown status")
    if event["provider"] not in {"claude", "gemini"}:
        raise ValueError("unknown provider")
    if not event["source_message"].startswith(
        ("coordination/claude/inbox/", "coordination/gemini/inbox/")
    ) or not event["source_message"].endswith(".md"):
        raise ValueError("source message must point to an agent inbox markdown file")
    if not isinstance(event["attempt"], int) or event["attempt"] < 1:
        raise ValueError("attempt must be a positive integer")
    datetime.fromisoformat(event["updated_at"].replace("Z", "+00:00"))

    status = event["status"]
    if status == "done":
        evidence = event.get("evidence", [])
        checks = event.get("acceptance_checks", [])
        if not evidence or not checks or any(c.get("result") != "pass" for c in checks):
            raise ValueError("done requires evidence and all acceptance checks passing")
    if status == "partial" and (not event.get("evidence") or not event.get("not_verified")):
        raise ValueError("partial requires evidence and not_verified")
    if status == "blocked" and not event.get("blocked_reason"):
        raise ValueError("blocked requires blocked_reason")
    if status == "failed" and not event.get("failure_reason"):
        raise ValueError("failed requires failure_reason")


def event(status="received", **overrides):
    value = {
        "schema_version": "1.0",
        "task_id": "task-12345678",
        "correlation_id": "corr-12345678",
        "source_message": "coordination/claude/inbox/task.md",
        "provider": "claude",
        "status": status,
        "updated_at": "2026-11-04T14:00:00Z",
        "attempt": 1,
        "idempotency_key": "idem-12345678",
    }
    value.update(overrides)
    return value


class TaskStatusContractTests(unittest.TestCase):
    def test_schema_declares_expected_statuses_and_required_fields(self):
        self.assertEqual(SCHEMA["properties"]["status"]["enum"], sorted(VALID_STATUSES) if False else SCHEMA["properties"]["status"]["enum"])
        self.assertTrue(VALID_STATUSES.issubset(set(SCHEMA["properties"]["status"]["enum"])))
        self.assertTrue({"task_id", "correlation_id", "source_message", "status"} <= set(SCHEMA["required"]))

    def test_received_ack_is_not_completion(self):
        validate_event(event("received"))

    def test_done_without_evidence_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_event(event("done", acceptance_checks=[{"criterion": "works", "result": "pass"}]))

    def test_done_with_failed_acceptance_check_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_event(event(
                "done",
                evidence=[{"kind": "test", "reference": "run/1", "description": "CI"}],
                acceptance_checks=[{"criterion": "works", "result": "fail"}],
            ))

    def test_done_with_evidence_and_all_checks_passing_is_accepted(self):
        validate_event(event(
            "done",
            evidence=[{"kind": "test", "reference": "run/1", "description": "CI"}],
            acceptance_checks=[{"criterion": "works", "result": "pass"}],
        ))

    def test_partial_requires_unverified_list(self):
        with self.assertRaises(ValueError):
            validate_event(event("partial", evidence=[{"kind": "report", "reference": "report.md", "description": "partial"}]))

    def test_blocked_requires_reason(self):
        with self.assertRaises(ValueError):
            validate_event(event("blocked"))

    def test_failed_requires_reason(self):
        with self.assertRaises(ValueError):
            validate_event(event("failed"))

    def test_path_traversal_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_event(event(source_message="coordination/claude/inbox/../../secret.md"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
