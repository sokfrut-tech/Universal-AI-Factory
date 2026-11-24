#!/usr/bin/env python3
"""Dependency-free structural checks for the UPKB seed indexes."""
from __future__ import annotations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []

def load(relative: str):
    path = ROOT / relative
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        ERRORS.append(f"{relative}: cannot parse JSON: {exc}")
        return None

master = load("INDEX/MASTER_INDEX.json")
projects = load("INDEX/PROJECT_INDEX.json")
agents = load("INDEX/AGENT_INDEX.json")
for name in ("DOCUMENT_INDEX", "TASK_INDEX", "RESEARCH_INDEX", "ENVIRONMENT_INDEX", "CHECKPOINT_INDEX"):
    load(f"INDEX/{name}.json")
for name in ("document", "checkpoint", "environment"):
    schema = load(f"SCHEMA/{name}.schema.json")
    if schema and schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        ERRORS.append(f"SCHEMA/{name}.schema.json: unexpected JSON Schema dialect")

if master:
    if master.get("schema_version") != "1.0.0":
        ERRORS.append("MASTER_INDEX: schema_version must be 1.0.0")
    if not isinstance(master.get("repositories", {}).get("observed_repositories"), list):
        ERRORS.append("MASTER_INDEX: repositories.observed_repositories must be an array")
if projects:
    records = projects.get("projects")
    if not isinstance(records, list):
        ERRORS.append("PROJECT_INDEX: projects must be an array")
    else:
        ids = [p.get("project_id") for p in records]
        if len(ids) != len(set(ids)):
            ERRORS.append("PROJECT_INDEX: duplicate project_id")
        for p in records:
            for field in ("project_id", "name", "status", "next_action"):
                if not p.get(field):
                    ERRORS.append(f"PROJECT_INDEX: record missing {field}: {p}")
            if p.get("status") not in {"VERIFIED", "REPORTED", "PLANNED", "UNKNOWN"}:
                ERRORS.append(f"PROJECT_INDEX: invalid evidence status for {p.get('project_id')}")
if agents and not isinstance(agents.get("agents"), list):
    ERRORS.append("AGENT_INDEX: agents must be an array")

if ERRORS:
    print("\n".join(f"ERROR: {e}" for e in ERRORS))
    sys.exit(1)
print("UPKB structural validation passed.")
