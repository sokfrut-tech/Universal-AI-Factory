import os
import unittest
from unittest.mock import patch

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
            ProviderConfig("claude", True, True, "secret://PROVIDER_API_KEY"),
            transport,
        )

    def setUp(self):
        self.live_guard = patch.dict(os.environ, {"ALLOW_LIVE_PROVIDERS": "true"})
        self.live_guard.start()
        self.addCleanup(self.live_guard.stop)

    def test_disabled_by_default_and_does_not_call_transport(self):
        transport = MockTransport()
        adapter = ProviderAdapter(ProviderConfig(provider="claude", enabled=False), transport)
        result = adapter.dispatch(request())
        self.assertEqual(result.status, "blocked")
        self.assertEqual(transport.calls, [])

    def test_central_environment_guard_blocks_even_when_adapter_enabled(self):
        transport = MockTransport()
        adapter = ProviderAdapter(
            ProviderConfig("claude", True, True, "secret://PROVIDER_API_KEY"),
            transport,
        )
        with patch.dict(os.environ, {"ALLOW_LIVE_PROVIDERS": "false"}):
            result = adapter.dispatch(request())
        self.assertEqual(result.status, "blocked")
        self.assertEqual(transport.calls, [])

    def test_missing_environment_guard_blocks(self):
        transport = MockTransport()
        adapter = ProviderAdapter(
            ProviderConfig("claude", True, True, "secret://PROVIDER_API_KEY"),
            transport,
        )
        with patch.dict(os.environ, {}, clear=True):
            result = adapter.dispatch(request())
        self.assertEqual(result.status, "blocked")
        self.assertEqual(transport.calls, [])

    def test_missing_credential_blocks_without_call(self):
        transport = MockTransport()
        adapter = ProviderAdapter(
            ProviderConfig("gemini", True, False, "secret://GEMINI_API_KEY"),
            transport,
        )
        self.assertEqual(adapter.dispatch(request()).status, "blocked")
        self.assertEqual(transport.calls, [])

    def test_missing_transport_blocks(self):
        adapter = ProviderAdapter(
            ProviderConfig("claude", True, True, "secret://ANTHROPIC_API_KEY")
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

    def test_failed_provider_status_requires_definitive_failure_evidence(self):
        ambiguous = self.adapter(MockTransport(response=ProviderResponse(
            status="failed", summary="Provider reported failure"
        ))).dispatch(request())
        self.assertEqual(ambiguous.status, "outcome_unknown")
        self.assertEqual(ambiguous.failure_reason, "unverified_provider_failure")

        definite = self.adapter(MockTransport(response=ProviderResponse(
            status="failed", summary="Provider rejected request",
            failure_reason="invalid_request", failure_kind="definite_rejection"
        ))).dispatch(request())
        self.assertEqual(definite.status, "failed")

    def test_done_is_rejected_until_orchestrator_validates_evidence(self):
        result = self.adapter(
            MockTransport(response=ProviderResponse(status="done", summary="done",
                                                    provider_request_id="mock-123"))
        ).dispatch(request())
        self.assertEqual(result.status, "outcome_unknown")
        self.assertEqual(result.failure_reason, "invalid_transport_status")
        self.assertEqual(result.status, "outcome_unknown")

    def test_dispatch_running_and_review_require_provider_request_id(self):
        for status in ("dispatched", "running", "review"):
            with self.subTest(status=status):
                result = self.adapter(
                    MockTransport(response=ProviderResponse(status=status, summary="ok"))
                ).dispatch(request())
                self.assertEqual(result.failure_reason, "missing_provider_request_id")
                self.assertEqual(result.status, "outcome_unknown")

    def test_unknown_transport_status_is_rejected(self):
        result = self.adapter(
            MockTransport(response=ProviderResponse(status="received", summary="ack"))
        ).dispatch(request())
        self.assertEqual(result.failure_reason, "invalid_transport_status")

    def test_malformed_transport_response_is_rejected(self):
        result = self.adapter(MockTransport(response={"status": "running"})).dispatch(request())
        self.assertEqual(result.failure_reason, "invalid_transport_response")
        self.assertEqual(result.status, "outcome_unknown")

    def test_unknown_provider_is_rejected(self):
        with self.assertRaises(ValueError):
            ProviderAdapter(ProviderConfig("other"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
