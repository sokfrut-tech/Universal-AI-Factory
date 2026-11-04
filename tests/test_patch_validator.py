import unittest

from factory_runner.patch_validator import PatchValidationError, validate_patch

BASE = "a" * 40
TARGET = "sokfrut-tech/Universal-AI-Factory"


def patch_for(path="docs/readme.md", body="+updated"):
    return (
        f"diff --git a/{path} b/{path}\n"
        "index 1111111..2222222 100644\n"
        f"--- a/{path}\n"
        f"+++ b/{path}\n"
        "@@ -1 +1 @@\n"
        "-old\n"
        f"{body}\n"
    )


class PatchValidatorTests(unittest.TestCase):
    def validate(self, patch, **kwargs):
        values = dict(task_id="task-123", correlation_id="corr-456",
                      target_repo=TARGET, base_sha=BASE, patch=patch)
        values.update(kwargs)
        return validate_patch(**values)

    def assert_rejected(self, patch, **kwargs):
        with self.assertRaises(PatchValidationError):
            self.validate(patch, **kwargs)

    def test_valid_modify_and_stable_digest(self):
        patch = patch_for()
        first, second = self.validate(patch), self.validate(patch)
        self.assertEqual(first.patch_sha256, second.patch_sha256)
        self.assertEqual(first.changed_paths, ("docs/readme.md",))
        self.assertEqual(first.files[0].change_type, "modify")

    def test_valid_add(self):
        patch = ("diff --git a/new.txt b/new.txt\nnew file mode 100644\n"
                 "--- /dev/null\n+++ b/new.txt\n@@ -0,0 +1 @@\n+hello\n")
        self.assertEqual(self.validate(patch).files[0].change_type, "add")

    def test_valid_delete(self):
        patch = ("diff --git a/old.txt b/old.txt\ndeleted file mode 100644\n"
                 "--- a/old.txt\n+++ /dev/null\n@@ -1 +0,0 @@\n-bye\n")
        self.assertEqual(self.validate(patch).files[0].change_type, "delete")

    def test_valid_multiple_hunks(self):
        patch = patch_for().replace("+updated\n", "+updated\n@@ -5 +5 @@\n-before\n+after\n")
        self.assertEqual(len(self.validate(patch).files), 1)

    def test_rejects_hunk_underflow(self):
        self.assert_rejected(patch_for().replace("@@ -1 +1 @@", "@@ -1,2 +1,2 @@"))

    def test_rejects_hunk_overflow(self):
        self.assert_rejected(patch_for().replace("@@ -1 +1 @@", "@@ -0,0 +0,0 @@"))

    def test_rejects_traversal(self): self.assert_rejected(patch_for("../escape.txt"))
    def test_rejects_absolute_path(self): self.assert_rejected(patch_for("/etc/passwd"))
    def test_rejects_windows_path(self): self.assert_rejected(patch_for("C:/Windows/system.ini"))

    def test_rejects_symlink_mode(self):
        patch = ("diff --git a/link b/link\nnew file mode 120000\n--- /dev/null\n"
                 "+++ b/link\n@@ -0,0 +1 @@\n+target\n")
        self.assert_rejected(patch)

    def test_rejects_submodule_mode(self):
        self.assert_rejected(patch_for().replace("100644", "160000", 1))

    def test_rejects_binary(self): self.assert_rejected("GIT binary patch\n")
    def test_rejects_duplicate_paths(self): self.assert_rejected(patch_for() + patch_for())
    def test_rejects_oversized_patch(self): self.assert_rejected(patch_for(), max_patch_bytes=10)
    def test_rejects_malformed_hunk(self): self.assert_rejected(patch_for().replace("@@ -1 +1 @@", "@@ bad @@"))
    def test_rejects_unallowlisted_repo(self): self.assert_rejected(patch_for(), target_repo="someone/else")
    def test_rejects_short_base_sha(self): self.assert_rejected(patch_for(), base_sha="abc")
    def test_rejects_empty_patch(self): self.assert_rejected("")
    def test_rejects_path_with_backslash(self): self.assert_rejected(patch_for("folder\\..\\escape"))

    def test_rejects_rename(self):
        patch = patch_for().replace("index 1111111..2222222 100644\n",
                                    "rename from old.md\nrename to new.md\n")
        self.assert_rejected(patch)


if __name__ == "__main__":
    unittest.main()
