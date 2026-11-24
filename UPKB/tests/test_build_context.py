"""Fail-closed context builder contract tests."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_context import BuildContextError, build_context


class BuildContextTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for relative, text in {
            "README.md": "UPKB",
            "CORE/RULES.md": "Rules",
            "CORE/SECURITY.md": "Security",
            "CORE/AGENT_START_PROTOCOL.md": "Start",
            "PROJECTS/P1/README.md": "Project P1",
        }.items():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        checkpoint = {
            "checkpoint_id": "CP-P1", "project_id": "P1",
            "updated_at": "2026-11-24T00:00:00Z", "updated_by": "test",
            "verification_status": "REPORTED",
        }
        self.write_json("PROJECTS/P1/CHECKPOINT.json", checkpoint)
        indexes = {
            "INDEX/MASTER_INDEX.json": {"schema_version": "1.0.0"},
            "INDEX/PROJECT_INDEX.json": {"projects": [
                {"project_id": "P1", "name": "Project One", "status": "VERIFIED", "next_action": "Continue"},
            ]},
            "INDEX/DOCUMENT_INDEX.json": {"records": [
                {"document_id": "D1", "project_id": "P1", "title": "Relevant"},
                {"document_id": "D2", "project_id": "P2", "title": "Unrelated"},
            ]},
            "INDEX/TASK_INDEX.json": {"records": [
                {"task_id": "T1", "project_id": "P1", "title": "Task"},
            ]},
            "INDEX/RESEARCH_INDEX.json": {"records": []},
            "INDEX/AGENT_INDEX.json": {"agents": [
                {"agent_id": "GPT", "agent_type": "GPT"},
            ]},
            "INDEX/ENVIRONMENT_INDEX.json": {"records": []},
            "INDEX/CHECKPOINT_INDEX.json": {"records": [
                {"checkpoint_id": "CP-P1", "project_id": "P1",
                 "path": "UPKB/PROJECTS/P1/CHECKPOINT.json", "updated_at": "2026-11-24T00:00:00Z"},
            ]},
            "INDEX/PULL_REQUEST_INDEX.json": {"records": []},
        }
        for relative, value in indexes.items():
            self.write_json(relative, value)

    def tearDown(self):
        self.temp.cleanup()

    def write_json(self, relative, value):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")

    def test_builds_context_with_exact_commit_and_project_scoped_records(self):
        packet = build_context(self.root, "P1", "a" * 40)
        self.assertEqual("P1", packet["project_id"])
        self.assertEqual("a" * 40, packet["upkb_commit"])
        self.assertEqual("CP-P1", packet["checkpoint"]["checkpoint_id"])
        self.assertEqual(["D1"], [item["document_id"] for item in packet["related"]["documents"]])
        self.assertEqual(["T1"], [item["task_id"] for item in packet["related"]["tasks"]])
        self.assertEqual("Rules", packet["core"]["rules"])

    def test_missing_checkpoint_fails_closed(self):
        self.write_json("INDEX/CHECKPOINT_INDEX.json", {"records": []})
        with self.assertRaisesRegex(BuildContextError, "no checkpoint"):
            build_context(self.root, "P1", "a" * 40)

    def test_checkpoint_identity_mismatch_fails_closed(self):
        self.write_json("PROJECTS/P1/CHECKPOINT.json", {
            "checkpoint_id": "WRONG", "project_id": "P1",
        })
        with self.assertRaisesRegex(BuildContextError, "checkpoint_id"):
            build_context(self.root, "P1", "a" * 40)

    def test_unknown_project_fails_closed(self):
        with self.assertRaisesRegex(BuildContextError, "exactly one project record"):
            build_context(self.root, "MISSING", "a" * 40)

    def test_unsafe_checkpoint_path_fails_closed(self):
        self.write_json("INDEX/CHECKPOINT_INDEX.json", {"records": [
            {"checkpoint_id": "CP-P1", "project_id": "P1",
             "path": "UPKB/../../outside.json", "updated_at": "2026-11-24T00:00:00Z"},
        ]})
        with self.assertRaisesRegex(BuildContextError, "unsafe checkpoint path"):
            build_context(self.root, "P1", "a" * 40)

    def test_invalid_commit_fails_closed(self):
        with self.assertRaisesRegex(BuildContextError, "40-character"):
            build_context(self.root, "P1", "not-a-commit")


if __name__ == "__main__":
    unittest.main()
