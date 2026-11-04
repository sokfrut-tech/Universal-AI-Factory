"""Strict, side-effect-free validation for bounded unified Git patches.

This module never applies patches, invokes subprocesses, accesses the network, or reads
workspace files. It validates patch metadata and path safety before a later isolated
runner is allowed to consider applying anything.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re
from typing import Iterable


MAX_PATCH_BYTES = 1_000_000
DEFAULT_ALLOWED_TARGETS = frozenset({
    "sokfrut-tech/Universal-AI-Factory",
    "sokfrut-tech/Antigravity-Mobile",
    "sokfrut-tech/Gemeni",
    "sokfrut-tech/RussSearchOPPO",
    "sokfrut-tech/avtoy-korea-auto",
})
_SHA_RE = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_DIFF_RE = re.compile(r"^diff --git a/(.+) b/(.+)$")
_HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(?: .*)?$")


class PatchValidationError(ValueError):
    """Raised when a patch or its execution envelope is unsafe or malformed."""


@dataclass(frozen=True)
class FileChange:
    old_path: str | None
    new_path: str | None
    change_type: str


@dataclass(frozen=True)
class PatchReport:
    task_id: str
    correlation_id: str
    target_repo: str
    base_sha: str
    patch_sha256: str
    patch_bytes: int
    files: tuple[FileChange, ...]

    @property
    def changed_paths(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(
            path for item in self.files
            for path in (item.old_path, item.new_path) if path is not None
        ))


def _validate_id(value: str, label: str) -> None:
    if not isinstance(value, str) or not _ID_RE.fullmatch(value):
        raise PatchValidationError(f"invalid {label}")


def _safe_path(path: str) -> str:
    if not path or path == "/dev/null":
        raise PatchValidationError("empty path is not allowed here")
    if path.startswith("/") or path.startswith("\\") or "\\" in path:
        raise PatchValidationError("absolute paths and backslashes are forbidden")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in path):
        raise PatchValidationError("control characters in path")
    if ":" in path:
        raise PatchValidationError("drive/stream syntax is forbidden")
    parts = path.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise PatchValidationError("non-normalized or traversing path")
    if len(path.encode("utf-8")) > 240:
        raise PatchValidationError("path is too long")
    return path


def validate_patch(
    *,
    task_id: str,
    correlation_id: str,
    target_repo: str,
    base_sha: str,
    patch: str,
    allowed_targets: Iterable[str] = DEFAULT_ALLOWED_TARGETS,
    max_patch_bytes: int = MAX_PATCH_BYTES,
) -> PatchReport:
    """Validate a unified diff and return a deterministic, non-mutating report."""
    _validate_id(task_id, "task_id")
    _validate_id(correlation_id, "correlation_id")
    if target_repo not in frozenset(allowed_targets):
        raise PatchValidationError("target repository is not allowlisted")
    if not isinstance(base_sha, str) or not _SHA_RE.fullmatch(base_sha):
        raise PatchValidationError("base_sha must be a full 40- or 64-character hex SHA")
    if not isinstance(patch, str):
        raise PatchValidationError("patch must be text")

    encoded = patch.encode("utf-8")
    if not encoded or not encoded.strip():
        raise PatchValidationError("patch is empty")
    if max_patch_bytes <= 0 or len(encoded) > min(max_patch_bytes, MAX_PATCH_BYTES):
        raise PatchValidationError("patch exceeds the configured byte limit")
    if "\x00" in patch:
        raise PatchValidationError("NUL bytes are forbidden")
    if "GIT binary patch" in patch or re.search(r"^Binary files .* differ$", patch, re.M):
        raise PatchValidationError("binary patches are unsupported")

    lines = patch.splitlines()
    changes: list[FileChange] = []
    seen: set[str] = set()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line:
            index += 1
            continue
        match = _DIFF_RE.fullmatch(line)
        if not match:
            raise PatchValidationError("expected a diff --git header")
        old_header, new_header = match.groups()
        old_path = _safe_path(old_header)
        new_path = _safe_path(new_header)
        if old_path != new_path:
            raise PatchValidationError("renames and copies are not supported")
        if old_path in seen:
            raise PatchValidationError("duplicate or conflicting file path")
        seen.add(old_path)
        index += 1

        saw_old = saw_new = False
        saw_hunk = False
        change_type = "modify"
        while index < len(lines) and not lines[index].startswith("diff --git "):
            current = lines[index]
            if current.startswith(("rename from ", "rename to ", "copy from ", "copy to ")):
                raise PatchValidationError("renames and copies are unsupported")
            if current.startswith(("new file mode ", "deleted file mode ")):
                mode = current.rsplit(" ", 1)[-1]
                if mode in ("120000", "160000"):
                    raise PatchValidationError("symlinks and submodules are forbidden")
                if mode not in ("100644", "100755"):
                    raise PatchValidationError("unsupported file mode")
                change_type = "add" if current.startswith("new file") else "delete"
            elif current.startswith("old mode ") or current.startswith("new mode "):
                mode = current.rsplit(" ", 1)[-1]
                if mode not in ("100644", "100755"):
                    raise PatchValidationError("unsupported file mode")
            elif current.startswith("--- "):
                value = current[4:]
                if value == "/dev/null":
                    old_path = None
                    change_type = "add"
                elif value.startswith("a/"):
                    old_path = _safe_path(value[2:])
                else:
                    raise PatchValidationError("malformed old-file header")
                saw_old = True
            elif current.startswith("+++ "):
                value = current[4:]
                if value == "/dev/null":
                    new_path = None
                    change_type = "delete"
                elif value.startswith("b/"):
                    new_path = _safe_path(value[2:])
                else:
                    raise PatchValidationError("malformed new-file header")
                saw_new = True
            elif current.startswith("@@ "):
                if not _HUNK_RE.fullmatch(current):
                    raise PatchValidationError("malformed hunk header")
                saw_hunk = True
            elif current.startswith(("index ", "similarity index ", "dissimilarity index ")):
                pass
            elif current.startswith((" ", "+", "-", "\\ No newline")):
                if not saw_hunk:
                    raise PatchValidationError("diff content appears before a hunk header")
            elif current.startswith("GIT binary patch"):
                raise PatchValidationError("binary patches are unsupported")
            else:
                raise PatchValidationError("unexpected or unsupported diff metadata")
            index += 1

        if not (saw_old and saw_new and saw_hunk):
            raise PatchValidationError("each file change needs old/new headers and a hunk")
        if old_path is None and new_path is None:
            raise PatchValidationError("change cannot delete and add /dev/null")
        if old_path is not None and new_path is not None and old_path != new_path:
            raise PatchValidationError("header path does not match diff path")
        changes.append(FileChange(old_path, new_path, change_type))

    if not changes:
        raise PatchValidationError("patch contains no file changes")

    return PatchReport(
        task_id=task_id,
        correlation_id=correlation_id,
        target_repo=target_repo,
        base_sha=base_sha,
        patch_sha256=hashlib.sha256(encoded).hexdigest(),
        patch_bytes=len(encoded),
        files=tuple(changes),
    )
