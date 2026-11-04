import unittest

from provider_adapter import (
    ProviderAdapter,
    ProviderConfig,
    ProviderRequest,
    ProviderResponse,
)


class MockTransport:
    def __init__(self, response=None, error=None):
        self.response = response or ProviderResponse(
            status="running",
            summary="Mock provider accepted the request.",
            provider_request_id="mock-request-123",
        )
        self.error = error
        self.calls = []

    def invoke(self, request, secret_reference):
        self.calls.append((request, secret_reference))
        if self.error:
            raise self.error
        return self.response


def request():
    return ProviderRequest(
        task_id="task-12345678",
        correlation_id="corr-12345678",
        idempotency_key="idem-12345678",
        prompt="Review the supplied change.",
    )


class ProviderAdapterTests(unittest.TestCase):
    def adapter(self, transport):
        return ProviderAdapter(
            ProviderConfig("claude", True, True, "secret://PROVIDER_API_KEY", True),
            transport,
        )

    def test_disabled_by_default_and_does_not_call_transport(self):
        transport = MockTransport()
        adapter = ProviderAdapter(ProviderConfig(provider="claude", enabled=True, allow_live_providers=False), transport)
        result = adapter.dispatch(request())
        self.assertEqual(result.status, "blocked")
        self.assertEqual(transport.calls, [])

    def test_live_guard_blocks_even_when_adapter_enabled(self):
        transport = MockTransport()
        adapter = ProviderAdapter(
            ProviderConfig("claude", True, True, "secret://PROVIDER_API_KEY", False),
            transport,
        )
        result = adapter.dispatch(request())
        self.assertEqual(result.status, "blocked")
        self.assertEqual(transport.calls, [])

    def test_missing_credential_blocks_without_call(self):
        transport = MockTransport()
        adapter = ProviderAdapter(
            ProviderConfig("gemini", True, False, "secret://GEMINI_API_KEY", True),
            transport,
        )
        self.assertEqual(adapter.dispatch(request()).status, "blocked")
        self.assertEqual(transport.calls, [])

    def test_missing_transport_blocks(self):
        adapter = ProviderAdapter(
            ProviderConfig("claude", True, True, "secret://ANTHROPIC_API_KEY", True)
        )
        self.assertEqual(adapter.dispatch(request()).status, "blocked")

    def test_enabled_adapter_passes_reference_and_idempotent_request(self):
        transport = MockTransport()
        result = self.adapter(transport).dispatch(request())
        self.assertEqual(result.status, "running")
        self.assertEqual(transport.calls[0][1], "secret://PROVIDER_API_KEY")
        self.assertEqual(transport.calls[0][0].idempotency_key, "idem-12345678")

    def test_timeout_is_sanitized(self):
        result = self.adapter(
            MockTransport(error=TimeoutError("secret-value-must-not-leak"))
        ).dispatch(request())
        self.assertEqual(result.status, "outcome_unknown")
        self.assertEqual(result.outcome_kind, "timeout")
        self.assertEqual(result.failure_reason, "transport_timeout")
        self.assertNotIn("secret-value", result.summary)

    def test_exception_message_is_not_exposed(self):
        result = self.adapter(
            MockTransport(error=RuntimeError("private-token-123"))
        ).dispatch(request())
        self.assertEqual(result.status, "outcome_unknown")
        self.assertEqual(result.outcome_kind, "ambiguous_response")
        self.assertNotIn("private-token-123", result.summary)
        self.assertNotIn("private-token-123", result.failure_reason)

    def test_done_is_rejected_until_orchestrator_validates_evidence(self):
        result = self.adapter(
            MockTransport(response=ProviderResponse(status="done", summary="done",
                                                    provider_request_id="mock-123"))
        ).dispatch(request())
        self.assertEqual(result.status, "failed")
        self.assertEqual(result.failure_reason, "invalid_transport_status")

    def test_dispatch_running_and_review_require_provider_request_id(self):
        for status in ("dispatched", "running", "review"):
            with self.subTest(status=status):
                result = self.adapter(
                    MockTransport(response=ProviderResponse(status=status, summary="ok"))
                ).dispatch(request())
                self.assertEqual(result.failure_reason, "missing_provider_request_id")

    def test_unknown_transport_status_is_rejected(self):
        result = self.adapter(
            MockTransport(response=ProviderResponse(status="received", summary="ack"))
        ).dispatch(request())
        self.assertEqual(result.failure_reason, "invalid_transport_status")

    def test_malformed_transport_response_is_rejected(self):
        result = self.adapter(MockTransport(response={"status": "running"})).dispatch(request())
        self.assertEqual(result.failure_reason, "invalid_transport_response")

    def test_unknown_provider_is_rejected(self):
        with self.assertRaises(ValueError):
            ProviderAdapter(ProviderConfig("other"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
