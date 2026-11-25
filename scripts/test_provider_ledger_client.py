import unittest

from provider_adapter import ProviderResponse
from provider_ledger_client import build_ledger_transition, UnsupportedLedgerTransition


class ProviderLedgerClientContractTests(unittest.TestCase):
    def test_dispatched_maps_to_accepted_and_preserves_request_id(self):
        payload = build_ledger_transition(
            ProviderResponse(status="dispatched", summary="Accepted", provider_request_id="req_123"),
            "dispatching",
        )
        self.assertEqual(payload["nextStatus"], "accepted")
        self.assertEqual(payload["providerRequestId"], "req_123")
        self.assertEqual(payload["expectedStatus"], "dispatching")

    def test_running_result_after_acceptance_maps_to_running(self):
        payload = build_ledger_transition(
            ProviderResponse(status="running", summary="Work started", provider_request_id="req_123"),
            "accepted",
        )
        self.assertEqual(payload["nextStatus"], "running")
        self.assertEqual(payload["expectedStatus"], "accepted")

    def test_review_result_after_running_maps_to_review(self):
        payload = build_ledger_transition(
            ProviderResponse(status="review", summary="Ready for review", provider_request_id="req_123"),
            "running",
        )
        self.assertEqual(payload["nextStatus"], "review")

    def test_timeout_maps_to_unknown_without_retry_signal(self):
        payload = build_ledger_transition(
            ProviderResponse(status="outcome_unknown", summary="Timed out", outcome_kind="timeout"),
            "dispatching",
        )
        self.assertEqual(payload["nextStatus"], "outcome_unknown")
        self.assertEqual(payload["outcomeKind"], "timeout")
        self.assertNotIn("retry", payload)

    def test_unsupported_or_unsafe_failure_fails_closed(self):
        with self.assertRaises(UnsupportedLedgerTransition):
            build_ledger_transition(
                ProviderResponse(status="failed", summary="Failure", failure_kind="ambiguous"),
                "dispatching",
            )
        with self.assertRaises(UnsupportedLedgerTransition):
            build_ledger_transition(
                ProviderResponse(status="blocked", summary="Not sent"),
                "dispatching",
            )

    def test_acceptance_requires_provider_request_id(self):
        with self.assertRaises(UnsupportedLedgerTransition):
            build_ledger_transition(
                ProviderResponse(status="dispatched", summary="Accepted"),
                "dispatching",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
