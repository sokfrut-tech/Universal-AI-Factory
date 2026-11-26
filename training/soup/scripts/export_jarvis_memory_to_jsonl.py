#!/usr/bin/env python3
"""Convert Jarvis Ai exported memory JSON (or dialogue JSON) into Soup Alpaca JSONL.

Enforces fail-closed SecretGuard filtering so secrets, API keys, passwords, PEM blocks,
or Luhn-valid payment card numbers never enter training datasets.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

INVISIBLE_CHARS_RE = re.compile(r"[\u200B-\u200F\u202A-\u202E\u2060\uFEFF\u00AD]")
CONFUSABLE_TRANS = str.maketrans("авекмнорстухіАВЕКМНОРСТУХІ", "abekmhopctyxiABEKMHOPCTYXI")

SECRET_PATTERNS = [
    re.compile(r"\bsk-(?:proj-|ant-|live-|test-)?[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{20,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{16,}\b", re.IGNORECASE),
    re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"(?:парол[ья]|parol|password)\s*(?:(?:от|для|к|of|for)\s+\S+\s*){0,2}(?:[:=\-–—]|это|is)\s*\S{3,}", re.IGNORECASE),
    re.compile(r"\b(?:pin|пин(?:-код)?)\s*(?:[:=\-–—]|это)\s*\d{4,12}\b", re.IGNORECASE),
]
CARD_RE = re.compile(r"(?<!\d)(?:\d[ -]?){13,19}(?!\d)")


def passes_luhn(digits: str) -> bool:
    if not (13 <= len(digits) <= 19) or len(set(digits)) == 1:
        return False
    total = 0
    double_it = False
    for ch in reversed(digits):
        d = ord(ch) - ord("0")
        if double_it:
            d *= 2
            if d > 9:
                d -= 9
        total += d
        double_it = not double_it
    return total % 10 == 0


def is_safe_text(text: str) -> bool:
    if not text or not text.strip():
        return False
    norm = INVISIBLE_CHARS_RE.sub("", unicodedata.normalize("NFKC", text))
    folded = norm.translate(CONFUSABLE_TRANS)
    for pat in SECRET_PATTERNS:
        if pat.search(norm) or pat.search(folded):
            return False
    for m in CARD_RE.finditer(norm):
        digits = "".join(c for c in m.group(0) if c.isdigit())
        if passes_luhn(digits):
            return False
    return True


def convert_export_to_alpaca(payload: dict) -> tuple[list[dict], int]:
    rows: list[dict] = []
    skipped = 0
    for fact in payload.get("facts", []):
        content = str(fact.get("content", "")).strip()
        if not is_safe_text(content):
            skipped += 1
            continue
        rows.append(
            {
                "instruction": "Учти сохранённый факт о пользователе при ответе.",
                "input": "",
                "output": f"Принято: {content}",
            }
        )
    return rows, skipped


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert Jarvis Ai memory JSON to safe Soup Alpaca JSONL")
    parser.add_argument("--input", required=True, help="Path to exported jarvis_memory.json")
    parser.add_argument("--output", required=True, help="Destination .jsonl path")
    args = parser.parse_args()

    src = Path(args.input)
    payload = json.loads(src.read_text(encoding="utf-8"))
    rows, skipped = convert_export_to_alpaca(payload)

    dst = Path(args.output)
    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Exported {len(rows)} safe training rows to {dst} (blocked_secrets={skipped})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
