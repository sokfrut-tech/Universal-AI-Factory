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
    def test_disabled_by_default_and_does_not_call_transport(self):
        transport = MockTransport()
        adapter = ProviderAdapter(
            ProviderConfig(provider="claude"),
            transport,
        )
        result = adapter.dispatch(request())
        self.assertEqual(result.status, "blocked")
        self.assertEqual(transport.calls, [])

    def test_missing_credential_blocks_without_call(self):
        transport = MockTransport()
        adapter = ProviderAdapter(
            ProviderConfig(
                provider="gemini",
                enabled=True,
                credential_configured=False,
                secret_reference="secret://GEMINI_API_KEY",
            ),
            transport,
        )
        self.assertEqual(adapter.dispatch(request()).status, "blocked")
        self.assertEqual(transport.calls, [])

    def test_missing_transport_blocks(self):
        adapter = ProviderAdapter(
            ProviderConfig(
                provider="claude",
                enabled=True,
                credential_configured=True,
                secret_reference="secret://ANTHROPIC_API_KEY",
            )
        )
        self.assertEqual(adapter.dispatch(request()).status, "blocked")

    def test_enabled_adapter_passes_reference_and_idempotent_request(self):
        transport = MockTransport()
        adapter = ProviderAdapter(
            ProviderConfig(
                provider="claude",
                enabled=True,
                credential_configured=True,
                secret_reference="secret://ANTHROPIC_API_KEY",
            ),
            transport,
        )
        result = adapter.dispatch(request())
        self.assertEqual(result.status, "running")
        self.assertEqual(transport.calls[0][1], "secret://ANTHROPIC_API_KEY")
        self.assertEqual(transport.calls[0][0].idempotency_key, "idem-12345678")

    def test_timeout_is_sanitized(self):
        adapter = ProviderAdapter(
            ProviderConfig("gemini", True, True, "secret://GEMINI_API_KEY"),
            MockTransport(error=TimeoutError("secret-value-must-not-leak")),
        )
        result = adapter.dispatch(request())
        self.assertEqual(result.failure_reason, "transport_timeout")
        self.assertNotIn("secret-value", result.summary)

    def test_exception_message_is_not_exposed(self):
        adapter = ProviderAdapter(
            ProviderConfig("claude", True, True, "secret://ANTHROPIC_API_KEY"),
            MockTransport(error=RuntimeError("private-token-123")),
        )
        result = adapter.dispatch(request())
        self.assertEqual(result.status, "failed")
        self.assertNotIn("private-token-123", result.summary)
        self.assertNotIn("private-token-123", result.failure_reason)

    def test_done_without_provider_request_id_is_rejected(self):
        adapter = ProviderAdapter(
            ProviderConfig("claude", True, True, "secret://ANTHROPIC_API_KEY"),
            MockTransport(response=ProviderResponse(status="done", summary="done")),
        )
        result = adapter.dispatch(request())
        self.assertEqual(result.failure_reason, "missing_provider_request_id")

    def test_unknown_transport_status_is_rejected(self):
        adapter = ProviderAdapter(
            ProviderConfig("gemini", True, True, "secret://GEMINI_API_KEY"),
            MockTransport(response=ProviderResponse(status="received", summary="ack")),
        )
        result = adapter.dispatch(request())
        self.assertEqual(result.failure_reason, "invalid_transport_status")

    def test_unknown_provider_is_rejected(self):
        with self.assertRaises(ValueError):
            ProviderAdapter(ProviderConfig("other"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
