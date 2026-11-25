"""Build authenticated run-ledger transition payloads from adapter results.

No HTTP, database, credential lookup, or provider dispatch happens here. The
caller must persist each payload through the runner-authenticated CAS endpoint.
"""
from typing import Any, Dict

from provider_adapter import ProviderResponse


class UnsupportedLedgerTransition(ValueError):
    """The adapter result cannot safely be represented by the current ledger."""


_AMBIGUOUS_KINDS = {
    "timeout", "connection_lost", "process_interrupted", "ambiguous_response"
}


def build_ledger_transition(
    response: ProviderResponse,
    expected_status: str,
) -> Dict[str, Any]:
    """Return one API-compatible transition or fail closed.

    Provider acceptance is recorded as 'accepted'. A later poll/progress result
    can move accepted -> running/review using the new expected status.
    """
    if not isinstance(response, ProviderResponse):
        raise TypeError("response must be a ProviderResponse")

    if response.status == "outcome_unknown":
        kind = response.outcome_kind or "ambiguous_response"
        if kind not in _AMBIGUOUS_KINDS:
            kind = "ambiguous_response"
        if expected_status not in {"dispatching", "accepted", "running"}:
            raise UnsupportedLedgerTransition("unknown outcome is not allowed from this ledger state")
        return {
            "expectedStatus": expected_status,
            "nextStatus": "outcome_unknown",
            "outcomeKind": kind,
            "summary": response.summary[:500] or "Provider outcome is unknown",
        }

    if response.status == "failed":
        if expected_status == "dispatching" and response.failure_kind == "definite_rejection":
            reason = response.failure_reason or "provider_rejected"
            reason_code = "".join(c if c.isalnum() or c in "._-" else "_" for c in reason)[:80]
            if not reason_code:
                reason_code = "provider_rejected"
            return {
                "expectedStatus": "dispatching",
                "nextStatus": "failed",
                "failureKind": "definite_rejection",
                "reasonCode": reason_code,
                "summary": response.summary[:500] or "Provider definitively rejected the request",
            }
        if expected_status in {"running", "review"} and response.failure_kind == "execution_failed":
            reason = response.failure_reason or "provider_execution_failed"
            reason_code = "".join(c if c.isalnum() or c in "._-" else "_" for c in reason)[:80]
            if not reason_code:
                reason_code = "provider_execution_failed"
            return {
                "expectedStatus": expected_status,
                "nextStatus": "failed",
                "failureKind": "execution_failed",
                "reasonCode": reason_code,
                "summary": response.summary[:500] or "Provider execution failed",
            }
        raise UnsupportedLedgerTransition(
            "failure evidence or current ledger state does not permit a failed transition"
        )

    if response.status in {"dispatched", "running", "review"}:
        if expected_status == "dispatching":
            if not response.provider_request_id:
                raise UnsupportedLedgerTransition("provider request ID is required to record acceptance")
            return {
                "expectedStatus": "dispatching",
                "nextStatus": "accepted",
                "providerRequestId": response.provider_request_id,
                "summary": response.summary[:500] or "Provider accepted the request",
            }
        if expected_status == "accepted" and response.status in {"running", "review"}:
            return {
                "expectedStatus": "accepted",
                "nextStatus": response.status,
                "summary": response.summary[:500] or "Provider progress received",
            }
        if expected_status == "running" and response.status == "review":
            return {
                "expectedStatus": "running",
                "nextStatus": "review",
                "summary": response.summary[:500] or "Provider result submitted for review",
            }

    raise UnsupportedLedgerTransition(
        "adapter result has no safe transition from the supplied ledger status"
    )
