"""Negative and positive contract tests for the UPKB JSON Schemas."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from build_context import BuildContextError, build_context

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "SCHEMA"


def load_schema(name):
    schema = json.loads((SCHEMA_DIR / f"{name}.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())



class ContextBuilderContractTests(unittest.TestCase):
    COMMIT = "a" * 40

    def make_root(self, base, include_readme=True, checkpoint_path="PROJECTS/P1/CHECKPOINT.json"):
        root = Path(base) / "UPKB"
        (root / "CORE").mkdir(parents=True)
        (root / "INDEX").mkdir()
        (root / "PROJECTS" / "P1").mkdir(parents=True)
        for name in ("RULES.md", "SECURITY.md", "AGENT_START_PROTOCOL.md"):
            (root / "CORE" / name).write_text("test core", encoding="utf-8")
        (root / "README.md").write_text("UPKB test", encoding="utf-8")
        if include_readme:
            (root / "PROJECTS" / "P1" / "README.md").write_text("Project context", encoding="utf-8")
        checkpoint = {"checkpoint_id": "CP-1", "project_id": "P1", "verification_status": "REPORTED"}
        (root / "PROJECTS" / "P1" / "CHECKPOINT.json").write_text(json.dumps(checkpoint), encoding="utf-8")
        indexes = {
            "MASTER_INDEX.json": {},
            "PROJECT_INDEX.json": {"projects": [{"project_id": "P1", "name": "Project One"}]},
            "DOCUMENT_INDEX.json": {"records": []},
            "TASK_INDEX.json": {"records": []},
            "RESEARCH_INDEX.json": {"records": []},
            "AGENT_INDEX.json": {"agents": []},
            "ENVIRONMENT_INDEX.json": {"records": []},
            "CHECKPOINT_INDEX.json": {"records": [{
                "checkpoint_id": "CP-1", "project_id": "P1",
                "path": checkpoint_path, "updated_at": "2026-11-24T00:00:00Z",
            }]},
            "PULL_REQUEST_INDEX.json": {"records": []},
        }
        for name, value in indexes.items():
            (root / "INDEX" / name).write_text(json.dumps(value), encoding="utf-8")
        return root

    def test_context_packet_contains_exact_commit_and_project_checkpoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            packet = build_context(root, "P1", self.COMMIT)
            self.assertEqual(self.COMMIT, packet["upkb_commit"])
            self.assertEqual("P1", packet["project_id"])
            self.assertEqual("CP-1", packet["checkpoint"]["checkpoint_id"])
            self.assertEqual("Project context", packet["project_readme"])

    def test_context_builder_fails_closed_when_project_readme_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp, include_readme=False)
            with self.assertRaisesRegex(BuildContextError, "PROJECTS/P1/README.md"):
                build_context(root, "P1", self.COMMIT)

    def test_context_builder_rejects_checkpoint_path_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp, checkpoint_path="../outside.json")
            with self.assertRaisesRegex(BuildContextError, "unsafe checkpoint path"):
                build_context(root, "P1", self.COMMIT)

    def test_context_builder_requires_exact_source_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            with self.assertRaisesRegex(BuildContextError, "exact 40-character"):
                build_context(root, "P1", "unknown")

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


    def test_agent_report_schema_requires_exact_context_and_execution_evidence(self):
        validator = load_schema("agent_report")
        record = {
            "report_id": "RPT-1", "project_id": "P1", "task_id": "T1",
            "agent_id": "GEMINI", "agent_type": "GEMINI", "model": "test-model",
            "upkb_commit": "a" * 40, "context_id": "P1@" + "a" * 40,
            "execution_status": "partial", "generated_at": "2026-11-24T00:00:00Z",
            "summary": "Analysis completed with unverified items.",
            "changed_files": [], "evidence": ["https://example.org/run"],
            "checks": [{"name": "unit tests", "result": "passed", "exit_code": 0}],
            "unverified": ["Physical device"], "next_action": "Review report",
            "verification_status": "REPORTED",
        }
        self.assertEqual([], list(validator.iter_errors(record)))
        record["upkb_commit"] = "unknown"
        self.assertTrue(list(validator.iter_errors(record)))
        record["upkb_commit"] = "a" * 40
        record["checks"][0]["result"] = "green-ish"
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
