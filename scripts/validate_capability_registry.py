#!/usr/bin/env python3
"""Validate the factory capability registry without third-party dependencies."""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "config" / "capability-registry.json"
SCHEMA = ROOT / "schemas" / "capability-registry.schema.json"
VALID_STATES = {"operator_only", "adapter_pending", "agent_enabled", "blocked"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    try:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read valid JSON registry/schema: {exc}")

    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail("unexpected schema dialect")
    if registry.get("schema_version") != "1.0.0":
        fail("unsupported schema_version")
    if registry.get("access_states") != sorted(VALID_STATES):
        fail("access_states must enumerate all four supported states in sorted order")

    policy = registry.get("default_policy", {})
    required_policy = {
        "default_access": "operator_only",
        "default_permission": "read",
        "project_isolation": True,
        "secret_values_in_logs": False,
        "ack_is_execution": False,
    }
    for key, expected in required_policy.items():
        if policy.get(key) != expected:
            fail(f"default_policy.{key} must be {expected!r}")

    capabilities = registry.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        fail("capabilities must be a non-empty array")

    capability_properties = schema.get("properties", {}).get("capabilities", {}).get("items", {}).get("properties", {})
    if not {"data_boundary", "write_scope", "adapter_evidence"}.issubset(capability_properties):
        fail("schema is missing capability metadata properties used by the registry")

    seen = set()
    for item in capabilities:
        if not isinstance(item, dict):
            fail("each capability must be an object")
        capability_id = item.get("id")
        if not isinstance(capability_id, str) or not capability_id:
            fail("every capability needs a non-empty id")
        if capability_id in seen:
            fail(f"duplicate capability id: {capability_id}")
        seen.add(capability_id)
        if item.get("access_state") not in VALID_STATES:
            fail(f"{capability_id}: invalid access_state")
        if not isinstance(item.get("operations"), list) or not item["operations"]:
            fail(f"{capability_id}: operations must be a non-empty array")
        if item.get("access_state") == "blocked" and not item.get("blocked_reason"):
            fail(f"{capability_id}: blocked entries need blocked_reason")
        unknown = set(item) - set(capability_properties)
        if unknown:
            fail(f"{capability_id}: properties missing from schema: " + ", ".join(sorted(unknown)))
        for field in ("data_boundary", "write_scope", "adapter_evidence", "blocked_reason"):
            if field in item and not isinstance(item[field], str):
                fail(f"{capability_id}: {field} must be a string")
        if item.get("access_state") == "agent_enabled" and not item.get("adapter_evidence"):
            fail(f"{capability_id}: agent_enabled requires adapter_evidence")

    required = {"github", "files", "web_research", "image_generation", "appdeploy",
                "magicpath", "posthog", "automations", "openai_platform",
                "armorcodex", "skills", "personal_context", "python_container",
                "claude_provider", "gemini_provider"}
    missing = required - seen
    if missing:
        fail("missing capability entries: " + ", ".join(sorted(missing)))

    print(f"OK: {len(capabilities)} capabilities; unique IDs; safe defaults; blocked/provider evidence rules pass.")


if __name__ == "__main__":
    main()
