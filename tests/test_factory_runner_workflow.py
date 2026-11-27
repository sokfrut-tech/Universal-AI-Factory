import pathlib
import re
import unittest

WORKFLOW = pathlib.Path(".github/workflows/factory-runner.yml")


class FactoryRunnerWorkflowSecurityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = WORKFLOW.read_text(encoding="utf-8")

    def test_read_only_permissions(self):
        self.assertRegex(self.text, r"(?m)^permissions:\s*\n\s+contents: read\s*$")
        self.assertNotRegex(self.text, r"(?m)^\s+contents: write\s*$")

    def test_only_manual_dispatch(self):
        self.assertIn("  workflow_dispatch:", self.text)
        self.assertNotRegex(self.text, r"(?m)^  (push|pull_request):")

    def test_explicit_task_path_required(self):
        self.assertRegex(self.text, r"(?ms)task_file:.*?required: true")
        self.assertNotIn("newest", self.text.lower())
        self.assertNotIn("find . -maxdepth", self.text)

    def test_allowlist_and_path_validation(self):
        self.assertIn('if target not in allowed:', self.text)
        self.assertIn('part in ("", ".", "..")', self.text)
        self.assertIn("candidate.is_symlink()", self.text)
        self.assertIn("resolve(strict=True)", self.text)

    def test_no_inline_user_input_in_shell(self):
        self.assertNotIn("${{ github.event.inputs.", self.text)
        self.assertNotIn("${{ inputs.task_file }}\n          ", self.text)

    def test_no_pat_or_privileged_modes(self):
        self.assertNotIn("FACTORY_PAT", self.text)
        self.assertNotIn("merge_pr_43_and_verify", self.text)
        self.assertNotIn("sync_task_to_target", self.text)
        self.assertNotRegex(self.text, r"(?m)^\s*git push\b")

    def test_no_raw_task_dump(self):
        self.assertIn("task contents are not copied", self.text)
        self.assertNotRegex(self.text, r'cat\s+["$].*TASK')

    def test_actions_are_commit_pinned(self):
        actions = re.findall(r"uses:\s+([^\s]+)", self.text)
        self.assertGreaterEqual(len(actions), 3)
        for action in actions:
            self.assertRegex(action, r"@[0-9a-f]{40}(?:\s+#.*)?$")

    def test_checkout_credentials_not_persisted(self):
        self.assertEqual(self.text.count("persist-credentials: false"), 2)


if __name__ == "__main__":
    unittest.main()
