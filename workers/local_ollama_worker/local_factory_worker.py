#!/usr/bin/env python3
"""Local zero-cost Factory Worker backed strictly by loopback Ollama (127.0.0.1 / localhost).

Scans coordination/<channel>/inbox/*.md for uncompleted tasks (no matching REPORT_*.md in outbox/),
validates strict offline loopback boundary (blocks any non-loopback URL or paid cloud API),
redacts secret patterns before logging/writing, and writes structured draft reports into
coordination/<channel>/outbox/ (never writing empty ACKs).
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "qwen3.5:4b"
SUPPORTED_CHANNELS = ("qwen", "gemini", "claude", "chatgpt")

SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{16,}\b"),
    re.compile(r"\bAIza[0-9A-Za-z\-_]{20,}\b"),
    re.compile(r"(?i)(bearer\s+)[A-Za-z0-9\-._~+/=]{16,}"),
    re.compile(r"(?i)(password|passwd|api[_-]?key|secret|token)\s*[:=]\s*['\"]?([A-Za-z0-9\-._~+/!@#$%^&*=]{8,})"),
    re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
)


def validate_loopback_ollama_url(raw_url: str) -> str:
    """Enforce zero-cost local-only rule: refuse any non-loopback or non-HTTP(S) endpoint."""
    parsed = urllib.parse.urlparse((raw_url or "").strip())
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported scheme for local Ollama worker: {parsed.scheme!r}")
    host = (parsed.hostname or "").strip().lower()
    if not host:
        raise ValueError("Ollama URL must include a loopback hostname")
    if host != "localhost":
        try:
            ip = ipaddress.ip_address(host)
        except ValueError as exc:
            raise ValueError(
                f"External host blocked ({host!r}): local factory worker allows only localhost/127.0.0.1/::1"
            ) from exc
        if not ip.is_loopback:
            raise ValueError(
                f"Non-loopback IP blocked ({host!r}): local factory worker cannot reach remote networks"
            )
    return raw_url.rstrip("/")


def redact_secrets(text: str) -> str:
    """Mask accidental credentials before persisting worker reports or printing diagnostics."""
    cleaned = text or ""
    for pat in SECRET_PATTERNS:
        if pat.groups >= 2:
            cleaned = pat.sub(lambda m: f"{m.group(1)}=[REDACTED]", cleaned)
        elif pat.groups == 1:
            cleaned = pat.sub(r"\1[REDACTED]", cleaned)
        else:
            cleaned = pat.sub("[REDACTED_SECRET]", cleaned)
    return cleaned


def strip_think_blocks(text: str) -> str:
    """Strip inline <think>...</think> reasoning blocks emitted by thinking models."""
    return re.sub(r"(?is)<think>.*?</think>", "", text or "").strip()


def is_substantive_task_file(path: Path) -> bool:
    name = path.name
    if not path.is_file() or path.suffix.lower() != ".md":
        return False
    if name.startswith(".") or name.upper() == "README.MD":
        return False
    return True


def expected_report_path(repo_root: Path, channel: str, inbox_file: Path) -> Path:
    stem = inbox_file.stem
    report_name = f"REPORT_{stem.upper()}.md"
    return repo_root / "coordination" / channel / "outbox" / report_name


def has_existing_report(repo_root: Path, channel: str, inbox_file: Path) -> bool:
    outbox = repo_root / "coordination" / channel / "outbox"
    if not outbox.is_dir():
        return False
    if expected_report_path(repo_root, channel, inbox_file).is_file():
        return True
    stem_norm = re.sub(r"[^a-z0-9]+", "", inbox_file.stem.lower())
    # Ignore empty ACK_/ACCEPTED_ placeholders: only real REPORT_* closes an inbox task.
    for existing in outbox.glob("REPORT_*.md"):
        norm = re.sub(r"[^a-z0-9]+", "", existing.stem.lower())
        if stem_norm and stem_norm in norm and existing.stat().st_size > 200:
            return True
    return False


def discover_pending_tasks(repo_root: Path, channels: list[str] | tuple[str, ...] | None = None) -> list[tuple[str, Path]]:
    targets = tuple(channels) if channels else SUPPORTED_CHANNELS
    pending: list[tuple[str, Path]] = []
    for channel in targets:
        if channel not in SUPPORTED_CHANNELS:
            raise ValueError(f"Unsupported channel {channel!r}; expected one of {SUPPORTED_CHANNELS}")
        inbox_dir = repo_root / "coordination" / channel / "inbox"
        if not inbox_dir.is_dir():
            continue
        for item in sorted(inbox_dir.iterdir()):
            if is_substantive_task_file(item) and not has_existing_report(repo_root, channel, item):
                pending.append((channel, item))
    return pending


def ollama_http_json(url: str, payload: dict[str, Any] | None = None, timeout_s: float = 120.0) -> dict[str, Any]:
    validated_base = validate_loopback_ollama_url(url) if payload is None else url
    full_url = validated_base
    if payload is not None:
        base_root = f"{urllib.parse.urlparse(url).scheme}://{urllib.parse.urlparse(url).netloc}"
        validate_loopback_ollama_url(base_root)
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(full_url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    else:
        req = urllib.request.Request(full_url, method="GET")
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        return json.loads(resp.read().decode("utf-8"))


def check_ollama_health(base_url: str, model: str, transport: Callable[..., dict[str, Any]] = ollama_http_json) -> dict[str, Any]:
    root = validate_loopback_ollama_url(base_url)
    tags = transport(f"{root}/api/tags", None, timeout_s=10.0)
    models = [m.get("name", "") for m in tags.get("models", []) if isinstance(m, dict)]
    return {
        "ok": True,
        "url": root,
        "requested_model": model,
        "model_available": model in models or any(m.startswith(model.split(":")[0]) for m in models),
        "installed_models": models,
    }


def build_task_prompt(channel: str, inbox_path: Path, raw_text: str, repo_root: Path) -> str:
    clipped = raw_text[:6000]
    if len(raw_text) > 6000:
        clipped += "\n\n[... содержимое обрезано до 6000 символов для локального контекста ...]"
    rel = inbox_path.relative_to(repo_root).as_posix()
    return (
        "Ты локальный zero-cost ревьюер Universal AI Factory. "
        "Пиши строго технически на русском языке, не придумывай непроверенные тесты/устройства, "
        "не выводи пустых ACK и не используй платные облачные API. "
        "Пиши компактно (до ~700–1000 слов), не выдумывай URL, пути репозитория, названия файлов моделей "
        "или замеры производительности — опирайся только на факты из задания и явно помечай открытые вопросы для ручной проверки. "
        "Не копируй статус `QUEUED` или `PENDING` из исходного задания как статус самого отчёта — "
        "указывай статус `LOCAL_OLLAMA_DRAFT`. Напиши полный законченный отчёт со всеми разделами, не обрывая списки.\n\n"
        f"Канал: {channel}\nЗадача: `{rel}`\n\n"
        "Подготовь структурированный черновой отчёт строго по следующим разделам:\n"
        "1. Резюме и соблюдение zero-cost.\n"
        "2. Проверенные факты из задания.\n"
        "3. Исключённые платные и облачные варианты.\n"
        "4. Ограничения и риски (включая отсутствие замеров на физическом OPPO).\n"
        "5. Следующие шаги без мержа PR и запуска платных сервисов.\n\n"
        f"{clipped}"
    )


def _generate_with_think_fallback(
    root: str,
    model: str,
    prompt: str,
    transport: Callable[..., dict[str, Any]],
) -> dict[str, Any]:
    """Call /api/generate with think=False and fall back cleanly if a model rejects 'think' with HTTP 400."""
    payload: dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "think": False,
        "options": {"temperature": 0.2, "num_ctx": 8192, "num_predict": 4096},
    }
    try:
        return transport(f"{root}/api/generate", payload, timeout_s=240.0)
    except urllib.error.HTTPError as exc:
        if exc.code != 400:
            raise
        fallback_payload = dict(payload)
        fallback_payload.pop("think", None)
        return transport(f"{root}/api/generate", fallback_payload, timeout_s=240.0)


def run_once(
    repo_root: Path,
    base_url: str = DEFAULT_OLLAMA_URL,
    model: str = DEFAULT_MODEL,
    channels: list[str] | None = None,
    dry_run: bool = False,
    max_tasks: int = 1,
    transport: Callable[..., dict[str, Any]] = ollama_http_json,
) -> dict[str, Any]:
    root = validate_loopback_ollama_url(base_url)
    pending = discover_pending_tasks(repo_root, channels)
    selected = pending[: max(1, max_tasks)]
    results: list[dict[str, Any]] = []

    if dry_run:
        return {
            "mode": "dry_run",
            "ollama_url": root,
            "model": model,
            "pending_total": len(pending),
            "pending": [
                {"channel": ch, "inbox": str(p.relative_to(repo_root).as_posix()), "target_report": str(expected_report_path(repo_root, ch, p).relative_to(repo_root).as_posix())}
                for ch, p in pending
            ],
        }

    health = check_ollama_health(root, model, transport=transport)
    if not health["model_available"]:
        raise RuntimeError(
            f"Requested local model {model!r} not found in Ollama ({health['installed_models']})"
        )

    for channel, inbox_file in selected:
        raw_task = redact_secrets(inbox_file.read_text(encoding="utf-8", errors="replace"))
        prompt = build_task_prompt(channel, inbox_file, raw_task, repo_root)
        t0 = time.monotonic()
        resp = _generate_with_think_fallback(root, model, prompt, transport)
        elapsed_s = round(time.monotonic() - t0, 2)
        done_reason = str(resp.get("done_reason") or "").strip()
        answer = redact_secrets(strip_think_blocks(resp.get("response") or ""))
        if len(answer) < 80:
            raise RuntimeError(f"Ollama returned an empty or too short response ({len(answer)} chars) — refusing empty ACK.")
        if done_reason == "length":
            answer += "\n\n> [!WARNING]\n> Генерация достигла лимита `num_predict` (`done_reason=length`). Требуется проверка полноты отчёта.\n"

        target = expected_report_path(repo_root, channel, inbox_file)
        target.parent.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        header = (
            f"# Local Ollama Draft Report — {inbox_file.name}\n\n"
            f"- **Generated at:** {stamp}\n"
            f"- **Worker:** `local_factory_worker.py` (strict loopback `127.0.0.1`, zero-cost)\n"
            f"- **Model:** `{model}` (`{elapsed_s}s`, `done_reason={done_reason or 'unknown'}`)\n"
            f"- **Source task:** `{inbox_file.relative_to(repo_root).as_posix()}`\n"
            f"- **Notice:** Draft generated offline from inbox specification; verify source code and run tests before merge.\n\n"
            "---\n\n"
        )
        target.write_text(header + answer + "\n", encoding="utf-8")
        results.append(
            {
                "channel": channel,
                "inbox": inbox_file.relative_to(repo_root).as_posix(),
                "report": target.relative_to(repo_root).as_posix(),
                "bytes": target.stat().st_size,
                "elapsed_s": elapsed_s,
                "done_reason": done_reason,
            }
        )

    return {
        "mode": "executed",
        "ollama_url": root,
        "model": model,
        "pending_before": len(pending),
        "processed": results,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Zero-cost loopback Ollama worker for Universal AI Factory.")
    parser.add_argument("--repo", default=str(Path(__file__).resolve().parents[2]), help="Path to Universal-AI-Factory repo")
    parser.add_argument("--ollama-url", default=os.environ.get("OLLAMA_HOST", DEFAULT_OLLAMA_URL))
    parser.add_argument("--model", default=os.environ.get("FACTORY_LOCAL_MODEL", DEFAULT_MODEL))
    parser.add_argument("--channel", action="append", choices=SUPPORTED_CHANNELS, help="Restrict scan to specific channel(s)")
    parser.add_argument("--max-tasks", type=int, default=1)
    parser.add_argument("--health", action="store_true", help="Check local loopback Ollama health and installed models")
    parser.add_argument("--dry-run", action="store_true", help="List pending inbox tasks without invoking model or writing files")
    parser.add_argument("--once", action="store_true", help="Process up to --max-tasks pending inbox tasks and exit")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo).resolve()
    try:
        if args.health:
            out = check_ollama_health(args.ollama_url, args.model)
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return 0 if out["model_available"] else 2
        if args.dry_run or args.once:
            out = run_once(
                repo_root=repo_root,
                base_url=args.ollama_url,
                model=args.model,
                channels=args.channel,
                dry_run=args.dry_run,
                max_tasks=args.max_tasks,
            )
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return 0
        parser.print_help()
        return 1
    except (ValueError, RuntimeError, urllib.error.URLError) as exc:
        print(json.dumps({"ok": False, "error": redact_secrets(str(exc))}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
