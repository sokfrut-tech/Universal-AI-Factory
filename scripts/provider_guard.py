"""Central fail-closed guard for every live provider dispatch path."""
import os
from typing import Mapping, Optional


def live_provider_dispatch_allowed(
    adapter_enabled: bool,
    environ: Optional[Mapping[str, str]] = None,
) -> bool:
    """Allow live traffic only when adapter is enabled and explicit env opt-in is true.

    An injected mapping is supported for deterministic tests. Production callers
    should omit it so the process environment is read at dispatch time.
    """
    source = os.environ if environ is None else environ
    return adapter_enabled is True and source.get("ALLOW_LIVE_PROVIDERS") == "true"
