#!/usr/bin/env python3
"""Validate UPKB JSON indexes, JSON Schemas, records, and cross-index references."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
FORMAT_CHECKER = FormatChecker()


def load(relative: str):
    path = ROOT / relative
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        ERRORS.append(f"{relative}: cannot load JSON: {exc}")
        return None


def validate_record(schema_name: str, record: object, source: str) -> None:
    schema = SCHEMAS.get(schema_name)
    if schema is None:
        ERRORS.append(f"{source}: schema {schema_name!r} unavailable")
        return
    validator = Draft202012Validator(schema, format_checker=FORMAT_CHECKER)
    for error in sorted(validator.iter_errors(record), key=lambda e: list(map(str, e.absolute_path))):
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        ERRORS.append(f"{source}:{location}: {error.message}")


def require_array(document: dict | None, key: str, source: str) -> list:
    if not isinstance(document, dict) or not isinstance(document.get(key), list):
        ERRORS.append(f"{source}: {key!r} must be an array")
        return []
    return document[key]


SCHEMA_NAMES = ("document", "checkpoint", "environment")
SCHEMAS: dict[str, dict] = {}
for name in SCHEMA_NAMES:
    schema = load(f"SCHEMA/{name}.schema.json")
    if isinstance(schema, dict):
        try:
            Draft202012Validator.check_schema(schema)
            if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
                ERRORS.append(f"SCHEMA/{name}.schema.json: unexpected JSON Schema dialect")
            SCHEMAS[name] = schema
        except Exception as exc:
            ERRORS.append(f"SCHEMA/{name}.schema.json: invalid schema: {exc}")

master = load("INDEX/MASTER_INDEX.json")
projects_doc = load("INDEX/PROJECT_INDEX.json")
agents_doc = load("INDEX/AGENT_INDEX.json")
indexes = {
    "DOCUMENT_INDEX": load("INDEX/DOCUMENT_INDEX.json"),
    "TASK_INDEX": load("INDEX/TASK_INDEX.json"),
    "RESEARCH_INDEX": load("INDEX/RESEARCH_INDEX.json"),
    "ENVIRONMENT_INDEX": load("INDEX/ENVIRONMENT_INDEX.json"),
    "CHECKPOINT_INDEX": load("INDEX/CHECKPOINT_INDEX.json"),
    "PULL_REQUEST_INDEX": load("INDEX/PULL_REQUEST_INDEX.json"),
}

project_records = require_array(projects_doc, "projects", "PROJECT_INDEX")
project_ids: set[str] = set()
for i, record in enumerate(project_records):
    source = f"PROJECT_INDEX.projects[{i}]"
    if not isinstance(record, dict):
        ERRORS.append(f"{source}: record must be an object")
        continue
    for field in ("project_id", "name", "status", "next_action"):
        if not record.get(field):
            ERRORS.append(f"{source}: missing required field {field!r}")
    project_id = record.get("project_id")
    if isinstance(project_id, str):
        if project_id in project_ids:
            ERRORS.append(f"{source}: duplicate project_id {project_id!r}")
        project_ids.add(project_id)
    if record.get("status") not in {"VERIFIED", "REPORTED", "PLANNED", "UNKNOWN"}:
        ERRORS.append(f"{source}: invalid evidence status {record.get('status')!r}")

if isinstance(master, dict):
    if master.get("schema_version") != "1.0.0":
        ERRORS.append("MASTER_INDEX: schema_version must be 1.0.0")
    repositories = master.get("repositories")
    if not isinstance(repositories, dict) or not isinstance(repositories.get("observed_repositories"), list):
        ERRORS.append("MASTER_INDEX: repositories.observed_repositories must be an array")
    for key in ("projects_index", "documents_index", "tasks_index", "research_index",
                "agents_index", "environments_index", "checkpoints_index", "pull_request_index"):
        path = master.get(key)
        if not isinstance(path, str) or not (ROOT / "INDEX" / path).is_file():
            ERRORS.append(f"MASTER_INDEX: {key} must reference an existing INDEX file")

if isinstance(agents_doc, dict):
    agents = require_array(agents_doc, "agents", "AGENT_INDEX")
    seen_agents: set[str] = set()
    for i, agent in enumerate(agents):
        if not isinstance(agent, dict) or not agent.get("agent_id"):
            ERRORS.append(f"AGENT_INDEX.agents[{i}]: expected object with agent_id")
            continue
        if agent["agent_id"] in seen_agents:
            ERRORS.append(f"AGENT_INDEX.agents[{i}]: duplicate agent_id {agent['agent_id']!r}")
        seen_agents.add(agent["agent_id"])

for name, document in indexes.items():
    if not isinstance(document, dict):
        continue
    records = require_array(document, "records", name)
    seen: set[str] = set()
    id_field = {
        "DOCUMENT_INDEX": "document_id",
        "TASK_INDEX": "task_id",
        "RESEARCH_INDEX": "research_id",
        "ENVIRONMENT_INDEX": "environment_id",
        "CHECKPOINT_INDEX": "checkpoint_id",
        "PULL_REQUEST_INDEX": None,
    }[name]
    for i, record in enumerate(records):
        source = f"{name}.records[{i}]"
        if not isinstance(record, dict):
            ERRORS.append(f"{source}: record must be an object")
            continue
        if id_field:
            identifier = record.get(id_field)
            if not isinstance(identifier, str) or not identifier:
                ERRORS.append(f"{source}: missing {id_field}")
            elif identifier in seen:
                ERRORS.append(f"{source}: duplicate {id_field} {identifier!r}")
            else:
                seen.add(identifier)
        project_id = record.get("project_id")
        if project_id is not None and project_id not in project_ids:
            ERRORS.append(f"{source}: unknown project_id {project_id!r}")
        if name == "DOCUMENT_INDEX":
            validate_record("document", record, source)
        elif name == "ENVIRONMENT_INDEX":
            validate_record("environment", record, source)
        elif name == "CHECKPOINT_INDEX":
            checkpoint_path = record.get("path")
            if not isinstance(checkpoint_path, str):
                ERRORS.append(f"{source}: checkpoint path is required")
            else:
                checkpoint = load(checkpoint_path)
                if checkpoint is not None:
                    validate_record("checkpoint", checkpoint, checkpoint_path)
                    if checkpoint.get("checkpoint_id") != record.get("checkpoint_id"):
                        ERRORS.append(f"{source}: checkpoint_id does not match {checkpoint_path}")
                    if checkpoint.get("project_id") != project_id:
                        ERRORS.append(f"{source}: project_id does not match {checkpoint_path}")

if ERRORS:
    print("\n".join(f"ERROR: {error}" for error in ERRORS))
    sys.exit(1)

print(
    "UPKB validation passed: "
    f"{len(project_records)} projects, "
    f"{sum(len(doc.get('records', [])) for doc in indexes.values() if isinstance(doc, dict))} indexed records, "
    f"{len(SCHEMAS)} JSON Schemas checked."
)
