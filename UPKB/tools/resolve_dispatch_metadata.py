#!/usr/bin/env python3
"""Resolve strict project/task metadata from one Gemini dispatch Markdown file."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
import sys


PROJECT_RE = re.compile(r"^[A-Z0-9][A-Z0-9_:-]{1,63}$")
TASK_RE = re.compile(r"^[A-Z0-9][A-Z0-9._:-]{1,95}$")
REQUIRED = {"upkb_project_id", "upkb_task_id"}


class DispatchMetadataError(RuntimeError):
    pass


def resolve_dispatch(task_file: Path, repo_root: Path, task_index_path: Path) -> dict:
    root = repo_root.resolve()
    candidate = task_file.resolve()
    try:
        relative = candidate.relative_to(root).as_posix()
    except ValueError as exc:
        raise DispatchMetadataError("dispatch file must be inside the repository") from exc
    if not re.fullmatch(r"coordination/gemini/dispatch/[A-Za-z0-9._-]+\.md", relative):
        raise DispatchMetadataError("dispatch file must be a Markdown file under coordination/gemini/dispatch")
    try:
        lines = candidate.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise DispatchMetadataError(f"cannot read dispatch file: {exc}") from exc
    if len(lines) < 4 or lines[0].strip() != "---":
        raise DispatchMetadataError("dispatch file must start with a strict metadata block")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise DispatchMetadataError("metadata block terminator is missing") from exc
    values = {}
    for line_number, line in enumerate(lines[1:end], start=2):
        if not line.strip():
            continue
        if ":" not in line:
            raise DispatchMetadataError(f"malformed metadata line {line_number}")
        key, value = (part.strip() for part in line.split(":", 1))
        if key not in REQUIRED:
            raise DispatchMetadataError(f"unknown metadata key {key!r}")
        if key in values:
            raise DispatchMetadataError(f"duplicate metadata key {key!r}")
        values[key] = value
    if set(values) != REQUIRED or not all(values.values()):
        raise DispatchMetadataError("both upkb_project_id and upkb_task_id are required exactly once")
    project_id, task_id = values["upkb_project_id"], values["upkb_task_id"]
    if not PROJECT_RE.fullmatch(project_id):
        raise DispatchMetadataError("invalid upkb_project_id")
    if not TASK_RE.fullmatch(task_id):
        raise DispatchMetadataError("invalid upkb_task_id")
    if not any(line.strip() for line in lines[end + 1:]):
        raise DispatchMetadataError("dispatch task body must not be empty")
    try:
        index = json.loads(task_index_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DispatchMetadataError(f"cannot load task index: {exc}") from exc
    records = index.get("records") if isinstance(index, dict) else None
    if not isinstance(records, list) or any(not isinstance(item, dict) for item in records):
        raise DispatchMetadataError("TASK_INDEX.records must be an array of objects")
    matches = [item for item in records if item.get("task_id") == task_id]
    if len(matches) != 1:
        raise DispatchMetadataError(f"expected exactly one task record for {task_id!r}; found {len(matches)}")
    if matches[0].get("project_id") != project_id:
        raise DispatchMetadataError(
            f"task {task_id!r} belongs to {matches[0].get('project_id')!r}, not {project_id!r}"
        )
    return {
        "project_id": project_id,
        "task_id": task_id,
        "dispatch_path": relative,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-file", required=True, type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--task-index", type=Path, default=Path("UPKB/INDEX/TASK_INDEX.json"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        root = args.repo_root.resolve()
        task_index = args.task_index if args.task_index.is_absolute() else root / args.task_index
        result = resolve_dispatch(args.task_file, root, task_index)
        rendered = json.dumps(result, ensure_ascii=False, indent=2) + chr(10)
        if args.output:
            args.output.write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
        return 0
    except DispatchMetadataError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
