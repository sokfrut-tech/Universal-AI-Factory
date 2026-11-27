#!/usr/bin/env python3
"""
6 GB VRAM StraTA + GRPO (Group Relative Policy Optimization) trainer for Jarvis Ai.

Trains a hot-swappable LoRA cartridge (QLoRA 4-bit NF4 + bfloat16) using TRL GRPOTrainer
with verifiable Russian rewards (StraTA planning, SecretGuard, voice fluency, zero preaching).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import torch
from datasets import Dataset
from peft import LoraConfig
from transformers import AutoTokenizer, BitsAndBytesConfig
from trl import GRPOConfig, GRPOTrainer

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jarvis_grpo_rewards import (  # noqa: E402
    reward_no_preaching,
    reward_russian_fluency,
    reward_task_verifiable,
)

SYSTEM_PROMPT = (
    "Ты — Джарвис (J.A.R.V.I.S.), персональный локальный ИИ-ассистент пользователя. "
    "Отвечай на грамотном, живом русском языке: коротко и естественно для голосовых вопросов, "
    "чётко по шагам (1., 2., 3.) для сложных стратегических задач, прямо и без нравоучений, "
    "но всегда отказывайся сохранять пароли, ключи и сид-фразы в память (SecretGuard)."
)


def load_grpo_dataset(path: Path) -> Dataset:
    rows = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            rows.append(
                {
                    "prompt": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": item["prompt"]},
                    ],
                    "task_type": item.get("task_type", "general"),
                    "expected_regex": item.get("expected_regex", ""),
                    "forbidden_regex": item.get("forbidden_regex", ""),
                }
            )
    return Dataset.from_list(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Train Jarvis Ai StraTA-GRPO LoRA cartridge on 6 GB VRAM.")
    parser.add_argument(
        "--base-model",
        default="C:/Users/user/Desktop/codex/soup_runs/jarvis_ru_3b_orpo_merged",
        help="Path or HF ID of base model.",
    )
    parser.add_argument(
        "--dataset",
        default=str(Path(__file__).resolve().parents[1] / "data" / "jarvis_strata_grpo.jsonl"),
        help="Path to StraTA GRPO JSONL dataset.",
    )
    parser.add_argument(
        "--output-dir",
        default="C:/Users/user/Desktop/codex/soup_runs/jarvis_ru_3b_strata_grpo",
        help="Output directory for LoRA cartridge adapter.",
    )
    parser.add_argument("--max-steps", type=int, default=40, help="Total GRPO optimizer steps.")
    parser.add_argument("--num-generations", type=int, default=4, help="Group size G per prompt.")
    parser.add_argument("--max-completion-length", type=int, default=140, help="Max generated tokens per rollout.")
    parser.add_argument("--lr", type=float, default=5e-5, help="Learning rate.")
    parser.add_argument("--lora-r", type=int, default=16, help="LoRA rank.")
    args = parser.parse_args()

    t0 = time.monotonic()
    dataset = load_grpo_dataset(Path(args.dataset))
    print(f"[GRPO] Loaded {len(dataset)} StraTA/Jarvis prompts from {args.dataset}")
    print(f"[GRPO] Base model: {args.base_model}")
    print(f"[GRPO] CUDA: {torch.cuda.is_available()} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})")

    tokenizer = AutoTokenizer.from_pretrained(args.base_model, trust_remote_code=False)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    peft_config = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_r * 2,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    )

    grpo_config = GRPOConfig(
        output_dir=args.output_dir,
        max_steps=args.max_steps,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=2,
        generation_batch_size=args.num_generations,
        num_generations=args.num_generations,
        max_completion_length=args.max_completion_length,
        learning_rate=args.lr,
        lr_scheduler_type="cosine",
        warmup_steps=4,
        bf16=True,
        gradient_checkpointing=True,
        logging_steps=2,
        save_steps=args.max_steps,
        report_to="none",
        temperature=0.8,
        beta=0.04,
        model_init_kwargs={
            "quantization_config": bnb_config,
            "torch_dtype": torch.bfloat16,
            "device_map": "auto",
        },
    )

    trainer = GRPOTrainer(
        model=args.base_model,
        processing_class=tokenizer,
        reward_funcs=[
            reward_russian_fluency,
            reward_no_preaching,
            reward_task_verifiable,
        ],
        args=grpo_config,
        train_dataset=dataset,
        peft_config=peft_config,
    )

    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()

    train_result = trainer.train()
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)

    peak_gb = (torch.cuda.max_memory_allocated() / (1024 ** 3)) if torch.cuda.is_available() else 0.0
    elapsed = time.monotonic() - t0
    summary = {
        "base_model": args.base_model,
        "output_dir": args.output_dir,
        "max_steps": args.max_steps,
        "num_generations": args.num_generations,
        "train_loss": float(train_result.training_loss),
        "peak_vram_gb": round(peak_gb, 2),
        "elapsed_sec": round(elapsed, 1),
    }
    summary_path = Path(args.output_dir) / "grpo_run_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[GRPO] DONE in {elapsed:.1f}s | peak VRAM: {peak_gb:.2f} GB | summary -> {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
