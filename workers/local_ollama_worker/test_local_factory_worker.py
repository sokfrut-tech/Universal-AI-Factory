import io
import json
import sys
import tempfile
import threading
import unittest
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import local_factory_worker as w  # noqa: E402


class LocalFactoryWorkerTests(unittest.TestCase):
    def test_blocks_non_loopback_and_non_http_urls(self):
        self.assertEqual(w.validate_loopback_ollama_url("http://127.0.0.1:11434/"), "http://127.0.0.1:11434")
        self.assertEqual(w.validate_loopback_ollama_url("http://localhost:11434"), "http://localhost:11434")
        self.assertEqual(w.validate_loopback_ollama_url("http://[::1]:11434"), "http://[::1]:11434")

        for bad in (
            "https://api.openai.com/v1",
            "https://dashscope.aliyuncs.com",
            "http://192.168.1.50:11434",
            "file:///etc/passwd",
        ):
            with self.assertRaises(ValueError):
                w.validate_loopback_ollama_url(bad)

    def test_redacts_secrets(self):
        raw = "token sk-abcdefghijklmnop12345 and ghp_0123456789abcdef0123456789 and Bearer mySuperSecretJwtToken123456"
        redacted = w.redact_secrets(raw)
        self.assertNotIn("sk-abcdefghijklmnop12345", redacted)
        self.assertNotIn("ghp_0123456789abcdef0123456789", redacted)
        self.assertNotIn("mySuperSecretJwtToken123456", redacted)

    def test_skips_completed_and_writes_substantive_report_via_loopback_mock(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            q_in = root / "coordination" / "qwen" / "inbox"
            q_out = root / "coordination" / "qwen" / "outbox"
            q_in.mkdir(parents=True)
            q_out.mkdir(parents=True)

            # Done task (has real REPORT_*, >200B)
            (q_in / "2026-11-25_done_task.md").write_text("# Done\nTest\n", encoding="utf-8")
            (q_out / "REPORT_2026-11-25_DONE_TASK.md").write_text("# Report\n" + ("Detailed finding. " * 20), encoding="utf-8")

            # Pending task (only has empty ACK_, must NOT be considered done)
            (q_in / "2026-11-26_open_task.md").write_text("# Open Task\nInspect Jarvis memory module.\n", encoding="utf-8")
            (q_out / "ACK_2026-11-26_open_task.md").write_text("ACK only", encoding="utf-8")

            class MockHandler(BaseHTTPRequestHandler):
                def log_message(self, format, *args):
                    return

                def do_GET(self):
                    if self.path == "/api/tags":
                        body = json.dumps({"models": [{"name": "qwen3.5:4b"}]}).encode("utf-8")
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.send_header("Content-Length", str(len(body)))
                        self.end_headers()
                        self.wfile.write(body)

                def do_POST(self):
                    if self.path == "/api/generate":
                        _len = int(self.headers.get("Content-Length", "0"))
                        _ = self.rfile.read(_len)
                        reply = (
                            "## Резюме\nПроверена спецификация задачи. Требуется аудит.\n\n"
                            "## Риски\nФизический телефон ещё не тестировался. Секрет Bearer abcd1234567890efghij не должен утечь."
                        )
                        body = json.dumps({"response": reply}).encode("utf-8")
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.send_header("Content-Length", str(len(body)))
                        self.end_headers()
                        self.wfile.write(body)

            server = ThreadingHTTPServer(("127.0.0.1", 0), MockHandler)
            th = threading.Thread(target=server.serve_forever, daemon=True)
            th.start()
            try:
                url = f"http://127.0.0.1:{server.server_port}"
                dry = w.run_once(root, base_url=url, model="qwen3.5:4b", channels=["qwen"], dry_run=True)
                self.assertEqual(dry["pending_total"], 1)

                done = w.run_once(root, base_url=url, model="qwen3.5:4b", channels=["qwen"], dry_run=False, max_tasks=1)
                self.assertEqual(len(done["processed"]), 1)
                report_path = root / done["processed"][0]["report"]
                self.assertTrue(report_path.is_file())
                content = report_path.read_text(encoding="utf-8")
                self.assertIn("Проверена спецификация задачи", content)
                self.assertNotIn("abcd1234567890efghij", content)

                # Subsequent scan must see 0 pending tasks
                dry2 = w.run_once(root, base_url=url, model="qwen3.5:4b", channels=["qwen"], dry_run=True)
                self.assertEqual(dry2["pending_total"], 0)
            finally:
                server.shutdown()
                server.server_close()

    def test_refuses_empty_ack_response(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            q_in = root / "coordination" / "qwen" / "inbox"
            q_in.mkdir(parents=True)
            (q_in / "task1.md").write_text("# Task 1\nVerify something\n", encoding="utf-8")

            def fake_transport(url, payload=None, timeout_s=10.0):
                if url.endswith("/api/tags"):
                    return {"models": [{"name": "qwen3.5:4b"}]}
                return {"response": "ACK"}

            with self.assertRaises(RuntimeError):
                w.run_once(root, base_url="http://127.0.0.1:11434", model="qwen3.5:4b", channels=["qwen"], transport=fake_transport)

    def test_sends_no_think_extended_context_strips_think_and_falls_back_on_http_400(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            q_in = root / "coordination" / "qwen" / "inbox"
            q_in.mkdir(parents=True)
            (q_in / "task2.md").write_text("# Task 2\nAudit local Qwen runtime constraints.\n", encoding="utf-8")

            seen_payloads = []

            def fake_transport(url, payload=None, timeout_s=10.0):
                if url.endswith("/api/tags"):
                    return {"models": [{"name": "qwen3.5:4b"}]}
                seen_payloads.append(dict(payload))
                if len(seen_payloads) == 1:
                    raise urllib.error.HTTPError(
                        url=url,
                        code=400,
                        msg="Bad Request",
                        hdrs=None,
                        fp=io.BytesIO(b"think not supported"),
                    )
                return {
                    "done_reason": "stop",
                    "response": (
                        "<think>скрытые рассуждения не должны попасть в отчёт</think>\n"
                        "## Резюме\nПроверка выполнена офлайн без платных API и показала полную работоспособность.\n\n"
                        "## Следующие шаги\nНе мержить PR без тестов на устройстве."
                    ),
                }

            done = w.run_once(
                root,
                base_url="http://127.0.0.1:11434",
                model="qwen3.5:4b",
                channels=["qwen"],
                transport=fake_transport,
            )
            self.assertEqual(len(seen_payloads), 2)
            self.assertFalse(seen_payloads[0]["think"])
            self.assertEqual(seen_payloads[0]["options"]["num_ctx"], 8192)
            self.assertEqual(seen_payloads[0]["options"]["num_predict"], 4096)
            self.assertNotIn("think", seen_payloads[1])
            self.assertEqual(done["processed"][0]["done_reason"], "stop")

            content = (root / done["processed"][0]["report"]).read_text(encoding="utf-8")
            self.assertNotIn("<think>", content)
            self.assertNotIn("скрытые рассуждения", content)
            self.assertIn("done_reason=stop", content)


if __name__ == "__main__":
    unittest.main()
