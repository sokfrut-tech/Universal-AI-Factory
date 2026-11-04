"""Safe provider adapter boundary.

This module deliberately contains no HTTP client and performs no network calls.
A real provider transport must be supplied explicitly by a separately reviewed
integration. The default configuration is disabled.
"""
from dataclasses import dataclass
from typing import Callable, Optional, Protocol


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


class ProviderAdapter:
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
        if not self._config.enabled:
            return ProviderResponse(
                status="blocked",
                summary="No provider request was sent.",
                blocked_reason="Provider dispatch is disabled by configuration.",
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
                status="failed",
                summary="Provider request timed out.",
                failure_reason="transport_timeout",
            )
        except Exception as exc:  # Never copy exception text; it may contain secrets.
            return ProviderResponse(
                status="failed",
                summary="Provider transport failed.",
                failure_reason=f"transport_error:{type(exc).__name__}",
            )

        if response.status not in {"dispatched", "running", "review", "done", "partial", "blocked", "failed"}:
            return ProviderResponse(
                status="failed",
                summary="Provider returned an unsupported status.",
                failure_reason="invalid_transport_status",
            )
        if response.status == "done" and not response.provider_request_id:
            return ProviderResponse(
                status="failed",
                summary="Provider response lacked a request reference.",
                failure_reason="missing_provider_request_id",
            )
        return response
