"""Negative and positive contract tests for the UPKB JSON Schemas."""
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "SCHEMA"


def load_schema(name):
    schema = json.loads((SCHEMA_DIR / f"{name}.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


class SchemaContractTests(unittest.TestCase):
    def test_document_schema_rejects_missing_id_and_unknown_fields(self):
        validator = load_schema("document")
        self.assertTrue(list(validator.iter_errors({"title": "missing identity"})))
        self.assertTrue(list(validator.iter_errors({
            "document_id": "DOC-1", "project_id": "P1", "document_type": "other",
            "title": "Example", "status": "active", "verification_status": "VERIFIED",
            "created_at": "2026-11-24T00:00:00Z", "updated_at": "2026-11-24T00:00:00Z",
            "surprise": True,
        })))

    def test_document_schema_accepts_minimal_valid_record(self):
        validator = load_schema("document")
        record = {
            "document_id": "DOC-1", "project_id": "P1", "document_type": "other",
            "title": "Example", "status": "active", "verification_status": "VERIFIED",
            "created_at": "2026-11-24T00:00:00Z", "updated_at": "2026-11-24T00:00:00Z",
        }
        self.assertEqual([], list(validator.iter_errors(record)))

    def test_checkpoint_schema_rejects_invalid_evidence_status(self):
        validator = load_schema("checkpoint")
        record = {
            "checkpoint_id": "CP-1", "project_id": "P1",
            "updated_at": "2026-11-24T00:00:00Z", "updated_by": "test",
            "verification_status": "MAYBE",
        }
        self.assertTrue(list(validator.iter_errors(record)))

    def test_environment_schema_rejects_out_of_range_port(self):
        validator = load_schema("environment")
        record = {
            "environment_id": "ENV-1", "project_id": "P1", "host_type": "remote",
            "purpose": "test", "created_by": "test", "status": "running",
            "cleanup_policy": "never-auto-delete", "port": 70000,
        }
        self.assertTrue(list(validator.iter_errors(record)))


    def test_task_schema_validates_priority_and_required_fields(self):
        validator = load_schema("task")
        record = {
            "task_id": "TASK-1", "project_id": "P1", "title": "Inventory",
            "status": "active", "priority": "high", "owner": "GPT",
            "next_action": "Read source docs", "evidence": [],
            "verification_status": "REPORTED",
        }
        self.assertEqual([], list(validator.iter_errors(record)))
        record["priority"] = "urgent-ish"
        self.assertTrue(list(validator.iter_errors(record)))

    def test_agent_schema_rejects_unknown_agent_type(self):
        validator = load_schema("agent")
        record = {
            "agent_id": "GEMINI", "agent_type": "GEMINI", "status": "available",
            "capabilities": "Review", "verification_status": "REPORTED",
        }
        self.assertEqual([], list(validator.iter_errors(record)))
        record["agent_type"] = "UNREGISTERED"
        self.assertTrue(list(validator.iter_errors(record)))

    def test_pull_request_schema_rejects_malformed_commit_sha(self):
        validator = load_schema("pull_request")
        record = {
            "project_id": "P1", "repository": "owner/repo", "number": 7,
            "title": "Example", "head": "feature/example", "head_sha": "a" * 40,
            "base": "main", "draft": True, "url": "https://github.com/owner/repo/pull/7",
            "verification_status": "VERIFIED", "state": "open", "checked_at": "2026-11-24",
        }
        self.assertEqual([], list(validator.iter_errors(record)))
        record["head_sha"] = "not-a-sha"
        self.assertTrue(list(validator.iter_errors(record)))

    def test_research_schema_requires_provenance_and_adoption_state(self):
        validator = load_schema("research")
        record = {
            "research_id": "RES-1", "project_id": "P1", "title": "Model review",
            "source": "https://example.org/research", "source_date": "2026-11-24",
            "project_scope": ["P1"], "summary": "Reviewed candidate model.",
            "adoption_status": "under-review", "verification_status": "REPORTED",
        }
        self.assertEqual([], list(validator.iter_errors(record)))
        record["adoption_status"] = "deployed"
        self.assertTrue(list(validator.iter_errors(record)))

    def test_all_schema_files_are_valid_draft_2020_12(self):
        for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
            with self.subTest(schema=path.name):
                schema = json.loads(path.read_text(encoding="utf-8"))
                Draft202012Validator.check_schema(schema)
                self.assertEqual(
                    "https://json-schema.org/draft/2020-12/schema",
                    schema.get("$schema"),
                )


if __name__ == "__main__":
    unittest.main()
