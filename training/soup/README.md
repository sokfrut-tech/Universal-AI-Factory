# Обучение локальных моделей Jarvis Ai через Soup (`MakazhanAlpamys/Soup`)

Интеграция открытого инструмента **Soup** ([MakazhanAlpamys/Soup](https://github.com/MakazhanAlpamys/Soup), лицензия **Apache-2.0**, препринт Zenodo DOI `10.5281/zenodo.21918325`) в экосистему **Universal AI Factory** и мобильного ассистента **Jarvis Ai** (`sokfrut-tech/Gemeni`).

## Зачем нужен Soup для Jarvis Ai

1. **Exact Layer Streaming (`stream_layers: true`)** — позволяет дообучать крупные модели (до 8B параметров, например `Saiga / Llama 3.1 8B`) даже на ноутбучной видеокарте с **4–6 ГБ VRAM** за счёт потоковой подачи слоёв из ОЗУ.
2. **Единый декларативный YAML** — обучение (`SFT`, `DPO`, `GRPO`, `RAFT`), проверка утечки данных (`soup data leakage`), проверка сохранения базовых знаний (`soup eval retention`), слияние LoRA-адаптера (`soup merge`) и экспорт в **`GGUF Q4_K_M`** (`soup export --format gguf --quant q4_k_m`) для прямой загрузки в **Jarvis Ai** на Android (`Модели ИИ` → `Импортировать свой .gguf`).
3. **RAFT (`data.format: raft`)** — учит компактные 1.5B–3B модели точно опираться на нужный фрагмент документа из `JarvisDocumentStore` и игнорировать нерелевантный шум.
4. **Непрерывный цикл (`soup serve` / `soup loop` / `soup ship --gate loop-v2`) и MCP** — автоматический отбор качественных правок с откатом при деградации метрик.

## Рецепты в этой папке (`RTX 4050 Laptop 6 ГБ VRAM` / `16 ГБ RAM`)

| Конфиг | Задача | Модель по умолчанию | Датасет |
|---|---|---|---|
| [jarvis-ru-0.5b-pilot-sft.yaml](configs/jarvis-ru-0.5b-pilot-sft.yaml) | Быстрый пилот SFT (`BF16/FP16 LoRA`) на 6 ГБ VRAM | `Qwen/Qwen2.5-0.5B-Instruct` | [jarvis_ru_starter.jsonl](data/jarvis_ru_starter.jsonl) (`90` зап.) |
| [jarvis-ru-3b-sft.yaml](configs/jarvis-ru-3b-sft.yaml) | SFT / 4-bit QLoRA (умещается в 6 ГБ VRAM целиком) | `Qwen/Qwen2.5-3B-Instruct` | [jarvis_ru_starter.jsonl](data/jarvis_ru_starter.jsonl) (`90` зап.) |
| [jarvis-ru-8b-stream-6gb.yaml](configs/jarvis-ru-8b-stream-6gb.yaml) | Layer Streaming (`stream_layers: true`) для 8B моделей | `meta-llama/Llama-3.1-8B-Instruct` (или открытая 8B) | [jarvis_ru_starter.jsonl](data/jarvis_ru_starter.jsonl) (`90` зап.) |
| [jarvis-ru-rag-raft.yaml](configs/jarvis-ru-rag-raft.yaml) | RAFT-дообучение ответам по документам RAG | `Qwen/Qwen2.5-3B-Instruct` | [jarvis_ru_raft.jsonl](data/jarvis_ru_raft.jsonl) (`24` зап.) |

## Проверенный пилот на RTX 4050 (2026-11-27)

- **Конфигурация:** `configs/jarvis-ru-0.5b-pilot-sft.yaml` (`Qwen/Qwen2.5-0.5B-Instruct`, `LoRA r=16, alpha=32`, `epochs=3`, `81` train / `9` val).
- **Обучение (`run_20261127_112534_b07de7e2`):** `33/33` шага за `19.78 s`, `train_loss=2.412` (`2.8483 -> 2.3848`), `eval_loss=2.4979`, пик VRAM `2.0 / 6.0 GB` на `NVIDIA GeForce RTX 4050 Laptop GPU`.
- **Экспорт GGUF (вне git, в `C:\Users\user\Desktop\codex\soup_runs\`):**
  - `jarvis-ru-0.5b-soup-f16.gguf` — `994 156 544` байт, заголовок `GGUF` (`47 47 55 46`), SHA-256 `C21906993D52F80F8F37261E084F54CA55FCABC00C3FABF0DEEEF05E17F23B00`.
  - `jarvis-ru-0.5b-soup-q8_0.gguf` — `531 067 904` байт (~`506.5` МиБ), заголовок `GGUF` (`47 47 55 46`), SHA-256 `48C5CCF2B0B73D512FB813944D99D1070172BB5CA971CF8136F4EDD974AEDCC2` (готов к импорту в **Jarvis Ai** → `Модели` → `Импортировать свой .gguf`).

## Быстрый старт (локальное окружение `c:\Users\user\Desktop\codex\soup_env`)

> [!IMPORTANT]
> Виртуальное окружение с PyTorch/CUDA не хранится в git — оно вынесено в `c:\Users\user\Desktop\codex\soup_env`.

```powershell
# 1. Проверить GPU, CUDA и конфигурацию перед запуском обучения
c:\Users\user\Desktop\codex\soup_env\Scripts\soup.exe doctor --config training/soup/configs/jarvis-ru-3b-sft.yaml
c:\Users\user\Desktop\codex\soup_env\Scripts\soup.exe data inspect training/soup/data/jarvis_ru_starter.jsonl

# 2. Запустить обучение + экспорт GGUF для Android Jarvis Ai
.\training\soup\scripts\run_soup_train_and_gguf.ps1 -ConfigPath .\training\soup\configs\jarvis-ru-3b-sft.yaml

# 3. Конвертация экспортированной памяти Jarvis Ai (JSON) в безопасный JSONL (с SecretGuard)
c:\Users\user\Desktop\codex\soup_env\Scripts\python.exe .\training\soup\scripts\export_jarvis_memory_to_jsonl.py --input .\jarvis_memory_export.json --output .\training\soup\data\jarvis_personal.jsonl
```

## Указание авторства и лицензия

- Инструмент обучения **Soup** распространяется по лицензии **Apache-2.0** (`Copyright 2026 Makazhan Alpamys and the Soup contributors`).
- Мы используем `soup-cli` как внешний инструмент обучения и перенимаем инженерные паттерны (RAFT-формат, preflight-проверки конфига и утечки данных, конвейер `train -> merge -> gguf`) без копирования исходного кода Soup внутрь Android APK.
