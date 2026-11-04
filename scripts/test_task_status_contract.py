#!/usr/bin/env python3
"""Dependency-free regression tests for the factory task status contract."""
import json
import re
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "coordination/shared/task-status.schema.json").read_text())
ALLOWED_TRANSITIONS = {
    "new": {"received", "rejected", "cancelled"},
    "received": {"accepted", "blocked", "rejected", "cancelled"},
    "accepted": {"queued", "blocked", "cancelled"},
    "queued": {"dispatched", "blocked", "cancelled"},
    "dispatched": {"running", "failed", "blocked", "outcome_unknown"},
    "running": {"review", "partial", "failed", "blocked", "outcome_unknown"},
    "review": {"done", "partial", "running", "blocked"},
    "partial": {"accepted", "cancelled"},
    "blocked": {"accepted", "cancelled"},
    "failed": {"accepted", "cancelled"},
    "outcome_unknown": set(),
}
VALID_STATUSES = {
    "received", "accepted", "queued", "dispatched", "running", "review",
    "done", "partial", "blocked", "failed", "outcome_unknown", "rejected", "cancelled",
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
    if not re.fullmatch(
        r"coordination/(claude|gemini)/inbox/[A-Za-z0-9._-]+[.]md",
        event["source_message"],
    ):
        raise ValueError("source message must be a direct inbox markdown child")
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


def validate_transition(previous, current):
    if previous not in ALLOWED_TRANSITIONS or current not in ALLOWED_TRANSITIONS[previous]:
        raise ValueError(f"invalid task transition: {previous} -> {current}")


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
        self.assertEqual(set(SCHEMA["properties"]["status"]["enum"]), VALID_STATUSES)
        self.assertTrue(VALID_STATUSES.issubset(set(SCHEMA["properties"]["status"]["enum"])))
        self.assertTrue({"task_id", "correlation_id", "source_message", "status"} <= set(SCHEMA["required"]))

    def test_valid_transition_to_dispatched(self):
        validate_transition("queued", "dispatched")

    def test_received_cannot_jump_directly_to_done(self):
        with self.assertRaises(ValueError):
            validate_transition("received", "done")

    def test_done_is_terminal(self):
        with self.assertRaises(ValueError):
            validate_transition("done", "running")

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

    def test_outcome_unknown_is_allowed_but_not_automatically_retriable(self):
        validate_event(event("outcome_unknown"))
        with self.assertRaises(ValueError):
            validate_transition("outcome_unknown", "queued")
        with self.assertRaises(ValueError):
            validate_transition("outcome_unknown", "dispatched")

    def test_failed_requires_reason(self):
        with self.assertRaises(ValueError):
            validate_event(event("failed"))

    def test_path_traversal_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_event(event(source_message="coordination/claude/inbox/../../secret.md"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
