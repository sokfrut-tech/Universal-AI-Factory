"""Safe provider adapter boundary.

This module deliberately contains no HTTP client and performs no network calls.
A real provider transport must be supplied explicitly by a separately reviewed
integration. The default configuration is disabled. Completion is owned by the
factory orchestrator, which must attach and validate evidence before marking done.
"""
from dataclasses import dataclass
from typing import Optional, Protocol


@dataclass(frozen=True)
class ProviderRequest:
    task_id: str
    correlation_id: str
    idempotency_key: str
    prompt: str


@dataclass(frozen=True)
class ProviderResponse:
    status: str
    summary: str
    provider_request_id: Optional[str] = None
    blocked_reason: Optional[str] = None
    failure_reason: Optional[str] = None
    outcome_kind: Optional[str] = None


class ProviderTransport(Protocol):
    """Transport owns secret retrieval, HTTP, timeout and response sanitization."""

    def invoke(self, request: ProviderRequest, secret_reference: str) -> ProviderResponse:
        ...


@dataclass(frozen=True)
class ProviderConfig:
    provider: str
    enabled: bool = False
    credential_configured: bool = False
    secret_reference: Optional[str] = None
    allow_live_providers: bool = False


class ProviderAdapter:
    _TRANSPORT_STATUSES = {"dispatched", "running", "review", "partial", "blocked", "failed", "outcome_unknown"}
    _STATUSES_REQUIRING_REQUEST_ID = {"dispatched", "running", "review"}

    def __init__(
        self,
        config: ProviderConfig,
        transport: Optional[ProviderTransport] = None,
    ):
        if config.provider not in {"claude", "gemini"}:
            raise ValueError("unsupported provider")
        self._config = config
        self._transport = transport

    def dispatch(self, request: ProviderRequest) -> ProviderResponse:
        if not self._config.enabled or not self._config.allow_live_providers:
            return ProviderResponse(
                status="blocked",
                summary="No provider request was sent.",
                blocked_reason="Provider dispatch is disabled by configuration or ALLOW_LIVE_PROVIDERS is not enabled.",
            )
        if not self._config.credential_configured or not self._config.secret_reference:
            return ProviderResponse(
                status="blocked",
                summary="No provider request was sent.",
                blocked_reason="Provider credential is not configured.",
            )
        if self._transport is None:
            return ProviderResponse(
                status="blocked",
                summary="No provider request was sent.",
                blocked_reason="No reviewed provider transport is installed.",
            )

        try:
            response = self._transport.invoke(request, self._config.secret_reference)
        except TimeoutError:
            return ProviderResponse(
                status="outcome_unknown",
                summary="Provider request timed out; remote execution status is unknown.",
                failure_reason="transport_timeout",
                outcome_kind="timeout",
            )
        except Exception:  # A transport error may happen after the provider accepted the request.
            return ProviderResponse(
                status="outcome_unknown",
                summary="Provider transport failed; remote execution status is unknown.",
                failure_reason="transport_error",
                outcome_kind="ambiguous_response",
            )

        if not isinstance(response, ProviderResponse):
            return ProviderResponse(
                status="failed",
                summary="Provider transport returned a malformed response.",
                failure_reason="invalid_transport_response",
            )
        if response.status not in self._TRANSPORT_STATUSES:
            return ProviderResponse(
                status="failed",
                summary="Provider returned an unsupported status.",
                failure_reason="invalid_transport_status",
            )
        if response.status in self._STATUSES_REQUIRING_REQUEST_ID and not response.provider_request_id:
            return ProviderResponse(
                status="failed",
                summary="Provider response lacked a request reference.",
                failure_reason="missing_provider_request_id",
            )
        return response
