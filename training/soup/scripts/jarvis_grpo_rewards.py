#!/usr/bin/env python3
"""
Verifiable RLVR / StraTA reward functions for Jarvis Ai GRPO training on 6 GB VRAM.

Combines:
- StraTA (Strategic Trajectory Abstraction): rewards structured step-by-step plans on complex tasks.
- Voice-first Russian fluency: penalizes CJK/special-token leakage and bloated markdown on voice replies.
- Uncensored directness: penalizes preachy AI disclaimers ("как языковая модель...").
- SecretGuard safety: strictly rewards refusing to store passwords, seed phrases, and API tokens.
- Verifiable factual/math accuracy: checks expected/forbidden regexes per prompt.
"""

from __future__ import annotations

import re
from typing import Any

CJK_RE = re.compile(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]")
CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")
SPECIAL_LEAK_RE = re.compile(r"<\|(?:im_end|im_start|endoftext|eot_id|end_of_text)\|>|</s>", re.IGNORECASE)
PREACHY_RE = re.compile(
    r"как\s+(?:искусственн\w+\s+интеллект|языков\w+\s+модел\w+|ответственн\w+\s+ии)|"
    r"я\s+не\s+могу\s+(?:обсуждать|помочь\s+с\s+этим|выполнить\s+этот\s+запрос\s+по\s+этическим)|"
    r"нарушает\s+(?:политику|правила\s+безопасности)|"
    r"обратитесь\s+к\s+квалифицированному\s+специалисту",
    re.IGNORECASE,
)
SECRET_REFUSAL_RE = re.compile(
    r"secretguard|нельзя|запрещ|отклон|блокир|не\s+сохран|не\s+запис|не\s+запомина|не\s+буду\s+сохран",
    re.IGNORECASE,
)
SECRET_ACCEPT_RE = re.compile(
    r"успешно\s+сохран|запомнил\s+(?:ваш\s+)?(?:пароль|ключ|токен|сид|фразу)|(?:пароль|ключ|токен).*сохран[её]н",
    re.IGNORECASE,
)
STEP_LIST_RE = re.compile(r"(?:^|\n)\s*(?:1[\.\)]|шаг\s*1|[-•]\s+)", re.IGNORECASE)
MULTI_STEP_RE = re.compile(r"(?:^|\n)\s*(?:2[\.\)]|шаг\s*2)", re.IGNORECASE)


def extract_completion_text(completion: Any) -> str:
    """Normalizes TRL GRPO completion items (plain str or chat message list)."""
    if isinstance(completion, str):
        return completion.strip()
    if isinstance(completion, list) and completion:
        parts = []
        for msg in completion:
            if isinstance(msg, dict):
                parts.append(str(msg.get("content", "")))
            else:
                parts.append(str(msg))
        return "\n".join(parts).strip()
    if isinstance(completion, dict):
        return str(completion.get("content", "")).strip()
    return str(completion or "").strip()


def reward_russian_fluency(completions: list[Any], **kwargs: Any) -> list[float]:
    """Rewards clean Russian output without CJK leakage or special stop-token artifacts."""
    scores: list[float] = []
    for comp in completions:
        text = extract_completion_text(comp)
        if not text:
            scores.append(-1.0)
            continue
        score = 0.0
        if SPECIAL_LEAK_RE.search(text):
            score -= 1.0
        if CJK_RE.search(text):
            score -= 1.0
        cyr_count = len(CYRILLIC_RE.findall(text))
        if cyr_count >= 12:
            score += 0.6
        elif cyr_count >= 4:
            score += 0.2
        else:
            score -= 0.5
        if len(text) >= 15 and text[-1] in ".!?»\"')":
            score += 0.2
        scores.append(round(score, 4))
    return scores


def reward_no_preaching(completions: list[Any], **kwargs: Any) -> list[float]:
    """Penalizes preachy AI disclaimers; rewards direct, natural Jarvis tone."""
    scores: list[float] = []
    for comp in completions:
        text = extract_completion_text(comp)
        if not text:
            scores.append(-0.5)
            continue
        if PREACHY_RE.search(text):
            scores.append(-1.2)
        else:
            scores.append(0.4)
    return scores


def reward_task_verifiable(
    completions: list[Any],
    task_type: list[str] | None = None,
    expected_regex: list[str] | None = None,
    forbidden_regex: list[str] | None = None,
    **kwargs: Any,
) -> list[float]:
    """
    Task-aware verifiable reward (StraTA planning + SecretGuard + Voice conciseness + Exact facts).
    """
    n = len(completions)
    types = task_type if task_type and len(task_type) == n else ["general"] * n
    expected = expected_regex if expected_regex and len(expected_regex) == n else [""] * n
    forbidden = forbidden_regex if forbidden_regex and len(forbidden_regex) == n else [""] * n

    scores: list[float] = []
    for text_raw, ttype, exp_pat, bad_pat in zip(completions, types, expected, forbidden):
        text = extract_completion_text(text_raw)
        if not text:
            scores.append(-1.0)
            continue

        score = 0.0
        # 1. Exact verifiable checks
        if bad_pat and re.search(bad_pat, text, flags=re.IGNORECASE):
            score -= 1.5
        if exp_pat:
            if re.search(exp_pat, text, flags=re.IGNORECASE):
                score += 1.2
            else:
                score -= 0.6

        # 2. Task-specific StraTA / Voice / SecretGuard shaping
        if ttype == "secret_guard":
            if SECRET_ACCEPT_RE.search(text):
                score -= 2.0
            elif SECRET_REFUSAL_RE.search(text):
                score += 1.2
            else:
                score -= 0.5
        elif ttype == "strata":
            if STEP_LIST_RE.search(text) and MULTI_STEP_RE.search(text):
                score += 0.9
            elif STEP_LIST_RE.search(text):
                score += 0.3
            else:
                score -= 0.3
            if 100 <= len(text) <= 750:
                score += 0.3
        elif ttype == "voice":
            if 15 <= len(text) <= 240 and "```" not in text and "|" not in text:
                score += 0.8
            elif len(text) > 450:
                score -= 0.5

        scores.append(round(score, 4))
    return scores
