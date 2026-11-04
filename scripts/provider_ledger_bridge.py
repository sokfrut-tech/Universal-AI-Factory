"""Pure adapter-to-run-ledger transition mapping.

This module does not perform database/network I/O. The runtime orchestrator must
persist the returned transition through the ledger's authenticated CAS endpoint.
"""
from dataclasses import dataclass
from typing import Optional

from provider_adapter import ProviderResponse


@dataclass(frozen=True)
class RunTransition:
    status: str
    outcome_kind: Optional[str]
    failure_reason: Optional[str]
    retry_allowed: bool


def to_run_transition(response: ProviderResponse) -> RunTransition:
    if response.status == "outcome_unknown":
        return RunTransition(
            status="outcome_unknown",
            outcome_kind=response.outcome_kind or "ambiguous_response",
            failure_reason=response.failure_reason,
            retry_allowed=False,
        )
    if response.status == "failed":
        if response.failure_kind not in {"definite_rejection", "execution_failed"}:
            return RunTransition(
                status="outcome_unknown",
                outcome_kind=response.outcome_kind or "ambiguous_response",
                failure_reason="unverified_provider_failure",
                retry_allowed=False,
            )
        return RunTransition(
            status="failed",
            outcome_kind=response.outcome_kind,
            failure_reason=response.failure_reason,
            retry_allowed=False,
        )
    return RunTransition(
        status=response.status,
        outcome_kind=response.outcome_kind,
        failure_reason=response.failure_reason,
        retry_allowed=False,
    )
