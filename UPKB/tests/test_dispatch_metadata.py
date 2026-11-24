"""Fail-closed Gemini dispatch metadata contract tests."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from resolve_dispatch_metadata import DispatchMetadataError, resolve_dispatch


class DispatchMetadataTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "coordination/gemini/dispatch").mkdir(parents=True)
        (self.root / "UPKB/INDEX").mkdir(parents=True)
        self.task = self.root / "coordination/gemini/dispatch/task.md"
        self.write_task("JARVIS_PRIMARY", "JARVIS-DEVICE-001")
        self.index = self.root / "UPKB/INDEX/TASK_INDEX.json"
        self.write_index([{
            "task_id": "JARVIS-DEVICE-001",
            "project_id": "JARVIS_PRIMARY",
            "status": "active"
        }])

    def tearDown(self):
        self.temp.cleanup()

    def write_task(self, project="JARVIS_PRIMARY", task="JARVIS-DEVICE-001", body="Inspect APK evidence"):
        self.task.write_text(
            f"---\nupkb_project_id: {project}\nupkb_task_id: {task}\n---\n\n{body}\n",
            encoding="utf-8",
        )

    def write_index(self, records):
        self.index.write_text(json.dumps({"records": records}), encoding="utf-8")

    def resolve(self):
        return resolve_dispatch(self.task, self.root, self.index)

    def test_valid_dispatch_resolves_exact_project_and_task(self):
        result = self.resolve()
        self.assertEqual("JARVIS_PRIMARY", result["project_id"])
        self.assertEqual("JARVIS-DEVICE-001", result["task_id"])
        self.assertEqual("coordination/gemini/dispatch/task.md", result["dispatch_path"])

    def test_missing_metadata_is_rejected(self):
        self.task.write_text("# Task without metadata\nDo work\n", encoding="utf-8")
        with self.assertRaisesRegex(DispatchMetadataError, "metadata block"):
            self.resolve()

    def test_duplicate_metadata_key_is_rejected(self):
        self.task.write_text(
            "---\nupkb_project_id: JARVIS_PRIMARY\nupkb_task_id: JARVIS-DEVICE-001\n"
            "upkb_task_id: OTHER-1\n---\nBody\n", encoding="utf-8")
        with self.assertRaisesRegex(DispatchMetadataError, "duplicate metadata key"):
            self.resolve()

    def test_unknown_metadata_key_is_rejected(self):
        self.task.write_text(
            "---\nupkb_project_id: JARVIS_PRIMARY\nupkb_task_id: JARVIS-DEVICE-001\n"
            "project: Jarvis\n---\nBody\n", encoding="utf-8")
        with self.assertRaisesRegex(DispatchMetadataError, "unknown metadata key"):
            self.resolve()

    def test_cross_project_task_is_rejected(self):
        self.write_task("AVTOY_KOREA", "JARVIS-DEVICE-001")
        with self.assertRaisesRegex(DispatchMetadataError, "belongs to"):
            self.resolve()

    def test_unknown_or_duplicate_task_record_is_rejected(self):
        self.write_index([])
        with self.assertRaisesRegex(DispatchMetadataError, "found 0"):
            self.resolve()
        self.write_index([
            {"task_id": "JARVIS-DEVICE-001", "project_id": "JARVIS_PRIMARY"},
            {"task_id": "JARVIS-DEVICE-001", "project_id": "JARVIS_PRIMARY"},
        ])
        with self.assertRaisesRegex(DispatchMetadataError, "found 2"):
            self.resolve()

    def test_empty_task_body_is_rejected(self):
        self.write_task(body="  \n ")
        with self.assertRaisesRegex(DispatchMetadataError, "body must not be empty"):
            self.resolve()

    def test_dispatch_outside_allowed_directory_is_rejected(self):
        outside = self.root / "coordination/gemini/inbox/task.md"
        outside.parent.mkdir(parents=True)
        outside.write_text(self.task.read_text(encoding="utf-8"), encoding="utf-8")
        with self.assertRaisesRegex(DispatchMetadataError, "under coordination/gemini/dispatch"):
            resolve_dispatch(outside, self.root, self.index)


if __name__ == "__main__":
    unittest.main()
