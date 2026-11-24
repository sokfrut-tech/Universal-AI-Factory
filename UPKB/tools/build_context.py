#!/usr/bin/env python3
"""Build deterministic, fail-closed project context packets from UPKB."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath


class BuildContextError(RuntimeError):
    """Raised when a safe, unambiguous project context cannot be assembled."""


CORE_FILES = (
    "README.md",
    "CORE/RULES.md",
    "CORE/SECURITY.md",
    "CORE/AGENT_START_PROTOCOL.md",
)
INDEX_FILES = {
    "master": "INDEX/MASTER_INDEX.json",
    "projects": "INDEX/PROJECT_INDEX.json",
    "documents": "INDEX/DOCUMENT_INDEX.json",
    "tasks": "INDEX/TASK_INDEX.json",
    "research": "INDEX/RESEARCH_INDEX.json",
    "agents": "INDEX/AGENT_INDEX.json",
    "environments": "INDEX/ENVIRONMENT_INDEX.json",
    "checkpoints": "INDEX/CHECKPOINT_INDEX.json",
    "pull_requests": "INDEX/PULL_REQUEST_INDEX.json",
}
COMMIT_RE = re.compile(r"^[0-9a-fA-F]{40}$")


def read_text(root: Path, relative: str) -> str:
    path = root / relative
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise BuildContextError(f"required file {relative!r} is unavailable: {exc}") from exc


def read_json(root: Path, relative: str) -> dict:
    try:
        value = json.loads(read_text(root, relative))
    except json.JSONDecodeError as exc:
        raise BuildContextError(f"invalid JSON in {relative}: {exc}") from exc
    if not isinstance(value, dict):
        raise BuildContextError(f"{relative} must contain a JSON object")
    return value


def records(index: dict, key: str, source: str) -> list[dict]:
    values = index.get(key)
    if not isinstance(values, list) or any(not isinstance(item, dict) for item in values):
        raise BuildContextError(f"{source}.{key} must be an array of objects")
    return values


def resolve_indexed_path(root: Path, raw_path: object) -> Path:
    if not isinstance(raw_path, str) or not raw_path:
        raise BuildContextError("checkpoint index path must be a non-empty string")
    normalized = PurePosixPath(raw_path)
    if normalized.is_absolute() or ".." in normalized.parts:
        raise BuildContextError(f"unsafe checkpoint path: {raw_path!r}")
    parts = list(normalized.parts)
    if parts and parts[0] == "UPKB":
        parts = parts[1:]
    candidate = root.joinpath(*parts).resolve()
    base = root.resolve()
    if candidate != base and base not in candidate.parents:
        raise BuildContextError(f"checkpoint path escapes UPKB root: {raw_path!r}")
    return candidate


def build_context(root: Path, project_id: str, source_commit: str, task_id: str | None = None) -> dict:
    """Build one context packet; refuse missing or ambiguous project/checkpoint data."""
    root = root.resolve()
    if not project_id or not isinstance(project_id, str):
        raise BuildContextError("project_id is required")
    if not COMMIT_RE.fullmatch(source_commit or ""):
        raise BuildContextError("source_commit must be an exact 40-character Git commit SHA")

    core = {name: read_text(root, path) for name, path in (
        ("upkb_readme", CORE_FILES[0]),
        ("rules", CORE_FILES[1]),
        ("security", CORE_FILES[2]),
        ("agent_start_protocol", CORE_FILES[3]),
    )}
    loaded = {name: read_json(root, path) for name, path in INDEX_FILES.items()}

    projects = records(loaded["projects"], "projects", "PROJECT_INDEX")
    matches = [item for item in projects if item.get("project_id") == project_id]
    if len(matches) != 1:
        raise BuildContextError(f"expected exactly one project record for {project_id!r}; found {len(matches)}")
    project = matches[0]

    selected_task = None
    if task_id is not None:
        task_records = records(loaded["tasks"], "records", "TASK_INDEX")
        task_matches = [item for item in task_records if item.get("task_id") == task_id]
        if len(task_matches) != 1:
            raise BuildContextError(
                f"expected exactly one task record for {task_id!r}; found {len(task_matches)}"
            )
        selected_task = task_matches[0]
        if selected_task.get("project_id") != project_id:
            raise BuildContextError(
                f"task {task_id!r} belongs to {selected_task.get('project_id')!r}, not {project_id!r}"
            )

    project_readme_path = f"PROJECTS/{project_id}/README.md"
    project_readme = read_text(root, project_readme_path)

    checkpoint_records = records(loaded["checkpoints"], "records", "CHECKPOINT_INDEX")
    candidates = [item for item in checkpoint_records if item.get("project_id") == project_id]
    if not candidates:
        raise BuildContextError(f"no checkpoint is indexed for project {project_id!r}")
    candidates.sort(key=lambda item: (str(item.get("updated_at", "")), str(item.get("checkpoint_id", ""))))
    latest = candidates[-1]
    if len(candidates) > 1 and candidates[-1].get("updated_at") == candidates[-2].get("updated_at"):
        raise BuildContextError(f"ambiguous latest checkpoints for project {project_id!r}")
    checkpoint_path = resolve_indexed_path(root, latest.get("path"))
    try:
        checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BuildContextError(f"cannot read indexed checkpoint {latest.get('path')!r}: {exc}") from exc
    if not isinstance(checkpoint, dict):
        raise BuildContextError("indexed checkpoint must contain a JSON object")
    if checkpoint.get("checkpoint_id") != latest.get("checkpoint_id"):
        raise BuildContextError("checkpoint_id does not match CHECKPOINT_INDEX")
    if checkpoint.get("project_id") != project_id:
        raise BuildContextError("checkpoint project_id does not match requested project")

    project_records = {}
    for name in ("documents", "tasks", "research", "environments", "pull_requests"):
        items = records(loaded[name], "records", name.upper() + "_INDEX")
        project_records[name] = [item for item in items if item.get("project_id") == project_id]

    agent_records = records(loaded["agents"], "agents", "AGENT_INDEX")
    return {
        "context_schema_version": "1.0.0",
        "context_id": f"{project_id}@{source_commit.lower()}",
        "upkb_commit": source_commit.lower(),
        "project_id": project_id,
        "project": project,
        "task": selected_task,
        "core": core,
        "project_readme": project_readme,
        "checkpoint": checkpoint,
        "related": project_records,
        "agents": agent_records,
    }


def resolve_git_commit(root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root, check=True,
            capture_output=True, text=True, timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise BuildContextError(f"cannot determine exact UPKB Git commit: {exc}") from exc
    commit = result.stdout.strip()
    if not COMMIT_RE.fullmatch(commit):
        raise BuildContextError("Git returned an invalid HEAD commit SHA")
    return commit


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-id")
    parser.add_argument("--task-id", help="Require exactly one task record scoped to --project-id")
    parser.add_argument("--all-checkpointed", action="store_true")
    parser.add_argument("--source-commit", help="Exact 40-character commit SHA; defaults to git rev-parse HEAD")
    parser.add_argument("--output")
    parser.add_argument("--output-dir")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args(argv)

    if bool(args.project_id) == bool(args.all_checkpointed):
        parser.error("provide exactly one of --project-id or --all-checkpointed")
    if args.all_checkpointed and not args.output_dir:
        parser.error("--output-dir is required with --all-checkpointed")
    if args.project_id and args.output_dir:
        parser.error("--output-dir is only valid with --all-checkpointed")
    if args.task_id and not args.project_id:
        parser.error("--task-id requires --project-id and cannot be used with --all-checkpointed")

    try:
        repo_root = args.repo_root.resolve()
        root = repo_root / "UPKB"
        if not root.is_dir():
            raise BuildContextError(f"UPKB directory not found under repository root {repo_root}")
        commit = args.source_commit or resolve_git_commit(repo_root)
        if args.all_checkpointed:
            checkpoint_index = read_json(root, INDEX_FILES["checkpoints"])
            project_ids = sorted({
                item.get("project_id")
                for item in records(checkpoint_index, "records", "CHECKPOINT_INDEX")
                if isinstance(item.get("project_id"), str)
            })
            if not project_ids:
                raise BuildContextError("no project checkpoints are indexed")
            output_dir = Path(args.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            for project_id in project_ids:
                packet = build_context(root, project_id, commit)
                (output_dir / f"{project_id}.context.json").write_text(
                    json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
                )
            print(f"Built {len(project_ids)} project context packets at UPKB commit {commit}.")
            return 0

        packet = build_context(root, args.project_id, commit, args.task_id)
        rendered = json.dumps(packet, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            Path(args.output).write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
        return 0
    except BuildContextError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
