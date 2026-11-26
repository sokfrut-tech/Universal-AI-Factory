import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from export_jarvis_memory_to_jsonl import convert_export_to_alpaca, is_safe_text


class ExportJarvisMemoryTests(unittest.TestCase):
    def test_blocks_secrets_tokens_and_luhn_cards(self):
        self.assertFalse(is_safe_text("OpenAI sk-proj-abc1234567890XYZdef"))
        self.assertFalse(is_safe_text("пароль от почты: Secret999"))
        self.assertFalse(is_safe_text("р\u200Bassword: secret123"))
        self.assertFalse(is_safe_text("карта 4111 1111 1111 1111"))
        self.assertTrue(is_safe_text("Моя машина Li Xiang L7 и телефон OPPO Find X6 Pro"))

    def test_converts_safe_facts_and_skips_secrets(self):
        payload = {
            "facts": [
                {"key": "car", "content": "Вожу Li Xiang L7"},
                {"key": "leak", "content": "AIzaSyD83kLmNoPqRsTuVwXyZ1234567"},
                {"key": "city", "content": "Живу в Алматы"},
            ]
        }
        rows, skipped = convert_export_to_alpaca(payload)
        self.assertEqual(1, skipped)
        self.assertEqual(2, len(rows))
        self.assertIn("Li Xiang L7", rows[0]["output"])
        self.assertIn("Алматы", rows[1]["output"])


if __name__ == "__main__":
    unittest.main()
