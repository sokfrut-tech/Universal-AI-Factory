"""Strict metadata contract tests for Gemini dispatch tasks."""
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
        self.dispatch_dir = self.root / "coordination/gemini/dispatch"
        self.dispatch_dir.mkdir(parents=True)
        self.task_file = self.dispatch_dir / "task.md"
        self.index = self.root / "UPKB/INDEX/TASK_INDEX.json"
        self.index.parent.mkdir(parents=True)
        self.index.write_text(json.dumps({"records": [
            {"task_id": "T1", "project_id": "P1"},
            {"task_id": "T2", "project_id": "P2"},
        ]}), encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def write_task(self, metadata, body="Perform scoped analysis."):
        self.task_file.write_text("---\n" + metadata + "---\n" + body + "\n", encoding="utf-8")

    def test_valid_metadata_resolves_registered_project_task(self):
        self.write_task("upkb_project_id: P1\nupkb_task_id: T1\n")
        result = resolve_dispatch(self.task_file, self.root, self.index)
        self.assertEqual({"project_id": "P1", "task_id": "T1",
                          "dispatch_path": "coordination/gemini/dispatch/task.md"}, result)

    def test_missing_metadata_fails_closed(self):
        self.write_task("upkb_project_id: P1\n")
        with self.assertRaisesRegex(DispatchMetadataError, "both upkb_project_id"):
            resolve_dispatch(self.task_file, self.root, self.index)

    def test_duplicate_or_unknown_metadata_key_fails_closed(self):
        self.write_task("upkb_project_id: P1\nupkb_project_id: P1\nupkb_task_id: T1\n")
        with self.assertRaisesRegex(DispatchMetadataError, "duplicate"):
            resolve_dispatch(self.task_file, self.root, self.index)
        self.write_task("upkb_project_id: P1\nupkb_task_id: T1\nextra: no\n")
        with self.assertRaisesRegex(DispatchMetadataError, "unknown metadata key"):
            resolve_dispatch(self.task_file, self.root, self.index)

    def test_cross_project_or_unknown_task_fails_closed(self):
        self.write_task("upkb_project_id: P1\nupkb_task_id: T2\n")
        with self.assertRaisesRegex(DispatchMetadataError, "belongs to 'P2'"):
            resolve_dispatch(self.task_file, self.root, self.index)
        self.write_task("upkb_project_id: P1\nupkb_task_id: MISSING\n")
        with self.assertRaisesRegex(DispatchMetadataError, "found 0"):
            resolve_dispatch(self.task_file, self.root, self.index)

    def test_task_path_outside_dispatch_folder_is_rejected(self):
        outside = self.root / "other.md"
        outside.write_text("---\nupkb_project_id: P1\nupkb_task_id: T1\n---\nBody", encoding="utf-8")
        with self.assertRaisesRegex(DispatchMetadataError, "under coordination/gemini/dispatch"):
            resolve_dispatch(outside, self.root, self.index)

    def test_empty_body_and_malformed_project_id_are_rejected(self):
        self.write_task("upkb_project_id: P1\nupkb_task_id: T1\n", body="")
        with self.assertRaisesRegex(DispatchMetadataError, "body must not be empty"):
            resolve_dispatch(self.task_file, self.root, self.index)
        self.write_task("upkb_project_id: ../../P1\nupkb_task_id: T1\n")
        with self.assertRaisesRegex(DispatchMetadataError, "invalid upkb_project_id"):
            resolve_dispatch(self.task_file, self.root, self.index)


if __name__ == "__main__":
    unittest.main()
