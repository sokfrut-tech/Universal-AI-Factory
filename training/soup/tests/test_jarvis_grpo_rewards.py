from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from jarvis_grpo_rewards import (  # noqa: E402
    extract_completion_text,
    reward_no_preaching,
    reward_russian_fluency,
    reward_task_verifiable,
)


def test_extract_completion_text_handles_str_and_chat_list() -> None:
    assert extract_completion_text("  Привет! ") == "Привет!"
    assert extract_completion_text([{"role": "assistant", "content": "Готово."}]) == "Готово."


def test_russian_fluency_penalizes_cjk_and_stop_leaks() -> None:
    good, cjk, leak = reward_russian_fluency([
        "Я Джарвис, локальный голосовой помощник.",
        "Привет 你好 мир.",
        "Ответ готов.<|im_end|>",
    ])
    assert good > 0.5
    assert cjk < 0.0
    assert leak < 0.0


def test_no_preaching_penalizes_robotic_disclaimers() -> None:
    direct, preachy = reward_no_preaching([
        "Киберпанк-курьер скользит по мокрому неону, проверяя маршрут в визоре.",
        "Как языковая модель, я не могу обсуждать подобные темы.",
    ])
    assert direct > 0.0
    assert preachy < -0.5


def test_verifiable_rewards_cover_secret_guard_strata_voice_and_math() -> None:
    scores = reward_task_verifiable(
        completions=[
            "SecretGuard запрещает сохранять пароли и токены в память.",
            "Хорошо, я запомнил ваш пароль Qwerty123!",
            "1. Проверить температуру и RAM.\n2. Запустить 4-bit QLoRA.\n3. Прогнать Quality Gate.",
            "Сейчас проверю и сразу сделаю.",
            "3x = 27, значит x = 9.",
        ],
        task_type=["secret_guard", "secret_guard", "strata", "voice", "fact"],
        expected_regex=["", "", "", "", r"\b9\b"],
        forbidden_regex=["", "", "", "", r"x\s*=\s*[0-8]\b"],
    )
    assert scores[0] > 1.0
    assert scores[1] < -1.0
    assert scores[2] > 0.8
    assert scores[3] > 0.5
    assert scores[4] > 1.0
