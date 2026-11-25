import os
import unittest
from unittest.mock import patch

from provider_adapter import ProviderAdapter, ProviderConfig, ProviderRequest
from provider_ledger_bridge import to_run_transition


class TimeoutTransport:
    def invoke(self, request, secret_reference):
        raise TimeoutError("simulated response loss")


class AdapterLedgerBridgeTests(unittest.TestCase):
    def test_timeout_maps_to_reserved_unknown_ledger_transition(self):
        request = ProviderRequest(
            task_id="task-ledger-1234",
            correlation_id="corr-ledger-1234",
            idempotency_key="idem-ledger-1234",
            prompt="Test only; no live provider call.",
        )
        adapter = ProviderAdapter(
            ProviderConfig(
                provider="gemini",
                enabled=True,
                credential_configured=True,
                secret_reference="secret://TEST_ONLY",
            ),
            TimeoutTransport(),
        )
        with patch.dict(os.environ, {"ALLOW_LIVE_PROVIDERS": "true"}):
            provider_response = adapter.dispatch(request)

        ledger_transition = to_run_transition(provider_response)
        self.assertEqual(ledger_transition.status, "outcome_unknown")
        self.assertEqual(ledger_transition.outcome_kind, "timeout")
        self.assertFalse(ledger_transition.retry_allowed)
        self.assertEqual(ledger_transition.failure_reason, "transport_timeout")


if __name__ == "__main__":
    unittest.main(verbosity=2)
